# Labeling Strategy

## Rating-to-Sentiment Mapping

| Rating | Label | Notes |
|--------|-------|-------|
| 5 | Positive | Sangat puas |
| 4 | Positive | Cenderung puas |
| 3 | Neutral | Netral / mixed feelings |
| 2 | Negative | Cenderung tidak puas |
| 1 | Negative | Sangat tidak puas |

## 3-Class Sentiment Scheme

- **Positive** (ratings 4-5): Reviews expressing satisfaction, praise, or positive experience.
- **Neutral** (rating 3): Reviews that are factual, mixed, or neither clearly positive nor negative.
- **Negative** (ratings 1-2): Reviews expressing dissatisfaction, complaints, or negative experience.

## Handling Neutral Data

- Reviews with rating 3 are labeled as neutral.
- If neutral class is underrepresented (<10% of dataset), consider downsampling or using semi-supervised techniques.
- Neutral reviews containing both positive and negative aspects are kept as neutral to preserve balance.
- Edge cases: empty/meaningless text marked as neutral.

## Quality Assurance

- Random sample of 200 labeled reviews manually checked for correctness.
- Inter-annotator agreement (if multiple labelers): Cohen's κ ≥ 0.8.
- Class distribution report generated after labeling.
