#!/usr/bin/env python3
"""按白名单刊名 + 日期窗口，从 Crossref 确定性、近穷尽地拉取候选文献。
解决"每次 web_search 召回不一样、且不穷尽"的问题：Crossref 是固定索引，同样的
刊+窗口每次返回同一全集（仅受新文献入库影响）。

用法:
  python fetch_candidates.py 2026-05-26 2026-06-12 \
      --journals references/journals_a_tier.txt \
      --mailto you@example.com \
      --out /tmp/candidates_第9期.json

要点:
- 仅覆盖 A 类同行评审刊（Crossref 有 ISSN 的）。A2 预印本(arXiv/SSRN/NBER)、
  B 类咨询报告、C 类社媒不在此脚本范围，仍走 SKILL.md 的②③节点。
- 需联网到 api.crossref.org（本机一般可达；Claude 沙箱不可达，故在你的机器上跑）。
- 输出供节点④去重/归类、节点⑤评审；本脚本只负责"拉全"，不做相关性判定。
"""
import sys, json, time, argparse, re, urllib.parse, urllib.request

CROSSREF = "https://api.crossref.org"

def _get(url, mailto, tries=3):
    if mailto:
        url += ("&" if "?" in url else "?") + "mailto=" + urllib.parse.quote(mailto)
    req = urllib.request.Request(url, headers={"User-Agent": f"sanzhoubao/0.1 (mailto:{mailto or 'na'})"})
    for i in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            if i == tries - 1:
                print(f"  ! 请求失败: {e}", file=sys.stderr); return None
            time.sleep(2 * (i + 1))

def resolve_issn(name, mailto):
    """刊名 -> ISSN（取 Crossref 期刊检索的最佳匹配）。若传入已是 ISSN 则直接用，免歧义。"""
    if re.fullmatch(r"\d{4}-?\d{3}[\dxX]", name.strip()):
        z=name.strip();  return (z if "-" in z else z[:4]+"-"+z[4:]), z
    url = f"{CROSSREF}/journals?query={urllib.parse.quote(name)}&rows=5"
    d = _get(url, mailto)
    if not d: return None, None
    items = d.get("message", {}).get("items", [])
    nl = name.lower()
    for it in items:                       # 优先精确同名
        if it.get("title", "").lower() == nl:
            return (it.get("ISSN") or [None])[0], it.get("title")
    if items:                              # 否则取第一个并提示人工核对
        return (items[0].get("ISSN") or [None])[0], items[0].get("title")
    return None, None

def fetch_works(issn, dfrom, dto, mailto):
    """按 ISSN + 出版日期窗口翻页拉全。"""
    out, cursor = [], "*"
    while True:
        url = (f"{CROSSREF}/journals/{issn}/works?"
               f"filter=from-pub-date:{dfrom},until-pub-date:{dto}"
               f"&rows=100&cursor={urllib.parse.quote(cursor)}"
               f"&select=DOI,title,author,issued,container-title,URL")
        d = _get(url, mailto)
        if not d: break
        msg = d.get("message", {})
        items = msg.get("items", [])
        if not items: break
        for it in items:
            au = "; ".join(
                f"{a.get('family','')} {a.get('given','')}".strip()
                for a in it.get("author", [])[:6]
            )
            out.append({
                "doi": it.get("DOI", ""),
                "title": (it.get("title") or [""])[0],
                "authors": au,
                "date": "-".join(map(str, (it.get("issued", {}).get("date-parts", [[None]])[0]))),
                "journal": (it.get("container-title") or [""])[0],
                "url": it.get("URL", ""),
            })
        cursor = msg.get("next-cursor")
        if not cursor: break
        time.sleep(0.3)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("date_from"); ap.add_argument("date_to")
    ap.add_argument("--journals", default="references/journals_a_tier.txt")
    ap.add_argument("--mailto", default="")
    ap.add_argument("--out", default="candidates.json")
    ap.add_argument("--add", action="append", default=[], help="临时加一本刊(刊名或ISSN)，可重复 --add")
    ap.add_argument("--extra", default="", help="临时刊清单文件(一行一刊名或ISSN)")
    ap.add_argument("--min-tier", dest="min_tier", default="3", choices=["4", "3", "2"],
                    help="检索深度: 4=只4*/4顶刊; 3=含3星(默认); 2=含2星具名。x(跨学科)始终纳入。")
    a = ap.parse_args()

    def parse(line):
        p = line.split("\t")
        return p[0].strip(), (p[1].strip() if len(p) > 1 and p[1].strip() else "x")
    def keep(tier):
        if tier == "x":
            return True
        try:
            return int(tier) >= int(a.min_tier)
        except ValueError:
            return True

    entries = [parse(l) for l in open(a.journals, encoding="utf-8") if l.strip()]
    entries += [(x, "x") for x in a.add]            # 临时加刊始终纳入
    if a.extra:
        entries += [parse(l) for l in open(a.extra, encoding="utf-8") if l.strip()]
    entries = [(n, t) for (n, t) in entries if keep(t)]
    names = [n for (n, _t) in entries]
    print(f"窗口 {a.date_from} → {a.date_to}；min-tier={a.min_tier}；纳入 {len(names)} 本")
    all_rows, unresolved = [], []
    for n in names:
        issn, matched = resolve_issn(n, a.mailto)
        if not issn:
            unresolved.append(n); print(f"  ? 未解析 ISSN: {n}"); continue
        rows = fetch_works(issn, a.date_from, a.date_to, a.mailto)
        if matched and matched.lower() != n.lower():
            print(f"  ~ {n} -> 匹配为「{matched}」(ISSN {issn})，请人工核对")
        print(f"  ✓ {n} [{issn}]: {len(rows)} 篇")
        all_rows.extend(rows)
        time.sleep(0.3)

    # 同 DOI 去重(同刊多 ISSN 可能重复)
    seen, dedup = set(), []
    for r in all_rows:
        k = r["doi"] or r["title"].lower()
        if k in seen: continue
        seen.add(k); dedup.append(r)

    json.dump({"window": [a.date_from, a.date_to], "count": len(dedup),
               "unresolved_journals": unresolved, "items": dedup},
              open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\n共 {len(dedup)} 篇候选 -> {a.out}"
          f"{'；未解析刊:' + ', '.join(unresolved) if unresolved else ''}")
    print("注意: 这是 A 类同行评审刊的全量候选;相关性判定/归类见 SKILL.md ④⑤;"
          "A2 预印本、B 咨询、C 社媒仍需另行检索/上传。")

if __name__ == "__main__":
    main()
