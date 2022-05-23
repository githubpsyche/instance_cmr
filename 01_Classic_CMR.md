## The Prototype-Based Account of Context Maintenance and Retrieval
Retrieved context theories explain memory search in terms of interactions between two representations across experience: one of temporal context (a context layer, $C$) and another of features of studied items (an item layer, $F$). While this paper introduces an instance-based account of these interactions, we here specify a variant of the original prototype-based context maintenance and retrieval (CMR) model [@polyn2009context] to support comparison against this account. The instance-based model we emphasize tracks the history of interactions between context and item features by storing a discrete record of each experience in memory for later inspection. In contrast, PrototypeCMR maintains a simplified neural network whose connection weights accumulate a center of tendency representation reflecting context and item interactions across experiences. 

| Structure Type        | Symbol            | Name                    | Description                                                 |
|:----------------------|:------------------|:------------------------|:------------------------------------------------------------|
| Architecture          |                   |                         |                                                             |
|                       | $C$               | temporal context        | A recency-weighted average of encoded items      |
|                       | $F$               | item features           | Current pattern of item feature unit activations      |
|                       | $M^{FC}$          |                         | encoded feature-to-context associations      |
|                       | $M^{CF}$          |                         | encoded context-to-feature associations      |
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

 : Parameters and structures specifying CMR


### Initial State
Associative connections built within prototypeCMR are represented by matrices $M^{FC}$ and $M^{CF}$.

To summarize pre-experimental associations built between relevant item features and possible contextual states, we initialize $M^{FC}$ according to:

$$
M^{FC}_{pre(ij)} = \begin{cases} \begin{alignedat}{2} 1 - \gamma \text{, if } i=j \\\
          0 \text{, if } i \neq j
   \end{alignedat} \end{cases}
$${#eq-1}

This connects each unit on $F$ to a unique unit on $C$. Used this way, $\gamma$ controls the relative contribution of pre-experimentally acquired associations to the course of retrieval compared to experimentally acquired associations. Correspondingly, context-to-feature associations tracked by $M^{CF}$ are set according to:

$$
M^{CF}_{pre(ij)} = \begin{cases} \begin{alignedat}{2} 1 - \delta \text{, if } i=j \\\
          \alpha \text{, if } i \neq j
       \end{alignedat} \end{cases}
$${#eq-2}

Like $\gamma$ for $M^{FC}$, the $\delta$ parameter controls the contribution of pre-experimental context-to-feature associations relative to experimentally acquired ones. Since context-to-feature associations organize the competition of items for retrieval, the $\alpha$ parameter specifies a uniform baseline extent to which items support one another in that competition.

Context is initialized with a state orthogonal to any of those pre-experimentally associated with a relevant item feature. Feature representations corresponding to items are also assumed to be orthonormal to one another such that each unit on $F$ corresponds to one item.


### Encoding Phase
Whenever an item $i$ is presented for study, its corresponding feature representation $f_i$ is activated on $F$ and its contextual associations encoded into $M^{FC}$ are retrieved, altering the current state of context $C$.

The input to context is determined by:

$$
c^{IN}_{i} = M^{FC}f_{i}
$$ {#eq-3}

and normalized to have length 1. Context is updated based on this input according to:

$$ 
c_i = \rho_ic_{i-1} + \beta_{enc} c_{i}^{IN}
$$ {#eq-4}

with $\beta$ (for encoding we use $\beta_{enc}$) shaping the rate of contextual drift with each new experience, and $\rho$ enforces the length of $c_i$ to 1 according to:

$$ 
\rho_i = \sqrt{1 + \beta^2\left[\left(c_{i-1} \cdot c^{IN}_i\right)^2 - 1\right]} - \beta\left(c_{i-1} \cdot
c^{IN}_i\right)
$$ {#eq-5}

Associations between each $c_i$ and $f_i$ are built through Hebbian learning:

$$
\Delta M^{FC}_{exp} = \gamma c_i f^{'}_i
$$ {#eq-6}

and

$$
\Delta M^{CF}_{exp} = \phi_i f_i c^{'}_i
$$ {#eq-7}

where $\phi_i$ enforces a primacy effect, scales the amount of learning based on the serial position of the studied item according to

$$ 
\phi_i = \phi_se^{-\phi_d(i-1)} + 1
$$ {#eq-8}

This function decays over time, such that $\phi_{s}$ modulates the strength of primacy while $\phi_{d}$ modulates the rate of decay.

This extended Hebbian learning process characterizes how PrototypeCMR performs abstraction. When each item is encoded with a particular temporal context, representations are updated to aggregate a prototypical summary of the item's temporal contextual associations in $M^{FC}$ and vice versa in $M^{CF}$. 


### Retrieval Phase
To help the model account for the primacy effect, we assume that between the encoding and retrieval phase of a task, the content of $C$ has drifted some amount back toward its pre-experimental state and set the state of context at the start of retrieval according to following, with $\rho$ calculated as specified above:

$$ 
c_{start} = \rho_{N+1}c_N + \beta_{start}c_0
$$ {#eq-9}

At each recall attempt, the current state of context is used as a cue to attempt the retrieval of some studied item. An activation $a$ is solicited for each item according to:

$$ 
a = M^{CF}c
$$ {#eq-10}

Each item gets a minimum activation of $10^{-7}$. To determine the probability of a given recall event, we first calculate the probability of stopping recall - returning no item and ending memory search. This probability varies as a function of output position $j$:

$$
P(stop, j) = \theta_se^{j\theta_r}
$$ {#eq-11}

In this way, $\theta_s$ and $\theta_r$ control the scaling and rate of increase of this exponential function. Given that recall is not stopped, the probability $P(i)$ of recalling a given item depends mainly on its activation strength according

$$
P(i) = (1-P(stop))\frac{a^{\tau}_i}{\sum_{k}^{N}a^{\tau}_k}
$$ {#eq-12}

$\tau$ here shapes the contrast between well-supported and poorly supported items: exponentiating a large activation and a small activation by a large value of $\tau$ widens the difference between those activations, making recall of the most activated item even more likely. Small values of $\tau$ can alternatively drive recall likelihoods of differentially activated items toward one another.

If an item is recalled, then that item is reactivated on $F$, and its contextual associations retrieved for integration into context again according to:

$$
c^{IN}_{i} = M^{FC}f_{i}
$$ {#eq-13}

Context is updated again based on this input (using $\beta_{rec}$ instead of $\beta_{enc}$) and used to cue a successive recall attempt. This process continues until recall stops.