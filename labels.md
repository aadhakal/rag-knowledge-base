# Hand labels — 30 answers from two runs

Ground truth for scoring judge() and llm_as_judge(). Two rules decided before
labelling, applied uniformly to every run of the same question:

1. **Marchwood** — naming Marchwood as the exception counts as answering the
   question, even where the phrasing is indirect. A reader learns where late
   eating survives.
2. **6am** — "early morning" is true but is not a time. The question asked for a
   time and the corpus states one, so a vaguer answer is a fail.

See CONTESTED at the bottom for the one row where rule 1 strains.

## When did the railway line north of Brightwater close?

`expects`: **1963**

### 1. (run_2026-09-23_1735.md)

```
The railway line north of Brightwater closed in 1963. This information comes from `guide_regional_transport.md`.
```

- verdict: pass
- reason: States 1963 outright. Unambiguous.

### 2. (run_2026-09-23_1735.md)

```
The railway line north of Brightwater closed in 1963. 

Source: `guide_regional_transport.md`
```

- verdict: pass
- reason: States 1963 outright. Unambiguous.

### 3. (run_2026-09-23_1735.md)

```
The railway line north of Brightwater closed in 1963. 

Source: guide_regional_transport.md
```

- verdict: pass
- reason: States 1963 outright. Unambiguous.

### 4. (run_2026-09-23_1745.md)

```
The railway line north of Brightwater closed in 1963. 

Source: `guide_regional_transport.md`
```

- verdict: pass
- reason: States 1963 outright. Unambiguous.

### 5. (run_2026-09-23_1745.md)

```
The railway line north of Brightwater closed in 1963, according to *guide_regional_transport.md*.
```

- verdict: pass
- reason: States 1963 outright. Unambiguous.

### 6. (run_2026-09-23_1745.md)

```
The railway line north of Brightwater closed in 1963. 

Source: guide_regional_transport.md
```

- verdict: pass
- reason: States 1963 outright. Unambiguous.

## Where is it cheaper to eat in Halden Bay than the harbour front?

`expects`: **Fell Street**

### 1. (run_2026-09-23_1735.md)

```
It is cheaper to eat on Fell Street, which is one level up from the harbour front (guide_halden_bay.md and guide_eating.md).
```

- verdict: pass
- reason: Names Fell Street as the cheaper option. Direct answer.

### 2. (run_2026-09-23_1735.md)

```
It is cheaper to eat on Fell Street, which is one level up from the harbour front (guide_halden_bay.md and guide_eating.md).
```

- verdict: pass
- reason: Names Fell Street as the cheaper option. Direct answer.

### 3. (run_2026-09-23_1735.md)

```
It is cheaper to eat on Fell Street, which is one level up from the harbour front (guide_halden_bay.md and guide_eating.md).
```

- verdict: pass
- reason: Names Fell Street as the cheaper option. Direct answer.

### 4. (run_2026-09-23_1745.md)

```
It is cheaper to eat on Fell Street, which is one level up from the harbour front (guide_halden_bay.md and guide_eating.md).
```

- verdict: pass
- reason: Names Fell Street as the cheaper option. Direct answer.

### 5. (run_2026-09-23_1745.md)

```
It is cheaper to eat on Fell Street, one level up from the harbour front (guide_halden_bay.md and guide_eating.md).
```

- verdict: pass
- reason: Names Fell Street as the cheaper option. Direct answer.

### 6. (run_2026-09-23_1745.md)

```
It is cheaper to eat on Fell Street, which is one level up from the harbour front. 

Sources: `guide_halden_bay.md` and `guide_eating.md`
```

- verdict: pass
- reason: Names Fell Street as the cheaper option. Direct answer.

## Where can I eat late at night in this region?

`expects`: **Marchwood**

### 1. (run_2026-09-23_1735.md)

```
Based on the provided documents, kitchens across the region stop serving at 9pm and often earlier, outside of Marchwood. 

Source: `guide_eating.md`
```

- verdict: pass
- reason: RULE: naming Marchwood as the exception counts as answering.

### 2. (run_2026-09-23_1735.md)

```
Based on the provided documents, kitchens across the region stop serving at 9pm and often earlier, and there is no mention of anywhere to eat late at night. 

Source: `guide_eating.md`
```

- verdict: fail
- reason: Never names Marchwood and asserts there is nowhere to eat late. Wrong on the fact.

### 3. (run_2026-09-23_1735.md)

```
Based on the provided documents, kitchens across the region stop serving at 9pm and often earlier, outside of Marchwood. 

Source: `guide_eating.md`
```

- verdict: pass
- reason: RULE: naming Marchwood as the exception counts as answering.

### 4. (run_2026-09-23_1745.md)

```
Based on the provided documents, you cannot eat late at night in this region. Outside of Marchwood, kitchens stop serving at 9pm and often earlier, and Kestrelford's pubs only serve from 12 to 2 and 6 to 8:30 with nowhere to eat outside those windows. 

Source: `guide_eating.md`
```

- verdict: pass
- reason: RULE: naming Marchwood as the exception counts as answering.  ⚠ CONTESTED — see bottom.

### 5. (run_2026-09-23_1745.md)

```
Based on the provided documents, kitchens across the region stop serving at 9pm and often earlier, except in Marchwood where you might find later options. 

Source: guide_eating.md
```

- verdict: pass
- reason: RULE: naming Marchwood as the exception counts as answering.

### 6. (run_2026-09-23_1745.md)

```
Based on the provided documents, kitchens across the region stop serving at 9pm and often earlier, so eating late at night is generally not supported. (Source: `guide_eating.md`)
```

- verdict: fail
- reason: Never names Marchwood and asserts there is nowhere to eat late. Wrong on the fact.

## Are the seafront hotels in Pellew Sands quieter than the guesthouses?

`expects`: **noisier**

### 1. (run_2026-09-23_1735.md)

```
No, the seafront hotels are noisier than the Marine Terrace guesthouses (guide_pellew_sands.md).
```

- verdict: pass
- reason: Gets the comparison right — hotels are noisier than the guesthouses. The leading 'No' is the correct answer to the question as asked, not a refusal.

### 2. (run_2026-09-23_1735.md)

```
No, the seafront hotels are noisier than the Marine Terrace guesthouses. 

Source: guide_pellew_sands.md
```

- verdict: pass
- reason: Gets the comparison right — hotels are noisier than the guesthouses. The leading 'No' is the correct answer to the question as asked, not a refusal.

### 3. (run_2026-09-23_1735.md)

```
No, the seafront hotels are noisier than the Marine Terrace guesthouses (guide_pellew_sands.md).
```

- verdict: pass
- reason: Gets the comparison right — hotels are noisier than the guesthouses. The leading 'No' is the correct answer to the question as asked, not a refusal.

### 4. (run_2026-09-23_1745.md)

```
No, the seafront hotels are noisier than the Marine Terrace guesthouses. 

(Source: guide_pellew_sands.md)
```

- verdict: pass
- reason: Gets the comparison right — hotels are noisier than the guesthouses. The leading 'No' is the correct answer to the question as asked, not a refusal.

### 5. (run_2026-09-23_1745.md)

```
No, the seafront hotels are noisier than the Marine Terrace guesthouses. 

Source: `guide_pellew_sands.md`
```

- verdict: pass
- reason: Gets the comparison right — hotels are noisier than the guesthouses. The leading 'No' is the correct answer to the question as asked, not a refusal.

### 6. (run_2026-09-23_1745.md)

```
No, the seafront hotels are actually noisier than the Marine Terrace guesthouses. 

Source: guide_pellew_sands.md
```

- verdict: pass
- reason: Gets the comparison right — hotels are noisier than the guesthouses. The leading 'No' is the correct answer to the question as asked, not a refusal.

## What time do the boats land at Halden Bay?

`expects`: **6am**

### 1. (run_2026-09-23_1735.md)

```
The boats land in the early morning (guide_halden_bay.md).
```

- verdict: fail
- reason: RULE: 'early morning' is true but is not a time, and the question asked for one. guide_halden_bay.md:19 states 6am; the pipeline didn't surface it.

### 2. (run_2026-09-23_1735.md)

```
The boats land in the early morning (guide_halden_bay.md).
```

- verdict: fail
- reason: RULE: 'early morning' is true but is not a time, and the question asked for one. guide_halden_bay.md:19 states 6am; the pipeline didn't surface it.

### 3. (run_2026-09-23_1735.md)

```
The boats land in the early morning (guide_halden_bay.md).
```

- verdict: fail
- reason: RULE: 'early morning' is true but is not a time, and the question asked for one. guide_halden_bay.md:19 states 6am; the pipeline didn't surface it.

### 4. (run_2026-09-23_1745.md)

```
The boats land in the early morning (guide_halden_bay.md).
```

- verdict: fail
- reason: RULE: 'early morning' is true but is not a time, and the question asked for one. guide_halden_bay.md:19 states 6am; the pipeline didn't surface it.

### 5. (run_2026-09-23_1745.md)

```
The boats land in the early morning (guide_halden_bay.md).
```

- verdict: fail
- reason: RULE: 'early morning' is true but is not a time, and the question asked for one. guide_halden_bay.md:19 states 6am; the pipeline didn't surface it.

### 6. (run_2026-09-23_1745.md)

```
The boats land in the early morning (guide_halden_bay.md).
```

- verdict: fail
- reason: RULE: 'early morning' is true but is not a time, and the question asked for one. guide_halden_bay.md:19 states 6am; the pipeline didn't surface it.

---

## CONTESTED — one row to confirm or flip

Rule 1 says naming the exception counts as answering. This answer does name it,
but opens by flatly denying the fact:

```
Based on the provided documents, you cannot eat late at night in this region. Outside of Marchwood, kitchens stop serving at 9pm and often earlier, and Kestrelford's pubs only serve from 12 to 2 and 6 to 8:30 with nowhere to eat outside those windows. 

Source: `guide_eating.md`
```

(run_2026-09-23_1745.md)

Labelled **pass** because rule 1 is about whether Marchwood gets named as the
exception, and it does. But the first sentence asserts the opposite, so a
stricter reading of the same rule would fail it.

This single row decides which judge scores better — see the run of
`score_judges.py`. Flip it if you disagree; the rest are unaffected.
