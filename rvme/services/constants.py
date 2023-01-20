from model_utils import Choices

STATS_TIME_PERIODS = Choices(
    ('001_day', 'Last Day'),
    ('007_week', 'Last Week'),
    ('031_month', 'Last Month'),
    ('091_threemonths', 'Last 3 Months'),
    ('183_sixmonths', 'Last 6 Months'),
    ('365_year', 'Last Year'),
)
