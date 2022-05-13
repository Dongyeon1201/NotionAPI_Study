def print_json_pretty(json_obj):
    print(json.dumps(json_obj, indent=4, sort_keys=True, ensure_ascii=False))


def db_info(ID, headers, content=False, filter={}, page_size=100):

    if content:
        url = f"https://api.notion.com/v1/databases/{ID}/query"
        payload = {
            "page_size": page_size,
        }

        if filter:
            payload["filter"] = filter

        response = requests.post(url, headers=headers, json=payload)
    else:
        url = f"https://api.notion.com/v1/databases/{ID}"
        response = requests.get(url, headers=headers)

    return json.loads(response.text)


def db_row_add(ID, headers, properties={}):
    url = f"https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": ID},
        "properties": properties,
    }
    response = requests.post(url, headers=headers, json=payload)
    return json.loads(response.text)


import requests
import json
from datetime import datetime

NOTION_DATABASE_ID = ""
SECRET_TOKEN = ""

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22",
    "Authorization": SECRET_TOKEN,
}

# Daily 작업들만 확인하는 필터
# Daily 옵션이 Yes 이며, 날짜 값이 존재하지 않을 때
filter_json = {
    "and": [{"property": "Daily", "select": {"equals": "Yes"}}, {"property": "날짜", "date": {"is_empty": True}}]
}

# Daily 작업 조회 결과
daily_tasks = db_info(NOTION_DATABASE_ID, headers, content=True, filter=filter_json)

# 각 Daily 작업을 1개씩 오늘 날짜로 추가
for row in daily_tasks["results"]:

    properties_data = {}

    # 모든 속성 그대로
    for property, data in row["properties"].items():

        # 날짜 속성은 오늘 날짜로 설정
        if data["type"] == "date":
            properties_data[property] = {
                "start": datetime.now().strftime("%Y-%m-%d"),
            }
        else:
            properties_data[property] = data[data["type"]]

    # 오늘 작업에 추가
    db_row_add(NOTION_DATABASE_ID, headers, properties=properties_data)
