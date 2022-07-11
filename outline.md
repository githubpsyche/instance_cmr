# InstanceCMR
![[index]]

## Introduction
[[00_Introduction]]

1. Instance-based models conceptualize memory as a stack of trace vectors representing discrete experiences and supporting recall through parallel, nonlinear activation based on similarity to a probe.
2. Prototype-based models conceptualize abstraction as enacted during encoding. New experiences update memory representations to reflect prototypical features that are common across past experiences.
3. Linear associator networks encode pattern associations via outer product sums. Instance models can represent them through pattern concatenation.
4. [[Theory competition across different areas of memory research has focused on differences in how architectures access associations.]]
5. The implications of these differences for explaining memory search haven't been investigated yet; we do that here by comparing parallel implementations of CMR.

## Model Specification
### [[01_Classic_CMR]]
### [[02_Instance_CMR]]

## Evaluation Approach
[[03_Evaluation_Approach]]

1. We introduce a new instance-based specification of CMR that encodes associations between studied items and context as concatenated vectors.
2. We compare it with the prototype-based specification of CMR that encodes associations in a Hebbian linear associator network.
3. We apply a likelihood-based fitting to each model. Compare optimized log-likelihoods and simulated benchmark phenomena (CRP, PFR, SPC) to evaluate each specification's ability to account for free recall performance.
4. We select datasets to probe differences in how the architectures represent and access associations.

## Baseline Comparison
[[04_Baseline_Comparison]]

1. First, we establish that InstanceCMR is equivalent to PrototypeCMR when accounting for benchmark recall phenomena under benchmark tasks conditions (i.e., free recall of semantically unrelated, singly presented items)
2. We use the PEERS dataset, where many participants freely recall many lists of semantically unrelated items.
We conclude that prototype- and Instance- CMR can similarly account for free recall performance in pure lists.

## Variable List Lengths
[[instance_cmr/05_Variable_List_Lengths]]

1. A significant achievement of PrototypeCMR is its ability to account for apparent differences in subjects' performance across list lengths using a single parameter configuration.
2. To confirm that dynamics in instance-based models scale similarly as list length increases, we compare the performance of InstanceCMR to PrototypeCMR on the Murdock (1962) dataset where participants recalled lists of lengths 20, 30, and 40.
3. We conclude that Prototype- and Instance- CMR can similarly account for free recall performance across pure lists of variable list length.

## Item Repetitions
[[06_Item_Repetitions]]

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

## Discussion
[[07_Discussion]]

1. We presented an instance-based specification of CMR that encodes associations between studied items and context as concatenated vectors.
2. We showed that Instance- and PrototypeCMR equivalently accounts for free recall performance across diverse research conditions.
3. We identify discrepancies in the model variants' predictions about abstraction over nonorthogonal item features, but fail to link them to differences in models' ability to account for performance across considered datasets.
4. By straightforwardly porting concepts from retrieved context theory into an instance-based architecture, these results demonstrate an underlying unity across research efforts in model-based memory science.

# Plans
To start, I need to collect notes across the vault and maybe also elsewhere and list them here for further integration.

## Unorganized Notes
[[planning]] also has detailed notes about how to organize introduction, attempting to split into the following notes:
[[Abstraction]]
[[Instance Models]]
[[Prototype models]]
[[Linear Associators]]
[[Retrieved Context Theory]]
[[Benchmark Phenomena in Free Recall]]
[[Architectural Contrasts in Free Recall]]
[[Prototype vs Instance CMR]]

[[2022-05-15 Introduction Planning]]
archived
links to [[@jamieson2018instance]] which points out relevant notes and poses relevant questions

[[2022-05-31 ICMR Results Roundup]]
archived, reviews results from 5-31 of my subtle contrasts comparisons

[[Theory competition across different areas of memory research has focused on differences in how architectures access associations.]] is a pretty well organized review of theory competition circumstances. It's interesting how I integrate these notes into outline even though presentation is inappropriate for paper.

[[Literature_Review.todolist]] is a text file inside priority with some notes identifying further references I might explore (and why).

[[Goal-Pass All Fitting Results to Sean]] has notes surrounding plan for passing fitting results to Sean. Clarifies intention to generalize batch processing flow to work locally, clarifies plans for fitting reports template outputs into paper workflow.

[[2022-06-01]] is a more high-level review of the stuff in [[2022-05-31 ICMR Results Roundup]]. I can probably archive it. But it remains on top of my mind for the current iteration.

[[Subtle Contrasts in ICMR Evaluation]] is an interestingly designed todolist/overview of the different model variants I explored through the May 31 thing.

[[@anderson1995introduction]] has a detailed account of how linear associators compare to instance models in categorization.

[[@jamieson2018instance]] mostly just contains notes focused on that question about how instance and prototype models compare. I definitely have more extensive notes elsewhere.

[[@stanton2002comparisons]] focuses on the first categorization paper I explored focusing on contrasting instance and prototype models.

[[2022-06-15 Batch Processing]] helps clarify goals and motivation for batch processing step I want to enforce.

## Issues
I'm still deciding how I want this "landing page" to be organized.
[[Planning the ICMR Landing Page]]

Sean's feedback from the 14th
[[instance_cmr - Sean Feedback 2022-06-14]]

#### Relevant Library Maintenance
Leaving this stuff in a specific report template will make generating novel reports harder and clutter the reports in general.
[[reports.subjectwise_model_evaluation.template - Refactor Novel Functions From Subjectwise Model Comparison Template]]

In particular I want to make sure this analysis works within my pipeline for both control lists and lists with item repetitions.
[[analyses.lag_crp - Organize and clarify tests for lag contiguity analysis]]

Small differences in implementations matter for log-likelihoods, but not in theory. So I should prune away variants that don't matter.
[[models - Clean Up and Document Relevant and Defunct Model Implementations]]

This will make it easier to test and develop my code. Maybe.
[[general - Don't leave numba jit on by default]]

#### Benchmark Model Comparison
Current draft doesn't have current results or anything from the current result pipeline.
[[issues/Update ICMR Results Section]]

I need to figure out if comparing single and dual stack models is worth doing in the paper. But that's just a result to include for Sean, right?
[[instance_cmr - Integrate Single Stack and Two Stack ICMR Evaluations]]

#### Variable List Lengths
Might want to use selective model evaluation technique to improve visualization of Murdock 1962 fitting results. Will have to compare and contrast using appendix, probably. And may have to update results pipeline to select my preferred fitting routine.
[[fitting - Document Selective Likelihood-Based Model Evaluation]]

#### Repetition Effects
Ideally I'd have the spacing and neighbor contiguity analyses from the Lohnas Dataset and apply them both to the Howard & Kahana 2005 dataset and the original dataset.
[[analyses.neighbor_contiguity - Finish implementation and test for neighbor contiguity analysis]]
[[analyses.recall_probability_by_lag - Extend plot_rpl to support different designs than Lohnas 2014 Dataset]]
[[analyses.recall_probability_by_lag - Add jitter or other control to make default plot_rpl figure cleaner]]

#### Deficient Repetition Contiguity
I might want to argue that ICMR can more easily account for this effect.

I have a lot of versions of this thing and need to make sure I'm working with the right one.
[[analyses.repetition_contiguity - add convincing tests for repetition contiguity analysis]]

This might already exist. But I'm unsure if it even works.
[[analyses.repetition_contiguity - Implement plot repetition contiguity function]]

I believe this is mostly just the control analysis stuff that lets me compare model predictions about recall rates of items at same serial positions that are not repetitions.
[[analyses - Finish refactoring assets from Measuring_Repetition_Effects notebook]]

#### Semantic Effects
I might want to argue that ICMR can more easily accomodate semantic organizational effects. But do I really?
[[issues/Implement and Test Instance SCMR]]
[[issues/Semantic CRP for Report Templates]]
[[datasets - consistently track item level features in my simulate_DF_from_events and related code]]

#### Extras
Extras that I generated that might not belong in the paper anymore...
Parameter Shifting Experiments

I might find that model comparison is cleaner with this parameter gone...
[[models - Clear Up Outcome of Evaluation of Delay Drift Rate Parameter]]

## Archive
