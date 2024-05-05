import requests
from datetime import datetime
from bs4 import BeautifulSoup

# import json
from workflow.const import (
    slack_url,
    slack_header,
    channel_name,
    operator_url_dict,
    shinbundang_single_page_front_url,
    shinbundang_single_page_back_url,
    arex_single_page_front_url,
    arex_single_page_back_url,
    uiline_single_page_front_url,
    ictr_single_page_front_url,
    realtime_station_info_url,
    stn_static_schedule_headers,
)

# attachments = [
#             {
#                 "fallback": "Press the button to trigger an action.",
#                 "actions": [
#                     {
#                         "name": "my_button",
#                         "text": "Press me",
#                         "type": "button",
#                         "value": "button_pressed"
#                     }
#                 ]
#             }
#         ]

from datetime import datetime, timedelta

def within_one_month(date_to_check):
    current_date = datetime.today()
    one_week_ago = current_date - timedelta(weeks=4)
    return one_week_ago <= date_to_check <= current_date


def post_message(channel: str, text: str):
    try:
        response = requests.post(
            slack_url,
            headers=slack_header,
            data={
                "channel": channel,
                "text": text,
            },  # , "attachments": json.dumps(attachments)
        )
        print(response)
    except Exception as e:
        print(e)


def get_letskorail(operator: str):
    response = requests.get(operator_url_dict[operator])

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        tr_elements = soup.find_all("tr")

        data = []
        for tr in tr_elements:
            keys = ["no", "type", "title", "button", "date"]
            if tr.find("th"):
                continue
            td_elements = tr.find_all("td")
            single_row = {key: td.text for key, td in zip(keys, td_elements)}

            date_to_check = datetime.strptime(single_row["date"], "%Y-%m-%d")
            if within_one_month(date_to_check):
                data.append(single_row)

        if len(data) > 0:
            post_message(channel_name, f"*** {operator} 운행사 공지사항 ***")
            for idx, d in enumerate(data):
                post_message(
                    channel_name,
                    f"{idx + 1}. 제목: <{operator_url_dict[operator]}|{d['title']}> 날짜: {d['date']}",
                )

    else:
        print(f"Failed to fetch data from the URL. Status code: {response.status_code}")


def get_shinbundang(operator: str):
    response = requests.get(operator_url_dict[operator])

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.tbody.find_all("tr")

        data = []
        for row in rows:
            title_elem = row.find("td").find_next_sibling("td").find("a")
            title = title_elem.text.strip()
            view_no = title_elem["href"].split("'")[1]
            date = row.find_all("td", class_="ac")[-2].text
            
            date_to_check = datetime.strptime(date, "%Y-%m-%d")
            if within_one_month(date_to_check):
                data.append(
                    {
                        "view_no": view_no,
                        "title": title,
                        "date": date,
                    }
                )

        if len(data) > 0:
            post_message(channel_name, f"*** {operator} 운행사 공지사항 ***")
            for idx, d in enumerate(data):
                single_page_url = f"{shinbundang_single_page_front_url}{d['view_no']}{shinbundang_single_page_back_url}"
                post_message(
                    channel_name,
                    f"{idx + 1}. 제목: <{single_page_url}|{d['title']}> 날짜: {d['date']}",
                )

    else:
        print(f"Failed to fetch data from the URL. Status code: {response.status_code}")


def get_arex(operator: str):
    response = requests.get(operator_url_dict[operator])

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        table_div = soup.find("div", class_="table01 boardTable")
        tbody = table_div.find("tbody")
        rows = tbody.find_all("tr")

        data = []

        for row in rows:
            cols = row.find_all("td")

            title_tag = cols[1].find("a", class_="detail_view")
            title = title_tag.get_text(strip=True)
            data_no = title_tag["data-no"]
            date = cols[2].get_text(strip=True)

            date_to_check = datetime.strptime(date, "%Y-%m-%d")
            if within_one_month(date_to_check):
                data.append(
                    {
                        "title": title,
                        "data_no": data_no,
                        "date": date,
                    }
                )

        if len(data) > 0:
            post_message(channel_name, f"*** {operator} 운행사 공지사항 ***")
            for idx, d in enumerate(data):
                single_page_url = f"{arex_single_page_front_url}{d['data_no']}{arex_single_page_back_url}"
                post_message(
                    channel_name,
                    f"{idx + 1}. 제목: <{single_page_url}|{d['title']}> 날짜: {d['date']}",
                )

    else:
        print(f"Failed to fetch data from the URL. Status code: {response.status_code}")


def get_uiline(operator: str):
    response = requests.get(operator_url_dict[operator])

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.tbody.find_all("tr")

        data = []  # create an empty list to store the data of the current row
        keys = ["no", "single_page_url", "title", "writer", "date", "view"]

        for row in rows:
            single_row = []
            for cell in row.find_all("td"):
                anchor = cell.find("a")
                if anchor:
                    # Append the href attribute to the data list
                    single_row.append(anchor["href"])
                    # Append the anchor text to the data list
                    single_row.append(anchor.text.strip())
                else:
                    # Append the cell text to the data list
                    single_row.append(cell.text.strip())

            date_to_check = datetime.strptime(single_row[4], "%Y-%m-%d")
            if within_one_month(date_to_check):
                data.append({key: value for key, value in zip(keys, single_row)})

        if len(data) > 0:
            post_message(channel_name, f"*** {operator} 운행사 공지사항 ***")
            for idx, d in enumerate(data):
                single_page_url = uiline_single_page_front_url + d["single_page_url"]
                post_message(
                    channel_name,
                    f"{idx + 1}. 제목: <{single_page_url}|{d['title']}> 날짜: {d['date']}",
                )

    else:
        print(f"Failed to fetch data from the URL. Status code: {response.status_code}")


def get_ictr(operator: str):
    response = requests.get(operator_url_dict[operator])

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        li_elements = soup.find("ul", class_="generalList").find_all("li")

        data = []

        for li in li_elements:
            title_element = li.find("p", class_="title")
            title = title_element.get_text(strip=True) if title_element else None
            single_page_url = title_element.find("a")["href"] if title_element else None

            date_element = li.find("li", {"title": "작성일"})
            date = date_element.get_text(strip=True) if date_element else None

            if None in [title, date]:
                continue
            
            date_to_check = datetime.strptime(date, "%Y.%m.%d")
            if within_one_month(date_to_check):
                data.append(
                    {"title": title, "single_page_url": single_page_url, "date": date}
                )

        if len(data) > 0:
            post_message(channel_name, f"*** {operator} 운행사 공지사항 ***")
            for idx, d in enumerate(data):
                single_page_url = ictr_single_page_front_url + d["single_page_url"]
                post_message(
                    channel_name,
                    f"{idx + 1}. 제목: <{single_page_url}|{d['title']}> 날짜: {d['date']}",
                )

    else:
        print(f"Failed to fetch data from the URL. Status code: {response.status_code}")


def get_station_info():
    response = requests.get(
        realtime_station_info_url, headers=stn_static_schedule_headers
    )

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        table_rows = soup.find_all("tr")

        for row in table_rows:
            columns = row.find_all("td")

            # Make sure that we have enough columns before trying to access them
            if len(columns) >= 6:
                # Extract the file name from the title attribute of the span element within the third td
                file_name = columns[2].span["title"]

                # Extract the fifth column (index 4)
                updated_date = columns[4].text.strip()
        date_to_check = datetime.strptime(updated_date, "%Y.%m.%d.")
        if within_one_month(date_to_check):
            post_message(channel_name, f"*** 실시간 역 정보 변동 사항 ***")
            post_message(channel_name, f"파일 이름: <{realtime_station_info_url}|{file_name}>")
            
    else:
        print(f"Failed to fetch data from the URL. Status code: {response.status_code}")
