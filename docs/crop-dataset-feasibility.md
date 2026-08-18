# Crop Dataset Discovery & Feasibility Study

## 1. Research Question
**Can we construct a scientifically defensible dataset for Indian crop suitability/recommendation by combining reliable public agricultural datasets?**

## 2. Sources Investigated
1. **Directorate of Economics and Statistics (DES)**: Area, Production, and Yield (APY) reports. (Verified via data.gov.in and UPAg).
2. **India Meteorological Department (IMD)**: Historical district-wise rainfall and temperature datasets.
3. **Soil Health Card (SHC)**: Official portal and India Data Portal (IDP) summaries.
4. **ICAR NBSS&LUP**: Agro-Ecological Regions (AER) maps and soil-site suitability publications via BHOOMI Geoportal.

## 3. Dataset Comparison Table
| Source | Variables | Spatial Granularity | Temporal Granularity | Licensing / Access |
|---|---|---|---|---|
| **DES APY** | Crop, Area, Production, Yield | District | Annual / Seasonal | Open Data (Govt of India) |
| **IMD** | Rainfall, Temp, Humidity | District / 0.25° Grid | Daily / Monthly | Academic / Public (some restrictions) |
| **IDP SHC** | N, P, K, pH, OC, EC | District (Aggregated) | Cycle (e.g., 2017-2019) | Open Data |
| **ICAR AER** | Agro-Ecological Region, Soil Type | District (Mapped) | Static | Public |

## 4. Source Provenance
All sources are Tier-1 official Indian government resources or verified aggregators (IDP). They represent true field measurements and official government estimates, not synthetic data.

## 5. Variables Available
- **Location**: State, District.
- **Season**: Kharif, Rabi, Zaid/Summer, Whole Year.
- **Climate**: Pre-planting average temperature, average rainfall.
- **Soil**: District-level average N, P, K, pH, OC.
- **Outcome**: Crop grown, Area sown, Production volume, Yield (kg/ha).

## 6. Spatial Resolution
**DISTRICT LEVEL**. 
Raw farm-level soil data is protected by privacy laws and unavailable in bulk. Farm-level yield data is not systematically published in a unified open dataset. 

## 7. Temporal Resolution
**SEASONAL / ANNUAL**.
Crop outcomes are reported per season (Kharif, Rabi, Summer). Soil data is reported in 2-year cycles. Climate data is available monthly and can be aggregated to the pre-planting months.

## 8. Licensing
Datasets hosted on `data.gov.in` and `indiadataportal.com` are available under the Open Government Data License (India), permitting use for research and application development.

## 9. Joinability
The datasets can be successfully joined on the composite key: `[District] + [Season] + [Year]`.
ICAR AER static maps can be joined on `[District]`.

## 10. Data Quality Concerns
- **False Precision:** Merging district-level soil averages with district-level climate averages creates a *regional archetype*, not a specific farm.
- **Missing Values:** APY data often has missing yield values for minor crops in certain districts.
- **Temporal Mismatch:** Soil testing cycles (e.g., 2015-2017) may not perfectly align with annual crop yield data.

## 11. Candidate Dataset Architectures
- **Strategy A (Single authoritative dataset):** Infeasible. No such open dataset exists for India.
- **Strategy B (Multi-source integration):** Feasible at the district level.
- **Strategy C (ML + expert knowledge hybrid):** Highly feasible. ML predicts based on the integrated district dataset, and expert rules (ICAR AER) constrain the outputs.

## 12. ML Formulation Options
- **Regression:** Predict relative yield for a given crop in a given district.
- **Ranking / Multi-label:** Rank crops by historical frequency and yield success in the district's archetypal conditions.

## 13. Scientific Limitations
- The system can only predict *regional agronomic suitability*. The farmer must adapt the recommendation to their specific micro-farm conditions (e.g., specific water access, precise soil test).

## 14. Recommended Strategy
We recommend **Strategy C: ML + expert knowledge hybrid**. We will integrate DES APY, IMD, and IDP Soil data at the district level to predict regional crop suitability, and apply ICAR Agro-Ecological constraints as a strict post-processing filter.

## 15. Remaining Unknowns
- Can we automate the extraction of IMD gridded data to district-level averages programmatically without requiring manual GIS processing?
- How to handle districts that cross multiple Agro-Ecological Regions?
