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
cookie = {
    "ttwid": os.getenv('TikTok_TTWID_TOKEN'),
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
    search_res = resp.json()
    print(search_res)

    results = []
    for _item in search_res.get("data", []):
        item = _item.get("item", {})
        print('_item', _item, item)
        iframe_url = f"https://www.tiktok.com/embed/v2/{item.get('id', '')}"
        results.append({
            "title": item.get("desc", ""),
            "url": item.get("video", {}).get("playAddr", ""),
            "content": item.get("desc", ""),
            "author": item.get("author", {}).get("nickname", ""),
            "publishedDate": datetime.utcfromtimestamp(item.get("createTime")).strftime('%Y-%m-%d'),
            "thumbnail": item.get("video", {}).get("cover", ""),
            "iframe_src": iframe_url,
            "template": "videos.html",
        })
    return results


