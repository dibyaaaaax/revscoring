from ....datasources.meta import dicts, filters
from ....dependencies import DependentSet
from ....features.meta import aggregators


class Revision(DependentSet):

    def __init__(self, name, revision_datasources):
        super().__init__(name)
        self.datasources = revision_datasources

        self.dict_words = aggregators.len(self.datasources.dict_words)
        self.non_dict_words = \
            aggregators.len(self.datasources.non_dict_words)

        if hasattr(self.datasources, 'parent'):
            self.parent = Revision(name + ".parent", self.datasources.parent)

        if hasattr(self.datasources, 'diff'):
            self.diff = Diff(name + ".diff", self.datasources.diff)


class Diff(DependentSet):

    def __init__(self, name, diff_datasources):
        super().__init__(name)
        self.datasources = diff_datasources

        # Simple counts (based on wikitext.edit.diff)
        self.dict_words_added = \
            aggregators.len(self.datasources.dict_words_added)
        self.dict_words_removed = \
            aggregators.len(self.datasources.dict_words_removed)
        self.non_dict_words_added = \
            aggregators.len(self.datasources.non_dict_words_added)
        self.non_dict_words_removed = \
            aggregators.len(self.datasources.non_dict_words_removed)

        # Word frequency deltas
        dict_word_delta_values = dicts.values(self.datasources.dict_word_delta)
        self.dict_word_delta_sum = aggregators.sum(
            dict_word_delta_values,
            name=name + ".dict_word_delta_sum",
            returns=int
        )
        self.dict_word_delta_increase = aggregators.sum(
            filters.positive(dict_word_delta_values),
            name=name + ".dict_word_delta_increase",
            returns=int
        )
        self.dict_word_delta_decrease = aggregators.sum(
            filters.negative(dict_word_delta_values),
            name=name + ".dict_word_delta_decrease",
            returns=int
        )
        non_dict_word_delta_values = \
            dicts.values(self.datasources.non_dict_word_delta)
        self.non_dict_word_delta_sum = aggregators.sum(
            non_dict_word_delta_values,
            name=name + ".non_dict_word_delta_sum",
            returns=int
        )
        self.non_dict_word_delta_increase = aggregators.sum(
            filters.positive(non_dict_word_delta_values),
            name=name + ".non_dict_word_delta_increase",
            returns=int
        )
        self.non_dict_word_delta_decrease = aggregators.sum(
            filters.negative(non_dict_word_delta_values),
            name=name + ".non_dict_word_delta_decrease",
            returns=int
        )

        # Proportional word frequency deltas
        dict_word_prop_delta_values = \
            dicts.values(self.datasources.dict_word_prop_delta)
        self.dict_word_prop_delta_sum = aggregators.sum(
            dict_word_prop_delta_values,
            name=name + ".dict_word_prop_delta_sum"
        )
        self.dict_word_prop_delta_increase = aggregators.sum(
            filters.positive(dict_word_prop_delta_values),
            name=name + ".dict_word_prop_delta_increase"
        )
        self.dict_word_prop_delta_decrease = aggregators.sum(
            filters.negative(dict_word_prop_delta_values),
            name=name + ".dict_word_prop_delta_decrease"
        )

        non_dict_word_prop_delta_values = \
            dicts.values(self.datasources.non_dict_word_prop_delta)
        self.non_dict_word_prop_delta_sum = aggregators.sum(
            non_dict_word_prop_delta_values,
            name=name + ".non_dict_word_prop_delta_sum"
        )
        self.non_dict_word_prop_delta_increase = aggregators.sum(
            filters.positive(non_dict_word_prop_delta_values),
            name=name + ".non_dict_word_prop_delta_increase"
        )
        self.non_dict_word_prop_delta_decrease = aggregators.sum(
            filters.negative(non_dict_word_prop_delta_values),
            name=name + ".non_dict_word_prop_delta_decrease"
        )
