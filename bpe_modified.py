#!/usr/bin/env python
# -*- coding: utf-8 -*-
# bpe_modified.py

from __future__ import unicode_literals

import codecs
import re
import argparse
import sys
import collections
import math

from io import open
argparse.open = open

def create_parser(subparsers=None):

  if subparsers:
      parser = subparsers.add_parser('learn-bpe',
          formatter_class=argparse.RawDescriptionHelpFormatter,
          description="learn BPE-based word segmentation(modified)")
  else:
      parser = argparse.ArgumentParser(
          formatter_class=argparse.RawDescriptionHelpFormatter,
          description="learn BPE-based word segmentation(modified)")

  parser.add_argument(
      '--input', '-i', type=argparse.FileType('r'), default=sys.stdin,
      metavar='PATH',
      help="Input text (default: standard input).")
  parser.add_argument(
      '--output', '-o', type=argparse.FileType('w'), default=sys.stdout,
      metavar='PATH',
      help="Output file for BPE codes (default: standard output)")
  parser.add_argument(
      '--orig', '-orig', action="store_true",
      help="original bpe mode.")
  parser.add_argument(
      '--symbols', '-s', type=int, default=10000,
      help="Create this many new symbols (each representing a character n-gram) (default: %(default)s))")

  return parser

# get number of counts of all pairs in vocab
def get_stats(vocab):
  pairs = collections.defaultdict(int)
  for word, freq in vocab.items():
    # if vocab is a complete word, skip that word
    if len(word) == 1:
      continue
    else: 
      symbols = word.split()
      for i in range(len(symbols)-1):
        pairs[symbols[i],symbols[i+1]] += freq
  return pairs

# merge vocab given pair with the best size
def merge_vocab(pair, v_in):
  v_out = {}
  bigram_pattern = re.escape(' '.join(pair))
  p = re.compile(r'(?<!\S)' + bigram_pattern + r'(?!\S)')
  for word in v_in:
    w_out = p.sub(''.join(pair), word)
    v_out[w_out] = v_in[word]
  return v_out

# count number of tokens from the whole vocab
def count_token(vocab):
  tokens = collections.defaultdict(int)
  for word, freq in vocab.items():
    symbols = word.split()
    for i in range(len(symbols)):
      tokens[symbols[i]] += freq
  return tokens

def get_vocabulary(fobj, is_dict=False):
  """Read text and return dictionary that encodes vocabulary
  """
  vocab = collections.Counter()
  for i, line in enumerate(fobj):
    for word in line.strip('\r\n ').split(' '):
        if word:
            vocab[word] += 1
  return vocab

def learn_bpe(infile, outfile, num_symbols, orig=False):
    
  vocab = get_vocabulary(infile)
  vocab = dict([((" ".join(x)+'</w>') ,y) for (x,y) in vocab.items()])

  for i in range(num_symbols):
    pairs = get_stats(vocab)
    tokens = count_token(vocab)
    total = sum(tokens.values())
    try:
      size = -1 # inintial size
      for key, value in pairs.iteritems():
        temp = 0
        # if key is a complete word, do not iterate
        if isinstance(key, str):
          temp += math.log(tokens.get(key), 2)
        else: 
          # if key is a pair, iterate
          for i in key:
            temp += math.log(tokens.get(i), 2)
        # original BPE mode
        if orig:
            pairSize = value
        else:
            pairSize = value * (math.log(value, 2) - temp + math.log(total, 2)) # function to calculate H - H_new
        # find pair with highest size
        if size < pairSize:
          size = pairSize
          best = key
    except ValueError:
      break
    if size < 0:
       sys.stderr.write('size is negative, stopping\n')
       break
    
    vocab = merge_vocab(best, vocab)
    
    # print change of vocab over number of merge operations
    outfile.write('{0} {1}\n'.format(*best))


if __name__ == '__main__':

  # python 2/3 compatibility
  if sys.version_info < (3, 0):
      sys.stderr = codecs.getwriter('UTF-8')(sys.stderr)
      sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)
      sys.stdin = codecs.getreader('UTF-8')(sys.stdin)
  else:
      sys.stderr = codecs.getwriter('UTF-8')(sys.stderr.buffer)
      sys.stdout = codecs.getwriter('UTF-8')(sys.stdout.buffer)
      sys.stdin = codecs.getreader('UTF-8')(sys.stdin.buffer)

  parser = create_parser()
  args = parser.parse_args()

  # read/write files as UTF-8
  if args.input.name != '<stdin>':
      args.input = codecs.open(args.input.name, encoding='utf-8')
  if args.output.name != '<stdout>':
      args.output = codecs.open(args.output.name, 'w', encoding='utf-8')

  learn_bpe(args.input, args.output, args.symbols, args.orig)

