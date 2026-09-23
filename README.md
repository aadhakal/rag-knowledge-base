# The Unofficial Guide

**Aashish Dhakal** — corpus: `city_guides`

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none, because the grader can't
> read it.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Week 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

This project answers questions using the 14 documents in `city_guides`.
You can ask about transport, food, places to stay, and other details covered by
the guides. It finds matching sections, uses them to write an answer, and names
the file the answer came from. If it can't find a close enough match, it says,
"I don't have enough information about that."

## Chunking Strategy

**Chunk size:** Varies by section, with no character limit. The current chunks
range from 174 to 762 characters, including the guide title and section heading.
**Overlap:** 0. Paragraphs aren't repeated, but each chunk includes the guide's
title so it's clear which place it describes.

<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->

The city guides already have sections like "Getting there" and "Eat and drink."
The original code ignored those headings and cut the text every 800 characters.
In the Marchwood guide, one chunk ended with "The centre is walk" and the next
started with "til midnight." That goes against my goal of keeping sentences whole.

I changed `chunker.py::split_documents` to split at the headings. Each section
stays together, and the introduction gets its own chunk. This keeps information
about food separate from information about buses or places to stay.

I first kept an 800-character target but let long paragraphs go over it. I then
removed the size check so the rule is simple: keep each section whole. The
largest current chunk is "Straightforward" in `guide_accessibility.md`, at 762
characters with the guide title included. That's its measured length, not a
limit. Longer sections would stay whole too.

I changed overlap from 120 to 0 because the paragraphs now stay whole. Each
chunk still repeats the guide title. For example, "Everything is on one street"
makes more sense with "Givens Mill" above it. I still need to check whether zero
overlap works well for questions that need information from two sections.

The old code made 51 chunks. The new code makes 94, ranging from 174 to 762
characters. Checks across all 14 guides showed that every paragraph was kept
once, in the right order, with no sentences cut in half. I haven't tested yet
whether this helps the system find better answers.

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

These five chunks came from `python app.py chunks -n 5`. The first is just an
introduction and doesn't answer a specific travel question. So even though the
text stays whole, some chunks may be more useful than others.

**Chunk 1** — source: `guide_accessibility.md#0` — produced by: `chunker.py::split_documents`

```
# Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.
```

**Chunk 2** — source: `guide_corry_vale.md#5` — produced by: `chunker.py::split_documents`

```
# Corry Vale

## Where to stay

Perhaps thirty beds in the entire valley, spread across two pubs and a handful of farmhouse rooms. In summer these are booked months ahead. Camping is permitted on two marked fields and nowhere else.
```

**Chunk 3** — source: `guide_givens_mill.md#2` — produced by: `chunker.py::split_documents`

```
# Givens Mill

## Getting around

Everything is on one street along the river. The mill is at one end and the church at the other, eight minutes apart. The riverside path continues in both directions for as far as you want to walk.
```

**Chunk 4** — source: `guide_kestrelford.md#4` — produced by: `chunker.py::split_documents`

```
# Kestrelford

## What to see

The market square on a Saturday morning is the main event and has run continuously since the 1400s. The parish church has a 13th-century tower you can climb for £2. The old trackbed walk runs six miles to the next village along an easy gradient and is the best half-day here.
```

**Chunk 5** — source: `guide_pellew_sands.md#6` — produced by: `chunker.py::split_documents`

```
# Pellew Sands

## When to go

June and September for the beach without the crowds. July and August are busy and the town is at its most itself, for better and worse. Winter is bleak, largely closed, and has a following among people who like that sort of thing.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** When did the railway line north of Brightwater close?

**Answer:**

```
(best distance 0.239, cutoff 0.65)
The railway line north of Brightwater closed in 1963. This information comes from `guide_regional_transport.md`.
Sources retrieved: guide_kestrelford.md, guide_marchwood.md, guide_regional_transport.md, guide_walking.md
1 model calls this session, 730 tokens (702 in, 28 out)
```

**My relevance cutoff:** 0.65

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

I ran `python measure_retrieval.py` with the five travel questions and five
unrelated questions. It uses `store.py::search`, the same search function as
`python app.py retrieve`, and retrieves five chunks for each question. The full
results are saved in [retrieval_distances.json](results/retrieval_distances.json).

The travel questions had distances from 0.222804 to 0.495222. The unrelated
questions ranged from 0.802559 to 0.975347, so the two groups didn't overlap.
The middle of the gap is about 0.64889. I rounded that to 0.65 and set it in
`config.py`. A question passes when its best distance is below 0.65.

This lets all five travel questions through and stops all five unrelated ones.
The original cutoff of 0.6 also separates these ten questions. Choosing 0.65
puts the cutoff near the middle of the gap; it doesn't show that the answers
have improved. A question passing the gate still needs a correct answer from
the retrieved text, and new questions may be harder to separate.

| Question | In corpus? | Best distance |
|---|---|---|
| When did the railway line north of Brightwater close? | Yes | 0.238950 |
| Where is it cheaper to eat in Halden Bay than the harbour front? | Yes | 0.222804 |
| Where can I eat late at night in this region? | Yes | 0.495222 |
| Are the seafront hotels in Pellew Sands quieter than the guesthouses? | Yes | 0.281499 |
| What time do the boats land at Halden Bay? | Yes | 0.281900 |
| What is the capital of Mongolia? | No | 0.802559 |
| How do I change the oil in a diesel engine? | No | 0.888096 |
| Who won the 1994 World Cup? | No | 0.975347 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.835036 |
| How do I write a for loop in Rust? | No | 0.836491 |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1. Asking questions and talking through the reasoning.** I went back and
forth with AI about cleanup, overlap, long paragraphs, and the cutoff. One time
I asked whether `clean_text` in `ingest.py` already did the work being added to
`split_documents`. AI explained that `clean_text` fixes whitespace, while
`split_documents` chooses where chunks start and end. It also found a repeated
`.strip()` call on the whole document. After that discussion, we removed that
call from the chunker and used the text that `ingest.py` had already cleaned.

**2. Writing the split function.** I asked AI to help write `split_documents`
for my city guides. Its first version used an 800-character target but allowed
long paragraphs to go over it. I questioned the point of a limit the code could
ignore. We changed it to keep each section in one chunk, with no character
limit.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Week 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     week 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     week — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
