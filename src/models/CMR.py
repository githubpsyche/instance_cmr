import numpy as np
from numba import float64, int32, boolean
from numba.experimental import jitclass

cmr_spec = [
    ("item_count", int32),
    ("encoding_drift_rate", float64),
    ("delay_drift_rate", float64),
    ("start_drift_rate", float64),
    ("recall_drift_rate", float64),
    ("shared_support", float64),
    ("item_support", float64),
    ("learning_rate", float64),
    ("primacy_scale", float64),
    ("primacy_decay", float64),
    ("stop_probability_scale", float64),
    ("stop_probability_growth", float64),
    ("choice_sensitivity", float64),
    ("context", float64[::1]),
    ("start_context_input", float64[::1]),
    ("delay_context_input", float64[::1]),
    ("preretrieval_context", float64[::1]),
    ("recall", int32[::1]),
    ("retrieving", boolean),
    ("recall_total", int32),
    ("primacy_weighting", float64[::1]),
    ("probabilities", float64[::1]),
    ("mfc", float64[:, ::1]),
    ("mcf", float64[:, ::1]),
    ("encoding_index", int32),
    ("items", float64[:, ::1]),
]


@jitclass(cmr_spec)
class Classic_CMR:
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

        # at the start of the list context is initialized with a state
        # orthogonal to the pre-experimental context
        # associated with the set of items
        self.context = np.zeros(item_count + 2)
        self.context[0] = 1
        self.preretrieval_context = self.context
        self.retrieving = False
        self.recall_total = 0
        self.recall = np.zeros(item_count, int32)

        # predefine primacy weighting vectors
        self.primacy_weighting = (
            parameters["primacy_scale"]
            * np.exp(-parameters["primacy_decay"] * np.arange(presentation_count))
            + 1
        )

        # preallocate for outcome_probabilities
        self.probabilities = np.zeros((item_count + 1))

        # predefine contextual input vectors relevant for delay_drift_rate and start_drift_rate parameters
        self.start_context_input = np.zeros((self.item_count + 2))
        self.start_context_input[0] = 1
        self.delay_context_input = np.zeros((self.item_count + 2))
        self.delay_context_input[-1] = 1

        # The two layers communicate with one another through two sets of
        # associative connections represented by matrices Mfc and Mcf.
        # Pre-experimental Mfc is 1-learning_rate and pre-experimental Mcf is
        # item_support for i=j. For i!=j, Mcf is shared_support.
        self.mfc = np.eye(item_count, item_count + 2, 1) * (1 - self.learning_rate)
        self.mcf = np.ones((item_count, item_count)) * self.shared_support
        for i in range(item_count):
            self.mcf[i, i] = self.item_support
        self.mcf = np.vstack(
            (np.zeros((1, item_count)), self.mcf, np.zeros((1, item_count)))
        )
        self.encoding_index = 0
        self.items = np.eye(item_count, item_count)

    def experience(self, experiences):

        for i in range(len(experiences)):
            self.update_context(self.encoding_drift_rate, experiences[i])
            self.mfc += self.learning_rate * np.outer(self.context, experiences[i]).T
            self.mcf += self.primacy_weighting[self.encoding_index] * np.outer(
                self.context, experiences[i]
            )
            self.encoding_index += 1

    def update_context(self, drift_rate, experience):

        # first pre-experimental or initial context is retrieved
        if len(experience) == len(self.mfc):
            context_input = np.dot(experience, self.mfc)
            context_input /= np.sqrt(
                np.sum(np.square(context_input))
            )  # norm to length 1
        else:
            # but sometimes we specify contextual input directly
            context_input = experience

        # new context is sum of context and input, modulated by rho to have len 1 and some drift_rate
        rho = np.sqrt(
            1
            + np.square(min(drift_rate, 1.0))
            * (np.square(self.context * context_input) - 1)
        ) - (min(drift_rate, 1.0) * (self.context * context_input))
        self.context = (rho * self.context) + (min(drift_rate, 1.0) * context_input)

    def activations(self, probe, use_mfc=False):
        if use_mfc:
            return np.dot(probe, self.mfc) + 10e-7
        else:
            return np.dot(probe, self.mcf) + 10e-7

    def outcome_probabilities(self):

        self.probabilities[0] = min(
            self.stop_probability_scale
            * np.exp(self.recall_total * self.stop_probability_growth),
            1.0 - ((self.item_count - self.recall_total) * 10e-7),
        )
        self.probabilities[1:] = 10e-7
        self.probabilities[self.recall[: self.recall_total] + 1] = 0

        if self.probabilities[0] < (
            1.0 - ((self.item_count - self.recall_total) * 10e-7)
        ):

            # measure the activation for each item; already recalled items have zero activation
            activation = self.activations(self.context)
            activation[self.recall[: self.recall_total]] = 0

            if np.sum(activation) > 0:

                # power sampling rule
                activation = np.power(activation, self.choice_sensitivity)

                # normalized result downweighted by stop prob is probability of choosing each item
                self.probabilities[1:] = (
                    (1 - self.probabilities[0]) * activation / np.sum(activation)
                )

        return self.probabilities

    def free_recall(self, steps=None):

        # some amount of the pre-list context is reinstated before initiating the recall
        if not self.retrieving:
            self.recall = np.zeros(self.item_count, int32)
            self.recall_total = 0
            self.preretrieval_context = self.context
            self.update_context(self.delay_drift_rate, self.delay_context_input)
            self.update_context(self.start_drift_rate, self.start_context_input)
            self.retrieving = True

        # number of items to retrieve is # of items left to recall if steps is unspecified
        if steps is None:
            steps = self.item_count - self.recall_total
        steps = self.recall_total + steps

        # at each recall attempt,
        while self.recall_total < steps:

            # the current state of context is used as a retrieval cue
            # we compute outcome probabilities and make choice based on distribution
            outcome_probabilities = self.outcome_probabilities()
            if np.any(outcome_probabilities[1:]):
                choice = np.sum(
                    np.cumsum(outcome_probabilities) < np.random.rand(), dtype=int32
                )
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
            self.recall = np.zeros(self.item_count, int32)
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
