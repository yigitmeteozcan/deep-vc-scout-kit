# Anti-Mainstream Filter

This filter defines what to downgrade or reject before finalizing the candidate list.

Apply this filter after candidate extraction, before producing CSV output.

---

## What to Downgrade or Reject

### 1. Mainstream startup media as primary source

Downgrade or reject any candidate whose primary source is:

- TechCrunch, TechEU, Sifted, EU-Startups
- Business Insider startup coverage
- Forbes 30 Under 30 or similar lists
- Fast Company, Wired startup coverage
- Local equivalent mainstream startup news (e.g., the dominant startup media site in the target country)
- General press releases on newswires

**Why:** If it appeared in mainstream startup media, every analyst in your sector has already seen it.

### 2. Obvious startup databases

Downgrade or reject any candidate found primarily through:

- Crunchbase (as discovery source, not verification)
- AngelList / Wellfound listings
- PitchBook profiles
- Dealroom profiles
- LinkedIn company search without deeper evidence
- CB Insights reports

**Why:** These databases lag real early-stage activity by 12-24 months and are checked by every analyst.

### 3. Companies already widely covered

Downgrade or reject any company that:

- Has appeared in more than two mainstream media articles
- Has a Crunchbase profile with multiple rounds already listed
- Has been featured on a well-known VC portfolio page visible to all analysts
- Is already included in widely-shared ecosystem maps or startup databases

**Why:** Wide coverage means wide analyst awareness. The edge is gone.

### 4. Old companies with no recent activity

Reject any company that:

- Was founded more than 5 years ago with no update in the last 24 months
- Has a website last updated more than 2 years ago
- Has no founder activity (LinkedIn, hiring, press) in the last 18 months
- Appears to be dormant, pivoted, or quietly shut down

**Why:** Recency is a signal of momentum. Old companies without signals are traps.

### 5. Generic AI wrapper claims

Reject any company described as:

- "AI-powered platform for [vague enterprise workflow]"
- "GPT-based tool for [generic use case]"
- "AI assistant for [broad category]"
- Any company where removing the word "AI" makes the description empty

Without a specific technical layer, specific buyer workflow, or specific evidence of product differentiation, AI framing is noise.

**Why:** Thousands of AI wrapper companies launched in 2023-2024. Without differentiation evidence, they are indistinguishable.

### 6. No founder or team evidence

Reject any company where:

- No founder name is findable
- No LinkedIn profile for a founder exists
- No team page exists
- The company appears to have no identified humans behind it

**Why:** Anonymous companies cannot be evaluated. Outreach is impossible. Risk is unquantifiable.

### 7. No traction or proof

Downgrade any company with:

- No pilot customers mentioned
- No grant, accelerator acceptance, or corporate partnership
- No revenue signal
- No LOI or strategic partner
- Only the founders' own claims with no external validation

A company with strong team and no traction can still pass if the team signal is extremely strong. But traction absence must be noted explicitly.

### 8. Startups that only sound interesting because of buzzwords

Apply this test: **remove every buzzword from the description.** What remains?

Buzzwords to test for: AI, deep tech, machine learning, blockchain, Web3, climate tech, sustainability, ESG, digital transformation, platform, ecosystem, disruptive, innovative, next-generation, state-of-the-art.

After removing buzzwords:
- Is the description still meaningful?
- Is there a specific buyer, specific workflow, specific problem?
- Is there a reason this company and no other company?

If the answer is no to all of these, it is a buzzword company. Reject.

---

## The Normal Analyst Test

Before including any candidate in the final list, ask:

> If a normal VC analyst sat down for 30 minutes with a Google search and Crunchbase, would they find this company?

If yes — it is not a hidden gem. Downgrade or reject.

The value of this scouting methodology is finding companies that do not appear in a normal analyst's 30-minute research session. That is the only edge worth capturing.

A candidate passes the normal analyst test only if:
- It was found through a non-obvious source path
- It has not been covered by mainstream startup media
- It does not appear prominently in public startup databases
- The reason it is non-obvious is specific and real

---

## Borderline Cases

Some candidates will be borderline: semi-hidden, somewhat covered, partially evidenced.

For borderline cases:
- Note explicitly that the candidate is borderline
- Explain which mainstream sources cover it
- Explain what hidden evidence exists
- Let the analyst decide — do not automatically reject or pass

The goal is transparency, not artificial scarcity.

---

## Filter Priority Order

When applying the filter, prioritize in this order:

1. Reject hard — no source URL, no recent signal, no founder evidence
2. Reject — mainstream only, old and dead, buzzword with no substance
3. Downgrade — semi-hidden but with some mainstream coverage
4. Pass with note — clear hidden source, strong evidence, specific thesis fit

Never pass a candidate that fails the hard rejection criteria in step 1.
