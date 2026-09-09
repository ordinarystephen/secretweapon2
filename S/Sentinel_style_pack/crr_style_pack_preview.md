# CRR Style Pack: preview (all files in one place)

Illustrative skeleton. See README for conventions.

---


This folder is an example of the machine-readable form of the CRR language standards and house writing style. It is a skeleton: the structure and schemas are the proposal, the entries are illustrative and drawn from the leveraged lending workpaper decomposition, the seed terminology lexicon, and Steve's writing guidelines. Anything marked `status: pending_adjudication` is a placeholder for the team's decision.

## Files

| File | Owner | Changes | Consumed by |
|---|---|---|---|
| `manifest.yaml` | CRR analytics | every release | everything; the standards version rulings point to |
| `structure.yaml` | SME / RIC | rarely | prompt assembly per section; completeness view in UI |
| `terminology.yaml` | SME | often (grows) | prompt assembly; linter; ontology / knowledge graph |
| `assessment_language.yaml` | SME / team | after adjudication | prompt assembly; linter; right-rail "standard applied" |
| `evidence_conventions.yaml` | SME | rarely | prompt assembly; citation checker |
| `writing_rules.yaml` | CRR analytics | rarely | linter; guideline baseline report; Word guide |
| `lexicons.yaml` | anyone on the team | often | linter |
| `exemplars.yaml` | CRR analytics | each corpus run | few-shot grounding; Word guide examples |
| `schemas/*.json` | CRR analytics | with the pack | validation in tests |

## Conventions that apply to every entry

- `id`: stable, never reused. Prefix by file (TERM-, ASSESS-, EVID-, RULE-, LEX-, EX-).
- `scope`: which sections or grid topics the entry applies to. `all` when universal.
- `enforcement`: `must`, `should`, or `info`. Only `must` and `should` reach the linter.
- `status`: `adopted`, `pending_adjudication`, or `retired`.
- `provenance`: where the entry came from. `workbook_row` points at the adjudication workbook; `evidence` carries the corpus counts that supported the decision.
- Entries are declarative. Prose explanations belong in the Word guide, which is generated from the same workbook.
- No borrower, counterparty, or person names anywhere in the pack. Exemplars are pointers by unit id.

## How the pack is produced

Adjudication workbook (team decisions) + aggregate report (corpus evidence) -> generator -> this pack + the Word guide. The two outputs cannot drift because they share a source.

---

## manifest.yaml

```yaml
# CRR Style Pack manifest
# The standards_version is what a Sentinel ruling records alongside the question,
# positions, and evidence. Bump it on every change to any file in the pack.

pack: crr-house-style
standards_version: "0.1.0-draft"
effective_date: null            # set when adopted
owner: "Credit Risk Review, Analytics"
approved_by: null               # team / RIC sign-off record
derived_from:
  adjudication_workbook: "crr_style_adjudication_v0.xlsx"   # illustrative name
  aggregate_report_run: null    # run id of the corpus run the evidence came from
  corpus_papers: null           # count of papers in that run
applies_to:
  workpaper_types: [leveraged_lending_target_review]        # extend per decomposition
  review_types: [target, thematic]

files:
  - path: structure.yaml
    schema: schemas/structure.schema.json
  - path: terminology.yaml
    schema: schemas/terminology.schema.json
  - path: assessment_language.yaml
    schema: schemas/assessment_language.schema.json
  - path: evidence_conventions.yaml
    schema: schemas/evidence_conventions.schema.json
  - path: writing_rules.yaml
    schema: schemas/writing_rules.schema.json
  - path: lexicons.yaml
    schema: schemas/lexicons.schema.json
  - path: exemplars.yaml
    schema: schemas/exemplars.schema.json

consumers:
  prompt_assembly: [structure, terminology, assessment_language, evidence_conventions, writing_rules]
  linter: [writing_rules, lexicons, terminology, assessment_language]
  ui_standard_applied: [assessment_language, evidence_conventions, writing_rules]
  knowledge_graph: [terminology, structure]
  word_guide_generator: [all]

changelog:
  - version: "0.1.0-draft"
    date: "2026-09-08"
    note: "Skeleton with illustrative entries. No adjudicated content."
```

---

## structure.yaml

```yaml
# Workpaper structure: what each register and section is for, and what it must contain.
# Length and figure envelopes are filled from the aggregate report's composition metrics
# (median and interquartile range), not invented.

rating_scale:
  # Discovered from the corpus by the rating normalizer; confirm with the SME.
  values: [Satisfactory, Needs_Improvement, Unsatisfactory]   # illustrative
  aliases:
    Satisfactory: ["Sat", "Satisfactory."]
    Needs_Improvement: ["Needs Improvement", "NI"]
  status: pending_adjudication

grid:
  name: "Credit Analysis Topics"
  row_fields: [topic, rating, justification]
  justification_envelope:
    words: {median: null, p25: null, p75: null}   # from corpus run
  topics:
    - id: GRID-FIN
      label: "Financial Analysis"
      maps_to_section: SEC-FIN
    - id: GRID-UW
      label: "Underwriting & Documentation"
      maps_to_section: SEC-UW
    - id: GRID-PM
      label: "Portfolio Management"
      maps_to_section: SEC-PM
    - id: GRID-RR
      label: "Risk Rating"
      maps_to_section: SEC-RR
    - id: GRID-TRD
      label: "Trading Activity"
      maps_to_section: SEC-TRD
      applicability: "not applicable to leveraged loans"

sections:
  - id: SEC-BCO
    order: 1
    title: "Borrower / Counterparty & Relationship Overview"
    purpose: "Establish who the obligor is, the UBS relationship, and the transaction under review."
    subsections:
      - {heading: "Counterparty Overview", requirement: required}
      - {heading: "Recent Developments", requirement: required}
      - {heading: "External Credit Ratings & Outlook", requirement: required}
      - {heading: "Transaction Description", requirement: required}
      - {heading: "Capitalization", requirement: required}
    answers_questions:            # ids from the decomposition question inventory
      - Q-BCO-01   # obligor, country, industry, sub-segment, time in business
      - Q-BCO-02   # sponsor ownership and tenure
      - Q-BCO-03   # transaction types with UBS
      - Q-BCO-04   # leveraged loan identification per 5-G-006360 p.8
    expected_topics: [company_overview, sponsor, external_ratings, transaction_terms, pro_forma_capitalization, pro_forma_leverage]
    envelope:
      words: {median: null, p25: null, p75: null}
      figures: {median: null}
      tables: {median: null}
    conclusion_required: false

  - id: SEC-FIN
    order: 2
    title: "Financials"
    purpose: "Evaluate the credit team's financial analysis and CRR's view of it."
    subsections:
      - {heading: "CRR Assessment", requirement: required, position: first}
      - {heading: "Credit Team Financial Analysis", requirement: required}
      - {heading: "Model Assessments", requirement: conditional, condition: "projection update triggers under 5-G-006360 s8.4"}
      - {heading: "Financial Projections", requirement: required}
      - {heading: "EV / Total Debt Coverage", requirement: required}
    answers_questions: [Q-FIN-01, Q-FIN-02, Q-FIN-03, Q-FIN-04, Q-FIN-05]
    expected_topics: [revenue, ebitda, ebitda_adjustments, free_cash_flow, leverage, liquidity, projections, debt_repayment_capacity, enterprise_value]
    envelope:
      words: {median: null, p25: null, p75: null}
      figures: {median: null}
      tables: {median: null}
    conclusion_required: true
    conclusion_position: first     # bottom line on top

  - id: SEC-UW
    order: 3
    title: "Underwriting & Documentation"
    purpose: "Assess transaction structure, credit analysis, sources of repayment, standards, and approvals."
    subsections:
      - {heading: "CRR Assessment", requirement: required, position: first}
      - {heading: "Transaction Structure", requirement: required}
      - {heading: "Credit Analysis", requirement: required}
      - {heading: "Source of Repayment", requirement: required}
      - {heading: "Underwriting Standards", requirement: required}
      - {heading: "Credit Approval Authority", requirement: required}
    answers_questions: [Q-UW-01, Q-UW-02, Q-UW-03, Q-UW-04, Q-UW-05, Q-UW-06]
    expected_topics: [lmt_protection, psor, ssor, covenants, underwriting_exceptions, approval_authority]
    envelope: {words: {median: null, p25: null, p75: null}, figures: {median: null}, tables: {median: null}}
    conclusion_required: true
    conclusion_position: first

  - id: SEC-PM
    order: 4
    title: "Portfolio Management"
    purpose: "Assess post-origination monitoring, covenant compliance, and watchlist treatment."
    subsections:
      - {heading: "CRR Assessment", requirement: required, position: first}
      - {heading: "Post-Origination Monitoring", requirement: required}
      - {heading: "Covenant Compliance", requirement: required}
      - {heading: "Credit Watchlist", requirement: required}
    answers_questions: [Q-PM-01, Q-PM-02, Q-PM-03, Q-PM-04]
    expected_topics: [review_timeliness, covenant_compliance, watchlist_status]
    envelope: {words: {median: null, p25: null, p75: null}, figures: {median: null}, tables: {median: null}}
    conclusion_required: true
    conclusion_position: first

  - id: SEC-RR
    order: 5
    title: "Risk Rating Accuracy"
    purpose: "Assess regulatory classification, triggers, PD, and LGD."
    subsections:
      - {heading: "CRR Assessment", requirement: required, position: first}
      - {heading: "Regulatory Risk Rating Classification", requirement: required}
      - {heading: "Risk Rating Triggers", requirement: required}
      - {heading: "PD Rating", requirement: required}
      - {heading: "LGD Rating", requirement: required}
    answers_questions: [Q-RR-01, Q-RR-02, Q-RR-03, Q-RR-04, Q-RR-05]
    expected_topics: [regulatory_classification, rating_triggers, pd_rating, lgd_rating, override_justification]
    envelope: {words: {median: null, p25: null, p75: null}, figures: {median: null}, tables: {median: null}}
    conclusion_required: true
    conclusion_position: first

  - id: SEC-TRD
    order: 6
    title: "Trading Activity and Exposure Analysis"
    purpose: "Counterparty credit risk exposure analysis; not applicable to leveraged loans."
    applicability: {workpaper_types: [counterparty_credit_risk]}
    subsections: []
    answers_questions: []
    expected_topics: []
    envelope: {words: {median: null, p25: null, p75: null}, figures: {median: null}, tables: {median: null}}
    conclusion_required: true
```

---

## terminology.yaml

```yaml
# Terminology: one entry per concept. This file is also the seed of the ontology.
# variant.status: preferred | acceptable | avoid | pending_adjudication
# acronym_rule: expand_on_first_use | never_expand | always_expand

defaults:
  acronym_rule: expand_on_first_use
  first_use_format: "{expansion} ({acronym})"

concepts:
  - id: TERM-001
    canonical: "primary source of repayment"
    kind: term
    acronym: PSOR
    variants:
      - {text: "primary source of repayment", status: preferred}
      - {text: "PSOR", status: acceptable, note: "after first-use expansion"}
      - {text: "primary repayment source", status: pending_adjudication}
    definition: "The cash flow or asset the credit team identifies as the expected source of debt service."
    source: {document: "5-G-006360", section: null}
    relations:
      broader: [TERM-REPAYMENT]
      related: [TERM-002]
      used_in: [SEC-UW]
    scope: all
    status: adopted
    provenance:
      workbook_row: null
      evidence: {n_papers: null, n_occurrences: null, sections: [SEC-UW]}

  - id: TERM-002
    canonical: "secondary source of repayment"
    kind: term
    acronym: SSOR
    variants:
      - {text: "secondary source of repayment", status: preferred}
      - {text: "SSOR", status: acceptable}
    definition: "The fallback source of repayment if the primary source fails, typically collateral or refinancing."
    source: {document: "5-G-006360", section: null}
    relations: {broader: [TERM-REPAYMENT], related: [TERM-001], used_in: [SEC-UW]}
    scope: all
    status: adopted
    provenance: {workbook_row: null, evidence: {n_papers: null, n_occurrences: null}}

  - id: TERM-003
    canonical: "credit watchlist"
    kind: term
    acronym: CWL
    variants:
      - {text: "credit watchlist", status: preferred}
      - {text: "CWL", status: acceptable}
      - {text: "watchlist", status: acceptable, note: "only after the full term has appeared"}
      - {text: "watch list", status: avoid}
    definition: "The list of obligors under heightened monitoring per Global CWL Criteria."
    source: {document: "1-G-012756", section: "4.2"}
    relations: {used_in: [SEC-PM], governed_by: ["1-G-012756"]}
    scope: all
    status: adopted
    provenance: {workbook_row: null, evidence: {n_papers: null, n_occurrences: null}}

  - id: TERM-004
    canonical: "Commercial Committee memo"
    kind: document
    acronym: "ComCo Memo"
    variants:
      - {text: "ComCo Memo", status: preferred, note: "house convention; the expansion is rarely written"}
      - {text: "Commercial Committee memo", status: acceptable}
      - {text: "committee memo", status: avoid}
    definition: "The credit approval memorandum presented to the Commercial Committee."
    source: {document: "5-P-000247", section: null}
    relations: {kind_of: [TERM-APPROVAL-DOC], used_in: [SEC-BCO, SEC-UW]}
    acronym_rule: never_expand
    scope: all
    status: pending_adjudication
    provenance: {workbook_row: null, evidence: {n_papers: null, n_occurrences: null}}

  - id: TERM-005
    canonical: "UBS Adjusted EBITDA"
    kind: metric
    variants:
      - {text: "UBS Adjusted EBITDA", status: preferred}
      - {text: "adjusted EBITDA", status: acceptable, note: "when the UBS basis is already established"}
      - {text: "EBITDA adjustments", status: acceptable, note: "refers to the adjustments, not the metric"}
    definition: "EBITDA after the credit team's adjustments for non-cash and non-recurring items."
    source: {document: "5-G-006360", section: "8.4"}
    relations:
      narrower_of: [TERM-EBITDA]
      related: [TERM-006, TERM-007]
      used_in: [SEC-FIN]
    scope: [SEC-FIN, GRID-FIN]
    status: adopted
    provenance: {workbook_row: null, evidence: {n_papers: null, n_occurrences: null}}

  - id: TERM-006
    canonical: "UBS Expected Case"
    kind: scenario
    variants:
      - {text: "UBS Expected Case", status: preferred}
      - {text: "Expected Case", status: acceptable}
      - {text: "base case", status: avoid, note: "ambiguous with management case"}
    definition: "The credit team's central projection scenario."
    source: {document: "5-G-006360", section: null}
    relations: {sibling: [TERM-007], used_in: [SEC-FIN]}
    scope: all
    status: adopted
    provenance: {workbook_row: null, evidence: {n_papers: null, n_occurrences: null}}

  - id: TERM-007
    canonical: "UBS Downside Case"
    kind: scenario
    variants:
      - {text: "UBS Downside Case", status: preferred}
      - {text: "Downside Case", status: acceptable}
      - {text: "stress case", status: avoid}
    definition: "The credit team's adverse projection scenario."
    source: {document: "5-G-006360", section: null}
    relations: {sibling: [TERM-006], used_in: [SEC-FIN]}
    scope: all
    status: adopted
    provenance: {workbook_row: null, evidence: {n_papers: null, n_occurrences: null}}

  - id: TERM-008
    canonical: "workpaper"
    kind: colloquialism
    variants:
      - {text: "workpaper", status: preferred}
      - {text: "work paper", status: avoid}
      - {text: "linecard", status: avoid, note: "colloquial; understood but not written"}
    definition: "The CRR review work product for a single obligor or counterparty."
    source: {document: "1-G-007544", section: null}
    relations: {has_parts: [SEC-BCO, SEC-FIN, SEC-UW, SEC-PM, SEC-RR, SEC-TRD]}
    scope: all
    status: adopted
    provenance: {workbook_row: null, evidence: {n_papers: null, n_occurrences: null}}

  - id: TERM-009
    canonical: "review"
    kind: term
    senses:                     # same word, different meaning by context
      - {sense: "CRR review", context: "CRR as actor; the engagement this workpaper belongs to", preferred_text: "CRR review"}
      - {sense: "credit team periodic review", context: "the credit team's Annual or Quarterly Review of the obligor", preferred_text: "Annual Review | Quarterly Review"}
    variants:
      - {text: "the review", status: avoid, note: "ambiguous between senses; name which"}
    scope: all
    status: pending_adjudication
    provenance: {workbook_row: null, evidence: {n_papers: null, n_occurrences: null}}

# Candidate intake: entries promoted from terminology_candidates.csv land here with status
# pending_adjudication and kind set by the reviewer.
```

---

## assessment_language.yaml

```yaml
# Assessment language: how CRR states what it concludes.
# Part 1: one entry per assessment act (the "concept" tag from the extraction).
# Part 2: how language shifts by rating.
# construction.status: preferred | acceptable | avoid | pending_adjudication

conventions:
  actor: "CRR"                         # CRR is the grammatical subject of assessments
  actor_forms:
    preferred: "CRR"
    avoid: ["we", "the reviewer", "the review team", "it is assessed that"]
  tense: present                       # assessments in present tense; events in past
  person: third

assessment_acts:
  - id: ASSESS-CONCUR
    act: concur
    meaning: "CRR agrees with the credit team's analysis or conclusion."
    constructions:
      - {text: "CRR concurs with {object}", status: preferred, verb_lemma: concur}
      - {text: "CRR agrees with {object}", status: pending_adjudication, verb_lemma: agree}
      - {text: "CRR is in agreement with {object}", status: avoid, verb_lemma: agree, reason: "wordier form of the same act"}
      - {text: "CRR does not disagree with {object}", status: avoid, reason: "double negative"}
    object_examples: ["the credit team's EBITDA adjustments", "the assigned regulatory classification"]
    scope: all
    enforcement: should
    status: pending_adjudication
    provenance:
      workbook_row: null
      evidence: {variants_observed: null, authors_split: null}

  - id: ASSESS-NOTE
    act: note_observation
    meaning: "CRR records a fact or observation without asserting a deficiency."
    constructions:
      - {text: "CRR notes that {clause}", status: preferred, verb_lemma: note}
      - {text: "CRR observes that {clause}", status: pending_adjudication, verb_lemma: observe}
      - {text: "It is noted that {clause}", status: avoid, reason: "passive, no actor"}
    scope: all
    enforcement: should
    status: pending_adjudication
    provenance: {workbook_row: null, evidence: {variants_observed: null, authors_split: null}}

  - id: ASSESS-ADEQUATE
    act: assess_adequate
    meaning: "CRR judges an element sufficient, supported, or appropriate."
    constructions:
      - {text: "CRR assesses {object} as {adequate|appropriate|sufficiently supported}", status: preferred, verb_lemma: assess}
      - {text: "CRR considers {object} to be {adjective}", status: acceptable, verb_lemma: consider}
      - {text: "{object} appears {adjective}", status: avoid, reason: "hedged where a judgment is required"}
    scope: all
    enforcement: should
    status: pending_adjudication
    provenance: {workbook_row: null, evidence: {variants_observed: null, authors_split: null}}

  - id: ASSESS-FLAG
    act: flag_issue
    meaning: "CRR identifies a deficiency, gap, or exception."
    constructions:
      - {text: "CRR identified {issue}", status: preferred, verb_lemma: identify}
      - {text: "CRR notes a gap in {object}", status: acceptable, verb_lemma: note}
      - {text: "{object} may indicate {issue}", status: avoid, reason: "an identified issue is stated, not hedged"}
    required_elements: [what_was_expected, what_was_found, policy_reference_if_any]
    scope: all
    enforcement: must
    status: pending_adjudication
    provenance: {workbook_row: null, evidence: {variants_observed: null, authors_split: null}}

  - id: ASSESS-LIMIT
    act: limitation_or_preclusion
    meaning: "CRR states that an assessment could not be made and why."
    constructions:
      - {text: "CRR's assessment of {object} is precluded by {reason}", status: preferred, verb_lemma: preclude}
      - {text: "CRR was unable to assess {object} because {reason}", status: acceptable}
      - {text: "{object} could not be reviewed", status: avoid, reason: "no actor, no reason"}
    required_elements: [what_could_not_be_assessed, reason, what_would_resolve_it]
    scope: all
    enforcement: must
    status: pending_adjudication
    provenance: {workbook_row: null, evidence: {variants_observed: null, authors_split: null}}

  - id: ASSESS-ATTRIB
    act: attribute_to_source
    meaning: "CRR reports a position held by the credit team or a document, not its own."
    constructions:
      - {text: "The credit team {states|projects|expects} {clause}", status: preferred}
      - {text: "Per the {document}, {clause}", status: acceptable}
      - {text: "It is expected that {clause}", status: avoid, reason: "whose expectation is unclear"}
    scope: all
    enforcement: should
    status: pending_adjudication
    provenance: {workbook_row: null, evidence: {variants_observed: null, authors_split: null}}

hedging:
  allowed:
    - {text: "appears to", when: "reporting an inference from incomplete evidence, never in a conclusion sentence"}
    - {text: "may", when: "stating a forward-looking risk"}
  avoid:
    - {text: "seems", reason: "guideline: no hedging in conclusions"}
    - {text: "tends to", reason: "vague"}
    - {text: "probably", reason: "quantify or drop"}
  rule: "A conclusion sentence (the first sentence under CRR Assessment, and every grid justification) carries no hedge."
  enforcement: should
  status: pending_adjudication

rating_language:
  # How the register shifts by grid rating. Filled from the rating-conditioned language report.
  - rating: Satisfactory
    expected_acts: [concur, assess_adequate, note_observation]
    justification_shape: "One to two sentences: the conclusion, then the principal support."
    issue_introduction: null
    hedge_density: {max_per_100_words: null}   # from corpus baseline
    example_pattern: "CRR concurs with {object}; {support}."
    status: pending_adjudication
  - rating: Needs_Improvement
    expected_acts: [flag_issue, assess_adequate, concur]
    justification_shape: "Conclusion first, then the identified gap with what was expected versus found, then any mitigant."
    issue_introduction: {preferred: "CRR identified {issue}", position: first_or_second_sentence}
    hedge_density: {max_per_100_words: null}
    example_pattern: "CRR identified {issue}. {expected} {found}. {mitigant_if_any}."
    status: pending_adjudication
  - rating: Unsatisfactory
    expected_acts: [flag_issue]
    justification_shape: "Conclusion first, each deficiency enumerated (i), (ii), (iii), policy reference for each."
    issue_introduction: {preferred: "CRR identified {issue}", position: first_sentence}
    hedge_density: {max_per_100_words: 0}
    example_pattern: "CRR identified (i) {issue}; (ii) {issue}; (iii) {issue}."
    status: pending_adjudication
```

---

## evidence_conventions.yaml

```yaml
# Evidence conventions: how claims are tied to sources.
# One entry per source type (the enum from the extraction config).

defaults:
  date_required: true
  date_format: "{Mon}-{YY} | {n}Q{YY} | FY{YY}"      # e.g. Jun-26, 2Q26, FY25
  position: sentence_open                              # "Per the 2Q26 Quarterly Review, ..." preferred
  figure_pointer: "see Figure {n}"
  table_pointer: "see Table {n}"
  pointer_adjacency: must                               # a pointer sits in the paragraph before or after its figure

source_types:
  - id: EVID-ANNUAL
    source_type: annual_review
    label_form: "{FY} Annual Review"
    date_required: true
    citation_examples: ["Per the FY25 Annual Review, ..."]
    scope: all
    enforcement: should
    status: pending_adjudication
    provenance: {workbook_row: null, evidence: {n_statements: null, dated_share: null}}

  - id: EVID-QUARTERLY
    source_type: quarterly_review
    label_form: "{n}Q{YY} Quarterly Review"
    date_required: true
    citation_examples: ["The 2Q26 Quarterly Review reports ..."]
    scope: all
    enforcement: should
    status: pending_adjudication
    provenance: {workbook_row: null, evidence: {n_statements: null, dated_share: null}}

  - id: EVID-COMCO
    source_type: comco_memo
    label_form: "ComCo Memo dated {date}"
    date_required: true
    citation_examples: ["The ComCo Memo dated Mar-26 identifies ..."]
    scope: [SEC-BCO, SEC-UW]
    enforcement: should
    status: pending_adjudication
    provenance: {workbook_row: null, evidence: {n_statements: null, dated_share: null}}

  - id: EVID-AGENCY
    source_type: rating_agency
    label_form: "{Moody's|S&P} ({rating}, {outlook}, {date assigned})"
    date_required: true
    citation_examples: ["Moody's (B2, stable, assigned Jan-26)"]
    scope: [SEC-BCO, SEC-RR]
    enforcement: must
    status: pending_adjudication
    provenance: {workbook_row: null, evidence: {n_statements: null, dated_share: null}}

  - id: EVID-COVENANT
    source_type: covenant_compliance_certificate
    label_form: "{period} compliance certificate"
    date_required: true
    citation_examples: ["Per the 2Q26 compliance certificate, ..."]
    scope: [SEC-PM]
    enforcement: should
    status: pending_adjudication
    provenance: {workbook_row: null, evidence: {n_statements: null, dated_share: null}}

  - id: EVID-POLICY
    source_type: internal_policy
    label_form: "{doc id} s{section}"
    date_required: false
    citation_examples: ["per 5-G-006360 s8.4", "Annex F of 5-P-000247"]
    scope: all
    enforcement: must
    note: "Every flagged issue that rests on a policy requirement cites the policy id and section."
    status: pending_adjudication
    provenance: {workbook_row: null, evidence: {n_statements: null, dated_share: null}}

  - id: EVID-IRIS
    source_type: iris_document
    label_form: "{document name} (IRIS, {date})"
    date_required: true
    citation_examples: ["the executed credit agreement (IRIS, Mar-26)"]
    scope: all
    enforcement: should
    status: pending_adjudication
    provenance: {workbook_row: null, evidence: {n_statements: null, dated_share: null}}

rules:
  - id: EVID-R01
    statement: "A quantitative claim names its source in the same sentence or the one before."
    enforcement: must
    scope: all
  - id: EVID-R02
    statement: "A figure or table is referenced in prose before it appears; no orphan figures."
    enforcement: should
    scope: all
  - id: EVID-R03
    statement: "Sources are named as the credit team names them, not paraphrased."
    enforcement: should
    scope: all
```

---

## writing_rules.yaml

```yaml
# Writing rules: the prescriptive standard. Each rule is measurable or not; measurable
# rules carry the metric and a threshold. Thresholds marked null are set after the
# guideline baseline shows where current papers sit.
# enforcement: must | should | info

rules:
  - id: RULE-W01
    title: "Bottom line on top"
    statement: "The conclusion is the first sentence of a CRR Assessment subsection and of every grid justification."
    enforcement: must
    scope: [SEC-FIN, SEC-UW, SEC-PM, SEC-RR, SEC-TRD, grid]
    measurable: true
    metric: conclusion_position
    check: "first sentence of the unit contains an assessment act (see assessment_language)"
    threshold: {operator: eq, value: 1}
    status: adopted

  - id: RULE-W02
    title: "Main point first in every paragraph"
    statement: "The first sentence of a paragraph states its point; the rest develops it."
    enforcement: should
    scope: all
    measurable: true
    metric: paragraph_lead_ratio
    check: "share of paragraphs whose first sentence is shorter than the paragraph mean"
    threshold: {operator: gte, value: null}   # set from baseline
    status: adopted

  - id: RULE-W03
    title: "Active voice"
    statement: "Assessments and findings are written in active voice with a named actor."
    enforcement: should
    scope: all
    measurable: true
    metric: passive_rate
    threshold: {operator: lte, value: null}   # set from baseline; expected well under 0.20
    exemptions: ["descriptions of events where the actor is unknown or irrelevant"]
    status: adopted

  - id: RULE-W04
    title: "One idea per sentence"
    statement: "A sentence introduces one idea."
    enforcement: should
    scope: all
    measurable: true
    metric: clauses_per_sentence_mean
    threshold: {operator: lte, value: null}
    secondary_metric: {metric: words_per_sentence_p90, threshold: {operator: lte, value: null}}
    status: adopted

  - id: RULE-W05
    title: "Acronyms expanded on first use"
    statement: "An acronym is expanded the first time it appears in the workpaper body, unless terminology.yaml sets never_expand."
    enforcement: must
    scope: all
    measurable: true
    metric: acronym_first_use_defined
    threshold: {operator: eq, value: 1.0}
    status: adopted

  - id: RULE-W06
    title: "No vague quantifiers"
    statement: "Vague terms (see lexicons.vague_terms) are replaced with a number, a range, or a comparison."
    enforcement: should
    scope: all
    measurable: true
    metric: vague_term_hits_per_100_words
    threshold: {operator: lte, value: null}
    status: adopted

  - id: RULE-W07
    title: "Quantify where possible"
    statement: "A claim about size, change, or headroom carries a figure."
    enforcement: should
    scope: [SEC-FIN, SEC-PM, SEC-RR]
    measurable: true
    metric: numeric_density
    threshold: {operator: gte, value: null}
    status: adopted

  - id: RULE-W08
    title: "Short words"
    statement: "Prefer the short word: use, not utilize; start, not commence; about, not approximately."
    enforcement: info
    scope: all
    measurable: true
    metric: long_word_substitutions
    check: "hits against lexicons.short_word_substitutions"
    status: adopted

  - id: RULE-W09
    title: "No hedging in conclusions"
    statement: "A conclusion sentence carries no hedge (see assessment_language.hedging)."
    enforcement: should
    scope: all
    measurable: true
    metric: hedges_in_conclusion_sentences
    threshold: {operator: eq, value: 0}
    status: adopted

  - id: RULE-W10
    title: "Free from inconsistencies"
    statement: "A grid justification's claims are supported by the matching section; figures repeated across sections agree."
    enforcement: must
    scope: [grid]
    measurable: true
    metric: grid_section_support_rate
    threshold: {operator: gte, value: null}   # baseline from consistency report
    status: adopted

  - id: RULE-W11
    title: "Numbers: sensible order, close comparisons, rounded"
    statement: "Present figures in a consistent order (current then prior), keep the compared figures in the same sentence, and round to the precision the reader needs."
    enforcement: should
    scope: all
    measurable: false
    status: adopted

  - id: RULE-W12
    title: "Skim friendly"
    statement: "Subsection headings follow structure.yaml; enumerations use (i), (ii), (iii); labeled lead-ins such as '2Q26 Financials:' are used for period blocks."
    enforcement: should
    scope: all
    measurable: false
    status: adopted

  - id: RULE-W13
    title: "Clear voice"
    statement: "CRR is the actor; no 'we', no impersonal 'it is assessed'."
    enforcement: should
    scope: all
    measurable: true
    metric: actor_form_violations
    check: "hits against assessment_language.conventions.actor_forms.avoid"
    threshold: {operator: eq, value: 0}
    status: adopted

  - id: RULE-W14
    title: "No flowery language"
    statement: "No intensifiers or ornamental adjectives (see lexicons.ornamental)."
    enforcement: should
    scope: all
    measurable: true
    metric: ornamental_hits
    threshold: {operator: eq, value: 0}
    status: adopted
```

---

## lexicons.yaml

```yaml
# Lexicons: small word lists the linter consults. Edited freely by the team; no ids needed
# beyond the list name. Keep entries lowercase; matching is case-insensitive, word-boundary.

vague_terms:
  # RULE-W06. "material" is excluded because "material risk" is a term of art.
  - significant
  - considerable
  - appreciable
  - substantial
  - meaningful
  - notable
  - somewhat
  - relatively
  - fairly
  - adequate           # pending_adjudication: used as a term in "adequate coverage"?
  - a number of
  - various

ornamental:
  # RULE-W14
  - very
  - extremely
  - highly
  - robust
  - strong momentum
  - impressive
  - remarkable
  - solid

hedges_avoid:
  # mirrors assessment_language.hedging.avoid; kept here for the linter
  - seems
  - seem to
  - tends to
  - probably
  - perhaps
  - arguably

short_word_substitutions:
  # RULE-W08. left: avoid, right: use
  utilize: use
  utilization: use
  commence: start
  approximately: about
  in order to: to
  prior to: before
  subsequent to: after
  in the event that: if
  with respect to: on
  demonstrate: show
  facilitate: help
  in excess of: over

actor_forms_avoid:
  # RULE-W13; mirrors assessment_language.conventions.actor_forms.avoid
  - we
  - our
  - the reviewer
  - the review team
  - it is assessed that
  - it is noted that
  - it was observed that

banned_phrases:
  # things the team decides never appear; empty until adjudicated
  []
```

---

## exemplars.yaml

```yaml
# Exemplars: pointers to representative units, chosen by the deterministic
# representativeness score in the corpus run. No text is stored here; the consumer
# resolves unit ids against the sanitized exemplar store. "Representative" is the only
# label used.

source_run: null            # aggregate run id
selection_method: "representativeness score v1 (composition distance, top-k topic coverage, canonical constructions)"

by_section:
  - section: SEC-FIN
    review_type: target
    candidates:
      - {unit_id: "REF-XXXX:section:financials", rank: 1, score: null, reasons: [composition_within_iqr, top_topics_8_of_8, canonical_constructions_high]}
      - {unit_id: "REF-YYYY:section:financials", rank: 2, score: null, reasons: []}
      - {unit_id: "REF-ZZZZ:section:financials", rank: 3, score: null, reasons: []}
    sme_review: {status: pending, approved_unit_id: null, note: null}

  - section: SEC-UW
    review_type: target
    candidates: []
    sme_review: {status: pending, approved_unit_id: null, note: null}

by_grid_topic_and_rating:
  # one representative justification per topic per rating, for the rating_language chapter
  - {grid_topic: GRID-FIN, rating: Satisfactory, unit_id: null, sme_review: {status: pending}}
  - {grid_topic: GRID-FIN, rating: Needs_Improvement, unit_id: null, sme_review: {status: pending}}

by_paper:
  - {review_type: target, unit_id: "REF-XXXX", rank: 1, score: null, sme_review: {status: pending}}
```

---

## schemas/writing_rules.schema.json

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "crr-style-pack/writing_rules",
  "title": "CRR Style Pack: writing rules",
  "type": "object",
  "required": ["rules"],
  "properties": {
    "rules": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "title", "statement", "enforcement", "scope", "measurable", "status"],
        "additionalProperties": false,
        "properties": {
          "id": {"type": "string", "pattern": "^RULE-W[0-9]{2,3}$"},
          "title": {"type": "string", "maxLength": 80},
          "statement": {"type": "string"},
          "enforcement": {"enum": ["must", "should", "info"]},
          "scope": {
            "oneOf": [
              {"const": "all"},
              {"type": "array", "items": {"type": "string", "pattern": "^(SEC-[A-Z]+|GRID-[A-Z]+|grid|all)$"}, "minItems": 1}
            ]
          },
          "measurable": {"type": "boolean"},
          "metric": {"type": "string"},
          "check": {"type": "string"},
          "threshold": {
            "type": "object",
            "required": ["operator", "value"],
            "properties": {
              "operator": {"enum": ["eq", "lte", "gte", "lt", "gt"]},
              "value": {"type": ["number", "null"]}
            }
          },
          "secondary_metric": {"type": "object"},
          "exemptions": {"type": "array", "items": {"type": "string"}},
          "status": {"enum": ["adopted", "pending_adjudication", "retired"]},
          "provenance": {
            "type": "object",
            "properties": {
              "workbook_row": {"type": ["string", "integer", "null"]},
              "evidence": {"type": "object"}
            }
          }
        },
        "if": {"properties": {"measurable": {"const": true}}},
        "then": {"required": ["metric"]}
      }
    }
  }
}
```

