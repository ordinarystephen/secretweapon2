# Round 01 Brief — First Round in This Repository (consolidated, v2)

This file REPLACES every earlier Round 01 brief and addendum.
Seven steps: recover the working tree to its ported state, fix
the one honest defect the port surfaced (an environment leak the
golden detected), then the original round — the hygiene check
widens, the document store is verified where it points, the
platform bundle is proven free of the mock, the build pins its
mode, and the README is verified true.

HOW THIS ROUND RUNS (and every round here): this brief arrives
as the session's instructions and is NEVER committed — no copy
of it enters the tree. The round's report is the session's
final output (or a file under a git-ignored local path), NEVER
committed. Commit messages are neutral and describe the change
itself — no round numbers, no step numbers, no process
vocabulary. Read `HANDBOOK.md` before Step 0; it is the
repository's standing orientation.

If any step's expected outcome does not materialize after two
honest attempts, STOP and write up exactly where it stands —
command, full output, your reading — rather than improvising a
third approach. A precise stuck-report is a successful outcome
of this round; an improvised workaround is not.

Execute in order, starting with Step 0. Every step lands green
(`make check` / `make check-all`) except where Step 0 names the
one permitted red; commit per step. Stop and flag before
touching any unconditional rule stated in HANDBOOK.md. For
CONTROL SURFACES (the boundary checks, their floors, the
settings' required names, frozen result shapes): a fix inside
an ordered step proceeds only when the step's order covers it
AND it is watched red AND it appears in a dedicated "Control
surfaces touched under step orders" section at the TOP of the
report; outside an ordered step, stop and flag.

THE FROZEN SETTINGS CONTRACT (highest-priority constraint this
round): the platform's setting names are
`MODEL_SERVICE_ENDPOINT`, `MODEL_CHAT_DEPLOYMENT`,
`MODEL_API_VERSION`, `MODEL_EMBEDDINGS_DEPLOYMENT`,
`DOCINTEL_ENDPOINT`, `DOC_STORE_DIR` (plus the optional names
`KNOWN_SETTING_NAMES` declares). These are a frozen contract:
never rename, add, or remove one; never re-introduce
vendor-prefixed (`AZURE_*`, `OPENAI_*`) names anywhere; never
edit a test to make it pass; never hardcode an environment
value into a committed file. The ENVIRONMENT adapts to the
platform, never the reverse. The settings tests in
`tests/test_settings*.py` pin this contract — a failure there
means the MODULE drifted, and the fix is restoring the module.

Hard constraints (restated):
- Data handling per HANDBOOK.md: test fixtures stay fictional;
  real system names in deployed configuration only; policy
  identifiers out until activation. Nothing real enters a
  fixture, a test, or any commit this round.
- Contracts additive; the API seam's shape is preserved — if
  Step 4's fix cannot keep `createApi` synchronous, stop and
  flag with the options rather than changing the seam contract.
- The export is untouched. `elements_selected` is NOT renamed.
  Policy stays deferred. The version rule is absolute: any edit
  to a stamped artifact bumps it, with a domain-terms why.

## Step 0 — Recovery and first-session verification

The working tree may carry hand edits from earlier
troubleshooting (the settings module was partially renamed to
old vendor names; HANDBOOK.md may carry related edits). Recover
first, then verify.

1. `git status` and `git diff` (staged and unstaged). List
   EVERY modified or unexpected untracked file in the report
   with its diff. Also `git log --oneline -5` — record what the
   tree's commit history is, and whether any commits exist
   beyond the port commit (if a prior session committed partial
   work, record it; do not revert commits, only working-tree
   edits).
2. Restore the hand-edited files to the committed state:
   `git checkout -- sentinel_platform/config/settings.py` and
   likewise any other file whose diff is renaming-effort
   residue. EXCEPTION: `HANDBOOK.md` carries two OWNER-written
   sections (data handling; the control-surface protocol). If
   restoring HANDBOOK.md would remove them, save those
   paragraphs first and re-apply them verbatim after the
   restore; show before/after in the report. If they were never
   present, flag it and proceed — do not draft them.
3. Verify the environment carries the six required names:
   `env | grep -E 'MODEL_|DOCINTEL_ENDPOINT|DOC_STORE_DIR'`.
   Report the NAMES found (never the values). If any of the six
   is absent from this shell, STOP and report which — the owner
   sets them at the Domino project level and restarts the
   workspace; exporting values yourself is not the fix.
4. Settings sanity, in one command:
   `uv run python -c "from sentinel_platform.config.settings import get_settings; s=get_settings(); print('file:', s.settings_file); print('missing:', s.missing_required())"`
   Expected: `file: None` (or a deliberate file the owner
   names) and `missing: []`. Anything else ⇒ stop and report.
5. Baseline gates: `make check`, `npm run verify` (in `ui/`),
   `make check-all`. EXPECTED STATE: everything green EXCEPT
   exactly one platform failure —
   `test_the_golden_flow_reproduces_the_stored_record` (Step 1
   fixes it). The settings tests must be green after the
   restore. Any OTHER red ⇒ stop and report it verbatim before
   proceeding. Record every count and every skip reason.
6. Locate and note in the report: the context-assembly and
   manifest-accounting code the golden failure implicates; the
   hygiene check's discovery and its named-file tuple; the
   scope check's UI exception; the seam selection in
   `ui/src/api/client.ts` (`createApi`, `VITE_API`, default
   `'mock'`); the platform bundle's build command in the
   Makefile and `package.json`; the store builder in
   `sentinel_platform/documents/` — whether a missing store
   directory is created or refused.
7. Report discrepancies between this brief's assumptions and
   the repository as found; material ⇒ stop and flag.

## Step 1 — The golden's environment leak

The golden-flow reproduction test fails on this machine with a
`contextChars` difference (and possibly path-bearing strings in
`documents`/`prompt` fields) in the routing record. Diagnosis:
an environment-dependent value — very likely an absolute path —
enters the assembled context or the manifest's accounting, so
the golden matches only on the machine that generated it. The
golden detected real environment leakage; fix the leak, not the
test.

- Diagnose at the source: run the test `-vv`, read the full
  diff, and find what machine-dependent text (absolute paths,
  tmp roots, store roots, user names) reaches context assembly
  or the manifest's recorded fields.
- Fix it THERE: the assembled context and every manifest field
  must contain only environment-independent content — document
  names and logical ids, never absolute paths. Do NOT fix by
  regenerating the golden on this machine (that re-bakes this
  machine's paths and fails on the next one).
- Add a test, red-first against current behavior, asserting no
  absolute path (and no tmp-root marker) appears in any
  assembled context or recorded manifest field of the built
  golden flow.
- Then regenerate the golden ONCE, deliberately, with the diff
  named in the commit: expected movers are the accounting
  fields and any formerly path-bearing field, nothing else. If
  anything else moves, stop and flag.
- Own commit; own section in the report.

## Step 2 — The hygiene check widens to this whole repository

- The documentation-hygiene check's discovery reaches the WHOLE
  `ui/` tree minus `node_modules` and build output (`dist`),
  admitting `.sh` and `.txt` as whole-file prose beside the
  dotfiles (exclusions written for documentation trees stay
  written even where no such tree exists). The top-level
  `.gitignore` and `.gitattributes` join the named-file tuple,
  read as prose. The scope check's bounded exception widens to
  match; the floor moves and is raised RED before the discovery
  catches up; a planted violation in a newly reached file class
  (a `.sh`, a config `.ts`, a top-level dotfile) watched red by
  file, line and token, then removed.
- The e2e screenshot spec's output constant moves to a
  git-ignored `.local` path (the contrast audit's exact
  pattern) — after it, the check holds the tree at zero with NO
  declared exceptions.
- Tests red-first throughout; the e2e spec's product-glyph
  assertions must remain untouched and passing (prove one is
  reached and clean).

## Step 3 — The document store, verified where it points

- Verify the boot path end to end in THIS environment: the
  serve starts; the health envelope's `store_root` equals the
  configured `DOC_STORE_DIR`; a write-and-read round trip
  through the store lands under it and nowhere else.
- From Step 0's finding on the store builder: if a missing
  directory is refused, record the make-the-directory
  prerequisite in HANDBOOK.md's settings rows (the hygiene
  check must stay green on the edit); if it is silently
  created, verify the created directory's permissions are sane
  and record that instead.
- Record as an environment note in the report (no action): the
  values of `MODEL_CHAT_DEPLOYMENT` and
  `MODEL_EMBEDDINGS_DEPLOYMENT` are placeholders not yet
  verified against the model resource; nothing this round calls
  a model, and verification belongs to the first live-model
  work.
- No new machinery unless the round trip FAILS — then stop and
  flag with the failure, because a store that cannot write in
  this environment blocks everything after it.

## Step 4 — Mock isolation, proven at the bundle

- A new boundary check (a control surface, disclosed): after
  the platform bundle builds, its assets are scanned for a
  DISTINCTIVE mock-only string — chosen from
  `ui/src/api/mock/fixtures.ts` or `mockApi.ts` at Step 0,
  assembled from two halves in the test so the check never
  trips itself — and for the mock module's own name. Present ⇒
  red, naming the asset. Watch it red honestly: the MOCK bundle
  (built `VITE_API=mock`) must show the probe FINDS the string;
  then the platform bundle's scan decides.
- If the platform bundle is CLEAN as built: pin it — the check
  joins the gate after the platform bundle's build step, and
  the report says the bundler's dead-code elimination already
  excludes the mock.
- If the platform bundle CARRIES the mock: restructure the
  seam's selection so the bundler can eliminate the unused
  branch — `createApi` stays synchronous and the seam's
  documented contract unchanged (an `if` on the literal env
  comparison, separate entry modules, or the bundler's define
  mechanics — your call, disclosed, red-first with the bundle
  check as the proof). The mock, its fixtures, and every UI
  test are UNTOUCHED — isolation is about the shipped artifact,
  never about removing the test backend.

## Step 5 — The build-mode pin

- The platform bundle's build command sets `VITE_API=http`
  EXPLICITLY (in the script or the Makefile target the gate
  uses — wherever Step 0 found it), so an unset environment can
  never produce a demo bundle on the platform path. The
  dev-and-test default `'mock'` in `createApi` STAYS — it is
  the right default for `npm run dev` and the test suite; the
  pin plus Step 4's check are the enforcement where it matters.
- Tests: the gate's own run is the proof (the bundle check
  green on the pinned build); a report line names where the pin
  lives.

## Step 6 — The README, verified true

- The top-level `README.md` was written for a reader who has
  never seen this repository. Verify it claim by claim against
  the code: every command runs as written, every Makefile
  target it names exists (correct the serve wording to the
  actual target name), the required environment names match the
  settings module's SIX required names and the settings-file
  mechanism (the README currently undersells this — align it:
  the six names, the optional `SENTINEL_SETTINGS_FILE` /
  `settings.env` mechanism and its file-wins precedence, the
  persistent-storage warning for `DOC_STORE_DIR`), the layout
  tree matches the tree, the prerequisite versions match the
  lockfiles and `ui/.nvmrc`. Correct what differs — prose edits
  in the README's own voice — and list every correction in the
  report. The hygiene check must hold the file after the edits.
- If `HANDBOOK.md`'s settings section does not list the six
  required names, the settings-file mechanism, and the
  persistent-storage warning, flag the gap (the handbook edit
  is the owner's call) — except where Step 3 already ordered a
  specific settings-row addition.

## Step 7 — Close

The report (the session's final output, not a commit): the
Step 0 recovery section (every hand edit found and restored,
with diffs); the verification numbers; per-step summaries; the
test matrix; watch-it-fail with quoted red output for every
behavior change and widened check; the control-surfaces section
at the TOP if the protocol was used; the environment notes
(the unverified deployment values; anything the owner must set
or decide); disclosed rulings with cost-if-wrong; flags with
disposition requests; the floors as re-measured. The owner
pushes on his own close ritual.

## Explicitly out of scope this round

Any content work (criteria sets, question content, document
kinds); live-model evaluation and deployment-value verification
(the next round, not this one); real documents through intake;
policy anything; any renaming of the settings contract, in
either direction; anything HANDBOOK.md lists as deferred.
