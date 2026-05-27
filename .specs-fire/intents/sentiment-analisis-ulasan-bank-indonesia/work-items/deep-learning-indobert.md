---
id: deep-learning-indobert
title: Fine-tuning IndoBERT for >92% accuracy
intent: sentiment-analisis-ulasan-bank-indonesia
complexity: medium
mode: confirm
status: completed
depends_on:
  - experiment-matrix-design
created: 2026-05-27T01:40:00Z
run_id: run-submision-sentiment-analysist-002
completed_at: 2026-05-26T19:13:59.484Z
---

# Work Item: Fine-tuning IndoBERT

## Description

Melakukan fine-tuning IndoBERT untuk klasifikasi sentimen 3 kelas (Positive/Neutral/Negative) dengan target akurasi training dan testing >92%. Menangani class imbalance pada kelas Neutral.

## Acceptance Criteria

- [ ] IndoBERT berhasil di-fine-tune dengan data ulasan Bank Jago.
- [ ] Akurasi testing >= 92%.
- [ ] Akurasi training >= 92%.
- [ ] Confusion matrix dan classification report dihasilkan.
- [ ] Model dan tokenizer artifact tersimpan.
- [ ] Inference notebook diperbarui dengan model IndoBERT.

## Dependencies

- experiment-matrix-design

## Strategy

1. Handle class imbalance: oversampling Neutral, weighted loss
2. Fine-tune indobert-base-p1 (epochs=5, batch_size=16, LR=2e-5)
3. Evaluate: accuracy, precision, recall, F1 per class
4. Compare with baseline SVM (88.86%)
5. Save model + tokenizer to models/EXP-05_IndoBERT/
