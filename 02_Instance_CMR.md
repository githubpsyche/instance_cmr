## Context Maintenance and Retrieval within an Instance-Based Architecture

Prototype-based implementations of the retrieved context account of memory search generally suppose that learned item and contextual associations are encoded into abstractive prototype representations according to a Hebbian learning process and then retrieved based on activation from a cue. The memory architecture investigated in this paper alternatively supposes that learning episodes are stored as discrete instances in memory and only abstracted over at retrieval. Within previous examples of this architecture [e.g., @hintzman1984minerva; @jamieson2018instance], stored instances are represented as vectors stacked within a $m$ by $n$ memory matrix $M$. In model variations where vectors are not composed of binary values, at retrieval each trace is activated in parallel based on a positively accelerated transformation of its cosine similarity to a probe $p$:

$$
a(p)_i = \left({\frac {\sum^{j=n}_{j=1}{p_j \times M_{ij}}} {\sqrt{\sum^{j=n}_{j=1}{p^2_j}}
        \sqrt{\sum^{j=n}_{j=1}{M^2_{ij}}}}}\right)^{\tau}
$${#eq-14}

Within this architecture, the parameter $\tau$ exponentially scales this acceleration, effectively controlling the selectivity of retrieval by modulating the difference in activations between highly and less relevant traces. A sum of stored traces weighted by these nonlinearly scaled activations -- called an *echo*, $E(p)$, is taken to build an abstractive representation for retrieval:

$$
E(p) = \sum^{i=m}_{i=1}\sum^{j=n}_{j=1}a(p)_i \times M_{ij}
$${#eq-15}

Our instance-based implementation of the context maintenance and retrieval model (InstanceCMR) realizes the retrieved context account of memory search [as articulated by @morton2016predictive] by extending this instance-based architecture to capture how retrieved context theory avers that item and temporal contextual associations evolve and organize retrieval. To make comparison of architectures as straightforward as possible, mechanisms were deliberately specified to be as similar to those of the original prototypical specification as possible except where required by the constraints of the instance-based architecture.

| Structure Type        | Symbol            | Name                    | Description                                                 |
|:----------------------|:------------------|:------------------------|:------------------------------------------------------------|
| Architecture          |                   |                         |                                                             |
|                       | $M$               | memory                  | Array of accumulated memory traces                          |
|                       | $C$               | temporal context        | A recency-weighted average of encoded items                 |
|                       | $F$               | item features           | Current pattern of item feature unit activations            |
| Context Updating      |                   |                         |                                                             |
|                       | ${\beta}_{enc}$   | encoding drift rate     | Rate of context drift during item encoding                  |
|                       | ${\beta}_{start}$ | start drift rate        | Amount of start-list context retrieved at start of recall   |
|                       | ${\beta}_{rec}$   | recall drift rate       | Rate of context drift during recall                         |
| Associative Structure |                   |                         |                                                             |
|                       | ${\alpha}$        | shared support          | Amount of support items initially have for one another      |
|                       | ${\delta}$        | item support            | Initial pre-experimental contextual self-associations       |
|                       | ${\gamma}$        | learning rate           | Amount of experimental context retrieved by a recalled item |
|                       | ${\phi}_{s}$      | primacy scale           | Scaling of primacy gradient on trace activations            |
|                       | ${\phi}_{d}$      | primacy decay           | Rate of decay of primacy gradient                           |
| Retrieval Dynamics    |                   |                         |                                                             |
|                       | ${\tau}$          | choice sensitivity      | Exponential weighting of similarity-driven activation       |
|                       | ${\theta}_{s}$    | stop probability scale  | Scaling of the stop probability over output position        |
|                       | ${\theta}_{r}$    | stop probability growth | Rate of increase in stop probability over output position   |

  : Parameters and structures specifying InstanceCMR

### Model Architecture

Prototypical CMR stores associations between item feature representations (represented a pattern of weights in an item layer $F$) and temporal context (represented in a contextual layer $C$) by integrating prototypical mappings between the representations via Hebbian learning over the course of encoding. In contrast, InstanceCMR tracks the history of interactions between context and item features by storing a discrete record of each experience, even repeated ones, as separate traces within in a memory store for later inspection. Memory for each experience is encoded as a separate row in an $m$ by $n$ memory matrix $M$ where rows correspond to memory traces and columns correspond to features. Each trace representing a pairing $i$ of a presented item???s features $f_i$ and the temporal context of its presentation $c_i$ is encoded as a concatenated vector:

$$
M_i = (f_i, c_i)
$${#eq-16}

### Initial State

Structuring $M$ as a stack of concatenated item and contextual feature vectors $(f_i, c_i)$ makes it possible to define pre-experimental associations between items and contextual states similarly to the pattern by which PrototypeCMR's pre-experimental associations are specified in equations [-@eq-1] and [-@eq-2]. To set pre-experimental associations, a trace is encoded into memory $M$ for each relevant item. Each entry $j$ for each item feature component of pre-experimental memory traces trace $f_{pre}(i)$ is set according to

$$
f_{pre(i, j)} = \begin{cases} \begin{alignedat}{2} 1 - \gamma \text{, if } i=j \\\
          0 \text{, if } i \neq j
       \end{alignedat} \end{cases}
$${#eq-17}

This has the effect of relating each unit on $F$ to a unique unit on $C$ during retrieval. As within prototypical CMR, the $\gamma$ parameter controls the strength of these pre-experimental associations relative to experimental associations.

Similarly to control pre-experimental context-to-item associations, the content of each entry $j$ for the contextual component of each pre-experimental trace $c_{pre(i,j)}$ is set by:

$$
c_{pre(i,j)} = \begin{cases} \begin{alignedat}{2} \delta \text{, if } i=j \\\
          \alpha \text{, if } i \neq j
       \end{alignedat} \end{cases}
$${#eq-18}

Here, $\delta$ works similarly to $\gamma$ to connect indices on $C$ to the corresponding index on $F$ during
retrieval from a partial or mixed cue. The $\alpha$ parameter additionally allows all the items to support one
another in the recall competition in a uniform manner.

Before list-learning, context $C$ is initialized with a state orthogonal to the pre-experimental context associated
with the set of items via the extra index that the representation vector has relative to items??? feature vectors. Following the convention established for prototypical specifications of CMR, item features are further assumed to be orthonormal with respect to one another such that each unique unit on $F$ corresponds to one item.

## Encoding Phase

In a broad sense, the initial steps of item encoding within InstanceCMR proceed similarly to the process in PrototypeCMR. Just as with PrototypeCMR, when an item $i$ is presented during the study period, its corresponding feature representation $f_i$ is activated on $F$ and its contextual associations encoded into $M^{FC}$ are retrieved by presenting $f_i$ as a probe to memory. InstanceCMR, however, performs retrieval by applying an extension of the basic two-step echo $E$ mechanism outlined in equations [-@eq-14] and [-@eq-15].

The extension of the original mechanism differentiates between item- and context-based retrieval. When probes include item feature information ($p_f \neq 0$), activation for traces encoded during the experiment are modulated by $\gamma$ to control the contribution of experimentally-accumulated associations to retrieved representations relative to pre-experimental associations:

$$
(, c^{IN}) = E(f_i, 0) = \sum^{j=m}_{j=1}\sum^{k=n}_{k=1} {\gamma} \times a(f_i, 0)_j \times M_{jk}
$${#eq-19}

The contextual features of the retrieved echo determine contextual input; this retrieved pre-experimental context is normalized to have length 1. Upon retrieval of $c^{IN}$, the current state of context is updated the same way as it is under the prototype-based framework, applying equations [-@eq-4] and [-@eq-5] to drift $c$ toward $c^{IN}$ and enforce its length to 1, respectively.

After context is updated, the current item $f_i$ and the current state of context $c_i$ become associated in memory
$M$ by storing a concatenation of the two vectors as a new trace $(f_i, c_i)$. This mechanism reserves abstraction over learning episodes for cue-based retrieval rather than at the point of encoding as in PrototypeCMR.

### Retrieval Phase

Following the lead of the classic prototype-based implementation of CMR, before retrieval InstanceCMR reinstates some pre-list context according to [-@eq-9]. Similarly, at each recall attempt $i$, we calculate the probability of stopping recall (where no item is recalled and search is terminated) based on output position according to [-@eq-11].

To determine the probability of recalling an item given that recall does not terminate, first the current state of context is applied as a retrieval cue to retrieve an item feature presentation $f_{rec}$, again applying a modification of the echo-based retrieval mechanism characteristic of instance-based models that modulates trace activations before aggregation into an echo representation:

$$
(f_{rec},) = E(0, c_i) = \sum^{j=m}_{j=1}\sum^{k=n}_{k=1} {\phi}_j \times a(0, c_i)_j \times M_{jk}
$${#eq-20}

where ${\phi}_i$ scales the amount of learning, simulating increased attention to initial items in a list that has been
proposed to explain the primacy effect. ${\phi}_i$ depends on the serial position $i$ of the studied item the same as it does in PrototypeCMR (equation [-@eq-8]), with the free parameters ${\phi}_s$ and ${\phi}_d$ respectively controlling the magnitude and decay of the corresponding learning-rate gradient.

Since item feature representations are presumed to be orthogonal for the purposes of the model, the content of $f_{rec}$ can be interpreted as a measure of the relative support in memory for retrieval of each item $i$, setting the probability distribution of item recalls $P(i)$ to

$$
P(i) = (1-P(stop))\frac{f_{rec}}{\sum_{k}^{N}f_{rec}}
$${#eq-21}

If an item is recalled, then that item is reactivated on $F$, and its contextual associations retrieved for integration into context again according to @Eq-19. Context is updated again based on this input (using $\beta_{rec}$ instead of $\beta_{enc}$) and used to cue a successive recall attempt. This process continues until recall stops.

An important difference between equation [-@eq-21] and that applied in our specification of PrototypeCMR to compute $P(i)$ (equation [-@eq-12]) is that $\tau$ is not applied as an exponent to retrieval supports to shape the contrast between well-supported and poorly supported items. Instead, instance-based models apply this transformation to discrete trace activations before aggregation of an echo representation. This difference still achieves the effect of ultimately either widening or shrinking the difference between item supports driving retrieval, but is not trivial. Its consequences are explored in later sections.
