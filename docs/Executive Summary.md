# Customer Experience Intelligence — Executive Summary

**Project:** Clinical Diagnostics CX Intelligence Platform

---

## Key Findings

Built an end-to-end customer experience analytics platform on Databricks covering 50,000 customers, 350,000 support interactions, 1.1M usage records, and 30,000 NPS surveys. The platform identifies four behavioral customer segments, scores detractor risk per customer, surfaces theme-level satisfaction drivers from open-text feedback, and generates rules-based service tier recommendations.

**Three findings stand out:**

1. **Reliability drives 60.6% of negative survey sentiment** — the single largest detractor lever, ahead of pricing (53.9%) and far ahead of support quality (25.8%).
2. **79.8% of customers are in a misaligned service tier** — the majority need upgrades, ~17% can be downgraded for cost efficiency.
3. **The "Silent Majority" segment is the biggest hidden risk** — 46% of the customer base, heavy product users, near-zero VoC engagement. The current model has no signal into their satisfaction state.

**Recommended next step:** Pilot a tier-restructured service program targeting the top 100 high-ARR upgrade candidates over a 6-month window with NPS lift and churn reduction as primary success metrics.

---

## Context

A clinical diagnostics company operates across 50,000 active customers spanning hospitals, clinical labs, research institutions, and specialty clinics. The CX team needs an integrated view linking behavioral data (support burden, instrument usage), satisfaction signal (NPS surveys), and financial value (ARR) to inform service tier strategy.

This project synthesizes those data streams into a single platform with:

- A unified customer 360 view
- Behavioral segmentation
- Predictive detractor risk scoring with explainable drivers
- LLM-classified qualitative themes from open-text comments
- Per-customer service tier recommendations

---

## Method

### Data pipeline

- **Bronze → Silver → Gold medallion architecture** on Databricks, using PySpark, Delta Lake, and Unity Catalog
- 8 data quality validation rules with auditable DQ log table
- 50,000 customer records cleaned, ~9,000 corrupt records flagged or remediated

### Analytics layer

- **K-means segmentation** (K=4, chosen via elbow method) on 12 behavioral features
- **Gradient boosting detractor model** with SHAP explainability, tracked via MLflow
- **LLM-powered theme extraction** using Databricks `ai_query()` on 23,000 survey comments

### Output layer

- **15-table Gold layer** including customer_360, segments, propensity scores, themes, and tier recommendations
- **AI/BI dashboard** with 6 executive-ready tiles
- **Databricks Genie space** for natural-language self-service analytics

---

## Findings

### 1. Customer base segments into four distinct behavioral profiles

| Segment | Size | % of base | Profile |
|---|---|---|---|
| **Silent Majority** | 23,077 | 46% | Heavy product users, near-zero survey response |
| **Dormant / Disengaged** | 9,548 | 19% | No active instruments, minimal test volume |
| **Strategic Champions** | 8,732 | 17% | High instrument count, vocal in VoC |
| **At-Risk High-Touch** | 8,643 | 17% | 3.62 friction events/customer — ~2x baseline (1.86) |

The **At-Risk High-Touch** segment carries 97% friction penetration — nearly every customer in this group has experienced a Critical or High-priority support ticket. This is the segment where service intervention has the highest ROI.

### 2. Reliability is the dominant detractor driver

Theme classification of 23,000 open-text comments revealed:

| Theme | Avg NPS | % Negative |
|---|---|---|
| **Reliability** | 5.49 | **60.6%** |
| **Pricing** | 5.99 | 53.9% |
| Training | 6.76 | 37.2% |
| Support Quality | 7.39 | 25.8% |
| Software | 7.46 | 19.0% |

Counterintuitively, **support quality is the most-mentioned theme but is sentiment-neutral.** Customers talk about support a lot, but their satisfaction is driven by product reliability — not the service response to product problems.

**Implication:** investments in support tier differentiation produce limited NPS lift unless paired with reliability interventions.

### 3. NPS collapses between months 3-12, then stabilizes

A normalized view of NPS by tenure shows:

- 0–3 months: 42% Promoter / 29% Detractor — healthy honeymoon
- 3–12 months: 30% Promoter / **41% Detractor** — sharp drop-off
- 1–2 years: 34% Promoter / 37% Detractor — stable
- 2+ years: 33% Promoter / 37% Detractor — stable

The customer satisfaction problem is not gradual erosion; it is a **post-honeymoon collapse in the first year.** This points to onboarding handoff, not long-term retention, as the high-leverage intervention window.

### 4. Service tier and customer value are decoupled

Across the current Bronze / Silver / Gold tiers, average ARR is essentially flat (~$66K across all three). High-value accounts are scattered indiscriminately. When tier recommendations are derived from segment + propensity + ARR:

- **79.8% of customers are in a misaligned tier**
- **The majority are recommended for upgrade**
- **~17% can be downgraded** for service cost efficiency

The total upgrade pool represents **$2.64B in at-risk ARR**, concentrated heavily in the **Silent Majority** — heavy users who are silently disengaged from VoC channels.

---

## Recommended pilot

### Scope

Begin with the **top 100 high-ARR upgrade candidates** as a pilot wedge — a focused cohort drawn from the At-Risk High-Touch and Strategic Champions segments, where intervention has the clearest behavioral signal. This wedge is a small, high-value slice of the broader $2.64B upgrade pool, sized to be operationally manageable in a single pilot window.

### Pilot structure (6-month window)

1. **Month 1:** Assign Customer Success Managers to the 100 pilot accounts; complete account intake interviews
2. **Months 2–5:** Execute the new Platinum service playbook (quarterly business reviews, 4-hour SLAs, named technical contact, proactive uptime monitoring)
3. **Month 6:** Measure NPS lift, retention, expansion ARR vs a matched control group

### Success metrics

- **Primary:** NPS lift of 10+ points within the pilot cohort
- **Secondary:** Reduction in Critical-priority tickets per customer by 25%
- **Tertiary:** Expansion ARR uplift of 5% in pilot cohort vs control
- **Risk metric:** Service cost per pilot customer should not exceed 1.5x current Gold-tier cost

### Operational considerations

- The Platinum tier does not exist in the current service catalog and would need to be created with associated playbooks, SLAs, and staffing.
- Pilot CSMs should focus on **reliability-related interventions** (the highest detractor lever) rather than support-process improvements.
- Onboarding handoff for new customers should be revisited in parallel given the 3–12 month NPS collapse.

---

## Limitations

This project was built on synthetic data; the magnitudes (e.g., the 79.8% misalignment rate) reflect characteristics of the test dataset and would differ on production data. Specifically:

- **Detractor risk model** showed modest absolute differentiation across customers on synthetic data; real-world data with stronger feature-target relationships is expected to produce clearer separation.
- **Theme-by-segment correlation was flat** in synthetic data because comment generation was independent of behavioral clustering. Real data should reveal segment-specific complaint patterns.
- **Current tier assignment was effectively random** in the synthetic data, inflating the misalignment rate. Real production data with historically-assigned tiers would likely show 15–25% misalignment, not 79.8%.

**The pipeline, methodology, and analytic patterns are transferable;** the headline magnitudes are data-dependent and should be re-derived on production data before any pilot decision.

---

## Stack summary

**Engineering:** Databricks, PySpark, Delta Lake, Unity Catalog
**ML/AI:** scikit-learn (K-means, gradient boosting), SHAP, MLflow, Databricks `ai_query()` foundation models
**Analytics & delivery:** Databricks SQL, AI/BI Dashboard, Genie

**Code:** 10 PySpark notebooks (ingestion → cleaning → modeling → recommendations → orchestration → DLT)
**Documentation:** Data dictionary, DQ log, model cards, this executive summary
