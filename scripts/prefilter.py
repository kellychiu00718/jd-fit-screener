#!/usr/bin/env python3
"""Cheap first cut for a pile of job postings. Standard library only.

Reads postings from a folder of .txt/.md files or from a CSV (columns: title, company, text),
merges duplicates (same company + title), scores keyword hits, and drops postings with
negative keywords. The output is a ranked list for the language model to read, not a verdict.

Examples:
  python3 prefilter.py examples/jds --high "python,sql,analytics" --medium "dashboard,stakeholder" --negative "senior,principal"
  python3 prefilter.py postings.csv --profile profile.md --min-score 2 --format json
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path


def split_words(text):
    return [w.strip().lower() for w in text.split(",") if w.strip()]


def keywords_from_profile(path):
    """Read the '## Keywords' section of profile.md (lines starting with - High:/Medium:/Negative:)."""
    out = {"high": [], "medium": [], "negative": []}
    in_section = False
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            in_section = line.strip().lower().startswith("## keywords")
            continue
        if in_section:
            m = re.match(r"^\s*-\s*(high|medium|negative)\s*:\s*(.*)$", line, re.I)
            if m:
                out[m.group(1).lower()] = split_words(m.group(2))
    return out


def normalize(s):
    return re.sub(r"[^a-z0-9가-힣]+", " ", s.lower()).strip()


def load_postings(source):
    p = Path(source)
    postings = []
    if p.is_dir():
        for f in sorted(p.iterdir()):
            if f.suffix.lower() not in {".txt", ".md"}:
                continue
            text = f.read_text(encoding="utf-8")
            title = company = ""
            for line in text.splitlines()[:6]:
                if line.lower().startswith("title:"):
                    title = line.split(":", 1)[1].strip()
                if line.lower().startswith("company:"):
                    company = line.split(":", 1)[1].strip()
            postings.append({"id": f.name, "title": title or f.stem, "company": company, "text": text})
    else:
        with p.open(encoding="utf-8", newline="") as fh:
            for i, row in enumerate(csv.DictReader(fh), 1):
                postings.append({"id": row.get("id") or f"row{i}", "title": row.get("title", ""),
                                 "company": row.get("company", ""), "text": row.get("text", "")})
    return postings


def count_hits(words, text):
    return [w for w in words if w in text]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", help="folder of .txt/.md files, or a CSV with title, company, text")
    ap.add_argument("--profile", help="profile.md with a '## Keywords' section")
    ap.add_argument("--high", default="")
    ap.add_argument("--medium", default="")
    ap.add_argument("--negative", default="")
    ap.add_argument("--min-score", type=float, default=2.0)
    ap.add_argument("--format", choices=["table", "json"], default="table")
    a = ap.parse_args()

    kw = {"high": [], "medium": [], "negative": []}
    if a.profile:
        kw = keywords_from_profile(a.profile)
    for k in kw:
        extra = split_words(getattr(a, k))
        kw[k] = kw[k] + [w for w in extra if w not in kw[k]]
    if not any(kw.values()):
        sys.exit("No keywords given. Use --profile or --high/--medium/--negative.")

    seen = {}
    for p in load_postings(a.source):
        key = (normalize(p["company"]), normalize(p["title"]))
        # keep the longest text for duplicates, remember the other ids
        if key in seen and key != ("", ""):
            first = seen[key]
            first["also_seen_as"].append(p["id"])
            if len(p["text"]) > len(first["text"]):
                first["text"] = p["text"]
            continue
        p["also_seen_as"] = []
        seen[key if key != ("", "") else (p["id"], "")] = p

    rows, dropped = [], []
    for p in seen.values():
        text = p["text"].lower() + " " + p["title"].lower()
        high, med, neg = count_hits(kw["high"], text), count_hits(kw["medium"], text), count_hits(kw["negative"], text)
        score = 3.0 * len(high) + 1.5 * len(med) - 5.0 * len(neg)
        row = {"id": p["id"], "company": p["company"], "title": p["title"], "score": round(score, 1),
               "high": high, "medium": med, "negative": neg, "also_seen_as": p["also_seen_as"]}
        (rows if score >= a.min_score and not neg else dropped).append(row)

    rows.sort(key=lambda r: r["score"], reverse=True)
    if a.format == "json":
        print(json.dumps({"kept": rows, "dropped": dropped}, ensure_ascii=False, indent=2))
        return
    print(f"kept {len(rows)}, dropped {len(dropped)} (min score {a.min_score}, any negative keyword drops a posting)")
    for r in rows:
        print(f"{r['score']:>5}  {r['company'] or '-':<20} {r['title']:<40} high={','.join(r['high']) or '-'}")
    for r in dropped:
        why = f"negative: {','.join(r['negative'])}" if r["negative"] else f"score {r['score']} below {a.min_score}"
        print(f"drop   {r['company'] or '-':<20} {r['title']:<40} {why}")


if __name__ == "__main__":
    main()
