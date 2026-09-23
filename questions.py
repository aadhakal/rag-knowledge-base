"""
Your test questions.

Milestone 2 asks you to write five questions your system should be able to
answer from your corpus, specific enough to have a right answer.

  ✗ "What are good dining halls?"          — no right answer
  ✓ "What do students say about wait times at Commons during lunch?"

Fill in `QUESTIONS` below. `expects` is a word or short phrase you'd expect a
correct answer to contain — you'll use it in unit 2 when you build a scorer,
and having written it now means you decided what "correct" meant before you saw
any results.

`OUT_OF_SCOPE` holds five questions your documents clearly don't cover. You
need these in Milestone 4 to find where your relevance cutoff belongs, and
again in unit 2, where `run_eval.py` runs them through the gate and writes what
happened into your run log — that's the evidence for criterion 3.

Swap them for your own if you like. Keep five of them either way: criterion 3
names a target of "4 of 5", and four of three is not a thing.
"""

QUESTIONS = [
    # {"question": "...", "expects": "..."},

    # guide_regional_transport.md (also guide_kestrelford.md, guide_walking.md)
    # The date is stated outright in three separate documents, so retrieval has
    # three chances to find it. This is the question that should always work.
    {"question": "When did the railway line north of Brightwater close?",
     "expects": "1963"},

    # guide_halden_bay.md (also guide_eating.md)
    # Both the town guide and the regional eating guide state the same price
    # comparison. Tests which of two legitimate sources the system cites.
    {"question": "Where is it cheaper to eat in Halden Bay than the harbour front?",
     "expects": "Fell Street"},

    # guide_marchwood.md, competing with guide_eating.md
    # guide_eating.md says kitchens across the region stop serving at 9pm.
    # Marchwood is the stated exception. Retrieval has to find the exception
    # rather than the general rule, and the question uses none of the wording
    # either document uses.
    {"question": "Where can I eat late at night in this region?",
     "expects": "Marchwood"},

    # guide_pellew_sands.md
    # One of two questions here whose answer appears in a single document (the
    # other is the Halden Bay boats question). Nothing else in the corpus can
    # cover for a retrieval miss.
    {"question": "Are the seafront hotels in Pellew Sands quieter than the guesthouses?",
     "expects": "noisier"},

    # guide_halden_bay.md
    # The fact sits under "What to see" rather than anywhere about food or
    # opening times, so the question's wording points away from where the
    # answer actually lives.
    {"question": "What time do the boats land at Halden Bay?",
     "expects": "6am"},
]

# Questions from a different world entirely. Your gate should refuse all five.
#
# There are five of these because criterion 3 in criteria.md names a target of
# "at least 4 of 5" — you need five things to try before you can report 4 of 5.
# `run_eval.py` runs these through retrieval and the gate on every eval and
# records what happened, so criterion 3 has evidence in the run log alongside
# the others. They cost no model calls: a refusal never reaches the model.
OUT_OF_SCOPE = [
    "What is the capital of Mongolia?",
    "How do I change the oil in a diesel engine?",
    "Who won the 1994 World Cup?",
    "What is the recommended dosage of ibuprofen for a headache?",
    "How do I write a for loop in Rust?",
]


def answered() -> list[dict]:
    """The questions you've actually filled in."""
    return [q for q in QUESTIONS if q.get("question", "").strip()]
