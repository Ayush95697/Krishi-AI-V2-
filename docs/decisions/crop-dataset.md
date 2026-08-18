# Architectural Decision Record: Crop Recommendation Dataset Strategy

## Context
To train the Crop Recommendation ML module, we require a scientifically defensible dataset representing Indian agriculture. Common open-source datasets (e.g., Kaggle) are synthetic and suffer from data leakage. We investigated the feasibility of building a dataset from Tier-1 official sources (Govt of India OGD, ICAR, IMD).

## Decision
We will construct a **District-Level Hybrid Dataset**. We explicitly abandon the attempt to build a "farm-level" dataset from public sources, as raw farm-level soil and yield data are unavailable due to privacy and aggregation practices. 

## Rationale
1. **Availability:** District-wise Area, Production, and Yield (APY) data, IMD climate data, and IDP Soil Health aggregates are publicly available and legally usable.
2. **Joinability:** These datasets can be reliably joined using the composite key `[District] + [Season] + [Year]`.
3. **Scientific Integrity:** Acknowledging the spatial resolution as "District-Level" avoids the scientific fallacy of "False Precision" (pretending district averages apply identically to every micro-farm).

## Consequences
- The ML model will be trained to predict *regional* crop suitability based on district archetypes, rather than micro-farm optimality.
- The advisory layer (LLM/FastAPI) must clearly communicate to the farmer that the recommendation is a regional baseline requiring local verification.
- We must implement ICAR Agro-Ecological Region (AER) constraints to filter out biologically impossible recommendations that might arise from statistical anomalies in the aggregated data.
