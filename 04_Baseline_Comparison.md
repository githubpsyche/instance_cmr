## Simulation of Murdock and Okada (1970)

We start by comparing how our prototype- and instance-based implementations of CMR account for behavior in a classic experiment where each item is presented just once per study phase. For these simulations, we used the subset of the PEERS (Penn Electrophysiology of Encoding and Retrieval Study) dataset reported by by @healey2014memory. Each of 126 people between the ages of 17 and 30 performed 112 trials with study lists each consisting of 16 unique words. Given a particular subject, words were unique within trials and controlled to , and randomly selected from the Toronto Word Pool [@friendly1982toronto], a widely-used collection of high frequency nouns, adjectives, and verbs.

While the major focus of the original report by @murdock1970interresponse was to investigate inter-response times in single-trial free recall, here we focus consideration on the content of recorded recall sequences. Because it excludes within-list repetitions of studied items, this dataset presents the opportunity to compare model performance under simplified conditions. Since items' feature representations are assumed orthogonal under considered variants of CMR, retrieving a pattern of contextual associations given an item-based cue only requires abstraction over the cued item's pre-experimental and single experimental contextual associations. Interpretation of apparent differences in performance across model variants thus focus primarily on mechanisms for context-based item representation retrieval.

We compared the original prototype-based implementation of CMR against our novel instance-based implementation. First we evaluated each model variant based on their ability to predict the specific sequences of recalls exhibited by each participant. Considering all 20 trials performed by each participant in the dataset, we applied the differential evolution optimization technique to find for each model the parameter configuration that maximized the likelihood of recorded recall sequences. We obtained a unique optimal parameter configuration for each unique participant and each considered model variant. To measure the goodness-of-fit for each parameter configuration and corresponding model, [Figure @fig-HealeyKahana2014Fits] plots the log-likelihood of each participant's recall sequences given each model variant's corresponding optimized parameter configuration. The distribution of log-likelihood scores between participants for the PrototypeCMR and InstanceCMR model variants only marginally differ, suggesting little meaningful difference between variants in their effectiveness accounting for participant recall performance across the dataset.

::: {#fig-HealeyKahana2014Fits layout-nrow=2 layout-valign="center"}

![](figures/individual_HealyKahana2014.pdf)

| | ICMR_2_0_0 | ICMR_2_0_1 | ICMR_2_1_0 | ICMR_2_1_1 | PrototypeCMR | 
|:------|-------------:|-------------:|-------------:|-------------:|---------------:|
| count | 126 | 126 | 126 | 126 | 126 | 
| mean | 590.88 | 590.963 | 591.522 | 589.806 | 590.049 | 
| std | 95.2457 | 95.1915 | 95.6988 | 95.847 | 95.2172 | 
| min | 321.343 | 321.254 | 314.304 | 317.624 | 318.623 | 
| 25% | 524.942 | 525.175 | 526.318 | 520.045 | 521.627 | 
| 50% | 603.222 | 602.753 | 603.735 | 602.716 | 602.197 | 
| 75% | 656.658 | 655.863 | 658.4 | 655.447 | 653.205 | 
| max | 796.37 | 795.881 | 797.061 | 795.547 | 796.672 |

Distribution of log-likelihood scores of recall sequences exhibited by each subject under each considered model across list-lengths [@healey2014memory]
:::

As a follow-up, we also compared how readily each model could account for organizational summary statistics in the dataset. We found for each model variant the optimal parameter configuration maximizing the likelihood of the entire dataset rather than participant-by-participant. Using each fitted model variant, we simulated 1000 unique free recall trials and measured summary statistics from the result. [Figure @fig-HealeyKahana2014Summary] plots for each model against the corresponding statistics collected over the dataset how recall probability varies as a function of serial position, how the probability of recalling an item first varies as a function of serial position, and how the conditional recall probabability of an item varies as a function of its serial lag from the previously recalled item. Recapitulating our comparison of log-likelihood distributions fitted over discrete participants, we found that both our prototype-based and instance-based CMR implementations account for these benchmark organizational summary statistics across the full dataset to similar extents. To build on this finding of broad model equivalence with respect to the results reported by @murdock1970interresponse, we consider the model variants under broader experimental conditions.

::: {#fig-HealeyKahana2014Summary layout-nrow=2 layout-valign="center"}
![](figures/HealyKahana2014_PrototypeCMR_ll16_spc.pdf)

![](figures/HealyKahana2014_PrototypeCMR_ll16_crp.pdf)

![](figures/HealyKahana2014_PrototypeCMR_ll16_pfr.pdf)

![](figures/HealyKahana2014_ICMR_2_1_1_ll16_spc.pdf)

![](figures/HealyKahana2014_ICMR_2_1_1_ll16_crp.pdf)

![](figures/HealyKahana2014_ICMR_2_1_1_ll16_pfr.pdf)

Comparison of summary statistics between each model against observed data  [@healey2014memory]]
:::