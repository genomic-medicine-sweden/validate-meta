import pandas as pd
from pandas_schema import Column, Schema
from pandas_schema.validation import LeadingWhitespaceValidation, \
    TrailingWhitespaceValidation, MatchesPatternValidation, InRangeValidation, InListValidation, IsDistinctValidation


class DataFrameValidator:
    def __init__(self, df, definition):
        self.df = df
        self.definition = definition
        self.schema = self.create_schema(self.definition)

    def create_schema(self, definition):
        """
        Returns Schema based on definition dict
        """
        columns = []

        for field_name in definition['fields']:
            validators = []
            if 'distinct' in definition['fields'][field_name]:
                validators.append(IsDistinctValidation())
            if 'pattern' in definition['fields'][field_name]:
                validators.append(MatchesPatternValidation(definition['fields'][field_name]['pattern']))
            if 'list' in definition['fields'][field_name]:
                validators.append(InListValidation(definition['fields'][field_name]['list']))
            if 'range' in definition['fields'][field_name]:
                validators.append(InRangeValidation(definition['fields'][field_name]['range']))

            columns.append(Column(field_name, validators))

        return Schema(columns)

    # @staticmethod
    # def mk_distinct_validator():
    #     return IsDistinctValidation()
    #
    # @staticmethod
    # def mk_pattern_validator(pat):
    #     return MatchesPatternValidation(pat)
    #
    # @staticmethod
    # def mk_list_validator(lst):
    #     return InListValidation(lst)
    #
    # @staticmethod
    # def mk_range_validator(rng):
    #     return InRangeValidation(rng[0], rng[1])

    def validate(self):
        return self.schema.validate(self.df)


