#!/usr/bin/env python3
"""Score all five acceptance criteria against a run log.

    python measure_criteria.py results/run_2026-09-29_1930_scored.md

Criteria 2 and 5 are read out of the log, one value per run. Criteria 1 and 4
are deterministic — retrieval is a fixed query against a fixed index and the
chunker is a fixed pass over fixed files — so they are measured once and the
same number goes in all three run columns. Criterion 3 is already in the log,
measured the same way and for the same reason.

Prints the README's Run Log table so the numbers in the write-up are the ones
that came out of here, not ones I retyped.
"""
import re
import sys
from pathlib import Path

import config
import questions as qs
import scorer


def parse_log(path):
    """Pull (question, run, answer, sources) out of a run log's Real output."""
    entries = []
    for part in Path(path).read_text(encoding="utf-8").split("\n### ")[1:]:
        head, _, body = part.partition("\n")
        seg = body.split("```")
        if len(seg) < 2:
            continue
        m = re.match(r"(.+?) — run (\d+)", head.strip())
        if not m:
            continue
        entries.append({
            "question": m.group(1),
            "run": int(m.group(2)),
            "answer": seg[1].strip(),
        })
    return entries


def criterion_1():
    """Do the retrieved chunks contain the answer? Deterministic."""
    from store import search
    hits = 0
    for q in qs.answered():
        results = search(q["question"], top_k=config.TOP_K, corpus=config.CORPUS)
        hits += scorer.retrieval_hits(q["expects"], results) > 0
    return hits, len(qs.answered())


def criterion_2(entries, run):
    """Does every answer name a source document?"""
    rows = [e for e in entries if e["run"] == run]
    named = sum(bool(re.search(r"guide_[a-z_]+", e["answer"])) for e in rows)
    return named, len(rows)


def criterion_3(path):
    """Read the gate's out-of-scope result straight out of the log."""
    text = Path(path).read_text(encoding="utf-8")
    m = re.search(r"Refused (\d+) of (\d+)", text)
    return (int(m.group(1)), int(m.group(2))) if m else (0, 0)


def criterion_4():
    """Do any chunks start or end mid-sentence? Deterministic."""
    from ingest import load_documents
    from chunker import split_documents
    chunks = split_documents(load_documents(config.CORPUS))
    bad = sum(
        not re.match(r"^[#\-*\d(\"'A-Z]", c.text.strip())
        or not re.search(r"[.!?:)\"']$", c.text.strip())
        for c in chunks
    )
    return len(chunks) - bad, len(chunks)


def criterion_5(entries, run, docs):
    """Does each cited document actually contain the fact it's cited for?"""
    ok = total = 0
    for e in (x for x in entries if x["run"] == run):
        q = next((x for x in qs.QUESTIONS if x["question"] == e["question"]), None)
        if not q:
            continue
        total += 1
        needle = scorer.normalize(q["expects"])
        cited = {c + ".md" for c in set(re.findall(r"guide_[a-z_]+", e["answer"]))}
        ok += any(c in docs and needle in scorer.normalize(docs[c]) for c in cited)
    return ok, total


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    entries = parse_log(path)
    runs = sorted({e["run"] for e in entries})
    docs = {p.name: p.read_text(encoding="utf-8")
            for p in Path(f"corpora/{config.CORPUS}/documents").glob("*.md")}

    c1, c1n = criterion_1()
    c3, c3n = criterion_3(path)
    c4, c4n = criterion_4()

    rows = [
        ("1. Retrieved chunk contains the answer", "4 of 5",
         [f"{c1} of {c1n}"] * 3, c1 >= 4),
        ("2. Every answer names a source", "5 of 5",
         [f"{criterion_2(entries, r)[0]} of {criterion_2(entries, r)[1]}" for r in runs],
         all(criterion_2(entries, r)[0] == criterion_2(entries, r)[1] for r in runs)),
        ("3. Gate stops out-of-corpus questions", "4 of 5",
         [f"{c3} of {c3n}"] * 3, c3 >= 4),
        ("4. No chunk starts or ends mid-sentence", "0 broken",
         [f"{c4n - c4} of {c4n}"] * 3, c4 == c4n),
        ("5. Cited document contains the fact", "5 of 5",
         [f"{criterion_5(entries, r, docs)[0]} of {criterion_5(entries, r, docs)[1]}" for r in runs],
         all(criterion_5(entries, r, docs)[0] == criterion_5(entries, r, docs)[1] for r in runs)),
    ]

    print(f"Measured from {path} by measure_criteria.py\n")
    print("| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |")
    print("|---|---|---|---|---|---|")
    for name, target, cells, met in rows:
        cells = (cells + cells[-1:] * 3)[:3]
        print(f"| {name} | {target} | {' | '.join(cells)} | "
              f"{'MET' if met else 'MISSED'} |")

    print("\nPer-question answer verdicts (scorer.judge):")
    for q in qs.answered():
        marks = [
            "pass" if scorer.judge(q["question"], q["expects"], e["answer"], [])
            else "fail"
            for e in entries if e["question"] == q["question"]
        ]
        print(f"  {sum(m == 'pass' for m in marks)}/{len(marks)}  {q['question']}")


if __name__ == "__main__":
    main()
