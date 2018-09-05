# Byte Pair Encoding with Pointwise Mutual Information(PMI)
Notre Dame Natural Language Processing Group

# Overview

If a corpus is compressed using a Shannon-optimal code, the compressed size would be

<img src="https://i.imgur.com/NNjAzjF.jpg" width="300">

For experiement, if wordpieces σ1 and σ2 is merged, then let δ be the count of the merged wordpiece. 
It updates all the variables as follows:

<img src="https://i.imgur.com/6LywEBh.jpg" width="850">

So we should merge the two wordpieces that lead to the greatest decrease in compressed size, 
that is the two wordpieces that maximize:

<img src="https://i.imgur.com/q1dLh5J.jpg" width="600">

Standard BPE chooses the two wordpieces that maximize c(σ1σ2). But the above formula multiplies this by a correction factor known as the **pointwise mutual information** of σ1 and σ2, which measures “how much σ1 and σ2 have to do with each other.” It will favor wordpiece pairs with high PMI, and would be expected a word and punctuation to have low PMI.
Also, the above formula suggests that it should stop when the maximum of the above formula becomes negative.

# Usage
```bpe_modified.py -i <input> -o <output> -s <number of operations> -orig<original BPE_1 mode>```<sup>[1](#footnote1)</sup>
```apply-bpe -c codes_file < test_file > out_file```<sup>[2](#footnote2)</sup>




---
<a name="footnote1">1</a>: Original BPE from [subword_nmt](https://github.com/rsennrich/subword-nmt)


<a name="footnote2">2</a>: apply_bpe.py adapted from [subword_nmt](https://github.com/rsennrich/subword-nmt)
