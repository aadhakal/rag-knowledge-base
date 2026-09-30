import re


def normalize(text):
    """Strip away everything that isn't the fact.

    Runs on both sides of every comparison, so neither can fail on how it
    happened to get typed. Order matters: times before punctuation, or the
    colon in 6:00am is gone before the time pattern can see it.
    """
    text = text.lower()
    text = re.sub(r"\.(md|txt)\b", "", text)     # guide_halden_bay.md -> guide_halden_bay
    text = re.sub(r"[`*~]", "", text)            # markdown emphasis

    def _time(m):
        hour, mins, half = m.group(1), m.group(2), m.group(3)
        return f"{hour}{half}m" if mins in (None, "00") else f"{hour}:{mins}{half}m"

    # 6 am / 6:00am / 6 a.m. -> 6am, but 8:30pm keeps its minutes. No trailing
    # \.? — in "closes at 8:30 pm." that dot is the sentence ender, and
    # sentences() needs it.
    text = re.sub(r"(\d{1,2})(?::(\d{2}))?\s*([ap])\.?\s*m\b", _time, text)

    text = re.sub(r"[^\w\s.!?:]", " ", text)     # keep sentence enders for splitting
    return re.sub(r"\s+", " ", text).strip()


def sentences(text):
    """Split normalized text on sentence enders."""
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def judge(question, expects, answer, results) -> bool:
    """
    Judge if the question is right or wrong compared to our expectation

    Agrees with all 30 of my hand labels in labels.md. I also built the
    negation guard below, on the theory that an answer mentioning `expects`
    while denying it should fail. It scores 29/30, so it isn't used here —
    see judge_negation_guard.
    """
    return normalize(expects) in normalize(answer)


# Multi-word on purpose. Three of my correct answers open with "No, the
# seafront hotels are noisier...", where "No" is the right answer to the
# question as asked. A marker list containing bare "no" or "not" would fail
# them all.
NEGATION_MARKERS = [
    "no mention", "not mention", "cannot", "can t", "don t have",
    "does not say", "doesn t say", "not supported", "no information",
    "nowhere", "not possible",
]


def judge_negation_guard(question, expects, answer, results) -> bool:
    """Same as judge(), but rejects answers that deny the fact they mention.

    Kept so the comparison in my write-up is reproducible. Scores 29/30: it
    fails the answer that says "you cannot eat late at night in this region.
    Outside of Marchwood, ..." — which my labelling rule calls a pass, because
    naming the exception counts as answering. That one row is the whole
    difference between this and judge().
    """
    needle = normalize(expects)
    haystack = normalize(answer)
    if needle not in haystack:
        return False
    return not any(marker in haystack for marker in NEGATION_MARKERS)


def llm_as_judge(question, expects, answer, results) -> bool:
    """
    LLM as judge
    """
    return expects.lower().strip() in answer.lower().strip()


def retrieval_hits(expects, results) -> int:
    """
    Any part of the expect in the results(where the results are my chunks)

    Criterion 1, and a different measurement from judge(). The boats question
    is where the two come apart: the chunk holding "6am" is retrieved at rank
    1 and the answer still says "early morning". Retrieval found it,
    generation didn't use it.
    """
    needle = normalize(expects)
    return sum(needle in normalize(chunk.text) for chunk in results)
