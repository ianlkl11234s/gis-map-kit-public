#!/usr/bin/env python3
"""gis-system 產出的硬性檢查：python3 check_system.py <system 資料夾>

檢查 system.json（格式見 knowledge/00-system-thinking/00-09）：
- 每條邊有 relationship_type、verb_label、directed、evidence_status、confidence_basis
- evidence_status 只能是 observed／source_supported／hypothesized／simulated／unknown
- 標 observed／source_supported 的節點與邊，必須連到來源或「至少讀過 metadata」的資料集
- 用代理資料（proxy）表示的節點不可標 observed
- 沒有孤立節點、邊不指向不存在的節點
- 資料集的 verification_level 只能是 title／metadata／sample／fit
- 產出檔案裡不可出現真實的 api_key 值
有錯誤時 exit 1；警告不影響結果。
"""
import json
import sys
from pathlib import Path

EV = {"observed", "source_supported", "hypothesized", "simulated", "unknown"}
LEVELS = ["title", "metadata", "sample", "fit"]
STRONG = {"observed", "source_supported"}
EDGE_REQUIRED = ["relationship_type", "verb_label", "directed", "evidence_status", "confidence_basis"]


def main(folder: str) -> int:
    data = json.loads((Path(folder) / "system.json").read_text(encoding="utf-8"))
    if "nodes" not in data and isinstance(data.get("system"), dict):
        data = {**data, **data["system"]}
    nodes, edges = data.get("nodes", []), data.get("edges", [])
    datasets, sources = data.get("datasets", []), data.get("sources", [])
    errors, warnings = [], []

    level = {}
    for d in datasets:
        lv = d.get("verification_level")
        if lv not in LEVELS:
            errors.append(f"資料集 {d.get('id')} verification_level={lv!r}，應為 {LEVELS} 之一")
        level[d.get("id")] = lv
    source_ids = {s.get("id") for s in sources}

    def backed(obj) -> bool:
        if any(s in source_ids for s in obj.get("source_ids") or []):
            return True
        return any(LEVELS.index(level[d]) >= 1 for d in obj.get("dataset_ids") or [] if level.get(d) in LEVELS)

    node_ids = set()
    for n in nodes:
        node_ids.add(n.get("id"))
        st = n.get("evidence_status")
        if st not in EV:
            errors.append(f"節點 {n.get('id')} evidence_status={st!r}")
        if st in STRONG and not backed(n):
            errors.append(f"節點 {n.get('id')}「{n.get('label')}」標 {st}，但沒有連到來源或已讀 metadata 的資料集")
        if st == "observed" and n.get("is_proxy"):
            errors.append(f"節點 {n.get('id')}「{n.get('label')}」是代理資料（is_proxy），不可標 observed")

    used = set()
    for e in edges:
        for k in EDGE_REQUIRED:
            if e.get(k) in (None, ""):
                errors.append(f"邊 {e.get('id')} 缺 {k}")
        st = e.get("evidence_status")
        if st not in EV:
            errors.append(f"邊 {e.get('id')} evidence_status={st!r}")
        if st in STRONG and not backed(e):
            errors.append(f"邊 {e.get('id')}「{e.get('verb_label')}」標 {st}，但沒有連到來源或已讀 metadata 的資料集")
        if e.get("relationship_type") in {"association", "metric_proximity", "co_location"} and e.get("polarity"):
            errors.append(f"邊 {e.get('id')} 是 {e.get('relationship_type')}，不可帶因果極性")
        for k in ("from_node_id", "to_node_id"):
            used.add(e.get(k))
            if e.get(k) not in node_ids:
                errors.append(f"邊 {e.get('id')} 的 {k}={e.get(k)!r} 不存在")

    for n in node_ids - used:
        warnings.append(f"孤立節點 {n}")
    if not data.get("critical_uncertainties"):
        warnings.append("沒有列 critical_uncertainties（影響大但沒資料的因素）")
    title_only = [d.get("id") for d in datasets if d.get("verification_level") == "title"]
    if title_only:
        warnings.append(f"{len(title_only)} 筆資料集只看過標題：{title_only[:10]}")

    import re
    for f in Path(folder).rglob("*"):
        if f.is_file() and f.suffix in {".json", ".md"}:
            for m in re.finditer(r"api_key=([^&\s\"')]+)", f.read_text(encoding="utf-8", errors="ignore")):
                if not re.fullmatch(r"<[^>]*>|\$\{?\w+\}?|YOUR_[A-Z_]+|\.\.\.|xxx+", m.group(1), re.I):
                    errors.append(f"{f.name} 含真實 api_key 值（應改成 <REDACTED>）")
                    break

    for w in warnings:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    print(f"節點 {len(nodes)}、邊 {len(edges)}、資料集 {len(datasets)}、來源 {len(sources)}；錯誤 {len(errors)}、警告 {len(warnings)}")
    return 1 if errors else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
