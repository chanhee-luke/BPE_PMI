# Byte Pair Encoding with Pointwise Mutual Information(PMI)
Luke Song (Notre Dame NLP Group)

# Overview

This code explores a novel approach for pre-processing the corpus before training

# Mechanism

If a corpus is compressed using a Shannon-optimal code, the compressed size would be

<img src="https://i.imgur.com/NNjAzjF.jpg" width="300">

For this code, if wordpieces σ1 and σ2 is merged, then let δ be the count of the merged wordpiece. 
It updates all the variables as follows:

<img src="https://i.imgur.com/6LywEBh.jpg" width="850">

The code merges the two wordpieces that lead to the greatest decrease in compressed size, 
that is the two wordpieces that maximize:

<img src="https://i.imgur.com/q1dLh5J.jpg" width="600">

Standard BPE chooses the two wordpieces that maximize c(σ1σ2). But the above formula multiplies this by a correction factor known as the **pointwise mutual information** of σ1 and σ2, which measures “how much σ1 and σ2 have to do with each other.” It will favor wordpiece pairs with high PMI, and would be expected a word and punctuation to have low PMI.
Also, the above formula suggests that it should stop when the maximum of the above formula becomes negative.

# Usage
```bpe_modified.py -s <number of operations> [-orig] < text > codes_file```<sup>[1](#footnote1)</sup>

```apply_bpe.py -c codes_file < text > out_file```<sup>[2](#footnote2)</sup>



<br><br>
<br><br>
<br><br>


---
<a name="footnote1">1</a>: Standard BPE mode from [subword_nmt](https://github.com/rsennrich/subword-nmt)


<a name="footnote2">2</a>: apply_bpe.py adapted from [subword_nmt](https://github.com/rsennrich/subword-nmt)
