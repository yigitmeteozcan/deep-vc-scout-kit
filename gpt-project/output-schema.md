# Output Schema

This defines the exact CSV format GPT must return and local scripts expect.

---

## CSV Columns

| Column | Type | Description |
|---|---|---|
| `company_name` | string | Company's legal or operating name |
| `website` | string | Company website URL |
| `source_url` | string | Exact URL where the company was found |
| `short_description` | string | One sentence: what they do, for whom, and what outcome |
| `founder_signal` | string | Founder name, background, LinkedIn URL, or specific team evidence |
| `geo_angle` | string | Geography or diaspora connection relevant to the fund |
| `recent_signal` | string | Most recent activity with approximate date |
| `traction_proof` | string | Customer, revenue, partnership, LOI, grant, or accelerator acceptance |
| `why_non_obvious` | string | Specific reason a mainstream analyst would miss this company |
| `why_fund_should_care` | string | Specific fit with the fund thesis — not generic |
| `sector` | string | Sector label (e.g., industrial SaaS, logistics software, energy tech) |
| `source_type` | string | Type of source (e.g., grant winner, demo day PDF, LinkedIn post, conference exhibitor) |

---

## Column Explanations

### company_name
The name the company uses publicly. If the legal name differs from the operating name, use the operating name and note the legal name in `short_description` if relevant.

### website
The company's primary website URL. If no website exists, write `missing`. Do not use LinkedIn or Crunchbase as the website.

### source_url
**This is the most important field.**

Write the exact URL where you found the company — the grant page, the conference exhibitor list, the LinkedIn post, the university spinout page, the demo day PDF.

This is not the company website. This is the source path that revealed the company.

If no specific URL exists, write `missing`. A candidate with `missing` in this field will fail the anti-mainstream filter.

### short_description
One sentence maximum. Include:
- What the company does (specific, not vague)
- For whom (buyer or user type)
- What outcome or problem it solves

Bad: "AI platform for enterprise automation"
Good: "Fleet maintenance scheduling software for mid-market logistics operators in the Baltics, replacing spreadsheet workflows"

### founder_signal
Write:
- Founder name (if findable)
- Relevant background (domain expertise, previous company, research background)
- LinkedIn URL (if available)
- Any specific signal: serial founder, PhD in relevant field, former operator at target customer type

If no founder evidence is findable, write `missing`.

### geo_angle
Write the geographic or diaspora angle relevant to the fund:
- Country of incorporation
- Country of operations
- Founder nationality or origin if relevant
- Market focus

Example: "Estonian company targeting Nordic and Baltic industrial clients" or "Turkish-Finnish founder team building for European logistics operators"

### recent_signal
Write the most recent activity you found with an approximate date:
- Product launch date
- Grant announcement date
- Accelerator acceptance announcement
- New hire or key role posting date
- Partnership announcement
- Conference presentation date

Example: "Accepted into EIT Manufacturing accelerator, March 2024" or "Posted 3 engineering roles on LinkedIn, April 2024"

If no recent signal is findable in the last 24 months, write `missing`. A candidate with `missing` here should be rejected.

### traction_proof
Write specific proof of commercial or operational progress:
- Paying customers (number or names if public)
- Revenue indication (ARR range if mentioned)
- LOI or signed pilot agreement
- Strategic partnership with named company
- Grant amount and funder
- Accelerator acceptance (prestigious = stronger signal)

If no traction evidence is findable, write `missing`. Note: strong team signal can partially compensate for missing traction, but both missing is a reject.

### why_non_obvious
Write the specific reason a mainstream analyst running a standard search would miss this company:
- Found only on a grant database, not in startup media
- Stealth mode with no press
- Operating in local language only
- Embedded in an industry vertical conference, not startup events
- University spinout not yet incorporated as a separate company
- Diaspora founder with network outside mainstream VC radar

"It is a small company" is not a valid answer.
"Not well known" is not a valid answer.
The reason must be specific.

### why_fund_should_care
Write the specific thesis fit for this particular fund:
- Sector match (specific, not generic)
- Stage match
- Geography match
- Value-add match (how can the fund specifically help this company)
- Portfolio synergy (if applicable)

"Interesting company" is not a valid answer.
Generic sector alignment is not a valid answer.
Connect it directly to what the fund thesis says.

### sector
A short sector label. Use consistent terms across candidates:
- industrial SaaS
- logistics software
- energy tech
- manufacturing automation
- supply chain visibility
- robotics
- climate infrastructure
- health tech
- fintech
- etc.

### source_type
A short label for the type of source path used to find the company:
- grant winner
- EU project partner
- demo day
- university spinout
- conference exhibitor
- LinkedIn founder post
- hiring post
- accelerator finalist
- corporate innovation challenge
- niche newsletter
- industry association

---

## Strict Output Rules

1. **CSV must include a header row** as the first line.
2. **One row per candidate.** Do not merge rows.
3. **Do not use a markdown table** when the user asks for CSV output.
4. **Do not invent facts.** If a field's evidence was not found, write `missing`.
5. **Do not leave fields blank.** Every field must have a value or `missing`.
6. **Wrap values in double quotes** if the value contains a comma.
7. **Do not add extra columns** beyond the schema.
8. **Do not add line breaks inside fields.** Keep each row on a single line.

---

## Example Row (Fake)

```
company_name,website,source_url,short_description,founder_signal,geo_angle,recent_signal,traction_proof,why_non_obvious,why_fund_should_care,sector,source_type
VoltGrid OY,https://voltgrid.example.com,https://eit.example.com/energy-program-2024/cohort,Grid balancing software for industrial energy buyers in Scandinavia reducing peak load costs by 15-30%,"Mikael Virtanen, former grid engineer at Fingrid (LinkedIn: linkedin.com/in/example)",Finnish company targeting Nordic industrial energy buyers,Accepted into EIT InnoEnergy accelerator Q1 2024,"2 paid pilots with Finnish manufacturing clients, EUR 180k grant from Business Finland",Found only on EIT InnoEnergy cohort page — not in Finnish startup media or Crunchbase,Strong thesis fit: industrial energy operations software with Scandinavian buyer pull matches fund sector and geography focus,energy tech,EU program participant
```

---

## Rejected Candidates Format

After the CSV, include this section:

```
REJECTED CANDIDATES

Company: [name]
Source: [where found]
Reason: [specific rejection reason]
```

Do not omit this section. Every company researched and not included must appear here.
