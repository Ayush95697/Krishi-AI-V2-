# Architectural Decision Record: Crop Recommendation ML Strategy

## Context
The KrishiAI+ project requires a Crop Recommendation module. The naive approach to this problem is a simple multiclass classification model trained on a synthetic dataset (e.g., standard Kaggle datasets predicting a single crop from exact soil/weather values). However, this approach suffers from data leakage (using realized weather), false precision (assuming district-level data applies to micro-farms), and biological impossibility (recommending crops outside their agro-ecological zones).

## Decision
We will formulate the Crop Recommendation problem as a **Suitability Ranking / Multi-Label Classification** problem constrained by expert rules, rather than a naive Multiclass Classification problem.

## Rationale
1. **Biological Reality:** Multiple crops can grow successfully in the same soil and climate. Forcing the model to pick a single "optimal" crop ignores crop rotation, market economics, and farmer preference.
2. **Data Availability:** We do not possess farm-level yield data mapped to farm-level soil data. We only possess district-level aggregates. Therefore, the model predicts *regional suitability*.
3. **Leakage Prevention:** We explicitly reject the use of realized post-harvest weather data as features. We will only use historical climate averages available prior to planting.

## Consequences
- The ML model will output a ranked list or suitability scores for multiple crops.
- We must implement a secondary "Expert Rule" layer (using ICAR Agro-Ecological Region constraints) to filter out mathematically probable but biologically inappropriate recommendations.
- The evaluation metrics will prioritize Top-K Accuracy and Macro F1 over absolute Top-1 Accuracy.
