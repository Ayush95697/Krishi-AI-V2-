# Crop Recommendation ML Specification

## 1. Problem Definition
The Crop Recommendation module aims to predict the most suitable crop(s) for a specific district/region in India based on pre-planting agronomic realities. 
**Important Note:** The system does NOT predict the absolute "optimal" crop for a micro-farm based on precise GPS, as such data is largely unavailable or heavily confounded. Instead, it predicts a **suitability score/ranking** based on regional soil aggregates, historical climate, and expert constraints.

### Target Definition
The target is a ranked list of suitable crops for a given district and season. This is framed as a **Suitability Ranking** or **Multi-Label Classification** problem rather than a mutually exclusive Multiclass Classification problem, as multiple crops can thrive in the same conditions.

### Inputs (Candidate Features)
- **Soil Features:** Nitrogen (N), Phosphorus (P), Potassium (K), pH, Organic Carbon (OC), Electrical Conductivity (EC). 
  *Status*: Scientifically meaningful. Sourced at district-aggregate levels.
- **Climate Features:** Pre-planting historical average rainfall, temperature, and humidity for the growing season. 
  *Status*: Prone to leakage if realized (post-harvest) weather is used. We must strictly use historical averages or seasonal forecasts.
- **Geographic Context:** State, District, Agro-Ecological Region (AER). 
  *Status*: Crucial for preventing biologically impossible recommendations (e.g., apples in tropical plains).

## 2. Dataset Analysis
**Status:** No dataset is currently implemented in the repository. The directories `ml/crop_recommendation/data/` remain empty pending procurement of a scientifically defensible dataset.

## 3. Dataset Provenance
**Status:** Provenance is currently unestablished. We explicitly reject random Kaggle/GitHub datasets lacking documented collection methodologies. Future datasets must originate from Tier-1 sources (Govt of India, ICAR, IMD).

## 4. Feature Analysis
Features must reflect information actually available to a farmer *before* planting. 
- Realized seasonal rainfall: **REJECTED** (Data leakage).
- Historical average rainfall for the district: **ACCEPTED**.
- Farm-level soil macro-nutrients: **REJECTED** (Unavailable publicly at scale).
- District-level soil aggregates: **ACCEPTED**.

## 5. Target Analysis
Instead of an absolute "Ground Truth" crop, the target represents observed successful crop yields historically grown in the district, filtered by expert agro-ecological rules.

## 6. Scientific Limitations
- **False Precision:** District-level aggregates cannot provide sub-meter farm-level accuracy. The model provides a *regional baseline* that the farmer must adapt to their specific plot.
- **Weather Uncertainty:** Historical averages do not guarantee future weather. The model's recommendations are probabilistic.

## 7. Baseline Strategy
Before training complex models, we will establish:
1. **Majority-Class Baseline:** To quantify class imbalance.
2. **Logistic Regression:** A simple linear baseline.
3. **Random Forest:** A robust ensemble baseline that handles unscaled soil parameters and non-linear interactions well.

## 8. Evaluation Strategy
- **Split:** 70/15/15 (Train/Validation/Test).
- **Stratification:** Stratified splitting by Agro-Ecological Region and Season.
- **Metrics:** 
  - *Macro F1 & Weighted F1:* Preferred over accuracy due to expected class imbalance.
  - *Confusion Matrix:* To identify if the model confuses agronomically incompatible crops.
  - *Top-K Accuracy:* Since we output a ranked list, whether a viable crop appears in the Top-3 recommendations is highly relevant.

## 9. Explainability Strategy
- **Approach:** SHAP (SHapley Additive exPlanations) and tree-based Feature Importance.
- **Goal:** To generate human-readable reasoning (e.g., "Recommended because historical rainfall in your district during Kharif is ideal for Maize").

## 10. Model Persistence Strategy
- **Recommendation:** `joblib` packaged with `scikit-learn` pipelines.
- **Reasoning:** Native to Python, highly efficient for sklearn, and trivial to load into the FastAPI application. 

## 11. Reproducibility Strategy
- Hash the dataset prior to training.
- Pin `scikit-learn`, `pandas`, and `numpy` versions.
- Hardcode random seeds (`random_state=42`).
- Save a `metadata.json` alongside the `.joblib` artifact containing hyperparameter configurations and feature definitions.

## 12. Production Inference Architecture
```text
Farmer → React Frontend → FastAPI Endpoint → Advisory Engine
                                                 ↓
                                         ML Inference Module (loads .joblib)
                                                 ↓
                                         Crop Prediction + SHAP Explanations
```

## 13. Open Questions
- Can we secure access to granular ICAR Landscape Crop Assessment Survey (LCAS) data to improve spatial resolution?

## 14. Recommended Next Step
Proceed to the dataset procurement phase, specifically targeting the integration of DES Area/Production/Yield data with IMD climate data at the district level.
