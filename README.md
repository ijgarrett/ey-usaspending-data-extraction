# EY x ML@UVA: USAspending Data Pipeline & Cleaning Record

This repository contains the production-grade data engineering pipeline used to ingest, clean, and transform the bulk FY2026 USAspending transaction logs. The resulting dataset is optimized for dense NLP semantic embeddings, capability matching, and financial runway tracking.

## 📋 Transformation & Ingestion Record

### 1. Schema Optimization & Scope Filtering
* **Action:** Trimmed the raw USAspending layout from 297 columns down to core target variables, then filtered rows strictly to those matching NAICS code prefix `54` (Professional, Scientific, and Technical Services).
* **Impact:** Programmatically eliminated over 90% of administrative column noise and isolated relevant service records, refining the row count from 203 to 197 active rows.

### 2. Imputation & Rectangular Integrity
* **Action:** Missing text identifiers (e.g., `parent_award_id_piid`, `solicitation_identifier`) were mapped to empty string arrays (`""`). Missing date entries parsed during CSV round-trips were normalized to prevent native `NaT` (Not-a-Time) gaps in the final matrix.
* **Impact:** Achieved a strict target of **0 missing cells** across all 37 final attributes, preventing downstream tokenizers or embedding pipelines from throwing null exceptions.

### 3. Feature Engineering & Transformations
* **NLP Clean Text:** Created a composite string mapping macro descriptions to granular task orders (`nlp_clean_text`), lowercased, and stripped of fiscal year indicators or regulatory markers (e.g., *FY24*, *A-123*) so NLP algorithms focus purely on technical capabilities.
* **Log Scaling:** Applied a $\log_{10}(x + 1)$ scale transformation to the highly skewed `current_total_value_of_award` figures to prevent massive outlier awards from dominating future scoring weights.
* **Temporal Horizons:** Built integer countdown fields (`contract_duration_days` and `days_until_recompete`) relative to a standard pipeline tracking index (June 23, 2026) to identify imminent recompete windows.

## 🧠 Core Pipeline Assumptions
1. **Scope Boundary:** We assume any transaction outside of NAICS `54xxxx` is an outlier relative to EY’s primary professional services focus area and can be safely omitted.
2. **Missing Date Logic:** Contracts missing a formal potential end date are assumed to be static administrative/obligatory adjustments rather than active project extensions, and are safely backdated to a baseline placeholder (`1970-01-01`).
3. **Primary Text Weight:** We assume the core technical capabilities of an award are captured fully by combining the base transaction description with the specific product/service code description.
