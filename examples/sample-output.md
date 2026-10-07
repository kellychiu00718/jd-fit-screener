# Sample output

Illustrative only. I wrote this by hand to show the format, using `examples/profile.md` and the three fictional postings in `examples/jds/`. It is not the output of a real run, and the numbers will differ from run to run.

## Shortlist

| Rank | Company | Title | Fit | Confidence | Gates | Why | Biggest gap |
|---|---|---|---|---|---|---|---|
| 1 | Example Retail Co. | Junior Data Analyst | 87 | High | Location pass, visa pass (sponsorship offered), language pass, experience pass | Weekly SQL reporting and Tableau dashboards match the profile's SQL work on about 100,000 orders and its published Tableau dashboard | No evidence of running an A/B test readout |

### Posting 1 in detail
- **Responsibilities (32/40).** Posting: "Write SQL queries to pull order and customer data for weekly reporting." Profile: "wrote PostgreSQL queries on a public e-commerce dataset of about 100,000 orders". Dashboards also match. A/B test readouts are adjacent at best.
- **Requirements (27/30).** SQL is required and covered. Python is a plus and covered.
- **Level (20/20).** "0 to 2 years" matches 0 years.
- **Context (8/10).** Retail and e-commerce connect to the profile's dataset.
- **Question for the employer:** which tools does the team use for A/B tests, and does the analyst design them or only read them out?

## Dropped

| Company | Title | Fit | Why dropped |
|---|---|---|---|
| Demo Marketplace Ltd. | Customer Insight Analyst | 89 | Gate failed: the posting requires fluent Korean and the profile says intermediate. The fit is high (reviews and delivery data match the profile's project), so it is worth a second look if the Korean requirement is flexible. Posted date: not stated. |
| Sample Cloud Inc. | Senior Data Engineer | 7 | Gate failed: 7+ years required. Negative keyword "senior". Spark, Airflow and Kafka are not in the profile. |

## Note on how to read this
The fit score and the gate result are separate. A posting with a failed gate keeps its fit score so you can see what you would be giving up. Priority order only matters when two postings have similar fit.
