# Implementation Plan: Fine-tuning IndoBERT

## Approach

Fine-tune IndoBERT (indobenchmark/indobert-base-p1) on 10k Bank Jago reviews with class imbalance handling to target >92% training and testing accuracy.

## Strategy

1. **Handle class imbalance**: Oversample Neutral class (k=2), use weighted CrossEntropyLoss
2. **Fine-tune**: indobert-base-p1, 5 epochs, batch_size=16, learning_rate=2e-5, warmup=10%
3. **Evaluate**: accuracy, precision/recall/F1 per class, confusion matrix
4. **Compare**: benchmark against SVM baseline (88.86%)

## Files to Create

- `scripts/run_indobert.py`: Full fine-tuning script
- `models/EXP-05_IndoBERT/`: Model + tokenizer artifacts
- `reports/EXP-05_IndoBERT_classification.txt`: Evaluation results

## Files to Modify

- `notebooks/02_training.ipynb`: Add IndoBERT experiment section (optional)
- `notebooks/03_inference.ipynb`: Update to load IndoBERT model (best)

## Dependencies to Install

- torch (CPU or CUDA)
- transformers
- datasets
- accelerate

## Risk

| Risk | Mitigation |
|------|-----------|
| No GPU → slow training (~3-5h CPU) | Use batch_size=8, mixed precision, or skip if too slow |
| OOM on CPU | Reduce max_length=64, batch_size=4 |
| Neutral class still weak | Apply focal loss or class weighting |

---

**Approve plan? [Y/n]**
