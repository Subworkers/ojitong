from workflow.const import operator_list
from workflow.utils import (
    get_letskorail,
    get_shinbundang,
    get_arex,
    get_uiline,
    get_ictr,
    get_station_info,
)


def main():
    for operator in operator_list:
        if operator == "한국철도공사":
            get_letskorail(operator)
        elif operator == "신분당선주식회사":
            get_shinbundang(operator)
        elif operator == "공항철도주식회사":
            get_arex(operator)
        elif operator == "우이신설경전철":
            get_uiline(operator)
        elif operator == "인천교통공사":
            get_ictr(operator)
        else:
            raise Exception("Invalid operator name")
    get_station_info()


if __name__ == "__main__":
    main()
