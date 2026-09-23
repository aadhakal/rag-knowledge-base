# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

<!-- e.g. "One of my questions is about a topic only two documents mention, so
     I expect that one to be hard." -->
**Why this target:** One of my five is deliberately hard. "Where can I eat late
at night in this region?" is answered in guide_marchwood.md, but guide_eating.md
says kitchens across the region stop serving at 9pm, and my question doesn't use
the wording from either file. So retrieval has to land on the exception and not
the general rule. I expect that one to fail. The Pellew Sands hotel question is
the other risk, since only guide_pellew_sands.md mentions the answer at all. 4 of 5 gives me room for the obvious failure. Asking for 5 of 5
would mean assuming the hardest question I wrote works first time.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

<!-- Why all five and not four? What about your setup makes that achievable —
     or what would have to go wrong for it not to be? -->
**Why this target:** I want all five because anything less would mean the
pipeline is broken, not that a question was hard. generate.py ends the prompt by
telling the model to name the file it used, and every chunk arrives with its
filename attached. The model is only called after the gate has passed, so there
is always at least one real document in front of it. If an answer came back with
no source, the problem would be structural and I'd want to know straight away.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

<!-- What did your distances look like when you set the cutoff in Milestone 4?
     Was there a clean gap, or did the two groups overlap? -->
**Why this target:** Mongolia, diesel engines, the World Cup, ibuprofen, Rust.
None of that looks anything like a travel guide, so I'd expect all five to sit
well away from my documents. What I don't know yet is where my own questions
sit, and the cutoff has to go somewhere between the two. My nine town guides
also repeat the same block about cash, phone signal and hospitals word for word,
so a practical-sounding question could land closer than it deserves. That's the one
I am worried about.

---

## 4. Chunks don't start or end mid-sentence

<!-- YOU WRITE THIS ONE.

     How would you know if your chunks were the right size? Name something
     countable or observable.

     Examples of the right shape — don't copy these, they should come from
     what you actually saw in Milestone 3:
       - "At least 4 of 5 sampled chunks read as a complete thought, with no
          sentence cut in half at either end."
       - "No chunk is shorter than 200 characters, since anything below that
          in my corpus turned out to be a heading with no content under it." -->

No chunk in my index begins or ends in the middle of a sentence.

**Why this target:** The chunker counts to 800 and cuts, wherever that lands. My
documents are long enough that they have to be split somewhere, 1,400 to 2,500
characters each. But my longest paragraph is only 451 characters, so there is
always a paragraph break within reach before the window runs out. If a chunk
ends mid-sentence that is the chunker's doing, not the text's.

---

## 5. Sources are correct, not just present

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. It could be about
     speed, about refusals, about a particular kind of question your corpus
     handles badly, about source attribution being correct rather than merely
     present — anything, as long as it names a number or an observable
     outcome. -->

Every document an answer cites actually contains the fact it is cited for.

**Why this target:** Criterion 2 only checks that a source got named. My corpus
repeats itself a lot. The same bus times are in guide_kestrelford.md and
guide_regional_transport.md, the same price comparison in guide_halden_bay.md and
guide_eating.md. When retrieval hands the model several files that each cover part
of an answer, crediting the wrong one is easy. A wrong source is worse than a missing one,
because the source is the source of truth. There are only five answers, so I can open the
files and check each one myself.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
