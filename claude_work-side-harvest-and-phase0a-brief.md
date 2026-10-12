# Work-side brief — Step 0.4 harvest + Phase 0 part A (read-only)

**Repo:** `/home/aice/projects/sentinel-platform` (UBS Domino). **Nothing in this brief changes the repo, the stores, or the persistent config root.** No commits. No reruns. No model calls. If a step would require writing anywhere except the scratch folder named below, stop and report instead.
**Scratch folder:** `~/sentinel-scratch/2026-10-12/` — create it; every output lands there. Nothing from it is committed. Steve carries the reports out by hand.
**Secrets:** environment *names* and *shapes* only. Never write a value of any `*_KEY`, `*_SECRET`, token, connection string, or endpoint URL into any output. Deployment names and mount paths are fine.

---

## Gate (stop on failure)

1. `git status` clean on `main`; `git log -1` is c72b24f or a descendant. Report the hash.
2. `make check-all` green. Report counts.
3. The persistent mount is present and the 7-Eleven review exists in the store (list reviews via the API or the store index; name the review id). If more than one 7-Eleven review exists, use the most recent completed one and say so.
4. The persistent config root holds the simplified template. Report its path and template id.

## Part 1 — Step 0.4 harvest (do this first)

Write `01-environment-harvest.md` with these sections, each from the live environment, not from memory:

1. **Serving.** How the API and UI are reached: the forwarded prefix shape, which process serves what, the router mode in use, and any proxy headers the app depends on. Note what `spa.py` needs from the environment.
2. **Mount layout.** The persistent mount path, what sits under it (stores, config root, document dir, anything else), and which of those survive a rebuild. Which paths are blobfuse-backed.
3. **Environment on rebuild.** Which settings names are injected by the platform at start, which come from `settings.env`, which were lost on the last rebuild and had to be re-added by hand. Names only.
4. **Settings resolution.** Call the health endpoint and paste the envelope with every value redacted to `<set>` / `<unset>`, keeping the names and `resolvedViaAlias` flags intact.
5. **Dependencies.** How the UI build reaches packages (the mirror and its config file), how Python packages resolve, and anything that had to be pinned individually.
6. **Model.** The deployment names in use for chat and embeddings, the API version name, and how authentication works (describe, no values). The Document Intelligence endpoint's presence (yes/no, no URL).
7. **Known gaps.** Anything from the Round 01 close-out still open (the blobfuse `os.replace` atomicity question; anything else you can see).
8. **Session reports.** Locate the Round 01 session reports and briefs on this machine (scratch dirs, home, anywhere). Copy them into `reports/` under the scratch folder. List what was found and what could not be found.

## Part 2 — sibling template snapshot

Copy the simplified template directory from the persistent config root into `02-template-snapshot/`, preserving structure. Write `02-template-manifest.txt` with each file's relative path and sha256. Also record: the template id, the criteria-set id and version, the profile id and version, the question count, and which questions carry `fills`, `rating_input: true`, `applies_when`, `gate`, `na_allowed: false`, or `absence` in `answer_shape` (ids only). Do not edit anything.

## Part 3 — Phase 0 part A: classify the attention items (separable; skip if Steve says to hold Phase 0)

Against the named 7-Eleven review, read-only through the API and the store:

**A1. The attention table.** Write `03-attention-classification.csv` with one row per open attention item: attention id, section, the question id or spec block id it is about, carrier (prose / table / element / block), worker outcome as stored, and one origin class:

| Class | Test |
|---|---|
| spec_block_unresolved | the row maps to a `workpaper_spec` block whose section key or alias never matched an anchor in this document |
| routing_zero | question exists, zero spans routed, worker never ran or ran on empty context |
| missing_absence_carrier | worker ran, the source lacks the content, the question's `answer_shape` has no `absence`, output failed validation or is hollow |
| citation_verification_failure | substantive answer produced, verifier failed one or more citations |
| reviewer_decision_required | an explicit decision a criterion or gate asks of the reviewer, or a deterministic control flag — NOT a supported judgment with adequate evidence |
| custom_topic | analyst-entered topic from contextText |
| other | describe |

Add a `duplicate_of` column: rows about the same question as an earlier row. Add a `notes` column with one line of evidence for the classification (the stored status, the routed-span count, the verifier message).

**A2. Tallies.** In `03-attention-summary.md`: count per class; the duplicate pairs; for every `citation_verification_failure` row, whether the question carries `fills`, `rating_input`, `crr_judgment` in `assertion_roles`, `check_flag` in `output_role`, or is a feeder in `review_level_outputs` (this is the reliance-rule hypothesis; report only).

**A3. The surfaces in question.** From the same review read: the Story payload as returned (expected: docsLine only); the Fills payload (ids, destinations, values); the Coverage numbers and where in the response they come from; and whether spans consumed by deterministic `workpaper_spec` blocks count as consumed (say how you determined it).

## Report (paste back)

`00-report.md` in the scratch folder: gate results; Part 1 section-by-section done/not-done with anything that could not be determined from the live environment; Part 2 manifest summary and the metadata counts; Part 3 class tallies and the duplicate pairs; a list of every file written. Then stop. Nothing committed, nothing changed.
