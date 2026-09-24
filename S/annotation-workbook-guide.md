# How to review the annotation workbook (Gold Tool v0.1)

This guide is for the person reviewing a generated `annotation.xlsx`. It explains what to fill in, what to leave alone, and how to handle the situations that come up on a real quarterly credit review (QCR). The examples come from page 1 of the first real document.

**What you're doing.** Azure Document Intelligence (DI) has done a first pass over the PDF, and `gold init` has turned its output into rows. Your job has three parts:

1. check each row against the PDF;
2. correct what DI got wrong;
3. add the meaning a machine can't: structure, dates, what an image shows, and the business fields.

You never deal with coordinates. Those carry through from DI automatically.

**Keep the PDF open next to the workbook.** Every judgement below is "what does the printed page say?"

---

## 1. Order of work

Work in this order. Each pass makes the next one easier.

1. **Blocks, page by page, top to bottom.**
   - Exclude duplicates and junk.
   - Fix types.
   - Set levels and parents.
   - Split or join rows where DI got the boundaries wrong.
   - Add as-of dates and labels.
2. **Tables.** Check each grid against the printed table.
3. **Furniture.** Confirm the running headers, footers and page numbers.
4. **Fields.** Give every row a status.
5. **Document.** Fill in the sign-off keys.

Run a **draft compile** whenever you want a check. It's cheap, and the report tells you what's still wrong. Run `--final` only at the end.

---

## 2. Ground rules

These apply on every tab.

- **Grey columns belong to the tool.** Don't edit them: `id`, `page`, `row_ref`, the `REF` rows in Tables, and the tool's keys in Document. Compile checks them and stops on any change.
- **Never delete a generated row.** Mark it `EXCLUDED` instead. Deleting a generated row is a compile error, because the tool can't tell a deletion from a lost row.
- **Never sort the Blocks tab.** Row order *is* reading order. Filtering is fine; filter `review` to `UNREVIEWED` to see what's left. Moving a single row to fix reading order is also fine.
- **Rows you add get an ID starting with `h.`**
  - The ID must be unique, and must not look like a generated one (`p01.b023`).
  - `h.exp.lend` and `h.p01.b022.a` both work.
  - The ID doesn't set position: reading order comes from where the row sits, and hierarchy comes from `parent`.
- **Type text, not numbers or dates.** The editable columns are formatted as Text, so what you type stays exactly as typed. If Excel still turns something into a number or date, compile names the cell. Fix it by retyping with a leading apostrophe (`'181.0`, `'Mar-2026`). The apostrophe forces text and isn't stored.
- **Record what's printed.** Never infer, reconcile or fill in.
  - If two places in the document disagree, record each as printed.
  - If an as-of date isn't printed on a block or a heading above it, leave it blank.
  - Keep typos exactly as printed.
- **Don't rename or delete column headers.** The tool reads each tab by its header names.

---

## 3. Review status

Every row has a `review` value. Most rows start as `UNREVIEWED`.

| Value | Use when |
|---|---|
| `CONFIRMED` | DI's **text, value and type** are right. Use this even if you filled in or changed the structure columns (`parent`, `level`, `label`, `as_of`, `speaker`, `content_kind`, `continues`). |
| `MODIFIED` | You changed the **text, value or type** from what DI produced: an OCR fix, a split heading, a retyped row. |
| `ADDED` | A row you inserted (its ID starts with `h.`). |
| `EXCLUDED` | The row shouldn't be in the gold at all: a duplicate, noise, or an empty row. It's dropped from the gold and listed in the report. |
| `UNREVIEWED` | Not looked at yet. **None can remain in Blocks, Furniture or Fields at `--final`.** |

Compile compares text, value and type with DI's original. If they don't match, it warns about either case: edited but marked `CONFIRMED`, or marked `MODIFIED` with nothing changed. These are warnings, not errors. Fix them when convenient, because the report's "text changed" list is only a reliable record if the status matches what you did.

If you exclude a row, its children must be excluded too or moved to a new parent. Compile stops otherwise.

---

## 4. Blocks tab

One row per piece of content, in reading order.

### Columns

| Column | What to do |
|---|---|
| `id`, `page` | Tool-owned. Leave alone. |
| `review` | See section 3. |
| `type` | Correct it if DI got it wrong (see the types below). |
| `source_type` | `native` for normal PDF text; `image` for text read out of a picture. Correct it if wrong. |
| `content_kind` | **Tables and figures only**; an error on anything else. See 4.13. |
| `parent` | The ID of the heading or container this content sits under (see "Parents" below). |
| `label` | A run-in label or bullet lead-in, without the colon. For a figure or table, a short description. Blank for sections. |
| `text` | The printed text. For a section, the heading. For a `kv`, the label. Blank for tables. |
| `value` | **`kv` only**: the value as printed. Checkboxes are `[x]` or `[ ]`. |
| `level` | **Sections only**, and required on every section: `1` for a shaded section bar, `2` for a titled subsection. |
| `as_of` | Only where the block itself prints an as-of date. Enter it as printed. |
| `speaker` | Optional. See 4.12. |
| `applies_to` | **Footnotes only**. See 4.11. |
| `continues` | Only for the second half of something split by a page break. See 4.8. |
| `notes` | Anything worth telling the next reader. |

### Types

| Type | Use for | `text` | `label` | `value` | `level` |
|---|---|---|---|---|---|
| `section` | A heading: shaded bar (1) or titled subsection (2) | heading | blank | blank | 1 or 2 |
| `entry` | A dated sub-block, such as each date under Recent Developments | the date as printed (`Mar-2026`) | blank | blank | blank |
| `paragraph` | Prose | the text, without its run-in label | run-in label | blank | blank |
| `bullet` | A list item | the text, without its lead-in | lead-in | blank | blank |
| `kv` | A label/value pair in a form layout (Static Data) | the label | blank | the value | blank |
| `table` | Any grid; the content is in the Tables tab | blank | optional description | blank | blank |
| `figure` | A picture or screenshot region | blank | a description | blank | blank |
| `footnote` | A marked note (`*`, `(i)`) or a note under a table | the note | blank | blank | blank |
| `span` | Part of a paragraph attributed to someone else | the attributed words | blank | blank | blank |
| `furniture` | A running header or footer DI missed | as printed | blank | blank | blank |

### Parents

`parent` means "the container this sits under".

| This row | Parent |
|---|---|
| Level-1 section | blank |
| Level-2 section | its level-1 section. **`init` leaves every section's parent blank, so you set these.** |
| Content under a heading (`kv`, `paragraph`, `table`, `entry`) | the section, or the level-2 subsection, it sits under |
| Paragraph under a dated entry | the `entry` |
| Content inside a picture (a table or paragraphs read from an image) | the `figure` |
| `span` | the paragraph it's part of |
| `footnote` | the table (or section) it explains |

Nothing else is ever parented to a table. `init` proposes parents as "the nearest section above", which goes wrong whenever headings were merged or mistyped. Check parents after fixing the headings on a page.

Parents matter because **context flows down them.** An as-of date on a subsection applies to everything under it, and nothing else. A wrong parent silently gives content a date it isn't entitled to.

### Common situations

#### 4.1 A value holding several facts

Example: `Moody's Rating` → `Ba1/Stable 07-Nov-2025`, or `CREDAR(Prior/Final)` → `C06/C06`.

**Keep it as one `kv` row.** The page prints one pair, and the Blocks tab records what's printed. The splitting happens in the Fields tab (section 7): Moody's becomes three fields (rating, outlook, date) and CREDAR becomes two (prior, final), all pointing at the same block.

#### 4.2 A `kv` row and a paragraph repeating it

Example: row 1 is `kv` `Climate Risk Ratings Threshold Check` → `No`, and row 2 is a paragraph with the same label and text `No`.

**Keep the `kv` row and mark the paragraph `EXCLUDED`.** DI reports key-value text twice. The `kv` row is the useful copy, because it keeps the label and value paired, and the Fields row points at it. The same pattern showed up on page 1 for Total (Group) Exposure.

#### 4.3 Table content repeated as `kv` rows

Example: `Facility ID` → `7157371791`, `Seniority` → `Snr SecSnr Sec`.

These are a table's column headers turned into keys, with the table's values run together. The fix in `init` should stop them appearing. If they still show up, **mark every one `EXCLUDED` and keep the table.** First check the table's grid in the Tables tab is complete.

#### 4.4 Two headings merged into one row

Example: `Exposure Summary Lending Exposure (as of 30-Jan-2026)` as a single section.

**Split them.**

1. Edit the existing row down to the first heading (`Exposure Summary`, level 1, no as-of) and mark it `MODIFIED`.
2. Insert a row below it:
   - ID `h.…`, type `section`, level 2;
   - text `Lending Exposure (as of 30-Jan-2026)`;
   - `as_of` `30-Jan-2026`;
   - parent the level-1 row;
   - review `ADDED`.
3. Re-parent everything under the subsection (here, the facility table) to the new row.

The added row gets no coordinates. That's expected: the tool won't guess which half of the original region belongs to it.

#### 4.5 Content between or after dated subsections

Example: `Total (Group) Exposure (USDmm): 170.0` sits after the two "as of 30-Jan-2026" subsections but isn't inside either.

**Parent it to the level-1 section, and leave its `as_of` blank.** It must not inherit a date it doesn't print.

`Structured Hedges (USDmm): $58mm as of 2/28/2026` prints its own date, so it's a `kv` with `as_of` `2/28/2026`.

#### 4.6 A row with the wrong type

Example: `Structured Hedges` came back as a `section`.

Change the type (here to `kv`), move the text and value into the right columns, and mark it `MODIFIED`.

#### 4.7 OCR or transcription errors

Example: DI read `Ba 1`; the page prints `Ba1`.

Correct the cell and mark the row `MODIFIED`. The row keeps its coordinates, unless the new text is very different from DI's, in which case the report says the geometry was dropped.

#### 4.8 A paragraph or table split by a page break

DI gives you two rows, one per page.

- Keep both.
- On the **second** row, set `continues` to the first row's ID.
- Compile joins them into one block with both pages' coordinates.
- Don't paste the text together yourself.

For tables, the column counts must match. The continuation's repeated header rows are dropped, with a warning if they differ from the first table's.

#### 4.9 Dated entries (Recent Developments)

Each date line (`Mar-2026`, `Jan-2026`) is an `entry` row:

- the text is exactly as printed;
- the parent is the Recent Developments section;
- the paragraphs under each date are parented to that entry.

The date then flows to them automatically. Never type the date onto each paragraph.

#### 4.10 Run-in labels

For `Geopolitical Risks: Tariff risk is elevated…`, the label is `Geopolitical Risks` (no colon) and the text starts at `Tariff risk…`. The same applies to bullet lead-ins such as `Management Budget:`.

#### 4.11 Footnotes

A footnote is a `footnote` row parented to the table it explains.

- `applies_to` names what it explains: `row:Total Equity`, `col:Trading Level`, or a block ID. Separate several targets with `;`. Any text that picks out exactly one row or column label works.
- If the footnote moves a date (`* Market cap as of 23-Mar-2026`), put that date in its `as_of`. The date then applies to just that row or column.
- Two footnotes giving the same target different dates is a compile error.

#### 4.12 Speaker (optional)

Only annotate the obvious cases:

- the 1st Line of Defense section: `deal_team`, set once on the section;
- a rating-agency paragraph: `rating_agency:S&P` or `rating_agency:Moody's`;
- a clearly attributed sentence inside a paragraph ("According to a New York Post article…", "the Company has stated…"): add a `span` row with the attributed words, parent the paragraph, and speaker `press:New York Post` or `company`.

Allowed values are `author`, `deal_team`, `company`, `rating_agency:<name>`, `press:<name>` and `other:<name>`. A blank means *not annotated*, not "the author".

#### 4.13 Figures and image content

A pasted screenshot, financial model or chart is a `figure` row, with `source_type` `image`.

- Set `content_kind` from the list: `financial_model`, `capitalization_table`, `historical_financials`, `forecast_expected_case`, `downside_case`, `exposure_table`, `org_chart`, `chart`, `other_business`. It's required on every figure and every image-sourced table at `--final`.
- Put a short description in `label`, such as "FY24–FY28 expected case model".
- Tables and paragraphs DI read from inside the picture are its children (parent = the figure), with `source_type` `image`.
- Check OCR'd values carefully against the picture. That's where DI makes most of its mistakes.

#### 4.14 A header or footer that landed in Blocks

Change its type to `furniture`. Compile moves it out of the content.

#### 4.15 Empty rows

A row with nothing in it: mark it `EXCLUDED`.

---

## 5. Tables tab

Each table appears as a group of rows:

```
table_id | row_ref | kind | c0 | c1 | c2 | …
```

- The first row of each table has `kind` = `REF` and holds DI's column numbers. **Don't touch it.**
- `row_ref` is DI's row number. **Don't touch it on existing rows.** Leave it blank on rows you add.
- `kind` is `H` for a header row or `R` for a body row.
- `c0` is the row label (Cash, Total Debt, a facility ID).

**What you can do:**

- edit any cell to match the printed table;
- insert rows, with `row_ref` blank;
- delete rows or columns;
- insert columns (their REF cell stays blank).

Each table carries its own REF row, so inserting a sheet column doesn't break the other tables.

**What to check on each table:**

- the header rows match the printed headers, column for column;
- each printed row is one body row, with no rows split in two or merged;
- two-part values ("5.00% / 5.00%", "NIG Pass:100% / NIG Pass:100%") sit in **one** cell, as printed;
- no cell has run into its neighbour.

The table's review status, `content_kind`, label, parent and as-of live on its row in the **Blocks** tab. That review value covers every cell, so a corrected cell means the table's Blocks row is `MODIFIED`.

---

## 6. Furniture tab

Running headers, footers and page numbers. There's one row per occurrence, so expect about three per page.

- Confirm them. They're usually right, and filtering then filling down `CONFIRMED` is fine once you've spot-checked a few pages.
- If something here is actually content, set its `kind` to `content`. Compile moves it back into Blocks as a paragraph, with its coordinates.
- They still need reviewing for `--final`, because a content line wrongly left here would silently disappear from the gold.

---

## 7. Fields tab

The business data. `init` pre-fills one row for every field in the codebook, and **every row needs an answer.**

### Columns

| Column | What to do |
|---|---|
| `review` | `CONFIRMED` once you've given the row a status. `ADDED` on rows you copy for extra entities. `EXCLUDED` only for rows that shouldn't exist (see below). |
| `field_id` | From the codebook. Don't change it. |
| `entity` | Repeating fields only, as `<kind>:<key>`: `facility:71573`, `tranche:ABL`, `member:CR2439`. |
| `field_status` | `stated`, `absent` or `not_applicable` (below). |
| `verbatim` | The exact printed text the value comes from. |
| `source` | The ID of the block (or table) that text is in. |
| `row`, `col` | Table sources only: text that picks out exactly one row label and one column label. |
| `value` | **Usually blank.** The compiler works the value out from the verbatim using the codebook type. Fill it only when the verbatim needs interpreting, and it must still fit the type. |
| `notes` | Anything worth recording. |

### Status: stated, absent or not applicable

| Status | Meaning | `source` / `verbatim` |
|---|---|---|
| `stated` | The document states a value | both required |
| `absent` | The field could apply to this borrower, but this document doesn't state it | both blank |
| `not_applicable` | The concept doesn't apply here, or the document prints "N/A" | point at the printed N/A if there is one; otherwise blank |

**The test:** could this borrower have such a value, and the document just doesn't say? Then it's `absent`. If the question itself doesn't apply to this borrower, it's `not_applicable`.

**`absent` is not `EXCLUDED`.** An absent field is a real answer ("this document has no Fitch rating") and must reach the gold. Mark it `CONFIRMED`. Excluding the row drops the field entirely, and `--final` fails, because every codebook field needs a compiled record.

### Examples from page 1

| field_id | status | verbatim | source | row / col | compiles to |
|---|---|---|---|---|---|
| moodys_rating | stated | `Ba1` | Moody's `kv` | | "Ba1" |
| moodys_outlook | stated | `Stable` | Moody's `kv` | | "Stable" |
| moodys_rating_date | stated | `07-Nov-2025` | Moody's `kv` | | 2025-11-07 |
| credar_prior | stated | `C06` | CREDAR `kv` | | "C06" |
| credar_final | stated | `C06` | CREDAR `kv` | | "C06" |
| fitch_rating | absent | | | | null |
| authority | not_applicable | `N/A` | Authority `kv` | | null |
| leveraged_loan_flag | stated | `[x]` | Leveraged Loan `kv` | | true |
| admin_agent_role_flag | stated | `[ ]` | Admin Agent `kv` | | false |
| total_group_exposure | stated | `170.0` | Total Exposure `kv` | | 170.0, no as-of |
| facility_maturity | stated | `27-Aug-2030` | facility table | `71573` / `Maturity` | 2030-08-27 |

Points these illustrate:

- **Several fields from one block** is normal. The `field_id` says which part is which.
- **An unchecked box is `stated`** (`[ ]` → false). The document is saying no. A *blank* value is not false: if DI missed the box, type `[ ]` into the Blocks row and mark it `MODIFIED`.
- **Repeated text:** `C06` appears twice in `C06/C06`, so both CREDAR fields compile with no box on the page (`bbox: null`). That's expected, not an error; the block's own coordinates still hold.

### Repeating fields (facilities, tranches, members)

- The pre-filled row covers one entity. For each further facility or tranche, copy the row, set its `entity`, and mark the copy `ADDED`.
- Only one row per `field_id` may be something other than `ADDED` or `EXCLUDED`.
- Two live rows with the same `field_id` and `entity` is an error.

### When a field gets no coordinates

This is normal. It happens when:

- the verbatim appears more than once in its source;
- you corrected the text, so DI's words no longer match;
- the text runs across two pages.

The field still traces to its block or cell. You only lose the tight box around the characters.

---

## 8. Document tab

| Key | Who fills it |
|---|---|
| `doc_id`, `file_name`, `page_count`, `pdf_sha256`, `di_model`, `di_api_version`, `codebook_version` | The tool. Grey; don't edit. |
| `doc_type`, `title`, `borrower`, `header_date` | You, as printed. |
| `annotated_by`, `reviewed_by`, `reviewed_on` | You. `reviewed_by` and `reviewed_on` are required for `--final`. |

---

## 9. Compiling and reading the report

- `gold compile --work <work folder>` runs a **draft**. It writes the gold with `approved: false` if there are no errors, plus a report either way.
- `gold compile --work <work folder> --final --highlight` is the sign-off run. It also draws the highlighted review PDF.

**Errors** stop the compile, and no gold file is written. Fix them first.

**Warnings** don't block, but read them: text changed from DI, coordinates dropped, status mismatches, excluded rows, and values dropped when two rows were joined.

**`--final` additionally requires:**

- no `UNREVIEWED` rows in Blocks, Furniture or Fields;
- `content_kind` on every figure and image table;
- every codebook field compiled;
- `reviewed_by` and `reviewed_on` filled.

**Older gold files.** Every compile first moves any existing gold to `out/superseded/`. The gold in `out/` is always from the latest successful compile.

**The highlighted PDF** outlines every block, coloured by review status: green `CONFIRMED`, amber `MODIFIED`, blue `ADDED`, red `UNREVIEWED`, grey furniture. Field boxes are magenta. The last page lists what couldn't be drawn, in two lists: blocks without coordinates (always worth a look) and fields without boxes (usually routine).

---

## 10. Quick answers

| Question | Answer |
|---|---|
| Should I split "Ba1/Stable 07-Nov-2025" into separate rows? | No. One `kv` block, several Fields rows (4.1). |
| A field isn't in this document but could be in others. `absent` or `not_applicable`? | `absent`, marked `CONFIRMED` (section 7). |
| Should an absent field be `EXCLUDED`? | No. `EXCLUDED` drops it, and `--final` fails. |
| The Fields `value` column is blank. Is that OK? | Yes. The compiler works it out from the verbatim. |
| A checkbox value is blank in Blocks. Is it false? | No. Type `[ ]` and mark the row `MODIFIED`. |
| DI gave me a `kv` row and a paragraph saying the same thing. | Keep the `kv`, exclude the paragraph (4.2). |
| Two headings came out as one row. | Split them (4.4). |
| A section has no `level`. | Add it (1 or 2). Mark the row `CONFIRMED` if text and type were right. |
| A table's Blocks row has blank text. Is that wrong? | No. Tables keep their content in the Tables tab. |
| Section rows have nothing in `label`. Is that wrong? | No. The heading lives in `text`. |
| What ID do I give a row I add? | Anything unique starting `h.` (section 2). |
| What's the parent of a table? | The section or subsection it sits under. |
| What's the parent of rows printed below a table? | The heading they sit under, never the table (4.5). |
| Excel turned my entry into a date or number. | Retype it with a leading apostrophe (section 2). |
| I changed only `parent` or `level`. `CONFIRMED` or `MODIFIED`? | `CONFIRMED`. `MODIFIED` is for changes to text, value or type. |
