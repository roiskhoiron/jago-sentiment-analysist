# Implementation Plan: IndoBERT Hyperparameter Tuning

## Approach
Lanjutkan fine-tuning dari checkpoint EXP-05 (90.28%) untuk mencapai >92% accuracy.

## Changes from Baseline
| Parameter | EXP-05 | EXP-06 (this run) |
|-----------|--------|-------------------|
| Starting point | Pretrained IndoBERT | EXP-05 checkpoint |
| Max length | 64 | 96 |
| Epochs | 3 | +2 (resume) |
| Learning rate | 2e-5 | 1e-5 |
| Neutral oversample | Yes | Yes |

## Files to Create
- `scripts/tune_indobert.py`: Tuning script
- `models/EXP-06_IndoBERT_Tuned/`: Tuned model

## Files to Modify
- `reports/experiment_results.json`: Append EXP-06 results

## Expected Improvement
- Baseline EXP-05: 90.28%
- Target: >92%
- With longer sequences (96 vs 64) and continued fine-tuning, expected ~91-93%

---

**Approve? [Y/n]**
