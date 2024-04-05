from data.const import operator_list
from workflow.utils import (
    get_letskorail,
    get_shinbundang,
    get_arex,
    get_uiline,
    get_ictr,
    get_station_info,
***REMOVED***


def main(***REMOVED***:
    for operator in operator_list:
        if operator == "한국철도공사":
            get_letskorail(operator***REMOVED***
        elif operator == "신분당선주식회사":
            get_shinbundang(operator***REMOVED***
        elif operator == "공항철도주식회사":
            get_arex(operator***REMOVED***
        elif operator == "우이신설경전철":
            get_uiline(operator***REMOVED***
        elif operator == "인천교통공사":
            get_ictr(operator***REMOVED***
        else:
            raise Exception("Invalid operator name"***REMOVED***
    get_station_info(***REMOVED***


if __name__ == "__main__":
    main(***REMOVED***
