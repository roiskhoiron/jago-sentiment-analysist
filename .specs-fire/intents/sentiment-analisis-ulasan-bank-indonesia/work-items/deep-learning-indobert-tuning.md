---
id: deep-learning-indobert-tuning
title: Hyperparameter tuning IndoBERT >92%
intent: sentiment-analisis-ulasan-bank-indonesia
complexity: medium
mode: confirm
status: completed
depends_on:
  - deep-learning-indobert
created: 2026-05-26T19:15:00Z
run_id: run-submision-sentiment-analysist-003
completed_at: 2026-05-26T23:34:18.924Z
---

# Work Item: Hyperparameter Tuning IndoBERT

## Description
Melanjutkan fine-tuning IndoBERT dari checkpoint terbaik dengan hyperparameter optimal untuk menarget akurasi >92%.

## Acceptance Criteria
- [ ] Akurasi training >92%.
- [ ] Akurasi testing >92%.
- [ ] Model + tokenizer artifact tersimpan.

## Strategy
1. Load checkpoint EXP-05 IndoBERT
2. Resume training: +2 epoch, LR=1e-5, max_length=96
3. Jika belum >92%, coba LR=5e-6 dengan +2 epoch lagi
4. Evaluasi: accuracy, precision, recall, F1 per class
