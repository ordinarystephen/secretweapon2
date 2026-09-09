# CRR Style Pack v1 (directional): preview

---

## COVER_NOTE.md


**What this is.** A directional representation of the content CRR's use-case configuration will need to carry for workpaper drafting and checking: structure, terminology, assessment language, evidence conventions, writing rules, and word lists. It shows what the standards contain and how they group. It is not a format specification. Express it however Use-case Configuration expects packs to be expressed; the grouping and the ids are the part worth preserving.

**What it is not.** Not adopted standards. Entries marked `pending_adjudication` are placeholders for decisions the CRR team makes after the full-corpus analysis. Not a linter design. Where a rule is measurable, the metric name is given so the two sides can agree on vocabulary, but thresholds are empty and the checking mechanism is yours to decide.

**Where the content comes from.** Two sources. The historical workpaper corpus, analyzed by CRR's extraction tool, gives the evidence: which constructions, terms, and structures are actually in use, and how they vary by author and rating. The CRR team then decides what becomes canonical, acceptable, or avoided. The pack is the output of that decision, and it will be regenerated from the same decision record each time it changes.

**What matters first.** Three files carry most of the value and should be the first conversation: `terminology.yaml`, `assessment_language.yaml`, and `writing_rules.yaml` with its `lexicons.yaml`. `structure.yaml` and `evidence_conventions.yaml` are stable and low-risk. Derived data (typical section lengths, representative examples) is deliberately outside the versioned pack; a sample sits in `derived/` to show the shape.

**Questions for the platform side.**

1. How does Use-case Configuration expect a pack like this to be expressed and loaded, and who owns the loading step?
2. When a reviewer's ruling records a standards version, what does it resolve to, and is the manifest here a workable target?
3. Is prompt assembly per section a platform service or a use-case responsibility? The answer changes which files need machine-tight patterns and which can stay human-readable.
4. What happens when a pack fails validation: refuse to load, load with warnings, or fall back to the prior version?
5. Where do word lists that the business edits often (vague terms, substitutions) live so that changes don't require a release?

**Contact.** Stephen Costello, Credit Risk Review.

---

## README.md


A directional representation of CRR's language standards and house writing style in a form that could be loaded as configuration. Read `COVER_NOTE.md` first.

## Files

| File | Edited by | Cadence | What it holds |
|---|---|---|---|
| `manifest.yaml` | CRR analytics | each release | version, what the pack was derived from, file list |
| `structure.yaml` | SME / RIC | rarely | sections, subsections, review questions each section answers, grid topics, rating scale |
| `terminology.yaml` | SME | grows over time | one entry per concept: canonical term, variants with status, definition, source |
| `assessment_language.yaml` | CRR team | after adjudication | how CRR states each kind of assessment; hedging; how language shifts by rating |
| `evidence_conventions.yaml` | SME | rarely | how each source type is cited |
| `writing_rules.yaml` | CRR analytics | rarely | the prescriptive writing standard, one rule per entry |
| `lexicons.yaml` | anyone on the team | often | word lists the rules refer to |
| `schemas/` | CRR analytics | with the pack | one JSON schema as the pattern; the rest follow it |
| `derived/` | generated | each corpus run | NOT part of the standard: typical lengths, representative examples |

## Conventions

- Every entry has an `id` (stable, never reused), a `scope` (section ids, grid topic ids, `grid`, or `all`), and a `status` (`adopted`, `pending_adjudication`, `retired`).
- Rules and conventions carry `enforcement`: `must`, `should`, or `info`.
- `source` is a short free-text pointer to where the entry came from (a decision record row, a policy section, a corpus finding). One field, not a structure.
- Constructions carry a human-readable `template` and, where a check needs it, a machine `pattern`. Only the pattern is meant to be matched.
- Each word list lives in exactly one file. Other files refer to it by name.
- No borrower, counterparty, or person names anywhere.

## How it is produced

Corpus analysis (evidence) plus the CRR decision record (choices) generate this pack and the written style guide together, so the two never drift.

---

## manifest.yaml

```yaml
pack: crr-house-style
standards_version: "0.1.0-directional"
effective_date: null
owner: "Credit Risk Review, Analytics"
approved_by: null
derived_from:
  decision_record: null       # the CRR adjudication workbook this version was generated from
  corpus_run: null            # id of the corpus analysis run that supplied the evidence
applies_to:
  workpaper_types: [leveraged_lending_target_review]
files:
  - structure.yaml
  - terminology.yaml
  - assessment_language.yaml
  - evidence_conventions.yaml
  - writing_rules.yaml
  - lexicons.yaml
changelog:
  - {version: "0.1.0-directional", date: "2026-09-09", note: "Directional skeleton. No adopted content."}
```

---

## structure.yaml

```yaml
# Workpaper structure. Typical lengths and figure counts are derived data and live in derived/.

rating_scale:
  values: [Satisfactory, Needs_Improvement, Unsatisfactory]   # illustrative; confirm from corpus
  status: pending_adjudication

grid:
  name: "Credit Analysis Topics"
  row_fields: [topic, rating, justification]
  topics:
    - {id: GRID-FIN, label: "Financial Analysis", maps_to_section: SEC-FIN}
    - {id: GRID-UW,  label: "Underwriting & Documentation", maps_to_section: SEC-UW}
    - {id: GRID-PM,  label: "Portfolio Management", maps_to_section: SEC-PM}
    - {id: GRID-RR,  label: "Risk Rating", maps_to_section: SEC-RR}
    - {id: GRID-TRD, label: "Trading Activity", maps_to_section: SEC-TRD, applicability: "not leveraged loans"}

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
    answers_questions: [Q-BCO-01, Q-BCO-02, Q-BCO-03, Q-BCO-04]   # ids from the decomposition inventory
    expected_topics: [company_overview, sponsor, external_ratings, transaction_terms, pro_forma_capitalization, pro_forma_leverage]
    conclusion_required: false
    status: pending_adjudication

  - id: SEC-FIN
    order: 2
    title: "Financials"
    purpose: "Evaluate the credit team's financial analysis and state CRR's view of it."
    subsections:
      - {heading: "CRR Assessment", requirement: required, position: first}
      - {heading: "Credit Team Financial Analysis", requirement: required}
      - {heading: "Model Assessments", requirement: conditional, condition: "projection update triggers under 5-G-006360 s8.4"}
      - {heading: "Financial Projections", requirement: required}
      - {heading: "EV / Total Debt Coverage", requirement: required}
    answers_questions: [Q-FIN-01, Q-FIN-02, Q-FIN-03, Q-FIN-04, Q-FIN-05]
    expected_topics: [revenue, ebitda, ebitda_adjustments, free_cash_flow, leverage, liquidity, projections, debt_repayment_capacity, enterprise_value]
    conclusion_required: true
    conclusion_position: first
    status: pending_adjudication

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
    conclusion_required: true
    conclusion_position: first
    status: pending_adjudication

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
    conclusion_required: true
    conclusion_position: first
    status: pending_adjudication

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
    conclusion_required: true
    conclusion_position: first
    status: pending_adjudication

  - id: SEC-TRD
    order: 6
    title: "Trading Activity and Exposure Analysis"
    purpose: "Counterparty credit risk exposure analysis. Not applicable to leveraged loans; defined by a later decomposition."
    applicability: {workpaper_types: [counterparty_credit_risk]}
    subsections: []
    answers_questions: []
    expected_topics: []
    conclusion_required: true
    status: pending_adjudication
```

---

## terminology.yaml

```yaml
# Terminology: one entry per concept. Variants carry a status; the canonical form is the
# preferred variant. `source` is a short pointer (policy section or decision record row).
# variant.status: preferred | acceptable | avoid | pending_adjudication

defaults:
  acronym_rule: expand_on_first_use          # or never_expand, per entry
  first_use_format: "{expansion} ({acronym})"

concepts:
  - id: TERM-001
    canonical: "primary source of repayment"
    acronym: PSOR
    variants:
      - {text: "primary source of repayment", status: preferred}
      - {text: "PSOR", status: acceptable, note: "after first-use expansion"}
      - {text: "primary repayment source", status: pending_adjudication}
    definition: "The cash flow or asset the credit team identifies as the expected source of debt service."
    used_in: [SEC-UW]
    source: "5-G-006360"
    status: adopted

  - id: TERM-002
    canonical: "secondary source of repayment"
    acronym: SSOR
    variants:
      - {text: "secondary source of repayment", status: preferred}
      - {text: "SSOR", status: acceptable}
    definition: "The fallback source of repayment if the primary source fails, typically collateral or refinancing."
    used_in: [SEC-UW]
    source: "5-G-006360"
    status: adopted

  - id: TERM-003
    canonical: "credit watchlist"
    acronym: CWL
    variants:
      - {text: "credit watchlist", status: preferred}
      - {text: "CWL", status: acceptable}
      - {text: "watchlist", status: acceptable, note: "only after the full term has appeared"}
      - {text: "watch list", status: avoid}
    definition: "The list of obligors under heightened monitoring per Global CWL Criteria."
    used_in: [SEC-PM]
    source: "1-G-012756 s4.2"
    status: adopted

  - id: TERM-004
    canonical: "ComCo Memo"
    acronym_rule: never_expand
    variants:
      - {text: "ComCo Memo", status: preferred, note: "house convention; the expansion is rarely written"}
      - {text: "Commercial Committee memo", status: acceptable}
      - {text: "committee memo", status: avoid}
    definition: "The credit approval memorandum presented to the Commercial Committee."
    used_in: [SEC-BCO, SEC-UW]
    source: "5-P-000247"
    status: pending_adjudication

  - id: TERM-005
    canonical: "UBS Adjusted EBITDA"
    variants:
      - {text: "UBS Adjusted EBITDA", status: preferred}
      - {text: "adjusted EBITDA", status: acceptable, note: "when the UBS basis is already established"}
      - {text: "EBITDA adjustments", status: acceptable, note: "refers to the adjustments, not the metric"}
    definition: "EBITDA after the credit team's adjustments for non-cash and non-recurring items."
    used_in: [SEC-FIN, GRID-FIN]
    source: "5-G-006360 s8.4"
    status: adopted

  - id: TERM-006
    canonical: "UBS Expected Case"
    variants:
      - {text: "UBS Expected Case", status: preferred}
      - {text: "Expected Case", status: acceptable}
      - {text: "base case", status: avoid, note: "ambiguous with management case"}
    definition: "The credit team's central projection scenario."
    used_in: [SEC-FIN]
    source: "5-G-006360"
    status: adopted

  - id: TERM-007
    canonical: "UBS Downside Case"
    variants:
      - {text: "UBS Downside Case", status: preferred}
      - {text: "Downside Case", status: acceptable}
      - {text: "stress case", status: avoid}
    definition: "The credit team's adverse projection scenario."
    used_in: [SEC-FIN]
    source: "5-G-006360"
    status: adopted

  - id: TERM-008
    canonical: "workpaper"
    variants:
      - {text: "workpaper", status: preferred}
      - {text: "work paper", status: avoid}
      - {text: "linecard", status: avoid, note: "colloquial; understood but not written"}
    definition: "The CRR review work product for a single obligor or counterparty."
    used_in: [all]
    source: "1-G-007544"
    status: adopted

  - id: TERM-009
    canonical: "review"
    note: "Same word, two meanings. Name which one."
    senses:
      - {sense: "CRR review", preferred_text: "CRR review", context: "the engagement this workpaper belongs to"}
      - {sense: "credit team periodic review", preferred_text: "Annual Review | Quarterly Review", context: "the credit team's periodic review of the obligor"}
    variants:
      - {text: "the review", status: avoid, note: "ambiguous between senses"}
    used_in: [all]
    source: "corpus finding"
    status: pending_adjudication

# Intake: candidates promoted from the corpus tool's terminology_candidates file land here
# with status pending_adjudication.
```

---

## assessment_language.yaml

```yaml
# Assessment language: how CRR states what it concludes.
# `template` is for people and for drafting. `pattern` is the machine form for checking;
# given only where a check is likely to be wanted.
# construction.status: preferred | acceptable | avoid | pending_adjudication

conventions:
  actor: "CRR"                       # CRR is the grammatical subject of an assessment
  actor_forms_avoid: ["we", "our", "the reviewer", "the review team", "it is assessed that", "it is noted that", "it was observed that"]
  tense: present                     # assessments in present tense; events in past
  status: pending_adjudication

assessment_acts:
  - id: ASSESS-CONCUR
    act: concur
    meaning: "CRR agrees with the credit team's analysis or conclusion."
    constructions:
      - {template: "CRR concurs with {object}", pattern: "\\bCRR concurs with\\b", status: preferred}
      - {template: "CRR agrees with {object}", pattern: "\\bCRR agrees with\\b", status: pending_adjudication}
      - {template: "CRR is in agreement with {object}", pattern: "\\bCRR is in agreement with\\b", status: avoid, reason: "wordier form of the same act"}
      - {template: "CRR does not disagree with {object}", pattern: "\\bdoes not disagree\\b", status: avoid, reason: "double negative"}
    scope: all
    enforcement: should
    source: "corpus synonym group; decision pending"
    status: pending_adjudication

  - id: ASSESS-NOTE
    act: note_observation
    meaning: "CRR records a fact or observation without asserting a deficiency."
    constructions:
      - {template: "CRR notes that {clause}", pattern: "\\bCRR notes\\b", status: preferred}
      - {template: "CRR observes that {clause}", pattern: "\\bCRR observes\\b", status: pending_adjudication}
      - {template: "It is noted that {clause}", pattern: "\\bIt is noted that\\b", status: avoid, reason: "passive, no actor"}
    scope: all
    enforcement: should
    source: "corpus synonym group; decision pending"
    status: pending_adjudication

  - id: ASSESS-ADEQUATE
    act: assess_adequate
    meaning: "CRR judges an element sufficient, supported, or appropriate."
    constructions:
      - {template: "CRR assesses {object} as {adequate|appropriate|sufficiently supported}", pattern: "\\bCRR assesses\\b", status: preferred}
      - {template: "CRR considers {object} to be {adjective}", pattern: "\\bCRR considers\\b", status: acceptable}
      - {template: "{object} appears {adjective}", pattern: "\\bappears (to be )?(adequate|appropriate|sufficient)", status: avoid, reason: "hedged where a judgment is required"}
    scope: all
    enforcement: should
    source: "corpus synonym group; decision pending"
    status: pending_adjudication

  - id: ASSESS-FLAG
    act: flag_issue
    meaning: "CRR identifies a deficiency, gap, or exception."
    constructions:
      - {template: "CRR identified {issue}", pattern: "\\bCRR identified\\b", status: preferred}
      - {template: "CRR notes a gap in {object}", pattern: "\\bCRR notes a gap\\b", status: acceptable}
      - {template: "{object} may indicate {issue}", pattern: "\\bmay indicate\\b", status: avoid, reason: "an identified issue is stated, not hedged"}
    required_elements: [what_was_expected, what_was_found, policy_reference_if_any]
    scope: all
    enforcement: must
    source: "corpus synonym group; decision pending"
    status: pending_adjudication

  - id: ASSESS-LIMIT
    act: limitation_or_preclusion
    meaning: "CRR states that an assessment could not be made and why."
    constructions:
      - {template: "CRR's assessment of {object} is precluded by {reason}", pattern: "\\bis precluded by\\b", status: preferred}
      - {template: "CRR was unable to assess {object} because {reason}", pattern: "\\bCRR was unable to assess\\b", status: acceptable}
      - {template: "{object} could not be reviewed", pattern: "\\bcould not be reviewed\\b", status: avoid, reason: "no actor, no reason"}
    required_elements: [what_could_not_be_assessed, reason, what_would_resolve_it]
    scope: all
    enforcement: must
    source: "corpus synonym group; decision pending"
    status: pending_adjudication

  - id: ASSESS-ATTRIB
    act: attribute_to_source
    meaning: "CRR reports a position held by the credit team or a document, not its own."
    constructions:
      - {template: "The credit team {states|projects|expects} {clause}", status: preferred}
      - {template: "Per the {document}, {clause}", status: acceptable}
      - {template: "It is expected that {clause}", pattern: "\\bIt is expected that\\b", status: avoid, reason: "whose expectation is unclear"}
    scope: all
    enforcement: should
    source: "corpus synonym group; decision pending"
    status: pending_adjudication

hedging:
  # The single home for hedge word lists. writing_rules RULE-W09 refers here.
  allowed:
    - {text: "appears to", when: "reporting an inference from incomplete evidence; never in a conclusion sentence"}
    - {text: "may", when: "stating a forward-looking risk"}
  avoid: [seems, "seem to", "tends to", probably, perhaps, arguably]
  rule: "A conclusion sentence (the first sentence under CRR Assessment, and every grid justification) carries no hedge."
  enforcement: should
  status: pending_adjudication

rating_language:
  # How the register shifts by grid rating. Shapes are directional; densities come from the corpus.
  - rating: Satisfactory
    expected_acts: [concur, assess_adequate, note_observation]
    justification_shape: "One to two sentences: the conclusion, then the principal support."
    example_pattern: "CRR concurs with {object}; {support}."
    status: pending_adjudication
  - rating: Needs_Improvement
    expected_acts: [flag_issue, assess_adequate, concur]
    justification_shape: "Conclusion first, then the gap as expected versus found, then any mitigant."
    issue_introduction: {preferred: "CRR identified {issue}", position: first_or_second_sentence}
    example_pattern: "CRR identified {issue}. {expected} {found}. {mitigant_if_any}."
    status: pending_adjudication
  - rating: Unsatisfactory
    expected_acts: [flag_issue]
    justification_shape: "Conclusion first; each deficiency enumerated (i), (ii), (iii) with a policy reference."
    issue_introduction: {preferred: "CRR identified {issue}", position: first_sentence}
    example_pattern: "CRR identified (i) {issue}; (ii) {issue}; (iii) {issue}."
    status: pending_adjudication
```

---

## evidence_conventions.yaml

```yaml
# Evidence conventions: how claims are tied to sources.

defaults:
  date_required: true
  date_forms: ["{Mon}-{YY}", "{n}Q{YY}", "FY{YY}"]      # Jun-26, 2Q26, FY25
  position: sentence_open                                # "Per the 2Q26 Quarterly Review, ..."
  figure_pointer: "see Figure {n}"
  table_pointer: "see Table {n}"
  status: pending_adjudication

source_types:
  - {id: EVID-ANNUAL,    source_type: annual_review,                   label_form: "{FY} Annual Review",                    example: "Per the FY25 Annual Review, ...",              scope: all,               enforcement: should, status: pending_adjudication}
  - {id: EVID-QUARTERLY, source_type: quarterly_review,                label_form: "{n}Q{YY} Quarterly Review",             example: "The 2Q26 Quarterly Review reports ...",        scope: all,               enforcement: should, status: pending_adjudication}
  - {id: EVID-COMCO,     source_type: comco_memo,                      label_form: "ComCo Memo dated {date}",               example: "The ComCo Memo dated Mar-26 identifies ...",   scope: [SEC-BCO, SEC-UW], enforcement: should, status: pending_adjudication}
  - {id: EVID-AGENCY,    source_type: rating_agency,                   label_form: "{agency} ({rating}, {outlook}, {date})", example: "Moody's (B2, stable, assigned Jan-26)",         scope: [SEC-BCO, SEC-RR], enforcement: must,   status: pending_adjudication}
  - {id: EVID-COVENANT,  source_type: covenant_compliance_certificate, label_form: "{period} compliance certificate",       example: "Per the 2Q26 compliance certificate, ...",    scope: [SEC-PM],          enforcement: should, status: pending_adjudication}
  - {id: EVID-POLICY,    source_type: internal_policy,                 label_form: "{doc id} s{section}",                   example: "per 5-G-006360 s8.4",                           scope: all,               enforcement: must,   date_required: false, status: pending_adjudication}
  - {id: EVID-IRIS,      source_type: iris_document,                   label_form: "{document} (IRIS, {date})",             example: "the executed credit agreement (IRIS, Mar-26)", scope: all,               enforcement: should, status: pending_adjudication}

rules:
  - {id: EVID-R01, statement: "A quantitative claim names its source in the same sentence or the one before.", enforcement: must,   scope: all, status: pending_adjudication}
  - {id: EVID-R02, statement: "A figure or table is referenced in prose before it appears.",                  enforcement: should, scope: all, status: pending_adjudication}
  - {id: EVID-R03, statement: "A flagged issue that rests on a policy requirement cites the policy id and section.", enforcement: must, scope: all, status: pending_adjudication}
  - {id: EVID-R04, statement: "Sources are named as the credit team names them, not paraphrased.",           enforcement: should, scope: all, status: pending_adjudication}
```

---

## writing_rules.yaml

```yaml
# Writing rules: the prescriptive standard. Where a rule is measurable, `metric` names the
# quantity so both sides share vocabulary. Thresholds are null until the corpus baseline
# says where current papers sit. `refers_to` points at the word list or convention used.

rules:
  - id: RULE-W01
    title: "Bottom line on top"
    statement: "The conclusion is the first sentence of a CRR Assessment subsection and of every grid justification."
    enforcement: must
    scope: [SEC-FIN, SEC-UW, SEC-PM, SEC-RR, SEC-TRD, grid]
    measurable: true
    metric: conclusion_position
    threshold: {operator: eq, value: 1}
    refers_to: assessment_language.assessment_acts
    source: "CRR writing guidelines"
    status: adopted

  - id: RULE-W02
    title: "Main point first in every paragraph"
    statement: "The first sentence of a paragraph states its point; the rest develops it."
    enforcement: should
    scope: all
    measurable: true
    metric: paragraph_lead_ratio
    threshold: {operator: gte, value: null}
    source: "CRR writing guidelines"
    status: adopted

  - id: RULE-W03
    title: "Active voice"
    statement: "Assessments and findings are written in active voice with a named actor."
    enforcement: should
    scope: all
    measurable: true
    metric: passive_rate
    threshold: {operator: lte, value: null}
    exemptions: ["events where the actor is unknown or irrelevant"]
    source: "CRR writing guidelines"
    status: adopted

  - id: RULE-W04
    title: "One idea per sentence"
    statement: "A sentence introduces one idea."
    enforcement: should
    scope: all
    measurable: true
    metric: clauses_per_sentence_mean
    threshold: {operator: lte, value: null}
    source: "CRR writing guidelines"
    status: adopted

  - id: RULE-W05
    title: "Acronyms expanded on first use"
    statement: "An acronym is expanded the first time it appears in the workpaper body, unless terminology sets never_expand."
    enforcement: must
    scope: all
    measurable: true
    metric: acronym_first_use_defined
    threshold: {operator: eq, value: 1.0}
    refers_to: terminology
    source: "CRR writing guidelines"
    status: adopted

  - id: RULE-W06
    title: "No vague quantifiers"
    statement: "Vague terms are replaced with a number, a range, or a comparison."
    enforcement: should
    scope: all
    measurable: true
    metric: vague_term_hits_per_100_words
    threshold: {operator: lte, value: null}
    refers_to: lexicons.vague_terms
    source: "CRR writing guidelines"
    status: adopted

  - id: RULE-W07
    title: "Quantify where possible"
    statement: "A claim about size, change, or headroom carries a figure."
    enforcement: should
    scope: [SEC-FIN, SEC-PM, SEC-RR]
    measurable: true
    metric: numeric_density
    threshold: {operator: gte, value: null}
    source: "CRR writing guidelines"
    status: adopted

  - id: RULE-W08
    title: "Short words"
    statement: "Prefer the short word."
    enforcement: info
    scope: all
    measurable: true
    metric: long_word_substitution_hits
    refers_to: lexicons.short_word_substitutions
    source: "CRR writing guidelines"
    status: adopted

  - id: RULE-W09
    title: "No hedging in conclusions"
    statement: "A conclusion sentence carries no hedge."
    enforcement: should
    scope: all
    measurable: true
    metric: hedges_in_conclusion_sentences
    threshold: {operator: eq, value: 0}
    refers_to: assessment_language.hedging
    source: "CRR writing guidelines"
    status: adopted

  - id: RULE-W10
    title: "Free from inconsistencies"
    statement: "A grid justification's claims are supported by the matching section; figures repeated across sections agree."
    enforcement: must
    scope: [grid]
    measurable: true
    metric: grid_section_support_rate
    threshold: {operator: gte, value: null}
    source: "CRR writing guidelines"
    status: adopted

  - id: RULE-W11
    title: "Numbers: sensible order, close comparisons, rounded"
    statement: "Present figures in a consistent order (current then prior), keep compared figures in the same sentence, round to the precision the reader needs."
    enforcement: should
    scope: all
    measurable: false
    source: "CRR writing guidelines"
    status: adopted

  - id: RULE-W12
    title: "Skim friendly"
    statement: "Subsection headings follow structure; enumerations use (i), (ii), (iii); labeled lead-ins such as '2Q26 Financials:' introduce period blocks."
    enforcement: should
    scope: all
    measurable: false
    refers_to: structure
    source: "CRR writing guidelines"
    status: adopted

  - id: RULE-W13
    title: "Clear voice"
    statement: "CRR is the actor. No 'we', no impersonal 'it is assessed'."
    enforcement: should
    scope: all
    measurable: true
    metric: actor_form_violations
    threshold: {operator: eq, value: 0}
    refers_to: assessment_language.conventions.actor_forms_avoid
    source: "CRR writing guidelines"
    status: adopted

  - id: RULE-W14
    title: "No flowery language"
    statement: "No intensifiers or ornamental adjectives."
    enforcement: should
    scope: all
    measurable: true
    metric: ornamental_hits
    threshold: {operator: eq, value: 0}
    refers_to: lexicons.ornamental
    source: "CRR writing guidelines"
    status: adopted
```

---

## lexicons.yaml

```yaml
# Word lists the writing rules refer to. Each list lives only here.
# Hedges and actor forms are NOT here; they live in assessment_language.
# Matching: case-insensitive, word-boundary.

vague_terms:              # RULE-W06. "material" excluded: "material risk" is a term of art.
  - significant
  - considerable
  - appreciable
  - substantial
  - meaningful
  - notable
  - somewhat
  - relatively
  - fairly
  - a number of
  - various

ornamental:               # RULE-W14
  - very
  - extremely
  - highly
  - robust
  - impressive
  - remarkable
  - solid

short_word_substitutions: # RULE-W08. avoid: use
  utilize: use
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

banned_phrases: []        # empty until the team decides
```

---

## derived/README.md


Data regenerated from each corpus analysis run. It informs the standard (thresholds, typical shapes, examples) but is not itself a rule, so it is not versioned with the pack.

- `composition_baseline.yaml` — typical section lengths, figure and table counts, and sentence metrics per section (median and interquartile range). Used to set the null thresholds in `writing_rules.yaml`.
- `representative_units.yaml` — pointers (by unit id, no text) to sections and grid justifications the corpus tool scored as representative, awaiting SME review. Used for examples in the written guide and for grounding.

Sample shape of `composition_baseline.yaml`:

```yaml
run_id: null
sections:
  SEC-FIN:
    words: {median: null, p25: null, p75: null}
    figures: {median: null}
    tables: {median: null}
    passive_rate: {median: null, p75: null}
    words_per_sentence: {median: null, p90: null}
```

---

## schemas/writing_rules.schema.json

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "CRR Style Pack: writing rules (pattern for the other schemas)",
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
              {"type": "array", "minItems": 1, "items": {"type": "string", "pattern": "^(SEC-[A-Z]+|GRID-[A-Z]+|grid|all)$"}}
            ]
          },
          "measurable": {"type": "boolean"},
          "metric": {"type": "string"},
          "threshold": {
            "type": "object",
            "required": ["operator", "value"],
            "properties": {
              "operator": {"enum": ["eq", "lte", "gte", "lt", "gt"]},
              "value": {"type": ["number", "null"]}
            }
          },
          "exemptions": {"type": "array", "items": {"type": "string"}},
          "refers_to": {"type": "string"},
          "source": {"type": "string"},
          "status": {"enum": ["adopted", "pending_adjudication", "retired"]}
        },
        "if": {"properties": {"measurable": {"const": true}}},
        "then": {"required": ["metric"]}
      }
    }
  }
}
```

