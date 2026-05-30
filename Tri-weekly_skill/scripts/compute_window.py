#!/usr/bin/env python3
"""三周报 自报日期：从上一期日期推算本期期号、目标日(周五)与检索窗口。
用法: python compute_window.py --last 20260525 [--issue-no 8] [--last-window-end 20260525] [--buffer 7] [--today 20260529]
规则: 目标日 = 上一期 + 3周(21天) 后所在那一周的周五; 检索窗口 = 上一期覆盖次日 → 目标日 - 缓冲(默认7天).
"""
import argparse, datetime as dt

def parse(s): return dt.datetime.strptime(s, "%Y%m%d").date()
def friday_of_week(d):  # Mon=0..Sun=6, Fri=4
    return d + dt.timedelta(days=(4 - d.weekday()))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--last", required=True, help="上一期日期 YYYYMMDD")
    ap.add_argument("--issue-no", type=int, default=None, help="上一期期号(可选)")
    ap.add_argument("--last-window-end", default=None, help="上一期检索覆盖截止日 YYYYMMDD(可选,默认=上一期日期)")
    ap.add_argument("--buffer", type=int, default=7, help="索引缓冲天数(默认7)")
    ap.add_argument("--today", default=None, help="今天 YYYYMMDD(可选,默认系统今天)")
    a = ap.parse_args()

    last = parse(a.last)
    today = parse(a.today) if a.today else dt.date.today()
    seed = last + dt.timedelta(days=21)          # +3 周
    target = friday_of_week(seed)                 # 落到那一周的周五
    win_start = (parse(a.last_window_end) if a.last_window_end else last) + dt.timedelta(days=1)
    win_end = target - dt.timedelta(days=a.buffer)
    nxt = (a.issue_no + 1) if a.issue_no else None
    late = (today - target).days

    print("="*46)
    print(f"  上一期日期      : {last:%Y-%m-%d} ({last:%a})")
    if nxt: print(f"  本期期号        : 第 {nxt} 期")
    print(f"  本期目标日(周五): {target:%Y-%m-%d} ({target:%a})")
    print(f"  检索窗口        : {win_start:%Y-%m-%d}  →  {win_end:%Y-%m-%d}  (缓冲 {a.buffer} 天)")
    print(f"  今天            : {today:%Y-%m-%d}")
    if late > 0:   print(f"  ⚠ 已晚于目标日 {late} 天——窗口可顺延，但请手动确认下方区间。")
    elif late < 0: print(f"  距目标日还有 {-late} 天。")
    print("="*46)
    print("  → 请手动确认/调整以上检索窗口，确认后进入检索节点。")

if __name__ == "__main__":
    main()
