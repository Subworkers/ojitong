from dateutil import parser

# datetime parser
def parse_any_datetime_format(date_str):
    return parser.parse(date_str).strftime('%Y-%m-%d %H:%M:%S')