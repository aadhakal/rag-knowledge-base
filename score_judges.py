#!/usr/bin/env python3
"""Score judge() against my hand labels in labels.md.

    python score_judges.py

Reads the verdicts I wrote in labels.md, runs scorer.judge over the same 30
answers, and reports agreement plus every disagreement. The disagreements are
the finding; the percentage on its own says very little.
"""
import re
import sys
from pathlib import Path

import questions as qs


def load_labels(path=Path("labels.md")):
    """Pull (expects, answer, verdict) out of the labelling file."""
    if not path.exists():
        sys.exit("labels.md not found — generate it first.")

    rows, expects = [], None
    for block in path.read_text(encoding="utf-8").split("\n## ")[1:]:
        m = re.search(r"`expects`: \*\*(.+?)\*\*", block)
        if not m:
            continue
        expects = m.group(1)
        question = block.split("\n")[0].strip()
        for entry in block.split("\n### ")[1:]:
            ans = entry.split("```")
            if len(ans) < 2:
                continue
            verdict = re.search(r"- verdict:\s*(\S+)", entry)
            rows.append({
                "question": question,
                "expects": expects,
                "answer": ans[1].strip(),
                "label": verdict.group(1).lower() if verdict else None,
            })
    return rows


def main():
    rows = load_labels()
    unlabelled = [r for r in rows if r["label"] not in ("pass", "fail")]
    if unlabelled:
        sys.exit(f"{len(unlabelled)} of {len(rows)} rows still have no verdict. "
                 "Fill labels.md in first — the judge is measured against it.")

    import scorer

    agree, disagree = 0, []
    for r in rows:
        got = bool(scorer.judge(r["question"], r["expects"], r["answer"], []))
        want = r["label"] == "pass"
        if got == want:
            agree += 1
        else:
            disagree.append((r, got, want))

    print(f"judge() agrees with my labels on {agree}/{len(rows)} "
          f"({100 * agree / len(rows):.0f}%)\n")

    if not disagree:
        print("No disagreements. Worth asking whether the labels were independent.")
        return

    print(f"{len(disagree)} disagreement(s) — this is the part worth writing up:\n")
    for r, got, want in disagree:
        kind = "judge says PASS, I said fail" if got else "judge says FAIL, I said pass"
        print(f"  [{r['expects']}] {kind}")
        print(f"    {r['answer'][:100]}\n")


if __name__ == "__main__":
    main()
