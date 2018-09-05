# Sentencepiece
BPE with sentencepiece

# Overview

Compress the corpus using a Shannon-optimal code, the compressed size would be

<img src="https://i.imgur.com/NNjAzjF.jpg" width="300">

If we merge wordpieces σ1 and σ2, then let δ be the count of the merged wordpiece. 
We would update all the variables as follows:

<img src="https://i.imgur.com/6LywEBh.jpg" width="850">

So we should merge the two wordpieces that lead to the greatest decrease in compressed size, 
that is the two wordpieces that maximize:

<img src="https://i.imgur.com/q1dLh5J.jpg" width="600">

Standard BPE chooses the two wordpieces that maximize c(σ1σ2). But the above formula multiplies this by a correction factor known as the pointwise mutual information of σ1 and σ2, which measures “how much σ1 and σ2 have to do with each other.” It will favor wordpiece pairs with high PMI, and would be expected a word and punctuation to have low PMI.
Also, the above formula suggests that it should stop when the maximum of the above formula becomes negative.

# Usage
bpe_modified.py -i <input> -o <output> -s <number of operations> -orig<turn on original BPE by from subword_nmt>
