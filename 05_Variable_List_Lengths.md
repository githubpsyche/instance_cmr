## Simulation of Murdock Jr (1962)

A significant feature of the context maintenance and retrieval (CMR) model is its capacity to account for the relative scale-invariance of serial position effects with respect to list length. @murdock1962serial found that changing list lengths across trials in a free recall experiment impacted neither the shape of observed primacy effects during recall nor on the slope of apparent recency effects, though other features of recall sequences did change, such as the overall retrieval probability for initially encoded items as well as the list-list asymptote. Building on these observations, @polyn2009context found that the CMR model could account for these effects of list length on the shape of the serial position curve in free recall using a single parameter configuration.

Here we investigate whether our prototype- and instance-based implementations of CMR can similarly account for recall performance across different list lengths when fitted to predict the sequences of items recalled in our considered dataset. For these comparisons, we leverage a subset of the original behavioral data reported by @murdock1962serial. In the considered subset, 15 subjects performed 240 trials with study lists each consisting of either 20, 30, or 40 unique words presented sequentially -- 80 trials per list length.

For each model variant and each participant, we found through differential evolution optimization the parameter configuration maximizing the likelihood assigned by the model to each recall sequence in all relevant trials, whether with list length of 20 or 30 or 40. The log-likelihoods of the data corresponding to each participant and model variant are plotted in [Figure @fig-Murd62Fits], with a table providing summary statistics. The distribution of log-likelihood scores between participants for the PrototypeCMR and InstanceCMR model variants only marginally differ, suggesting little meaningful difference between variants in their effectiveness predicting recall sequences, even when using a single parameter configuration per participant to account for performance across variable list lengths.

::: {#fig-Murd62Fits layout-nrow=2 layout-valign="center"}

![](figures/individual_murdock1962.pdf)

|       |   InstanceCMR |   PrototypeCMR |
|:------|--------------:|---------------:|
| count |        15     |         15     |
| mean  |      5300.61  |       5281.17  |
| std   |       547.632 |        556.755 |
| min   |      4475.97  |       4381.06  |
| 25%   |      4873.37  |       4865.1   |
| 50%   |      5300.33  |       5280.25  |
| 75%   |      5620.59  |       5591.8   |
| max   |      6382.21  |       6375.89  |

Distribution of log-likelihood scores of recall sequences exhibited by each subject under each considered model across list-lengths [@murdock1962serial]
:::

Considering log-likelihoods alone though leaves ambiguous whether the influence of list length on serial position and related organizational effects are effectively accounted for by both models. To find out, we again focused scrutiny on the prototype-based and instance-based implementations of CMR. We fit each model based on the likelihood assigned to all recall sequences across the dataset rather than by subject or list length. Summary statistics including recall probability as a function of serial position, probability of first recall as a function of serial position, and conditional recall probability as a function of serial lag from the previously recalled item were computed based on simulation of free recall data using the model variants with their fitted parameters. Separate analyses simulated trials with study list lengths of 20 and of 30 items, with summary statistics tracked separately. [Figure @fig-Murd62Summary] plots the results of these simulations against statistics from corresponding subsets of the behavioral data from [@murdock1962serial], with unique sets of plots for both model variants and list lengths. As with previous analyses, we found that both our prototype-based and instance-based CMR implementations account for these benchmark organizational summary statistics across the considered data to similar extents.

::: {#fig-murd62summary layout-nrow=2}

![PrototypeCMR](figures/cmr_summary_murdock1962.pdf){#fig-PrototypeCMR}

![InstanceCMR](figures/icmr_summary_murdock1962.pdf){#fig-InstanceCMR}

Comparison of summary statistics between each model against observed data [@murdock1962serial]
:::
