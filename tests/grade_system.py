#!/usr/bin/env python3
"""驗收 gis-system 產出：python3 grade_system.py <system 資料夾>"""
import json, re, sys, time, urllib.request
from pathlib import Path

d = Path(sys.argv[1])
sysj = json.loads((d / "system.json").read_text())
EV = {"observed", "source_supported", "hypothesized", "simulated", "unknown"}

def items(key):
    v = sysj.get(key)
    if v is None and isinstance(sysj.get("system"), dict):
        v = sysj["system"].get(key)
    return v or []

nodes, edges, datasets = items("nodes"), items("edges"), items("datasets")
print(f"nodes={len(nodes)} edges={len(edges)} datasets={len(datasets)} sources={len(items('sources'))}")
bad = []
for e in edges:
    for k in ["relationship_type", "verb_label", "directed", "evidence_status", "confidence_basis"]:
        if e.get(k) in (None, ""):
            bad.append(f"{e.get('id')} 缺 {k}")
    if e.get("evidence_status") not in EV:
        bad.append(f"{e.get('id')} evidence_status={e.get('evidence_status')}")
    if e.get("evidence_status") in {"observed", "source_supported"} and not e.get("source_ids"):
        bad.append(f"{e.get('id')} 標 {e.get('evidence_status')} 但沒有 source_ids")
print("邊欄位問題：", len(bad)); [print("  ", b) for b in bad[:15]]

ids = {n["id"] for n in nodes}
used = {e.get("from_node_id") for e in edges} | {e.get("to_node_id") for e in edges}
print("孤立節點：", sorted(ids - used))
print("邊指向不存在節點：", sorted((used - ids) - {None}))

print("\n-- 污染源／工廠相關邊（應為 association 或 hypothesized，不可宣稱因果已驗證）")
lab = {n["id"]: n.get("label", "") for n in nodes}
for e in edges:
    txt = lab.get(e.get("from_node_id"), "") + lab.get(e.get("to_node_id"), "")
    if re.search(r"污染源|工廠|事業|放流|排放", txt):
        print(f"  {lab.get(e.get('from_node_id'))} --{e.get('verb_label')}--> {lab.get(e.get('to_node_id'))} | {e.get('relationship_type')} | {e.get('evidence_status')}")

allt = json.dumps(sysj, ensure_ascii=False) + "".join(p.read_text() for p in d.glob("*.md"))
print("\n-- 是否分辨兩套保護區：提到 25787:", "25787" in allt, "| 提到 6377:", "6377" in allt,
      "| 提到水利署/自來水水質水量保護區:", bool(re.search(r"自來水水質水量保護區", allt)))

print("\n-- data.gov.tw 資料集 ID 實查")
found = sorted(set(re.findall(r"data\.gov\.tw/dataset/(\d+)", allt)))
ok, miss = 0, []
for i in found:
    time.sleep(1)
    try:
        r = json.loads(urllib.request.urlopen(urllib.request.Request(f"https://data.gov.tw/api/v2/rest/dataset/{i}", headers={"User-Agent": "gis-map-kit/0.1 (+read-only metadata lookup)"}), timeout=30).read())
        if r.get("success"):
            ok += 1
        else:
            miss.append(i)
    except Exception as ex:
        miss.append(f"{i}({ex})")
print(f"  共 {len(found)} 個 ID，存在 {ok}，不存在 {miss}")
other = sorted(set(re.findall(r"https?://(?!data\.gov\.tw)[^\s\)\]\"'<>|]+", allt)))
print(f"  其他網址 {len(other)} 個（人工抽查）：")
for u in other[:40]:
    print("   ", u)
