# InstanceCMR
Click here for a visualization of this outline: https://gistpreview.github.io/?503c779cd2a6c405034b33f8294d0738/outline.html

In retrieved-context accounts of memory search like the Context Maintenance and Retrieval (CMR) model [@polyn2009context], representations of studied items in a free recall experiment are associated with states of an internal representation of temporal context that slowly evolves across the study period. 
These mechanisms enable models to account for organizational effects in recall sequences, such as the tendency for temporally contiguous items to be recalled successively.

Retrieved context models tend to specify these dynamics in terms of a simplified neural network, as building a single prototypical pattern of associations between each item and context (and vice versa) across experiences. 
By contrast, models of categorization and other memory phenomena have increasingly converged on instance-based architectures [@hintzman1984minerva] that conceptualize memory as a stack of trace vectors that each represent discrete experiences and support recall through parallel, nonlinear activation based on similarity to a probe. 

To investigate the consequences of this distinction, we present an instance-based specification of CMR that encodes associations between studied items and context by instantiating memory traces corresponding to each experience and drives recall through context-based coactivation of those traces. We analyze the model's ability to account for traditional phenomena that have been used as support for the original prototypical specification of CMR and evaluate conditions under which the specifications might behave differently.

## Introduction
1. Instance-based models conceptualize memory as a stack of trace vectors representing discrete experiences and supporting recall through parallel, nonlinear activation based on similarity to a probe. 
2. Prototype-based models conceptualize abstraction as enacted during encoding. New experiences update memory representations to reflect prototypical features that are common across past experiences. 
3. Linear associator networks encode pattern associations via outer product sums. Instance models can represent them through pattern concatenation.
4. Theory competition across different areas of memory research has focused on differences in how architectures access associations.
   1. Categorization
   2. Semantic Memory
   3. Free Recall?
5. The implications of these differences for explaining memory search haven't been investigated yet; we do that here!

## Model Specification

## Evaluation Approach
1. We introduce a new instance-based specification of CMR that encodes associations between studied items and context as concatenated vectors.
2. We compare it with the prototype-based specification of CMR that encodes associations in a Hebbian linear associator network.
3. We apply likelihood-based fitting to each model. Compare optimized log-likelihoods and simulated benchmark phenomena (CRP, PFR, SPC) to evaluate each specification's ability to account for free recall performance.
4. We select datasets to probe differences in how the architectures represent and access associations.

## Baseline Comparison
1. First, we establish that InstanceCMR is equivalent to PrototypeCMR when accounting for benchmark recall phenomena under benchmark tasks conditions (i.e., free recall of semantically unrelated, singly presented items) 
2. We use the PEERS dataset, where many participants freely recall many lists of semantically unrelated items.
3. We conclude that prototype- and Instance- CMR can similarly account for free recall performance in pure lists.

## Variable List Length
1. A significant achievement of PrototypeCMR is its ability to account for apparent differences in subjects' performance across list lengths using a single parameter configuration. 
2. To confirm that dynamics in instance-based models scale similarly as list length increases, we compare the performance of InstanceCMR to PrototypeCMR on the Murdock (1962) dataset where participants recalled lists of length 20, 30, and 40.
3. We conclude that Prototype- and Instance- CMR can similarly account for free recall performance across pure lists of variable list length.

## Item Repetitions

### Motivation
1. Much research focuses on understanding repetition effects in free recall.
2. The item feature orthogonality assumption in PrototypeCMR ported over to InstanceCMR limits the extent to which differences in model abstraction mechanisms might drive differences in model performance.
3. We show that when trials repeatedly present the same item, the item's memory strength given a random cue scales exponentially in simulations PrototypeCMR but quasi-linearly in simulations of InstanceCMR.
4. This is due to differences in how the models scale the influence/activation of different experiences in retrieved patterns based on their relevance to cues.

### Test
1. To test the hypothesis that the models predict different repetition effects in free recall, we evaluate the ability of each model to account for the Lohnas & Kahana (2014) dataset.
2. In this dataset, participants recalled pure lists with no item repetitions, massed lists with items repeated immediately after their first presentation; spaced lists with items repeated after intervals of 1-8 items; and mixed lists. 
3. Activation mechanism was not found to impact models' ability to account for free recall performance in the dataset. 
4. However, since trials only repeated items up to one time, we could not fully evaluate the feature overlap hypothesis.
5. Maybe the Howard Kahana 2005 dataset is better?

## Semantic Organizational Effects

### Motivation
1. Another way to explore how overlapping item representations within a trial might impact model performance is to examine semantic organizational effects in free recall.
2. To account for semantic organizational effects, we drop our orthogonality assumption and attempt to represent items' shared features within trials. 
3. Since all items are at least superficially similar, this may be a more realistic test of the feature overlap hypothesis.

### Test
1. To test the hypothesis that the models predict different semantic organizational effects in free recall, we re-evaluate the ability of each model to account for the PEERS dataset. 
2. This time, each model variant uses word vector similarities to enable recall based on semantic similarity.
3. Outcome unknown just yet.

## Conclusions
1. We presented a instance-based specification of CMR that encodes associations between studied items and context as concatenated vectors.
2. We showed that Instance- and PrototypeCMR equivalently accounts for free recall performance across diverse research conditions.
3. We identify discrepancies in the model variants' predictions about abstraction over nonorthgonal item features, but fail to link them to differences in models' ability to account for performance across considered datasets.
4. By straightforwardly porting concepts from retrieved context theory into an instance-based architecture, these results demonstrate an underlying unity across research efforts in model-based memory science.