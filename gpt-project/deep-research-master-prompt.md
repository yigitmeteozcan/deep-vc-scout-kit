# Deep Research Master Prompt

Paste this into a new chat inside your ChatGPT Project to start a scouting session.

---

## Prompt

You have access to an uploaded context pack (`context_pack.md`). Use it as your source of truth for this session.

**Your task:** Scout for startups that match the fund thesis described in the context pack.

---

### Step 1: Review the context pack

Before searching, read:
- Fund thesis (what the fund invests in)
- Known pipeline (companies to exclude)
- Good examples (what fund-fit looks like)
- Bad examples (what to reject)
- Mainstream sources to avoid (deprioritize these)
- Hidden sources to prioritize (start here)
- Scoring rubric (how candidates will be evaluated)
- Output schema (exact format required)

---

### Step 2: Search source-first

Do not search startup categories. Search source paths.

Run separate search missions for each of the following:

**Mission 1 – Founder signal**
Search for recent founder announcements, stealth founder posts, founder hiring posts, and founder LinkedIn activity in the target geography and sector.

**Mission 2 – Obscure accelerator cohorts**
Search for smaller, less-known accelerator batches, technopark residents, and startup program finalists outside the obvious programs.

**Mission 3 – University and lab spinouts**
Search for university technology transfer pages, research commercialization offices, and lab spinout announcements.

**Mission 4 – Grant and project winners**
Search for Horizon Europe project partners, national innovation grant winners, EIT program participants, government-backed R&D project lists, and public innovation fund recipients.

**Mission 5 – Conference and exhibitor lists**
Search for industry conference exhibitor lists, trade show participants, and niche industry event speaker or sponsor pages.

**Mission 6 – Hiring and stealth signals**
Search for companies posting technical or commercial roles that signal recent activity and growth without mainstream coverage.

**Mission 7 – Diaspora founder signals**
Search for founders from the target geography who are building in the target sector, including diaspora networks and international founder communities.

**Mission 8 – Local ecosystem edge cases**
Search for niche local ecosystem pages, corporate innovation challenge finalists, industry association event winners, and community announcements outside mainstream startup news.

---

### Step 3: Extract candidates

For each company found, collect:

- Company name
- Website
- Source URL (exact URL where you found them)
- What they do (one sentence, for whom)
- Founder / team signal
- Geography or founder angle
- Most recent signal (launch, hire, grant, pilot, accelerator)
- Traction or proof (customer, revenue, partnership, LOI)
- Why a mainstream analyst would miss this
- Why this fund should care (specific thesis fit)
- Sector
- Source type (grant winner, demo day, LinkedIn post, conference exhibitor, etc.)

---

### Step 4: Apply the anti-mainstream filter

Before including a candidate in the final list, apply this test:

- Would a normal VC analyst find this in five minutes from obvious sources?
- Is the evidence only from mainstream startup media?
- Is the reason for non-obviousness real and specific?
- Is there a real recent signal?
- Is there a real founder or team signal?
- Does this fit the fund thesis?

Reject if any of these fail.

---

### Step 5: Reject known pipeline companies

Check against the known pipeline in the context pack. Exclude any company already listed there.

---

### Step 6: Return results

Return in this exact order:

**1. Sources checked**
List each source path searched with a brief note on what was found.

**2. Rejected candidates**
List companies considered but rejected, with a specific rejection reason for each.

**3. Final candidates in CSV format**
Use this exact schema (one row per candidate, include header):

```
company_name,website,source_url,short_description,founder_signal,geo_angle,recent_signal,traction_proof,why_non_obvious,why_fund_should_care,sector,source_type
```

Use `missing` for any field where evidence was not found. Do not leave fields blank.

**4. Short reasoning per candidate**
After the CSV, write 2-3 sentences per final candidate explaining why it passed the filter.

**5. Questions to verify before outreach**
For each final candidate, list 2-3 things to confirm before reaching out to the founder.

---

### Hard limits

- Do not include companies with no source URL.
- Do not include companies with no recent signal.
- Do not include companies with no founder or team evidence.
- Do not include companies already in the known pipeline.
- Do not invent facts. Mark missing evidence clearly.
- Fewer strong candidates beats many weak candidates.
