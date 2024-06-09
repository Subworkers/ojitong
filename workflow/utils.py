import requests
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

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
***REMOVED***

# attachments = [
#             {
#                 "fallback": "Press the button to trigger an action.",
#                 "actions": [
#                     {
#                         "name": "my_button",
#                         "text": "Press me",
#                         "type": "button",
#                         "value": "button_pressed"
#                     ***REMOVED***
#                 ***REMOVED***
#             ***REMOVED***
#         ***REMOVED***

from datetime import datetime, timedelta

def within_one_month(date_to_check***REMOVED***:
    current_date = datetime.today(***REMOVED***
    one_week_ago = current_date - timedelta(weeks=4***REMOVED***
    return one_week_ago <= date_to_check <= current_date


def post_message(channel: str, text: str***REMOVED***:
    try:
        response = requests.post(
            slack_url,
            headers=slack_header,
            data={
                "channel": channel,
                "text": text,
            ***REMOVED***,  # , "attachments": json.dumps(attachments***REMOVED***
        ***REMOVED***
        print(response***REMOVED***
    except Exception as e:
        print(e***REMOVED***


def get_seoulmetro(operator: str***REMOVED***:
    response = requests.get(operator_url_dict[operator***REMOVED***, headers=stn_static_schedule_headers***REMOVED***

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser"***REMOVED***
        tr_elements = soup.find_all("tr"***REMOVED***

        data = [***REMOVED***
        for tr in tr_elements:
            if tr.find("th"***REMOVED***:
                continue
            td_elements = tr.find_all("td"***REMOVED***

            no = tr.find('td', class_='num t-disn bd1'***REMOVED***
            title = tr.find('td', class_='td-lf bd2'***REMOVED***.find('a'***REMOVED***.get_text(***REMOVED***
            link = tr.find('td', class_='td-lf bd2'***REMOVED***.find('a'***REMOVED***['href'***REMOVED***
            parsed_url = urlparse(link***REMOVED***
            query_params = parse_qs(parsed_url.query***REMOVED***
            bbs_idx = query_params.get('bbsIdx', [None***REMOVED******REMOVED***[0***REMOVED***
            date = tr.find('td', class_='t-disn bd5'***REMOVED***.get_text(***REMOVED***

            date_to_check = datetime.strptime(date, "%Y-%m-%d"***REMOVED***
            if within_one_month(date_to_check***REMOVED***:
                data.append(
                    {
                        "no": no, # post number
                        "title": title,
                        "date": date,
                        "link": f"{operator_url_dict[operator***REMOVED******REMOVED***&bbsIdx={bbs_idx***REMOVED***"
                    ***REMOVED***
                ***REMOVED***

        if len(data***REMOVED*** > 0:
            post_message(channel_name, f"*** {operator***REMOVED*** 운행사 공지사항 ***"***REMOVED***
            for idx, d in enumerate(data***REMOVED***:
                post_message(
                    channel_name,
                    f"{idx + 1***REMOVED***. 제목: <{d['link'***REMOVED******REMOVED***|{d['title'***REMOVED******REMOVED***> 날짜: {d['date'***REMOVED******REMOVED***",
                ***REMOVED***


def get_letskorail(operator: str***REMOVED***:
    response = requests.get(operator_url_dict[operator***REMOVED******REMOVED***

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser"***REMOVED***
        tr_elements = soup.find_all("tr"***REMOVED***

        data = [***REMOVED***
        for tr in tr_elements:
            keys = ["no", "type", "title", "button", "date"***REMOVED***
            if tr.find("th"***REMOVED***:
                continue
            td_elements = tr.find_all("td"***REMOVED***
            single_row = {key: td.text for key, td in zip(keys, td_elements***REMOVED******REMOVED***

            date_to_check = datetime.strptime(single_row["date"***REMOVED***, "%Y-%m-%d"***REMOVED***
            if within_one_month(date_to_check***REMOVED***:
                data.append(single_row***REMOVED***

        if len(data***REMOVED*** > 0:
            post_message(channel_name, f"*** {operator***REMOVED*** 운행사 공지사항 ***"***REMOVED***
            for idx, d in enumerate(data***REMOVED***:
                post_message(
                    channel_name,
                    f"{idx + 1***REMOVED***. 제목: <{operator_url_dict[operator***REMOVED******REMOVED***|{d['title'***REMOVED******REMOVED***> 날짜: {d['date'***REMOVED******REMOVED***",
                ***REMOVED***

    else:
        print(f"Failed to fetch data from the URL. Status code: {response.status_code***REMOVED***"***REMOVED***


def get_shinbundang(operator: str***REMOVED***:
    response = requests.get(operator_url_dict[operator***REMOVED******REMOVED***

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser"***REMOVED***
        rows = soup.tbody.find_all("tr"***REMOVED***

        data = [***REMOVED***
        for row in rows:
            title_elem = row.find("td"***REMOVED***.find_next_sibling("td"***REMOVED***.find("a"***REMOVED***
            title = title_elem.text.strip(***REMOVED***
            view_no = title_elem["href"***REMOVED***.split("'"***REMOVED***[1***REMOVED***
            date = row.find_all("td", class_="ac"***REMOVED***[-2***REMOVED***.text
            
            date_to_check = datetime.strptime(date, "%Y-%m-%d"***REMOVED***
            if within_one_month(date_to_check***REMOVED***:
                data.append(
                    {
                        "view_no": view_no,
                        "title": title,
                        "date": date,
                    ***REMOVED***
                ***REMOVED***

        if len(data***REMOVED*** > 0:
            post_message(channel_name, f"*** {operator***REMOVED*** 운행사 공지사항 ***"***REMOVED***
            for idx, d in enumerate(data***REMOVED***:
                single_page_url = f"{shinbundang_single_page_front_url***REMOVED***{d['view_no'***REMOVED******REMOVED***{shinbundang_single_page_back_url***REMOVED***"
                post_message(
                    channel_name,
                    f"{idx + 1***REMOVED***. 제목: <{single_page_url***REMOVED***|{d['title'***REMOVED******REMOVED***> 날짜: {d['date'***REMOVED******REMOVED***",
                ***REMOVED***

    else:
        print(f"Failed to fetch data from the URL. Status code: {response.status_code***REMOVED***"***REMOVED***


def get_arex(operator: str***REMOVED***:
    response = requests.get(operator_url_dict[operator***REMOVED******REMOVED***

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser"***REMOVED***
        table_div = soup.find("div", class_="table01 boardTable"***REMOVED***
        tbody = table_div.find("tbody"***REMOVED***
        rows = tbody.find_all("tr"***REMOVED***

        data = [***REMOVED***

        for row in rows:
            cols = row.find_all("td"***REMOVED***

            title_tag = cols[1***REMOVED***.find("a", class_="detail_view"***REMOVED***
            title = title_tag.get_text(strip=True***REMOVED***
            data_no = title_tag["data-no"***REMOVED***
            date = cols[2***REMOVED***.get_text(strip=True***REMOVED***

            date_to_check = datetime.strptime(date, "%Y-%m-%d"***REMOVED***
            if within_one_month(date_to_check***REMOVED***:
                data.append(
                    {
                        "title": title,
                        "data_no": data_no,
                        "date": date,
                    ***REMOVED***
                ***REMOVED***

        if len(data***REMOVED*** > 0:
            post_message(channel_name, f"*** {operator***REMOVED*** 운행사 공지사항 ***"***REMOVED***
            for idx, d in enumerate(data***REMOVED***:
                single_page_url = f"{arex_single_page_front_url***REMOVED***{d['data_no'***REMOVED******REMOVED***{arex_single_page_back_url***REMOVED***"
                post_message(
                    channel_name,
                    f"{idx + 1***REMOVED***. 제목: <{single_page_url***REMOVED***|{d['title'***REMOVED******REMOVED***> 날짜: {d['date'***REMOVED******REMOVED***",
                ***REMOVED***

    else:
        print(f"Failed to fetch data from the URL. Status code: {response.status_code***REMOVED***"***REMOVED***


def get_uiline(operator: str***REMOVED***:
    response = requests.get(operator_url_dict[operator***REMOVED******REMOVED***

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser"***REMOVED***
        rows = soup.tbody.find_all("tr"***REMOVED***

        data = [***REMOVED***  # create an empty list to store the data of the current row
        keys = ["no", "single_page_url", "title", "writer", "date", "view"***REMOVED***

        for row in rows:
            single_row = [***REMOVED***
            for cell in row.find_all("td"***REMOVED***:
                anchor = cell.find("a"***REMOVED***
                if anchor:
                    # Append the href attribute to the data list
                    single_row.append(anchor["href"***REMOVED******REMOVED***
                    # Append the anchor text to the data list
                    single_row.append(anchor.text.strip(***REMOVED******REMOVED***
                else:
                    # Append the cell text to the data list
                    single_row.append(cell.text.strip(***REMOVED******REMOVED***

            date_to_check = datetime.strptime(single_row[4***REMOVED***, "%Y-%m-%d"***REMOVED***
            if within_one_month(date_to_check***REMOVED***:
                data.append({key: value for key, value in zip(keys, single_row***REMOVED******REMOVED******REMOVED***

        if len(data***REMOVED*** > 0:
            post_message(channel_name, f"*** {operator***REMOVED*** 운행사 공지사항 ***"***REMOVED***
            for idx, d in enumerate(data***REMOVED***:
                single_page_url = uiline_single_page_front_url + d["single_page_url"***REMOVED***
                post_message(
                    channel_name,
                    f"{idx + 1***REMOVED***. 제목: <{single_page_url***REMOVED***|{d['title'***REMOVED******REMOVED***> 날짜: {d['date'***REMOVED******REMOVED***",
                ***REMOVED***

    else:
        print(f"Failed to fetch data from the URL. Status code: {response.status_code***REMOVED***"***REMOVED***


def get_ictr(operator: str***REMOVED***:
    response = requests.get(operator_url_dict[operator***REMOVED******REMOVED***

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser"***REMOVED***
        li_elements = soup.find("ul", class_="generalList"***REMOVED***.find_all("li"***REMOVED***

        data = [***REMOVED***

        for li in li_elements:
            title_element = li.find("p", class_="title"***REMOVED***
            title = title_element.get_text(strip=True***REMOVED*** if title_element else None
            single_page_url = title_element.find("a"***REMOVED***["href"***REMOVED*** if title_element else None

            date_element = li.find("li", {"title": "작성일"***REMOVED******REMOVED***
            date = date_element.get_text(strip=True***REMOVED*** if date_element else None

            if None in [title, date***REMOVED***:
                continue
            
            date_to_check = datetime.strptime(date, "%Y.%m.%d"***REMOVED***
            if within_one_month(date_to_check***REMOVED***:
                data.append(
                    {"title": title, "single_page_url": single_page_url, "date": date***REMOVED***
                ***REMOVED***

        if len(data***REMOVED*** > 0:
            post_message(channel_name, f"*** {operator***REMOVED*** 운행사 공지사항 ***"***REMOVED***
            for idx, d in enumerate(data***REMOVED***:
                single_page_url = ictr_single_page_front_url + d["single_page_url"***REMOVED***
                post_message(
                    channel_name,
                    f"{idx + 1***REMOVED***. 제목: <{single_page_url***REMOVED***|{d['title'***REMOVED******REMOVED***> 날짜: {d['date'***REMOVED******REMOVED***",
                ***REMOVED***

    else:
        print(f"Failed to fetch data from the URL. Status code: {response.status_code***REMOVED***"***REMOVED***


def get_station_info(***REMOVED***:
    response = requests.get(
        realtime_station_info_url, headers=stn_static_schedule_headers
    ***REMOVED***

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser"***REMOVED***

        table_rows = soup.find_all("tr"***REMOVED***

        for row in table_rows:
            columns = row.find_all("td"***REMOVED***

            # Make sure that we have enough columns before trying to access them
            if len(columns***REMOVED*** >= 6:
                # Extract the file name from the title attribute of the span element within the third td
                file_name = columns[2***REMOVED***.span["title"***REMOVED***

                # Extract the fifth column (index 4***REMOVED***
                updated_date = columns[4***REMOVED***.text.strip(***REMOVED***
        date_to_check = datetime.strptime(updated_date, "%Y.%m.%d."***REMOVED***
        if within_one_month(date_to_check***REMOVED***:
            post_message(channel_name, f"*** 실시간 역 정보 변동 사항 ***"***REMOVED***
            post_message(channel_name, f"파일 이름: <{realtime_station_info_url***REMOVED***|{file_name***REMOVED***>"***REMOVED***
            
    else:
        print(f"Failed to fetch data from the URL. Status code: {response.status_code***REMOVED***"***REMOVED***
