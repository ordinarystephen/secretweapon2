# CRR Style Pack (illustrative skeleton)

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
