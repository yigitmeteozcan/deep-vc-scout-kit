# Scoring Rubric

This rubric is used by `score_candidates.py` to evaluate each new candidate. It is also included in the context pack so GPT understands how candidates will be judged.

Each dimension is scored 0, 3, or 5. Maximum total score is 40.

---

## Dimensions

### 1. Team (team_score)

| Score | Meaning |
|---|---|
| 0 | No founder or team evidence found. Anonymous company. |
| 3 | Relevant founder background for the sector. Some domain knowledge evident. |
| 5 | Elite founder-market fit: deep technical or domain expertise, repeat founder, PhD in relevant field, former operator at a target customer type, or exceptional talent signal. |

Score from what is written in `founder_signal`. Missing or vague = 0.

---

### 2. Product (product_score)

| Score | Meaning |
|---|---|
| 0 | Vague idea. No product description, no demo, no workflow clarity. |
| 3 | Clear product or prototype. Specific use case and buyer described. |
| 5 | Painful buyer problem with clear workflow, specific use case, and evidence of product-market understanding. Not just a feature — a real product. |

Score from `short_description` and `traction_proof`. Buzzword-heavy descriptions without specifics = 0.

---

### 3. Technology (technology_score)

| Score | Meaning |
|---|---|
| 0 | Generic software. No differentiation evident. Could be built by anyone. |
| 3 | Defensible technical layer. Some technical depth visible in the description or source. |
| 5 | Deep tech, infrastructure, hardware-software integration, robotics, AI infrastructure (not wrapper), energy systems, materials science, industrial automation, or similar with specific evidence. |

Score from `short_description`, `why_non_obvious`, and `source_type`. AI wrapper claims without specifics = 0.

---

### 4. Commercialization (commercialization_score)

| Score | Meaning |
|---|---|
| 0 | No commercial proof. Idea stage with no external validation. |
| 3 | Pilot, grant, accelerator acceptance, LOI, or early customer (unpaid or paid). Some external validation exists. |
| 5 | Paying customer, meaningful revenue signal, strategic partnership with a named company, or strong buyer pull with multiple proof points. |

Score from `traction_proof`. Missing = 0.

---

### 5. Fund Fit (fund_fit_score)

| Score | Meaning |
|---|---|
| 0 | No fit with fund thesis. Wrong sector, stage, or geography. |
| 3 | Some fit. Sector or geography is close but not a strong match. |
| 5 | Strong fit. Company directly matches fund thesis on sector, stage, geography, and value-add potential. |

Score from `why_fund_should_care`. Generic alignment = 3 at most. Specific and compelling = 5.

---

### 6. Geography / Founder Angle (geo_angle_score)

| Score | Meaning |
|---|---|
| 0 | No geographic or founder angle relevant to the fund. |
| 3 | Weak market or team angle. Some connection to target geography or founder profile. |
| 5 | Strong founder-geography-market advantage. Diaspora founder, local market expertise, geography-specific buyer pull, or cross-border angle that directly fits fund positioning. |

Score from `geo_angle`. Missing = 0.

---

### 7. Non-Obviousness (non_obviousness_score)

| Score | Meaning |
|---|---|
| 0 | Mainstream. Found only in obvious sources. Every analyst knows this company. |
| 3 | Semi-hidden. Found in a slightly less obvious source but still somewhat covered. |
| 5 | Hidden gem. Found through a non-obvious source path (grant page, university spinout, conference exhibitor, LinkedIn founder post) with a real, specific reason others would miss it. |

Score from `why_non_obvious` and `source_type`. Source must match claim.

---

### 8. Recency Signal (recency_signal_score)

| Score | Meaning |
|---|---|
| 0 | Old, dead, or no updates. Last activity more than 2 years ago or company appears inactive. |
| 3 | Active in the last 12-24 months. Some recent signal but not fresh. |
| 5 | Recent launch, new hire, grant awarded, pilot announced, accelerator accepted, or stealth founder signal in the last 12 months. Fresh momentum. |

Score from `recent_signal`. Missing = 0.

---

## Total Score and Recommendation

| Total Score | Recommendation |
|---|---|
| 36 and above | Strong Meet |
| 30 to 35 | Meet |
| 22 to 29 | Watch |
| Below 22 | Pass |

Maximum possible score: 40

---

## Scoring Notes

- Do not give points for buzzwords alone. "AI-powered" does not score on technology without specifics.
- Missing evidence always scores 0 for that dimension.
- Vague evidence scores 0 or 3 depending on how specific the claim is.
- The rubric rewards specificity, evidence, and non-obviousness — not hype.
- A company can score high on team and low on traction. That is a Watch or Meet with a clear caveat.
- A company that scores 0 on non-obviousness is unusual to include at all — the scouting prompt should have filtered it already.

---

## After Scoring

Scored candidates go to `review_candidates.py` for a critic layer review.

The critic can downgrade recommendations by one level if major evidence gaps are found.

The final recommendation from the critic is what goes into `analyst_notes.md`.
