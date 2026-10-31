#!/usr/bin/env python3
"""data.gov.tw 唯讀查詢小工具（只用標準函式庫，內建限速）。

  python3 datagov.py meta <資料集ID或網址>      讀單一資料集 metadata（標題、機關、格式、欄位、更新頻率、授權、下載網址）
  python3 datagov.py search <關鍵字…> [--size N] 全文搜尋資料集（多個詞以空白分開會合併成一個查詢；預設 10 筆，上限 50）

注意：
- meta 用 data.gov.tw 公開的 /api/v2/rest/dataset/<id>；search 用網站前台的 /api/front/dataset/list，
  不是正式文件化的 API，格式可能變動，失敗時改用 WebSearch「site:data.gov.tw <關鍵字>」。
- 輸出會遮掉下載網址裡的 api_key 參數值，也不輸出聯絡人個資。
- 每次請求間隔至少 1 秒；不要用迴圈大量呼叫。
"""
import json
import re
import sys
import time
import urllib.request

BASE = "https://data.gov.tw"
UA = "gis-map-kit/0.1 (+read-only metadata lookup)"
_last = 0.0


def _request(url: str, body: dict | None = None) -> dict:
    global _last
    wait = 1.0 - (time.time() - _last)
    if wait > 0:
        time.sleep(wait)
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers={"User-Agent": UA, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        _last = time.time()
        return json.loads(r.read().decode("utf-8"))


def _mask(url: str) -> str:
    return re.sub(r"(api_key=)[^&]+", r"\1<REDACTED>", url or "")


def meta(arg: str) -> dict:
    m = re.search(r"(\d+)", arg)
    if not m:
        raise SystemExit("找不到資料集 ID")
    res = _request(f"{BASE}/api/v2/rest/dataset/{m.group(1)}")
    if not res.get("success"):
        raise SystemExit(f"查詢失敗：{res.get('error')}")
    d = res["result"]
    return {
        "dataset_id": d.get("datasetId"),
        "landing_url": f"{BASE}/dataset/{d.get('datasetId')}",
        "title": d.get("title"),
        "description": d.get("description"),
        "publisher_oid": d.get("publisherOID"),
        "agency": d.get("publisher") or d.get("agency"),
        "type": d.get("type"),
        "license_code": d.get("license"),
        "cost": d.get("cost"),
        "update_frequency": d.get("updateFrequency"),
        "spatial_coverage": d.get("spatialCoverage"),
        "temporal_coverage": [d.get("coverageStartedDate"), d.get("coverageEndedDate")],
        "modified": d.get("modifiedDate"),
        "related_url": d.get("relatedUrl"),
        "notes": d.get("notes"),
        "distribution": [
            {
                "description": x.get("resourceDescription"),
                "format": x.get("resourceFormat"),
                "encoding": x.get("resourceCharacterEncoding"),
                "download_url": _mask(x.get("resourceDownloadUrl")),
                "fields": [f"{f.get('name')}：{f.get('description')}" for f in x.get("resourceField") or []],
            }
            for x in d.get("distribution") or []
        ],
    }


def search(keyword: str, size: int = 10) -> dict:
    size = max(1, min(int(size), 50))
    body = {
        "bool": [{"fulltext": {"value": keyword}}],
        "filter": [],
        "page_num": 1,
        "page_limit": size,
        "tids": [],
        "sort": "_score_desc",
    }
    p = _request(f"{BASE}/api/front/dataset/list", body)["payload"]
    return {
        "keyword": keyword,
        "total": p.get("search_count"),
        "results": [
            {
                "dataset_id": r.get("nid"),
                "landing_url": f"{BASE}/dataset/{r.get('nid')}",
                "title": r.get("title"),
                "agency": r.get("agency_name"),
                "category": r.get("category_name"),
                "formats": r.get("all_file_format_name"),
                "update_frequency": r.get("updatefreq_desc"),
                "license": r.get("license_name"),
                "tags": r.get("all_tag_name"),
                "updated": (r.get("changed") or {}).get("date", "")[:10] if isinstance(r.get("changed"), dict) else r.get("changed"),
            }
            for r in p.get("search_result") or []
        ],
    }


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in {"meta", "search"}:
        print(__doc__)
        sys.exit(2)
    if sys.argv[1] == "meta":
        out = meta(sys.argv[2])
    else:
        args, size = sys.argv[2:], 10
        if "--size" in args:
            i = args.index("--size")
            size = int(args[i + 1])
            args = args[:i] + args[i + 2:]
        out = search(" ".join(args), size)
    print(json.dumps(out, ensure_ascii=False, indent=1))
