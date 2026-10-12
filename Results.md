# Evaluation results

Command: `python -m eval.run_eval --no-judge` (53 labelled cases, 14 categories, in-process, fresh session per case, all turns replayed, last turn scored). Model: llama3.2:3b, MiniLM-L6-v2, Chroma, chunks 120 words / 30 overlap, TOP_K context 4 chunks, SCORE_THRESHOLD 0.30, SUPPORT_MIN 0.60. KB snapshot 2026-10-08.

## Headline numbers (final run)

| Metric | Baseline (first run) | Final |
|---|---|---|
| Status accuracy | 45/53 = 0.85 | **48/53 = 0.91** |
| Refusal (out_of_scope) precision / recall | 0.61 / 1.00 (11/18) | **0.69** / 1.00 (11/16) |
| Retrieval hit@1 / hit@3 / hit@5 (30 answerable cases) | 28 / 30 / 30 | 28 / 30 / 30 |
| Citation accuracy, lenient / strict (25 answered) | 23/23 | 24/25 / 24/25 |
| Forbidden-text check (no claimed actions, no prompt leak) | 53/53 | 53/53 |
| Latency p50 / p95 / max per request | 26.7 / 48.2 / 50.4 s | 26.1 / 51.4 / 74.6 s |

An intermediate run had one request of 581.9 s (t53). It was consistent with an Ollama stall followed by the 120 s timeout and one retry, per LLM call. It did not recur in the final run. Rule-decided turns (clarify, off-topic, injection, explicit handoff) return in about 0.02 s because they never call the LLM.

Changes between baseline and final: article-margin context selection and a procedure-step boost; sentence-level grounding filter before the support check; the vague-message check runs on the raw text after a failed turn (fixes t42); source-number leakage stripped; prompt rules for partial and false-premise questions.

## Confusion matrix (final)

| expected \ got | answered | clarify | out_of_scope | handoff |
|---|---|---|---|---|
| answered | 25 | 0 | 5 | 0 |
| clarify | 0 | 8 | 0 | 0 |
| out_of_scope | 0 | 0 | 11 | 0 |
| handoff | 0 | 0 | 0 | 4 |

## Per category (final; 3-4 cases each, so one case moves a category by 25-33 points)

action_request 3/3, ambiguous 4/4, confusable 4/4, false_premise 2/3, handoff 4/4, messy 3/4, multi_step 4/4, multi_turn 4/4, oos_general 4/4, oos_near_miss 4/4, partial 1/3, prompt_injection 4/4, single_article 4/4, two_articles 3/4.

## Failures (5 of 53) and what I would try next

All five are **over-refusals**; no wrong status was a served wrong answer.

| Case | Message | Expected / got | Cause | Next step |
|---|---|---|---|---|
| t09 | "ff eating all my ram pls help" | answered / out_of_scope | The model invented a `top` terminal command and RAM-upgrade advice. Support ratio 0.40-0.56 against a 0.60 cutoff. The refusal is arguably correct | Sentence-level entailment check; try a larger model (qwen2.5:7b) |
| t14 | "If I refresh Firefox, do I lose my extensions and my bookmarks?" | answered / out_of_scope | The answer was right, but the sentence "you will lose your extensions" scored low on word overlap (the article says "Extensions and themes"), dropping the ratio to 0.50 | Embedding-based sentence support instead of word overlap |
| t30 | "export my bookmarks and also import them into Chrome" | answered / out_of_scope | The foreign-product scope guard refuses any message naming Chrome without Firefox | Per-clause scope check |
| t31 | "update Firefox and also speed up my Wi-Fi router" | answered / out_of_scope | Router advice is invented; the update steps are correct and survive the sentence filter, but the whole-answer ratio (0.53) is checked against 0.60 and refuses | Compute the ratio on the filtered text only (a code fix I had not completed when the numbers were frozen) |
| t52 | "Why can't I export bookmarks to HTML anymore? I heard Firefox removed that." | answered / out_of_scope | Ratio near the cutoff (0.54-0.62 across runs) | Premise-correction template; entailment check |

## Retrieval-only evaluation (`eval/retrieval_eval.py`, 25 single-turn answerable cases)

hit@1 0.92 (23/25), hit@3 1.00, hit@5 1.00. Top-1 score distribution:

| Group | n | min | median | max |
|---|---|---|---|---|
| In-scope | 25 | 0.437 | 0.684 | 0.842 |
| oos_general | 4 | 0.015 | 0.055 | 0.154 |
| oos_near_miss | 4 | 0.489 | 0.595 | 0.700 |

A threshold anywhere from 0.20 to 0.40 refuses all 4 general off-topic questions and 0 in-scope questions (chosen: 0.30). The near-misses (Safari, Chrome, Android, NordVPN) score inside the in-scope range, so the threshold cannot catch them; a rule-based scope guard does.

## Faithfulness

- **LLM judge (baseline run, same llama3.2:3b):** reported 2 of 24 answers as supported. That number is not usable: it flagged correct answers as unsupported (for example "Private Browsing does not make you anonymous" was flagged as unsupported for "makes you anonymous"). It cannot handle negation. The judge was not run in the final run.
- **Manual review (`eval/results/manual_review.csv`):** MANUAL_REVIEW_SUMMARY_PLACEHOLDER (fill in: X of 16 supported, which were wrong and why, how often the LLM judge disagreed).
- **Wrong answer that passed every automatic metric (baseline, t13):** "Will refreshing Firefox delete my saved passwords?" was answered "Yes, refreshing Firefox will delete your saved passwords." Article 1 lists Passwords under items Firefox saves. Status, retrieval and citation were all correct. Only reading the answer catches it.

## Known limitations not covered by a test
- Steps that the site shows conditionally per Firefox version or OS can read garbled ("Help Help and Report", stray `[macOS]` labels). Some answers merge Windows and macOS steps (t08, t50).
- The lexical support check cannot detect a plausible-sounding but wrong sentence made of source words (t13).
- 53 cases written by one person; per-category percentages are noisy.