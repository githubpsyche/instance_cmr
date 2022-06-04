# export

import numpy as np
from numba import float64, int32, boolean
from numba.experimental import jitclass
lb = np.finfo(float).eps

single_icmr_spec = [
    ("item_count", int32),
    ("encoding_drift_rate", float64),
    ("start_drift_rate", float64),
    ("recall_drift_rate", float64),
    ("delay_drift_rate", float64),
    ("shared_support", float64),
    ("item_support", float64),
    ("learning_rate", float64),
    ("primacy_scale", float64),
    ("primacy_decay", float64),
    ("stop_probability_scale", float64),
    ("stop_probability_growth", float64),
    ("choice_sensitivity", float64),
    ("context_sensitivity", float64),
    ("feature_sensitivity", float64),
    ("context", float64[::1]),
    ("start_context_input", float64[::1]),
    ("delay_context_input", float64[::1]),
    ("preretrieval_context", float64[::1]),
    ("recall", int32[::1]),
    ("retrieving", boolean),
    ("recall_total", int32),
    ("item_weighting", float64[::1]),
    ("context_weighting", float64[::1]),
    ("all_weighting", float64[::1]),
    ("probabilities", float64[::1]),
    ("memory", float64[:, ::1]),
    ("encoding_index", int32),
    ("items", float64[:, ::1]),
    ("norm", float64[::1]),
    ("learn_first", boolean)
]

@jitclass(single_icmr_spec)
class Single_ICMR:
    def __init__(self, item_count, presentation_count, parameters):

        # store initial parameters
        self.item_count = item_count
        self.encoding_drift_rate = parameters["encoding_drift_rate"]
        self.delay_drift_rate = parameters["delay_drift_rate"]
        self.start_drift_rate = parameters["start_drift_rate"]
        self.recall_drift_rate = parameters["recall_drift_rate"]
        self.shared_support = parameters["shared_support"]
        self.item_support = parameters["item_support"]
        self.learning_rate = parameters["learning_rate"]
        self.primacy_scale = parameters["primacy_scale"]
        self.primacy_decay = parameters["primacy_decay"]
        self.stop_probability_scale = parameters["stop_probability_scale"]
        self.stop_probability_growth = parameters["stop_probability_growth"]
        self.choice_sensitivity = parameters["choice_sensitivity"]
        self.context_sensitivity = parameters["context_sensitivity"]
        self.feature_sensitivity = parameters["feature_sensitivity"]
        self.learn_first = parameters["learn_first"]

        # at the start of the list context is initialized with a state
        # orthogonal to the pre-experimental context associated with the set of items
        self.context = np.zeros(item_count + 2)
        self.context[0] = 1
        self.preretrieval_context = self.context
        self.recall = np.zeros(item_count, np.int32)
        self.retrieving = False
        self.recall_total = 0

        # predefine activation weighting vectors
        self.item_weighting = np.ones(item_count + presentation_count)
        self.context_weighting = np.ones(item_count + presentation_count)
        self.item_weighting[item_count:] = self.learning_rate
        self.context_weighting[item_count:] = (
            self.primacy_scale
            * np.exp(-self.primacy_decay * np.arange(presentation_count))
            + 1
        )
        self.all_weighting = self.item_weighting * self.context_weighting

        # preallocate for outcome_probabilities
        self.probabilities = np.zeros((item_count + 1))

        # predefine contextual input vectors relevant for delay_drift_rate and start_drift_rate parameters
        self.start_context_input = np.zeros((self.item_count + 2))
        self.start_context_input[0] = 1
        self.delay_context_input = np.zeros((self.item_count + 2))
        self.delay_context_input[-1] = 1

        # initialize memory
        # we now conceptualize it as a pairing of two stores Mfc and Mcf respectivelysee
        # representing feature-to-context and context-to-feature associations
        mfc = np.eye(item_count, item_count + 2, 1) * (1 - self.learning_rate)
        mcf = np.ones((item_count, item_count)) * self.shared_support
        for i in range(item_count):
            mcf[i, i] = self.item_support
        mcf = np.hstack((np.zeros((item_count, 1)), mcf,  np.zeros((item_count, 1))))
        self.memory = np.zeros((item_count + presentation_count, item_count * 2 + 4))
        self.memory[:item_count,] = np.hstack((mfc, mcf))

        self.norm = np.zeros(item_count + presentation_count)
        self.norm[:item_count] = np.sqrt(np.sum(np.square(self.memory[0])))
        self.norm[item_count:] = np.sqrt(2)
        self.encoding_index = item_count
        self.items = np.hstack((np.eye(item_count, item_count + 2, 1), np.zeros((item_count, item_count+2))))

    def experience(self, experiences):

        for i in range(len(experiences)):
            self.update_context(self.encoding_drift_rate, self.memory[self.encoding_index])
            self.memory[self.encoding_index] = experiences[i]
            self.memory[self.encoding_index, self.item_count+2:] = self.context
            self.encoding_index += 1

    def update_context(self, drift_rate, experience):

        # first pre-experimental or initial context is retrieved
        if len(experience) == self.item_count * 2 + 4:
            context_input = self.echo(experience)[self.item_count + 2 :]
            context_input = context_input / np.sqrt(
                np.sum(np.square(context_input))
            )  # norm to length 1
        else:
            # but sometimes we specify contextual input directly
            context_input = experience

        # updated context is sum of context and input, modulated by rho to have len 1 and some drift_rate
        rho = np.sqrt(
            1 + np.square(drift_rate) * (np.square(self.context * context_input) - 1)
        ) - (drift_rate * (self.context * context_input))
        self.context = (rho * self.context) + (drift_rate * context_input)
        self.context = self.context / np.sqrt(np.sum(np.square(self.context)))

    def echo(self, probe):

        return np.dot(self.activations(probe), self.memory[:self.encoding_index])

    def activations(self, probe, probe_norm=1.0):

        activation = np.dot(self.memory[: self.encoding_index], probe) / (
            self.norm[: self.encoding_index] * probe_norm
        )

        # weight activations based on whether probe contains item or contextual features or both
        if np.any(probe[: self.item_count + 2]):  # if probe is an item feature cue as during contextual retrieval
            if not self.learn_first:
                activation = np.power(activation, self.feature_sensitivity)
            if np.any(
                probe[self.item_count + 2 :]
            ):  # if probe is (also) a contextual cue as during item retrieval
                # both mfc and mcf weightings, see below
                activation *= self.all_weighting[: self.encoding_index]
            else:
                # mfc weightings - scale by gamma for each experimental trace
                activation *= self.item_weighting[: self.encoding_index]
            if not self.learn_first:
                activation = np.power(activation, self.feature_sensitivity)
        else:
            # mcf weightings - scale by primacy/attention function based on experience position
            if not self.learn_first:
                activation *= self.context_weighting[: self.encoding_index]
                activation = np.power(activation, self.context_sensitivity)
            else:
                activation = np.power(activation, self.context_sensitivity)
                activation *= self.context_weighting[: self.encoding_index]

        return activation
        
    def outcome_probabilities(self):

        self.probabilities[0] = min(
            self.stop_probability_scale
            * np.exp(self.recall_total * self.stop_probability_growth),
            1.0 - ((self.item_count - self.recall_total) * lb),
        )
        self.probabilities[1:] = lb
        self.probabilities[self.recall[: self.recall_total] + 1] = 0

        if self.probabilities[0] < (1.0 - ((self.item_count - self.recall_total) * lb)):

            # measure the activation for each item; already recalled items have zero activation
            activation_cue = np.hstack((np.zeros(self.item_count + 2), self.context))
            activation = self.echo(activation_cue)[1:self.item_count + 1]

            # recall probability is a function of activation
            if np.sum(activation) > 0:
                activation = np.power(activation, self.choice_sensitivity)
                activation[activation==0] = lb
                activation[self.recall[:self.recall_total]] = 0
                self.probabilities[1:] = (1 - self.probabilities[0]) * activation / np.sum(activation)

        return self.probabilities

    def free_recall(self, steps=None):

        # some pre-list context is reinstated before initiating recall
        if not self.retrieving:
            self.recall = np.zeros(self.item_count, np.int32)
            self.recall_total = 0
            self.preretrieval_context = self.context
            self.update_context(self.delay_drift_rate, self.delay_context_input)
            self.update_context(self.start_drift_rate, self.start_context_input)
            self.retrieving = True

        # number of items to retrieve is infinite if steps is unspecified
        if steps is None:
            steps = self.item_count - self.recall_total
        steps = self.recall_total + steps

        # at each recall attempt
        while self.recall_total < steps:

            # the current state of context is used as a retrieval cue to
            # attempt recall of a studied item compute outcome probabilities
            # and make choice based on distribution
            self.outcome_probabilities()
            if np.any(self.probabilities[1:]):
                choice = np.sum(np.cumsum(self.probabilities) < np.random.rand(), dtype=np.int32)
            else:
                choice = 0

            # resolve and maybe store outcome
            # we stop recall if no choice is made (0)
            if choice == 0:
                self.retrieving = False
                self.context = self.preretrieval_context
                break

            self.recall[self.recall_total] = choice - 1
            self.recall_total += 1
            self.update_context(self.recall_drift_rate, self.items[choice - 1])
            
        return self.recall[: self.recall_total]

    def force_recall(self, choice=None):

        if not self.retrieving:
            self.recall = np.zeros(self.item_count, np.int32)
            self.recall_total = 0
            self.preretrieval_context = self.context
            self.update_context(self.delay_drift_rate, self.delay_context_input)
            self.update_context(self.start_drift_rate, self.start_context_input)
            self.retrieving = True

        if choice is None:
            pass
        elif choice > 0:
            self.recall[self.recall_total] = choice - 1
            self.recall_total += 1
            self.update_context(self.recall_drift_rate, self.items[choice - 1])
        else:
            self.retrieving = False
            self.context = self.preretrieval_context
        return self.recall[: self.recall_total]
