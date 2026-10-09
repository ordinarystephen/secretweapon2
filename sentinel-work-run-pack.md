# Sentinel work-side run pack — post-demo fixes, audit, aliases, golden

Run the four blocks IN ORDER, each in a FRESH agent session. Paste the
CONTEXT HEADER at the top of every session, then the block. Reports
come back to the architect chat after each block (or batched).

---

## CONTEXT HEADER (paste first, every session)

```
ENVIRONMENT CONTEXT (RiskLab AICE, PROD INTL — given, do not re-derive):
- AICE pre-injects environment variables into every execution:
  AZURE_OPENAI_ENDPOINT (URL of the LOCAL gateway proxy for model
  calls), OPENAI_API_VERSION, and AZURE_DOCINTEL_ENDPOINT (URL of the
  local SSL proxy for Document Intelligence — currently
  https://127.0.0.1:8443, alive, nginx). The local proxies attach
  metadata headers and forward to the AICE Gateway (PROD INTL:
  .../aice-openai and .../aice-docintel).
- Authentication for BOTH services is Azure AD tokens via
  DefaultAzureCredential (azure-identity) — no API keys anywhere, ever.
  Model clients use azure_ad_token_provider=get_bearer_token_provider(
  DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default").
  The DI client passes credential=DefaultAzureCredential().
- Deployment names are real in this environment: gpt-6-sol (chat) and
  text-embedding-3-small (embeddings) are valid green-zone deployments.
- AICE preinstalls NO AI libraries — missing-dependency findings are
  expected, resolved against crr-sentinel's uv.lock versions.
- The platform's settings contract (MODEL_*/DOCINTEL_ENDPOINT/
  DOC_STORE_DIR) is frozen; the environment adapts via settings.env
  and (after Block 3) aliases. Never rename contract names, never edit
  a test to pass, never put credentials in any file.
- This is an MVP for developer handoff: working beats hardened.
- Rules: neutral commit messages (no round/step vocabulary); briefs and
  reports are never committed; report quoted red output for every
  red-first test; stop and report rather than improvise past a failure.
```

---

## BLOCK 1 — store hardlink fallback + model dependency + model auth

```
POST-DEMO FIX — store fallback + model dependency + model auth

1) sentinel_platform/documents/document_store.py: the save path uses
   os.link, which fails on the persistent mount (OSError Errno 38).
   Add a fallback: try os.link; on OSError with errno in (ENOSYS,
   EPERM, EXDEV), fall back to an atomic copy (copy to a temp name in
   the destination directory, fsync, os.replace). Never overwrite an
   existing target; same final paths and semantics. Red-first test
   simulating the errno via monkeypatch. No other store changes.
   Commit alone, neutral message.
2) uv add langchain-openai==<version from crr-sentinel's uv.lock>
   (plus langchain-core if that lock pins it). Commit deps alone.
3) Restart serve; run ONE review end to end through the API (create
   review, upload a PDF, start the run, poll to completion).
   If the model call fails with auth/401/token errors: compare our
   model client construction against crr-sentinel's and the AICE
   pattern in the context header — AD token provider, never api_key.
   If ours differs, migrate that construction pattern (smallest diff,
   the client factory only), red-first where feasible, commit alone,
   retry once more.
4) Report RUN_SUCCESS or the final exception verbatim. STOP.
```

## BLOCK 2 — environment audit (report only)

```
ENVIRONMENT AUDIT — crr-sentinel vs sentinel-platform (REPORT ONLY)

GIVEN for the proxy table: the context header above. Verify which
AZURE_* names are actually injected in this workspace (report names
only) and record them as alias targets for a later change.

Produce one report with four gap tables (columns: item | crr-sentinel
| sentinel-platform | gap | suggested disposition):
1) ENV VARS: every environment name each app reads (settings modules,
   os.getenv/os.environ across both codebases) and every relevant name
   set in this workspace (names; values only where they are
   endpoints/ids/paths, never tokens). Map old name -> new name ->
   set/unset -> consumer.
2) PROXIES & LOCAL SERVICES: every localhost/port dependency in each
   app, what provides it (per the context header), and whether it is
   alive here. Include whether model calls route via the local gateway
   proxy in BOTH apps.
3) DEPENDENCIES: (a) every top-level import across sentinel_platform/
   + api/ runtime code vs pyproject.toml declarations — list
   undeclared imports; (b) crr-sentinel's uv.lock package set diffed
   against ours — packages it has that we lack, with versions, marking
   which are plausibly runtime-needed vs incidental.
4) ENVIRONMENT ASSUMPTIONS: filesystem behaviors on /mnt/private
   (hardlinks — known; atomic rename, locking), memory (the error-137
   kill of make serve — note workspace sizing), ports in use.
Append: current git status (the committed round-01-brief.md, stray
working-tree changes) as inventory, untouched.
STOP after the report. No fixes, no commits.
```

## BLOCK 3 — vendor-alias fallback

```
VENDOR-ALIAS FALLBACK v2 — settings read AICE-injected names; declare werkzeug

1) In sentinel_platform/config/settings.py: read() gains a DECLARED
   alias map consulted (file first, then process env — same order as
   now) when the canonical name resolves empty:
     MODEL_SERVICE_ENDPOINT      <- AZURE_OPENAI_ENDPOINT
     MODEL_CHAT_DEPLOYMENT       <- AZURE_OPENAI_DEPLOYMENT
     MODEL_API_VERSION           <- OPENAI_API_VERSION
     MODEL_EMBEDDINGS_DEPLOYMENT <- AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT
     DOCINTEL_ENDPOINT           <- AZURE_DOCINTEL_ENDPOINT
   Canonical always wins when both resolve. apply_to_process_env
   writes canonical names only. NEVER read AZURE_OPENAI_API_KEY or any
   credential name — the alias map is exactly these five, closed.
   Settings records which names resolved via alias; surface that list
   in the health envelope beside the existing settings reporting.
   Tests red-first: alias from process env; alias from file; canonical
   beats alias; no alias outside the map. KNOWN/REQUIRED tuples
   unchanged. One HANDBOOK.md settings-rows line documenting the
   aliases AND noting the two deployment names are not AICE-injected
   and must be supplied (settings file or project env). Commit alone
   ("accept vendor-prefixed environment names as aliases").
2) Declare werkzeug as a direct dependency (it is imported directly in
   errors.py and spa.py but only transitively locked): uv add
   werkzeug==<the version already in our uv.lock>. Commit alone
   ("declare directly imported dependencies").
3) make check green except the known golden test. Report, STOP.
```

## BLOCK 3b — align the embeddings constructor with the installed package's types

```
make check fails at mypy: llm.py:185 passes azure_deployment= and
api_version= to AzureOpenAIEmbeddings; the installed langchain-openai
declares different canonical parameter names (the current kwargs work
at runtime only as pydantic aliases).

1) Inspect the INSTALLED package's AzureOpenAIEmbeddings signature
   (and the chat model's at the same time, if constructed nearby) —
   read the actual class, not memory.
2) Change the constructor kwargs at llm.py:185 (and any sibling
   construction with the same pattern) to the canonical declared
   parameter names, passing the SAME values — behavior identical,
   types satisfied. No type: ignore, no config loosening, no other
   llm.py changes.
3) make check must now be green except the known golden test, with
   mypy fully clean. Report the before/after kwargs and the counts.
   Commit alone ("align model client constructor with the installed
   SDK's parameter names"). STOP.
```

## BLOCK 3c — authorized updates to the two tests pinning the old world

```
BLOCK 3c — authorized updates to the two tests pinning the old world
The two new failures are tests pinning pre-3b conditions. Authorized,
narrowly:
1) test_make_embeddings_constructs: update its kwarg assertions to the
   new canonical names (deployment, openai_api_version), same values —
   the test keeps pinning that the configured values reach the
   constructor, under the names the installed SDK declares.
2) test_missing_sdk_is_a_loud_import_error: it previously relied on the
   SDK actually being absent; now it must SIMULATE absence hermetically
   (block the module in sys.modules via monkeypatch so the import path
   raises) and keep asserting the loud, helpful ImportError. The
   production fail-loud behavior itself is unchanged.
No other test changes. Run both red-first-in-reverse: show each failing
BEFORE your edit (already captured) and passing after, with the suite
count. make check must now be green except the known golden test, mypy
clean. ONE commit: the llm.py constructor change plus these two test
updates ("align model client constructor with the installed SDK's
parameter names"). Report the counts. STOP.
```

## BLOCK 4 — golden environment leak

```
GOLDEN-FLOW FIX — remove the environment leak, then one regeneration

test_the_golden_flow_reproduces_the_stored_record fails because an
environment-dependent value (contextChars differs across machines; a
documents field carries path-like text) enters the assembled context
or the manifest accounting. Diagnose at the source: run the test -vv,
identify exactly what machine-dependent text (absolute paths, tmp
roots, store roots) reaches context assembly or recorded fields. Fix
THERE: context and manifest fields carry only environment-independent
content (document names/logical ids, never absolute paths). Do NOT
fix by regenerating on this machine first. Add a red-first test
asserting no absolute path appears in any assembled context or
recorded manifest field of the built golden flow. THEN regenerate the
golden ONCE, deliberately; the commit names the expected diff
(accounting fields and formerly path-bearing fields only — anything
else moving: stop and flag). Finish with make check-all; report every
count; expect everything green. STOP.
```
## BLOCK 4b — the leak is ordering, not paths: diagnose, pin, regenerate

```
BLOCK 4b — the leak is ordering, not paths: diagnose, pin, regenerate

Correct premise: no path string leaks; instead segment selection
differs across machines (chunk 19 here vs 10 stored, contextChars
3837 vs 3829). Prime suspect: a filesystem-order-dependent iteration
(glob/listdir/iterdir/Path.glob without sorted()) somewhere on the
golden build path — APFS and blobfuse2 return entries in different
orders.

1) DIAGNOSE first: dump the stored selection's span (chunk 10) and
   this machine's (chunk 19) side by side — are they the same text at
   shifted boundaries, reordered content, or genuinely different
   spans? Then trace the build path and list EVERY filesystem-order-
   dependent iteration feeding document loading, chunk assembly, or
   candidate ordering. Report findings before fixing.
2) FIX at the source: every such iteration gains a deterministic
   order by LOGICAL key (sorted filename / document id / stable chunk
   index), never by whatever the OS returns. Smallest diff; no
   scoring or selection logic changes.
3) Red-first hermetic test: build the golden flow with the directory
   listing monkeypatched to return entries in REVERSED (or shuffled-
   with-fixed-seed) order and assert the built result is byte-
   identical to a normal build — selection included. Red before the
   fix, green after. Commit fix+test alone.
4) THEN regenerate the golden ONCE if the fixed build still differs
   from the stored record. The commit names the expected diff:
   the segment_methodology_selection fields and context accounting
   ONLY — anything else moving: stop and flag.
5) make check-all; report every count; expect fully green. STOP.
```
## BLOCK 4c — deterministic ranking: quantize + stable tie-break (authorized)

```
BLOCK 4c — deterministic ranking: quantize + stable tie-break (authorized)

The cause is confirmed: a float64 tie broken by machine-dependent
float32 noise. The previous "no scoring/selection changes" constraint
is LIFTED for exactly this: make ranking deterministic without
changing relevance behavior.

1) In the retrieval ranking that feeds span selection:
   a) compute/compare ranking scores in float64;
   b) QUANTIZE scores for ordering (round to a named constant, e.g.
      SCORE_RANK_PRECISION = 6 decimal places — far below meaningful
      relevance differences, far above cross-machine float noise),
      with a comment stating why;
   c) break ties by a STABLE LOGICAL key — document order within the
      review, then chunk index — never by float residue, never by
      anything environment-dependent.
   Scope: ordering only. Score computation inputs, candidate set,
   context-cap logic, and selection output shapes unchanged.
2) Red-first hermetic test: two candidates whose injected scores
   differ only by sub-quantization noise (x and x+1e-8), presented in
   both orders; assert the SAME winner both times and that the winner
   is the stable-key choice. Red before the fix on this machine,
   green after. Commit fix+test alone ("make retrieval ranking
   deterministic across numerical environments").
3) Run the golden reproduction test. If the fixed build now matches
   the STORED golden byte-identically (plausible: the stable key may
   pick chunk 10, the Mac's winner), report that and DO NOT
   regenerate. Otherwise regenerate ONCE; the commit names the
   expected diff: segment_methodology_selection fields and context
   accounting only — anything else moving: stop and flag.
4) make check-all; report every count; expect fully green. STOP.
```
## BLOCK 4c — continuation: reorderings ratified, regenerate golden

```
BLOCK 4c — continuation: reorderings ratified, regenerate golden

The four span reorderings (capitalization, credit_watchlist_status,
external_ratings_check, validation_tests_actually_run) are RATIFIED.
Context-character counts unchanged confirms the same spans are
selected; only their order changed, from float-residue order to the
stable logical key. That is the same defect corrected in four more
places, not an unauthorized diff. Commit 81b572e stands.

1) Regenerate the golden ONCE. The commit message names the full
   expected diff: segment_methodology_selection fields, span ORDER
   within the four named units above (membership and context
   accounting unchanged), and nothing else. Any other field moving:
   stop and flag before committing.
2) make check-all. Report every count; expect fully green. STOP.
```

## BLOCK 5 — working-tree tidy (small, deliberate)

```
BLOCK 5 — tree hygiene and clean close

The golden flow is fixed and check-all is fully green. This block
only cleans the worktree. No source, test, or golden changes.

1) git status. Enumerate every uncommitted change and untracked file.
2) The Makefile change (VITE_ROUTER=hash pin on ui-build) is a real
   environment requirement: commit it ALONE with a message saying the
   workspace detection returns false here so the router must be
   pinned at build time.
3) The .gitignore change: report the exact added lines. If they
   ignore settings.env and local junk only, commit ALONE as
   "ignore local environment files". If anything else is in there,
   stop and list it.
4) git rm docs/rounds/round-01-brief.md and commit alone ("remove
   ported round brief; governance lives outside the repo"). After
   this, docs/ should not exist in the repo — confirm.
5) Any remaining untracked files: list them with one line each on
   what they appear to be. Do NOT delete or commit them — report only.
6) Final: git status must show a clean tree (untracked-only items
   from step 5 excepted, pending my disposition). git log --oneline
   -10 so I can see the port's commit history. make check-all once
   more; report every count. STOP.
```

---

## After Block 3 (owner, by hand)

Delete the five MODEL_*/DOCINTEL_ENDPOINT lines from settings.env,
keep DOC_STORE_DIR, restart serve, confirm the health envelope shows
the aliased names resolving and a review still runs. That is the
zero-config story the dev team inherits: AICE injects, aliases catch,
one line of local config (the store) remains.

## What comes back to the architect

Per block: the report (with quoted red output for every red-first
test, diffs for any client-construction change, and Block 2's four
tables). After Block 4: the full make check-all counts — expected
fully green for the first time on this machine. Then: ratification,
audit dispositions, and the trimmed remainder of Round 01 (mock-
isolation check, hygiene widening) sized to the MVP principle.
