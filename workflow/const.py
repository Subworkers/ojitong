# 운행사 공지사항 URL
channel_name = "운행사공지사항"
operator_list = [
    "한국철도공사",
    "신분당선주식회사",
    "공항철도주식회사",
    "우이신설경전철",
    "인천교통공사",
]
operator_url_dict = {
    "한국철도공사": "https://www.letskorail.com/ebizcom/cs/guide/guide/guide11.do",
    "신분당선주식회사": "https://www.shinbundang.co.kr/index.jsp?open_main=3&open_sub1=1&open_sub2=0&pageID=%2Fnotice%2Fnotice1.jsp&flag=",
    "공항철도주식회사": "https://www.arex.or.kr/content.do?url=&menuNo=MN201504230000000001&contentNo=&clientLocale=ko_KR&clientDevice=Normal",
    "우이신설경전철": "http://ui-line.com/html/info/info01/info_01_00.php?nowPage=1",
    "인천교통공사": "https://www.ictr.or.kr/main/board/notice.jsp",
}

shinbundang_single_page_front_url = "https://www.shinbundang.co.kr/index.jsp?pageID=%2Fnotice%2Fnotice1_view.jsp&open_main=3&open_sub1=1&open_sub2=0&viewNo="
shinbundang_single_page_back_url = "&nowPage=1&searchColumn=All&searchWord="
arex_single_page_front_url = "https://www.arex.or.kr/contentView.do?menuNo=MN201504230000000001&etcNo=ET201504230000000002&contentNo="
arex_single_page_back_url = "&searchCondition=0&searchKeyword=&pageIndex=1"
uiline_single_page_front_url = "http://ui-line.com/html/info/info01/"
ictr_single_page_front_url = "https://www.ictr.or.kr"

# 지하철 역 이름 확인
realtime_station_info_url = (
    "https://data.seoul.go.kr/dataList/OA-12764/F/1/datasetView.do"
)

# Slack Token
slack_url = "https://slack.com/api/chat.postMessage"
slack_token = "xoxb-4422415781072-5184316833383-GtI10lIjejPr3MaQoIUz6sG5"
slack_header = {"Authorization": "Bearer " + slack_token}


stn_static_schedule_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0"
}