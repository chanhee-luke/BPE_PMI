# Sentencepiece
BPE with sentencepiece

# Overview
Possible fix: Let $\Sigma$ be the set of wordpieces and let $c(\sigma)$
be the count of wordpiece $\sigma \in \Sigma$ and let
$N = \sum_{\sigma} c(\sigma)$ be the total number of wordpiece
occurrences.

If we were to compress the corpus using a Shannon-optimal code, the
compressed size would be $$\begin{aligned}
H &= -\sum_\sigma c(\sigma) \log(c(\sigma)/N) \\
&= -\sum_{\sigma} c(\sigma) \log c(\sigma) + N \log N.\end{aligned}$$ If
we merge wordpieces $\sigma_1$ and $\sigma_2$, then let $\delta$ be the
count of the merged wordpiece. We would update all the variables as
follows: $$\begin{aligned}
c(\sigma_1\sigma_2) &\leftarrow \delta \\
c(\sigma_1) & \leftarrow c(\sigma_1) - \delta \\
c(\sigma_2) & \leftarrow c(\sigma_2) - \delta \\
N &\leftarrow N - \delta \\
H_{\text{new}} &\approx - \sum_{\sigma} c(\sigma)\log c(\sigma) + c(\sigma_1\sigma_2) (\log c(\sigma_1) + \log c(\sigma_2) -\log c(\sigma_1\sigma_2)) + (N-c(\sigma_1\sigma_2)) \log N\\
\Sigma &\leftarrow \Sigma \cup \{ \sigma_1 \sigma_2 \}.\end{aligned}$$

So we should merge the two wordpieces that lead to the greatest decrease
in compressed size, that is the two wordpieces that maximize:
$$\begin{aligned}
H-H_{\text{new}} &= c(\sigma_1 \sigma_2) (\log c(\sigma_1\sigma_2) - \log c(\sigma_1) - \log c(\sigma_2) + \log N).\end{aligned}$$
Standard BPE chooses the two wordpieces that maximize
$c(\sigma_1\sigma_2)$. But the above formula multiplies this by a
correction factor known as the *pointwise mutual information* of
$\sigma_1$ and $\sigma_2$, which measures "how much $\sigma_1$ and
$\sigma_2$ have to do with each other." It will favor wordpiece pairs
with high PMI, and I would expect a word and punctuation to have low
PMI.

Also, the above formula suggests that we should stop when the maximum of
the above formula becomes negative.

# Usage
bpe_modified.py -i <input> -o <output> -s <number of operations> -orig<turn on original BPE>
