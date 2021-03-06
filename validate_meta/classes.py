import pandas as pd
from pandas_schema import Column, Schema
from pandas_schema.validation import LeadingWhitespaceValidation, CustomElementValidation, \
    TrailingWhitespaceValidation, MatchesPatternValidation, InRangeValidation, InListValidation, IsDistinctValidation, \
    DateFormatValidation
import datetime


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
            if 'lead_trail_whitespace' in definition['fields'][field_name]:
                validators.append(LeadingWhitespaceValidation())
                validators.append(TrailingWhitespaceValidation())

            if 'distinct' in definition['fields'][field_name]:
                validators.append(IsDistinctValidation())

            if 'pattern' in definition['fields'][field_name]:
                validators.append(MatchesPatternValidation(definition['fields'][field_name]['pattern']))

            if 'list' in definition['fields'][field_name]:
                validators.append(InListValidation(definition['fields'][field_name]['list']))

            if 'range' in definition['fields'][field_name]:
                validators.append(InRangeValidation(definition['fields'][field_name]['range']['start'],
                                                    definition['fields'][field_name]['range']['end']))

            if 'sane_date_pattern' in definition['fields'][field_name]:
                validators.append(DateFormatSanityValidation(definition['fields'][field_name]['sane_date_pattern']['pattern'],
                                                             definition['fields'][field_name]['sane_date_pattern']['sane_start']))

            columns.append(Column(field_name, validators))

        return Schema(columns)

    def validate(self):
        return self.schema.validate(self.df)


class DateFormatSanityValidation(DateFormatValidation):
    """
    Checks that each element in this column is a valid date according to a provided format string
    and within a sane timeframe
    """

    def __init__(self, date_format: str, sane_start: str, **kwargs):
        """
        :param date_format: The date format string to validate the column against. Refer to the date format code
            documentation at https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior for a full
            list of format codes
        """
        self.date_format = date_format
        _datetime_start = datetime.datetime.strptime(sane_start, self.date_format)
        self.interval_start_val = _datetime_start.date()
        self.interval_end_val = datetime.date.today()
        super().__init__(self.date_format, **kwargs)

    @property
    def default_message(self):
        return 'Invalid date format or outside valid interval "{}"'.format(self.date_format)

    def valid_date(self, val):
        try:
            sample_date = datetime.datetime.strptime(val, self.date_format)
            sample_date = sample_date.date()
        except:
            return False

        if not self.interval_start_val <= sample_date <= self.interval_end_val:
            return False

        return True

    def validate(self, series: pd.Series) -> pd.Series:
        return series.astype(str).apply(self.valid_date)
