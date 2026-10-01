# Sentinel deck style, reusable Copilot prompt (v2)

**How to use.** Copy one task block (A or B), then paste it together with the full style specification below it as a single Copilot message in PowerPoint. Works best inside a deck already on the UBS Templafy master, which supplies the logo, footer, classification marking, and page numbers; do not ask Copilot to recreate those. Treat Copilot's first output as a draft and nudge slide by slide; decline Designer suggestions, which will fight this style. Save this whole file in your Copilot prompt library or notebook so the spec travels with the task blocks.

*v2 reconciles Copilot's own derived prompt against the locked RCOO Townhall deck: adopted its scaffold, title-slide layout, chart rules, font fallback, and reference-deck override; corrected its body sizes, palette, and anti-panel guidance, which did not match the source deck.*

---

## Task block A: build

> Create a [NUMBER]-slide PowerPoint presentation about [TOPIC] for [AUDIENCE], using [SOURCE MATERIAL]. The presentation's purpose is [PURPOSE].
>
> Follow the style specification below exactly. Pick the structure that fits each idea: stacked horizontal bands for an architecture or layered system, a horizontal timeline with diamond milestones for status or progression, two side-by-side panels for a comparison or a two-part value story, a vertical labeled flow for a step-by-step process, or a plain text block for a simple statement. One visual idea per slide.

## Task block B: reformat

> Reformat the selected slide (or this deck) to match the style specification below. Do not change the wording, meaning, or order of the content; change only layout, shapes, colors, fonts, sizes, and alignment.

---

## Style specification (paste in full with either task block)

Overall character: a minimalist, Swiss-inspired corporate style. Formal, understated, precise, and spacious: white ground, strict alignment to one grid, generous empty space, flat shapes, and restrained color. No oversized promotional headlines, no decorative fonts, no all-caps headings. Keep the deck's existing slide size and master theme; do not change them. Apply all of the following rules; where a rule cannot be applied exactly, get as close as possible and leave the content untouched.

**Typography**
- Font: Frutiger 45 Light for all text. If unavailable, use Segoe UI Semilight, then Arial.
- Slide title: one single line, 28 pt, black, sentence case. The title is a complete statement that carries the slide's message, never a topic label. Never let a title wrap to two lines; shorten the sentence instead.
- Subtitle: one sentence directly under the title, 14 pt, gray #6B6B6B.
- Panel and section headers: 12 to 14 pt, bold, red #E60000.
- Body text: 12 pt, dark gray #3A3A3A; it may scale up modestly on a sparse slide but never below 12 pt. Labels and captions 11 pt. Footnotes and legends 10 pt, never smaller. Whole-number font sizes only. Split dense content across slides rather than shrinking text.
- Default weight is light or regular. Bold is reserved for lead-in phrases, panel headers, and key labels, not whole sentences.
- Lead-in pattern for list items: a short bold phrase in near-black #1E1E1E ending with a period, followed by a plain description (example: "Organize the evidence. Find the relevant text, tables, and figures.").
- Italic gray is used only for captions, quiet qualifiers, and status words.

**Color (strict)**
- White slide background (#FFFFFF). Keep most of every slide white; avoid large colored backgrounds.
- Containers: light tan #ECEBE4 for panels, darker tan #B8B3A2 for emphasis bands and solid chips, pale cream #F5F0E1 for quiet full-width strips and soft fields, white for small content cards sitting on tan panels.
- Red #E60000 is reserved for exactly four uses: panel or section headers, small circular number badges, a "Today" or current-state marker, and a thin 1 to 1.5 pt outline marking the single most important element on the slide (the current item, the first application, the human decision point). Never use red for titles, body text, or as a fill for large shapes.
- Text: black titles, near-black #1E1E1E emphasis, #3A3A3A body, #6B6B6B muted.
- No other colors. No gradients, shadows, reflections, 3D effects, decorative icons or imagery, stock photos, or AI-themed graphics such as brains, chips, or sparkles.

**Title and section slides**
- Short left-aligned title roughly one third down the slide (about 40 pt for a deck title slide), with a one-line statement subtitle beneath it (about 24 pt, black) and a small gray context line under that (14 pt).
- Leave most of the lower half and the right side empty.
- The logo, footer, classification marking, and page numbers come from the master; never invent or recreate a logo. If a draft label is requested, place a small bold red "Draft" near the upper left.

**Layout grammar**
- Build content slides from flat rectangles: tan panels that group content, horizontal bands for layers, small white cards or chips for items, and thin full-width strips for closing statements. Square corners by default; rounded corners only for small pill-shaped callouts.
- Containers are structural, not reflexive. Use a panel when it groups a genuine unit of meaning; inside a container, prefer open zones separated by thin divider lines over boxes nested in boxes; a simple slide can be a plain text block or two clean columns with no container at all.
- Generous whitespace and a consistent grid: one left margin for everything, equal gutters between panels, aligned tops and bottoms. Footer elements small and unobtrusive.
- A pale full-width strip at the very bottom of a slide carries a single principle or ownership statement, with a bold lead word followed by plain text.
- Exactly one element per slide may carry the thin red outline. Dashed gray outlines mean future or placeholder items.
- Status encoding, used consistently: solid dark marker means complete; solid red marker means in execution now; white marker with red outline means next and imminent; white marker with gray outline on a dashed connector means a future sequence that is not yet dated. Diamond shapes for timeline milestones; a dashed vertical red line for "Today".
- Arrows are small, plain, and gray #6B6B6B, used only where flow is real (convergence, inheritance upward from a foundation, a sequence).
- Density target: 60 to 120 words of body per content slide, organized into panels and labels, never paragraphs.

**Charts and tables**
- Charts and tables are always native, editable objects, never pasted images.
- Chart series use the house neutrals (tans #B8B3A2 and #ECEBE4 and grays #6B6B6B and #3A3A3A); red #E60000 highlights only the single most important data point or series.
- Thin rules, minimal gridlines, no legends where direct labels work, no chart decoration.

**Content conventions**
- Clear, direct business language. Short descriptive headings; factual supporting text; never invent data.
- Read in sequence, the slide titles alone should tell the story.
- Bullets that are sentences take a capital letter and a period; single-word or label bullets take neither.
- Concrete claims, no hype adjectives, no hedging words.
- Never use an em dash anywhere; use commas, colons, or periods instead.
- Keep current state, designed state, and target state clearly distinguished in wording; never imply something exists because it is planned.

If a reference slide or deck is attached, prioritize its actual theme, font settings, margins, and layouts over these written approximations.

---

## Notes for yourself (not part of the paste)

- Copilot cannot change the slide size or theme fonts from chat, and it sometimes approximates exact hex values and point sizes. Pasting into the Templafy master solves most of that; fix stragglers by hand or re-prompt on the single slide.
- Corrections made to Copilot's own derivation of this style, kept here so they are not re-learned the hard way: body text is 12 pt dark gray, not 16 to 20 pt black; the supporting palette is the warm tan system, not generic grays; and the panel-band-card grammar is the style's signature, so "avoid boxes and panels" was wrong, while its kernel (no boxes nested in boxes, open zones inside containers) was kept.
- For precision builds of full decks in this style, the programmatic deck builder saved in the Sentinel project (claude/sentinel-townhall-deck-builder.md) remains the exact route; this prompt is for quick everyday decks and cleanups.
- The style originates from the locked Risk COO Townhall deck (v21, September 2026); if the house style evolves, update the hexes and the status encoding here first.
