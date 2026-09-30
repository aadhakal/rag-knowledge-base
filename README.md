# The Unofficial Guide

**Aashish Dhakal** — corpus: `city_guides`

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

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

I ran `python app.py retrieve "..."` over the five travel questions and the
five unrelated ones, recording the best distance for each. That command goes
through `store.py::search` with `top_k=5`, which is the same search path the
eval uses, so these distances are the ones the gate actually sees. The full
output is saved in [retrieval_distances.json](results/retrieval_distances.json).

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

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
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
| 1. Retrieved chunk contains the answer | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 2. Every answer names a source | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 4. No chunk starts or ends mid-sentence | 0 broken | 0 of 94 | 0 of 94 | 0 of 94 | MET |
| 5. Cited document contains the fact | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |

Source run: `results/run_2026-09-29_1930_scored.md`, produced by
`run_eval.py::main`. Table computed by `measure_criteria.py`, so the numbers
here are the ones that came out of the script rather than ones I retyped.

Criteria 1, 3 and 4 carry the same number in all three run columns. Retrieval
is a fixed query against a fixed index, the gate is a comparison against a
fixed cutoff, and the chunker is a fixed pass over fixed files — none of them
vary between runs, so one measurement is the whole measurement.

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

**Criterion 1** — `scorer.py::retrieval_hits` over `store.py::search`, counting
chunks whose text contains `expects`:

```
  HIT  3/5 chunks  1963         When did the railway line north of Brightwater close?
  HIT  2/5 chunks  Fell Street  Where is it cheaper to eat in Halden Bay than the harbour front?
  HIT  1/5 chunks  Marchwood    Where can I eat late at night in this region?
  HIT  1/5 chunks  noisier      Are the seafront hotels in Pellew Sands quieter than the guesthouses?
  HIT  1/5 chunks  6am          What time do the boats land at Halden Bay?

criterion 1: 5 of 5
```

Both questions I flagged as fragile in `questions.py` survive on exactly one
chunk each. They passed, but there is no margin in either.

**Criterion 2** — every answer names a file. From `generate.py::answer_from_chunks`:

```
The railway line north of Brightwater closed in 1963.

Source: `guide_regional_transport.md`
```

**Criterion 3** — `run_eval.py::check_out_of_scope`, cutoff 0.65:

```
  refused  (best distance 0.803)  What is the capital of Mongolia?
  refused  (best distance 0.888)  How do I change the oil in a diesel engine?
  refused  (best distance 0.975)  Who won the 1994 World Cup?
  refused  (best distance 0.835)  What is the recommended dosage of ibuprofen for a headache?
  refused  (best distance 0.836)  How do I write a for loop in Rust?
  -> gate refused 5 of 5
```

My closest in-corpus question is the Marchwood one at 0.495. The nearest
refusal is 0.803. That is a gap of 0.308 with nothing in it, so the repeated
practical-information block I was worried about in week 1 never pulled an
out-of-scope question close to my documents.

**Criterion 4** — `chunker.py::split_documents` over `ingest.py::load_documents`:

```
criterion 4: 94 chunks; 0 start mid-sentence, 0 end mid-sentence
   lengths: min 174, median 306, max 762
```

The longest chunk is 762 characters against an 800 window, so the chunker never
had to cut a paragraph in half. That matches the week 1 argument: my longest
paragraph is 451 characters, so a break is always within reach.

**Criterion 5** — each cited file checked against the fact it was cited for,
by `measure_criteria.py::criterion_5`. 5 of 5 in every run. The Halden Bay
question cites both `guide_halden_bay.md` and `guide_eating.md` and both
genuinely carry the price comparison, which is the duplication I expected to
cause trouble.

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer | MET | 5 of 5 against a target of 4 of 5. `retrieval_hits` counts chunks containing `expects`; every question had at least one. Not close. |
| 2 | Every answer names a source | MET | 15 of 15 answers across three runs name a file, and none names a file that wasn't retrieved. |
| 3 | Gate stops out-of-corpus questions | MET | 5 of 5 refused. The closest refusal is 0.803 against a 0.65 cutoff, so none was near the line. |
| 4 | Chunks don't start or end mid-sentence | MET | 0 of 94 chunks break. I checked the first character against a sentence-start pattern and the last against `.!?:")'`. |
| 5 | Cited document contains the fact | MET | 5 of 5 in every run. Checked each cited filename against the corpus text for `expects`, rather than only checking that a name appeared. |

All five met. That is not as good a result as it looks, and the Diagnoses
section below is about why.

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

I missed nothing. All five criteria are MET, three of them above target.

I don't think the targets were set low, though. They were aimed at the wrong
place. Here is the problem with the clean sweep above:

```
Per-question answer verdicts (scorer.py::judge):
  3/3  When did the railway line north of Brightwater close?
  3/3  Where is it cheaper to eat in Halden Bay than the harbour front?
  2/3  Where can I eat late at night in this region?
  3/3  Are the seafront hotels in Pellew Sands quieter than the guesthouses?
  0/3  What time do the boats land at Halden Bay?
```

**One of my five questions is wrong in every single run, and not one of my five
criteria notices.** That is the real finding of this week.

**The mechanism — generation, not retrieval.** `guide_halden_bay.md` states the
answer under "What to see":

> The harbour at **6am** when the boats come in is the thing worth setting an
> alarm for.

and describes the same event vaguely under "Eat and drink":

> the **boats land** in the early morning and the two harbour restaurants buy
> directly

My chunker splits by section, so these land in two different chunks. Retrieval
puts the 6am chunk at **rank 1** and the "early morning" chunk at rank 2, and I
confirmed with `generate.py::build_prompt` that both are in the 2,023-character
prompt the model receives. The model answers from rank 2 every time:

```
The boats land in the early morning (guide_halden_bay.md).
```

My question says "what time do the boats **land**". Rank 2 contains that exact
verb; rank 1 says "come in". The model matched the phrasing rather than reading
for the fact. This is a generation failure with everything upstream working —
loading, chunking, embedding and retrieval all did their jobs.

I predicted the shape of this in `questions.py`: *"the question's wording points
away from where the answer actually lives."* I was right about the cause and
wrong about which stage would break on it — I expected retrieval to miss, and
retrieval was fine.

**Why no criterion caught it.** The failure falls in the gap between two of
them:

- **Criterion 1** passes because it asks whether the retrieved chunks *contain*
  the answer. They do — at rank 1.
- **Criterion 5** passes because it asks whether the cited document contains the
  fact it is cited for. `guide_halden_bay.md` does contain "6am". The answer
  cites it honestly and then doesn't use it.

So the chunk was retrieved, the citation is truthful, and the answer is still
wrong. Between "the right text was fetched" and "the citation is honest" there
is no criterion asking the obvious question: *was the answer right?*

**Which one I'd tighten.** Not a number — a target. Criterion 1 stops at
retrieval, so I'd add the missing stage rather than raise 4 of 5 to 5 of 5.
See the revision I added to `criteria.md`.

I measured what that missing criterion would have said. Scoring *"the answer
states the fact the question asked for"* across the three runs of the before
log gives:

```
proposed 1b per run: [4, 3, 4]   target 4 of 5 -> MISSED
```

Which is, exactly, the worked example of a miss in this file's own
instructions: *"If your target said 4 of 5 and your runs came out 4, 3, 4,
that's a MISS."* My five criteria went 5 for 5 while the one I didn't write
would have failed on the first thing it measured.

**Is this a pattern or one question?** One question, but a general shape. All
four of my other questions have their answer stated in wording close to how I
asked it. The boats question is the only one where the corpus says the fact in
different words from the question, and it is the only one that fails. With five
questions I can't tell whether that's a rule; I can say it's the single
distinguishing feature of the one that broke.

The Marchwood question at 2/3 is a separate and smaller thing: run 2 simply
didn't name Marchwood. Same prompt, same chunks, different sample. That's model
variance, not a pipeline fault, and it's the reason the assignment asks for
three runs instead of one.

## The Improvement

**What I changed:** Two rules added to `GROUNDING_INSTRUCTION` in
`generate.py`. Nothing else in the pipeline was touched.

```
- Read every excerpt before answering. The excerpt whose wording is closest to the
  question is not always the one holding the answer.
- If one excerpt gives a specific fact (a time, a date, a number, a place name) and
  another only describes it vaguely, answer with the specific one.
```

**Why I picked it:** The diagnosis puts the failure at generation with the
right chunk already at rank 1, so the fix has to be in the only stage that was
actually broken — and these two rules name the exact mistake the model made,
preferring the lexically closer excerpt over the one with the time in it.

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 2. Every answer names a source | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 4. No chunk starts or ends mid-sentence | 0 broken | 0 of 94 | 0 of 94 | 0 of 94 | MET |
| 5. Cited document contains the fact | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |

Source run: `results/run_2026-09-29_1934_after.md`. Same table, measured the
same way by `measure_criteria.py`.

**Did it help?**

No. It changed nothing.

The criteria table is identical because all five were already met. The thing
the change was aimed at is unmoved:

```
Per-question answer verdicts, before -> after:
  3/3 -> 3/3  When did the railway line north of Brightwater close?
  3/3 -> 3/3  Where is it cheaper to eat in Halden Bay than the harbour front?
  2/3 -> 2/3  Where can I eat late at night in this region?
  3/3 -> 3/3  Are the seafront hotels in Pellew Sands quieter than the guesthouses?
  0/3 -> 0/3  What time do the boats land at Halden Bay?
```

All three boat answers after the change:

```
run 1: The boats land in the early morning.  Source: guide_halden_bay.md
run 2: The boats land in the early morning.  Source: `guide_halden_bay.md`
run 3: The boats land in the early morning.  Source: `guide_halden_bay.md`
```

Byte-identical to before, apart from backticks. Not a near miss — the change
had no measurable effect at all.

**How I know it isn't a different bug.** Before concluding the fix failed I
checked that the fact still reaches the model, using `generate.py::build_prompt`
outside of any model call:

```
prompt contains 6am: True
prompt contains early morning: True
prompt chars: 2023
```

So the 6am chunk is in the prompt, the instruction telling the model to prefer
the specific fact is in the system message, and the model still answers with
the vague one. The fix was applied and was ignored.

**What I think that means.** My diagnosis assumed the model would treat "early
morning" and "6am" as two descriptions of one event, one vaguer than the other,
and my rule asked it to pick the specific one. But the two sentences sit under
different headings and use different verbs — "the boats **land** in the early
morning" under "Eat and drink", "the harbour at 6am when the boats **come in**"
under "What to see". I think the model reads these as two different facts
rather than one fact stated twice, and my rule only applies when it has already
noticed they are the same thing. The instruction can't fire because the
precondition it depends on is never met.

That is a real limit on prompt-level fixes I didn't appreciate before running
this: an instruction can only redirect a choice the model knows it is making.

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

No criterion is still missed, because none was missed to begin with. Two real
things are still broken anyway.

**1. The boats question, 0 of 3 both before and after.** My prompt fix failed
and I understand why it failed, which points at the next thing to try. The two
statements of the fact are in different sections, so my section-based chunker
guarantees they are never in the same chunk and the model never sees them
adjacent. The fix I'd try next is at the chunking stage rather than the prompt:
give each chunk a short document-level header, or overlap chunks so a section
carries a line of its neighbour. That is a change to `chunker.py::split_documents`
and it would re-index the whole corpus, so it needs its own before-and-after
rather than being bolted onto this one.

I stopped here because I'd rather report one fix that failed for an
understood reason than three fixes tried until something moved. I have the
mechanism, the evidence it didn't work, and a specific next step.

**2. My criteria don't measure whether answers are correct.** Covered in the
diagnoses, and it's the more serious of the two. A system can pass all five of
my criteria and still be wrong about a fifth of what it's asked. I added a
revision to `criteria.md` rather than quietly editing criterion 1, so the
original stays visible.

**Smaller things I know about and didn't chase:**

- Two of my five questions survive on a single chunk each (criterion 1 output
  above). They passed, but there's no margin. A chunking change could break
  either without warning.
- `scorer.py::judge` agrees with all 30 of my hand labels, which sounds good
  until you notice my `expects` values are tokens a correct answer can hardly
  avoid — `1963`, `Fell Street`, `noisier`. The judge is probably weaker than
  30 of 30 suggests; my questions are just easy to score.
- Model variance on the Marchwood question (2 of 3 in both runs) is unexplained
  beyond "different sample". Three runs isn't enough to say more.

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->

**Criterion 1, and it's not close.** I wrote *"the retrieved chunks include one
that contains the answer"* because in week 1 I was sure retrieval would be the
weak stage — I'd written a deliberately hard question and expected it to miss.
Retrieval turned out to be the strongest part of the system, 5 of 5 with the
hard question landing at rank 2. Meanwhile the stage I never wrote a criterion
for is the one that failed every run.

I'd write it as two criteria instead of one: *the retrieved chunks contain the
answer* (what I have), and *the answer states the fact the question asked for*
(what I'm missing). Splitting them is what would have let me see the boats
failure, because it's the difference between those two that the failure lives
in.

**Criterion 5 I'd keep but sharpen.** "The cited document contains the fact"
was the right instinct — it's stricter than criterion 2 and it caught the right
worry about my duplicated corpus. But it passed on the boats question, where
the answer cites a document that does contain 6am and then doesn't say 6am. It
verifies the citation without verifying the claim. I'd word it as *the cited
document supports the specific claim the answer makes*, which is harder to
check and would have failed honestly instead of passing hollowly.

**What I got right and would keep:** criterion 4. "No chunk starts or ends
mid-sentence" is countable, I could check it without judgement, and the reason
I gave — my longest paragraph is 451 characters against an 800 window — turned
out to predict the result exactly (longest chunk 762, zero breaks). That's what
a criterion should feel like.

**The general lesson.** Four of my five criteria measure a *stage* — retrieval
fetched, generation cited, the chunker cut, the gate refused. Only one of them
was ever about the thing I actually care about, which is whether the answer is
right, and that one turned out to measure a proxy for it. Every stage passing
is not the same as the system working, and I wrote five criteria without ever
noticing I hadn't asked the direct question.
