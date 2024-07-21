import json
import os
from datetime import datetime
from urllib.parse import urlencode

# Engine metadata
about = {
    "website": "https://www.tiktok.com",
    "wikidata_id": "Q48938223",
    "official_api_documentation": None,
    "use_official_api": False,
    "require_api_key": False,
    "results": "JSON",
}

# Engine configuration
paging = True
results_per_page = 12
categories = ["videos"]

# Search URL
base_url = "https://www.tiktok.com/api/search/general/full/"

# Example cookie to mimic the JavaScript logic
ttwid = os.getenv('TikTok_TTWID_TOKEN')
print('tiktok ttwid', ttwid)
cookie = {
    "ttwid": ttwid,
}


def request(keyword, params):
    params_dict = {
        "from_page": "search",
        "keyword": keyword,
        # "offset": params.get("offset", 0),
        # "search_id": params.get("search_id", "")
    }

    params["url"] = f"{base_url}?{urlencode(params_dict)}"
    params["cookies"] = cookie

    return params


def response(resp):
    print('tiktok resp', resp)
    print('Response content:', resp.text)  # Print the raw response content

    # Check if the response content is empty
    if not resp.content:
        print('Empty response content')
        return []

    try:
        search_res = resp.json()
    except json.JSONDecodeError as e:
        print(f'Error decoding JSON: {e}')
        print('Response content:', resp.text)  # Print the raw response content
        return []

    print('tiktok search_res', search_res)

    results = []
    for _item in search_res.get("data", []):
        print('_item', _item)

        if _item.get("type") == 1:
            item = _item.get("item", {})
            iframe_url = f"https://www.tiktok.com/embed/v2/{item.get('id', '')}"
            author = item.get("author", {})
            video = item.get("video", {})

            # https://www.tiktok.com/@evil0ctal/video/7156033831819037994
            video_url = f"https://www.tiktok.com/@{author.get('uniqueId', '')}/video/{item.get('id', '')}"

            results.append({
                "title": item.get("desc", ""),
                "url": video_url,
                # "url": video.get("playAddr", ""),
                # "url": video.get("downloadAddr", ""),
                "content": item.get("desc", ""),
                "author": author.get("nickname", ""),
                "publishedDate": datetime.utcfromtimestamp(item.get("createTime")),
                "thumbnail": video.get("cover", ""),
                "iframe_src": iframe_url,
                "template": "videos.html",
            })
    return results
