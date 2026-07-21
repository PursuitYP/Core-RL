# Proposal Poster Plan and Requirement Checklist

## 1. User requirements

### Original request

- Read and understand all relevant material under `poster/`, including the proposal, team chat, both research reports, experiment/result directories, example posters, and both PowerPoint templates.
- Develop a detailed, coherent poster story covering the title, members, motivation, research question, setting, method, results, analysis, conclusion, limitations, and reproducibility.
- Build the poster on `poster_template.pptx`; existing text may be edited or removed.
- Use the member order in `Proposal.md`.
- Produce an academically professional poster.

### Supplemental requirements and decisions

- The poster must balance importance, academic rigor, clarity, and visual quality.
- Select evidence according to the poster narrative; do not compress all report material onto the page.
- Final poster language: English.
- Retain the descriptive working title and add non-stationarity.
- Use `poster_template.pptx` as the working source and `poster_template_base.pptx` only as an untouched reference.
- Do not add a QR code because the supplied public link does not cover both research lines; use a compact textual reproducibility note.
- Keep both source templates unchanged and write new final artifacts.
- Redesign request (revision 2): substantially restructure rather than patch the first version.
- Eliminate unintended overlap, crossings, and lines that pass through other elements.
- Use a restrained academic body palette. The earlier instruction to replace the bottom treatment was later corrected: the final poster must preserve the template's original bottom color element.
- Remove the dense, card-heavy "AI-generated" visual style; favor open whitespace, typography, rules, and a small number of meaningful figures.
- Reduce the number of elements and retain only evidence required by the argument.
- Replace the three-column body with a two-column layout.
- Improve the poster's narrative and presentation logic, not only its surface styling.
- Enrich the first column where open space remains, but add only method content that closes a real narrative gap; do not fill the page with generic background or decorative elements.
- After enriching the first column, re-review and refine the entire poster for narrative coherence, scientific reasonableness, clarity, balance, and visual quality rather than validating the edited area in isolation.
- Extend the divider below the RQ3 study description to the same full first-column width as the other study dividers.
- Review the poster from multiple reader roles: a reader with no RL background, a reader with introductory RL knowledge, an Alberta Plan/GVF expert, a strict scientific reviewer, and a visual/print reviewer; synthesize their likely objections and implement the highest-value corrections.
- Normalize vertical spacing across content blocks, especially the oversized gap below the motivation paragraph, and manually balance explanatory line breaks so each line is used well without adding filler; any added words must clarify experimental logic or interpretation.
- Apply the same spacing review to every poster element—not only the motivation block—including section transitions, study rows, figure/table captions, answer blocks, the conclusion band, and the preserved template footer.
- Rebalance the second-column result narrative specifically: the RQ1 answer must not crowd its table, while the RQ3 answer must not float too far below its evidence; review the complete RQ1/RQ2/RQ3 column after correcting both local cases.
- Expand each RQ answer only with meaningful interpretation so that all three occupy two well-filled lines—never a short orphan line and never a third line.
- Conduct another independent full-page review and improve the poster as a complete composition, explicitly including the upper institutional color band and lower blue-purple gradient as well as content logic, spacing, alignment, readability, and visual balance.

## 2. Locked poster specification

### Title and authors

**Title:** Exploring Useful Predictive Representations for Streaming RL under Partial Observability and Non-Stationarity

**Authors:** Mingzhu Li · Xinwei Song · Yuqi Wei · Peng Yu

### Core RL question

> When does predictive knowledge become a useful state representation for replay-free streaming control?

Operationally, the project asks what makes a GVF-derived representation preserve decision-critical hidden information and translate it into control gains.

The poster unifies two investigations:

1. Diagnose whether fixed predictive state is semantically informative and accessible to an online controller.
2. Construct a small, diversity-aware GVF bank whose complementary roles remain useful under drift.

### Narrative order

1. Partial observability creates a state problem: current observations omit distinctions needed for action.
2. GVFs can provide predictive state, but usefulness has distinct bottlenecks: information preservation, control accessibility, and adaptation under drift.
3. **Part A — Diagnose:** test fixed predictive representations across controlled POMDPs, then isolate accessibility in a trace-only T-maze while holding decoded cue information constant.
4. Establish the central mechanism: cue information can be perfectly decodable yet unusable by a linear controller; tile coding exposes the same information and approaches oracle control.
5. **Part B — Construct:** maintain a small, role-diverse GVF bank under drift and compare it with raw, single-GVF, and non-diverse alternatives.
6. Conclude conservatively: useful predictive state requires preserved information, an accessible interface to control, and complementary predictive roles that can adapt as the world changes.

## 3. Evidence ledger

| Poster claim | Source evidence | Exact poster value | Scope / caveat |
|---|---|---|---|
| No statistical/geometric condition wins across environments | Integrated Chinese report, cross-environment main matrix | T-maze non-oracle near chance; Ringworld mixed/high uncertainty; Two-loop moment shaping 0.797±0.068 vs raw 0.495±0.004; Hidden velocity raw -0.063±0.018 | 3 seeds per condition; descriptive, not a significance claim |
| Decodability is not sufficient for online control | Core T-maze diagnostic | Trace-only junction cue decodability = 1.00; oracle also = 1.00 | Diagnostic uses 3 seeds; offline probe never trains the agent |
| Tile coding exposes already-present information to linear control | Stage B1 paired adapter experiment | Identity 0.5165; RFF 0.5380; tile coding 0.9780; oracle identity 0.9835 | 10 paired seeds; fixed adapter, not new predictive learning |
| Complementary GVF bank improves post-switch control | Useful-GVF Table 1 | Raw 0.5073; cue GVF 0.5246; diverse bank k=3 0.5565 | Mean over 4 seeds; no supplied uncertainty values, so no significance language |
| Diversity is the key bank ingredient in the supplied ablation | Useful-GVF Table 2 | k=2 0.4950; k=3 0.5565; k=4 0.5408; k=3 without diversity 0.5196 | Mean over 4 seeds; describe as observed mean differences |
| The remedy is not universal | Integrated report and Useful-GVF discussion | No fixed adapter wins consistently in hidden velocity; moderate drift remains unresolved | Present as a boundary, not a secondary result panel |

### Evidence explicitly excluded

- Full ten-condition matrices, all correlation plots, runtime tables, and audit appendices.
- Meta-heuristic weight traces, role occupancy, transfer, and other secondary results.
- Any claim of statistical significance or universal causality not supported by the supplied summaries.
- Contextual severe-drift values because `useful_GVF.pdf` and `useful_GVF/main.tex` disagree (0.7231/0.7809 versus 0.6212/0.8661).

## 4. Layout and visual system

- Keep the original 60 × 90 cm portrait size and institutional logos; retain the template only where it helps identity.
- Preserve the template's lower blue-purple gradient and use it only as a restrained provenance/reproducibility footer.
- Reading path: full-width motivation/question opening → two-column body → full-width synthesis and provenance.
- Left column: motivation and bottleneck chain → delayed-cue running example → shared controller interface → three controlled studies → online GVF-bank mechanism → controls, readout logic, and rationale for the RQ sequence.
- Right column: evidence organized strictly as RQ1/RQ2/RQ3; each result states its controlled question, selected evidence, bounded answer, and evidential limit.
- Use one strong paired-seed figure, one compact geometry table, one compact bank-ablation table, one simple T-maze schematic, and one typography-led method flow; remove repeated mini-cards and decorative pills.
- Use editable PowerPoint shapes for concise diagrams and charts. Do not use connectors or rules that cross another object.
- Typeface: Arial. Final hierarchy uses a 51 pt title, 31 pt authors, 24–27 pt major headings, 16–18 pt primary body text, and 13.5–15.7 pt only for secondary labels, axes, and provenance.
- Palette: deep navy, muted blue, desaturated green, charcoal, and warm gray. Use accent colors sparingly and never as a full-width decorative gradient.
- Prefer open whitespace, square or very lightly rounded containers, thin rules, left alignment, and direct labels.
- Target materially fewer slide objects than revision 1 (216); visual simplicity takes priority over filling available space.

## 5. Final content blocks

- **Opening claim and RL question** — one compact, full-width opening that explains the state problem and asks when predictive state becomes useful for control.
- **Motivation and bottlenecks** — continuing partial observability requires predictive state to preserve the action-relevant distinction, expose it to the learner, and adapt compactly under drift.
- **Running example and study map** — delayed-cue T-maze, shared controller input, and the controlled variation/seed count for RQ1 geometry, RQ2 accessibility, and RQ3 bank structure.
- **Online bank mechanism** — generate interpretable semantic-role candidates and mixtures, score them using control-oriented streaming statistics, then retain and expose a compact diversity-aware bank.
- **RQ1 evidence** — cross-environment counterexamples rule out a universal geometry-only selection rule.
- **RQ2 main evidence** — trace-only cue decodability = 1.00, yet identity remains near chance; tile coding reaches 0.9780 and approaches the 0.9835 oracle over 10 paired seeds.
- **RQ3 evidence** — diverse k=3 has the highest supplied 4-seed control mean (0.5565), versus cue GVF 0.5246, raw 0.5073, and no-diversity 0.5196; k=4 decodes more but controls worse, and uncertainty was not supplied.
- **Controls and readout logic** — replay-free/online constraints plus the mapping from decoding to preservation, post-switch accuracy to control, and recovery to adaptation.
- **Interpretation and boundaries** — no universal geometry or fixed adapter; moderate drift remains unresolved; next step is joint bank/controller adaptation.
- **Take-home and reproducibility** — usefulness = preservation × accessibility × adaptive complementarity, plus concise seeds, commits, and streaming constraints.

## 6. Acceptance checklist

- [x] Source templates remain byte-for-byte unchanged.
- [x] Final PPTX is one slide at 60 × 90 cm and all images are embedded.
- [x] Title and author order exactly match the locked specification.
- [x] The core RL question is visible immediately below the header.
- [x] The first column forms a complete motivation → example → study design → bank mechanism → evaluation-logic sequence without generic filler.
- [x] All three first-column study dividers share the same x-position and full column width; the RQ3 divider is no shorter than RQ1/RQ2.
- [x] Every numeric claim matches the evidence ledger.
- [x] Seed counts and limitations appear next to the relevant results.
- [x] No conflicting contextual severe-drift numbers appear.
- [x] No text overflow, overlap, distortion, or unreadably small captions.
- [x] The A4-scaled preview retains the problem statement, experimental logic, all three RQ answers, and conclusion.
- [x] Full-page, both-column, A4-scale, and grayscale reviews preserve a clear reading order and balanced visual hierarchy.
- [x] Multi-role review covers no-RL readers, introductory-RL readers, Alberta Plan/GVF experts, strict scientific reviewers, and visual/print reviewers.
- [x] Exported PDF and preview PNG match the PPTX visually.
- [x] The poster supports a 3–5 minute explanation in the locked narrative order.

## 7. Completed local artifacts

- `poster_final.pptx` — editable one-slide PowerPoint poster.
- `poster_final.pdf` — print/share export at the template's 60 × 90 cm page size.
- `poster_final_preview.png` — 2268 × 3402 visual inspection preview.
- `build_poster.py` — deterministic poster builder using the supplied template and evidence package.

Exact rebuild/export commands (the Python environment must provide `python-pptx`):

```bash
python poster/build_poster.py
libreoffice --headless --convert-to pdf --outdir poster poster/poster_final.pptx
pdftoppm -png -r 96 -singlefile poster/poster_final.pdf poster/poster_final_preview
```

The repository's default shell Python and the currently registered `core-rl` environment do not provide `python-pptx`; use an environment that supplies that package before invoking the builder. The delivered PPTX/PDF/PNG do not depend on that environment for viewing or printing.

Current paper-structured audit: 142 slide objects, 111 non-empty text objects, one embedded raster result figure plus the template background, zero out-of-bounds objects, zero text-to-text overlaps, zero rule/text crossings, zero external relationships, valid PPTX archive, and no use of the conflicting contextual severe-drift values.

## 8. QA iteration log

Rounds 1–5 document the initial three-column implementation; rounds 6–9 document the user-requested two-column redesign that supersedes it.

### Round 1 — Scientific claims and evidence boundaries

- Rechecked every displayed value against the integrated geometry/adapter report and Useful-GVF tables.
- Added the strongest paired result: tile − identity = +0.4615 ± 0.0144 SEM, with improvement in 10/10 paired seeds.
- Tightened Ringworld wording to “some positive means; high seed uncertainty.”
- Kept the cross-environment audit explicitly descriptive at 3 seeds per condition.
- Excluded the conflicting contextual severe-drift numbers from all artifacts.

### Round 2 — Academic completeness and wording

- Defined general value functions (GVFs) on first explanatory use.
- Marked the GVF-bank panel as “4-seed means · uncertainty not supplied.”
- Changed the bank headline to “highest observed mean” rather than implying statistical significance.
- Made the next step explicit: jointly learn bank structure and controller coupling.
- Added provenance for the GVF-bank 4-seed summaries alongside the two verified commits.

### Round 3 — Visual and accessibility review

- Inspected the full poster and high-resolution crops of all three columns.
- Removed a right-column overlap found in the first render and regenerated the artifacts.
- Enlarged chart labels, perturbation tags, method labels, captions, and footer text.
- Verified an A4-scale overview preserves the title, core question, three findings, and take-home message.
- Verified a grayscale rendering remains understandable without relying on color alone.

### Round 4 — Technical portability and narrative rehearsal

- Independent LibreOffice export produced a pixel-identical preview (absolute pixel error = 0).
- PPTX validation: one slide, 59.9987 × 89.9971 cm, 216 objects, zero out-of-bounds objects, zero external relationships, and two embedded images (template background plus one experiment figure).
- PDF validation: one 60 × 90 cm page with embedded substitute fonts and correct title/author metadata.
- Confirmed all course-poster elements: RL question, motivation, environment, method, baselines, result/failure, interpretation, next step, and reproducibility.
- Rehearsed reading order fits approximately 4 minutes 20 seconds without covering secondary appendix material.

### Round 5 — Contrast, repeatability, and final freeze

- Audited text/background contrast across the light cards, header, result panels, and synthesis strip.
- Darkened the accessibility accent from bright orange to burnt orange (`#B45F06`) so orange labels retain clear contrast on white and pale-orange backgrounds.
- Re-exported the frozen PPTX independently and compared the rendered preview pixel by pixel; absolute pixel error remained 0.
- Re-ran archive and metadata checks: the PPTX has no compressed-data errors, and the PDF remains a one-page 60 × 90 cm poster with the locked title and author order.
- Recorded SHA-256 hashes for the plan, builder, PPTX, PDF, and preview at final verification time; no source template was overwritten.

### Round 6 — Narrative re-audit for the two-column redesign

- Re-read `Proposal.md`, `chat.txt`, the two integrated paper lines, and both supplied poster examples before restructuring the page.
- Reframed the story as one causal chain: partial observability creates a state problem → predictive state must preserve the hidden distinction → the controller must be able to access it → complementary predictive roles must adapt under drift.
- Replaced three equal-weight findings with two linked investigations: **Part A — Diagnose the bottleneck** and **Part B — Construct useful state under drift**.
- Demoted the cross-environment geometry screen to compact context and promoted the paired trace-only adapter experiment to the central mechanism result.
- Added an explicit Alberta Plan motivation to the opening and kept the bank result as constructive but uncertainty-limited evidence.

### Round 7 — Structural and visual redesign

- Replaced the three-column body with two open columns and a full-width opening and synthesis.
- Historical redesign step (later superseded by the corrected footer requirement): removed the lower blue-purple gradient, dark synthesis bar, rounded card grid, colored pills, repeated mini-panels, and secondary result tables.
- Restricted the page to one supplied experimental figure, one editable lollipop comparison, one compact T-maze, and one three-step method diagram.
- Reduced editable slide objects from 216 to 120 while preserving the environment, method, baselines, results, interpretation, limitations, and reproduction information.
- The first redesign render exposed an overlap in the four-step GVF workflow; the workflow was simplified to three steps and the result panel was repositioned.

### Round 8 — Spacing, accessibility, and overlap audit

- Inspected the complete poster at full resolution, at A4 scale, and in grayscale.
- A geometry audit initially detected four 0.02–0.06 inch text-boundary contacts that were visually subtle; every contact was separated and the audit now reports zero text-to-text overlaps.
- Confirmed zero out-of-bounds objects and no connector, divider, or rule passing through another content object.
- Darkened the neutral gray used for raw baselines and retained direct labels so the results remain interpretable without color.
- Historical redesign check (later superseded): confirmed the then-current off-white footer covered the original lower gradient; Revision 3 restored and retained the template gradient.

### Round 9 — Final scientific and technical freeze

- Verified every displayed numerical claim, seed count, author name/order, streaming constraint, limitation, and next step against the evidence ledger.
- Confirmed that none of the four conflicting contextual severe-drift values appears in the poster.
- Revised the bank wording to “matches the highest supplied post-switch mean” because the no-novelty ablation ties the full bank at 0.5565.
- Independent LibreOffice re-export is pixel-identical to the delivered preview (absolute pixel error = 0).
- Final validation: one 59.9987 × 89.9971 cm slide, 120 objects, two embedded media images including the template background, no external relationships, valid PPTX archive, embedded PDF fonts, and correct title/author metadata.

## 9. Revision 3 — Paper-structured narrative

### Additional user requirements

- Organize the poster as an academic paper rather than as two loosely parallel project summaries.
- Use explicit sections such as Motivation/Introduction, Running Example, Research Questions, Method, Experiment Design, Results, Interpretation, and Conclusion.
- Select experiments because they answer a stated research question; do not display results merely because they are available.
- Interpret the experiments at mechanism level and state meaningful, bounded conclusions.
- Avoid generic claims, superficial summaries, and conclusions stronger than the supplied seed counts and uncertainty support.
- Preserve the prior redesign constraints: two columns, restrained body palette, substantially reduced visual clutter, a clean footer treatment, and no overlaps or crossings.
- Treat the named paper sections as a reasoning guide, not a requirement to create many separate visual blocks. Merge the running example, method, and experiment design when that produces a clearer narrative.
- Use `流式部分可观测强化学习_整合论文_中文版.pdf` and `useful_GVF.pdf` as the authoritative narrative and early-analysis sources.
- Take displayed experiment evidence from each paper's corresponding result directory: `所有的运行结果/` for the geometry/adapter line and `useful_GVF/` for the GVF-bank line.
- Preserve the template's original color elements, including the institutional header/logos and the lower blue-purple gradient. Use the gradient as a restrained footer rather than covering it with a new visual system.
- Strengthen the first-column logic by explaining the online GVF-bank mechanism between RQ3's experiment definition and the shared experimental controls: structured candidate generation → control-oriented scoring → diversity-aware retention and exposure to the linear policy.
- Make the evaluation logic explicit in the same column: cue decodability diagnoses preservation, post-switch accuracy measures control utility, and recovery measures adaptation speed.

### Research-question-to-evidence map

#### RQ1 — Does improved predictive-feature geometry reliably improve control?

- **Test:** four controlled POMDPs × ten representation conditions × three seeds; compare conditions within each environment because accuracy and return are not cross-environment commensurate.
- **Selected evidence:** non-oracle T-maze results remain near chance; Two-loop moment shaping reaches 0.797±0.068 versus raw 0.495±0.004; Hidden velocity favors raw GVF at −0.063±0.018.
- **Interpretation:** the sign and magnitude of a transformation's effect depend on the hidden-state structure. Statistical or geometric regularity is therefore a diagnostic property, not an environment-independent selection rule.
- **Boundary:** n=3 per condition supports counterexamples and effect directions, not a universal ranking or significance claim.

#### RQ2 — If hidden information is decodable, can the online controller actually use it?

- **Test:** hold the trace-only predictive representation and online linear controller fixed; vary only the fixed input adapter (identity, residual RFF, or tile coding) over ten paired seeds.
- **Selected evidence:** junction cue decodability is 1.00; control accuracy is 0.5165 with identity, 0.5380 with RFF, and 0.9780 with tile coding, versus 0.9835 for oracle identity. Tile − identity is +0.4615±0.0144 SEM with 10/10 paired improvements.
- **Interpretation:** the controlled adapter intervention isolates an accessibility bottleneck. Tile coding adds no cue information; it exposes already-present information as local features that the same linear online learner can use.
- **Boundary:** no fixed adapter wins consistently in Hidden velocity, so this mechanism is demonstrated rather than universalized.

#### RQ3 — What bank structure converts predictive diversity into control under drift?

- **Test:** four-seed big-world T-maze comparison and bank ablation under cue corruption, distractors, variable timing, and remapping.
- **Baselines:** raw observation 0.5073 and cue GVF 0.5246 mean post-switch accuracy.
- **Selected ablation:** k=2: decodability 0.6483 / control 0.4950; k=3 full: 0.7294 / 0.5565; k=4 full: 0.7386 / 0.5408; k=3 no diversity: 0.6951 / 0.5196; k=3 no novelty: 0.7294 / 0.5565.
- **Interpretation:** the gain is structural, not simply more features or more novelty. k=3 balances complementary roles; k=4 decodes slightly more but controls worse, consistent with redundancy/interference; removing diversity costs 3.69 percentage points, while removing novelty has no observed marginal effect in this implementation.
- **Boundary:** only means over four seeds are supplied, so all bank comparisons remain descriptive.

### Revised paper-style reading order

1. **Motivation / Introduction:** predictive knowledge is proposed as agent state, but prediction quality, decodability, and control utility answer different questions.
2. **Running Example:** continuing delayed-cue T-maze and its big-world perturbations make the hidden-memory requirement and drift concrete.
3. **Research Questions:** RQ1 geometry, RQ2 accessibility, and RQ3 bank structure.
4. **Method:** controller input `x_t = [o_t, f(g_t), 1]`; fixed transformations/adapters diagnose the interface, while the online GVF bank generates, scores, retains, and exposes complementary predictions.
5. **Experiment Design:** three explicit studies, with controlled variations, held-fixed components, baselines, metrics, seeds, and streaming constraints.
6. **Results by RQ:** each result panel begins with its question and ends with a bounded answer.
7. **Conclusion:** useful predictive state must preserve action-relevant information, make it accessible to the learner, and maintain a compact non-redundant predictive basis under drift.

### Revised two-column allocation

- **Left column — Why and how we test it:** motivation, running example, research questions, controller interface, and the three controlled experiments in one continuous argument.
- **Right column — Evidence and interpretation:** results organized as RQ1/RQ2/RQ3, with the paired adapter plot as the central figure and a compact bank-ablation table.
- **Full-width bottom:** Conclusion, scope limitations, next step, and reproducibility/provenance.

## 10. Revision 3 QA log

### Round 10 — Source lock and experimental-question mapping

- Re-read the problem formulation, experiment design, core results, discussion, and conclusion in `流式部分可观测强化学习_整合论文_中文版.pdf` and `useful_GVF.pdf`.
- Locked the poster to three questions that follow the papers' logic: cross-environment geometry, control accessibility with fixed predictions, and bank structure under drift.
- Mapped each question to a controlled variation, held-fixed components, metric, seed count, selected evidence, interpretation, and boundary before editing the poster.
- Verified geometry values against `所有的运行结果/02_From_Predictive_Feature_Geometry_to_Control_Utilization__integrated_findings.zip`, including its 120-run main matrix.
- Verified adapter means and paired effects against `tables/stage_b1_key.tex`, `tables/stage_b1_full.tex`, and the supplied Stage B1 figure in the same result package.
- Verified bank baselines and ablations against `useful_GVF/main.tex` Tables 1–2 and the corresponding `useful_GVF/figures/` artifacts.

### Round 11 — Paper-style argument without section clutter

- Replaced the earlier “Part A / Part B” presentation with a continuous left-column argument: why prediction quality is insufficient, the delayed-cue example, the representation–controller interface, and the three controlled experiments.
- Organized the right column strictly by RQ1/RQ2/RQ3; every result now states the experiment, selected values, answer, interpretation, and evidential boundary.
- Added the k=4 counterexample: decodability rises from 0.7294 to 0.7386 while post-switch control falls from 0.5565 to 0.5408.
- Added the diversity and novelty ablations: removing diversity costs 3.69 percentage points, while removing novelty leaves the supplied mean unchanged.
- Rewrote the conclusion around the evidence: representation usefulness belongs to the representation–learner interface, not to predictive features in isolation.

### Round 12 — Template fidelity, density, and readability

- Kept the 60 × 90 cm template, institutional header, logos, and original lower blue-purple color band.
- Restricted template color to the header/footer while keeping the central reading field neutral and the body palette restrained.
- Inspected the full poster, both high-resolution column crops, an A4-scaled overview, and a grayscale version.
- Removed a detached metrics block and integrated its information into the experiment controls, reducing visual fragmentation.
- Final geometry audit reports 123 objects, zero text-to-text overlaps, zero out-of-bounds objects, and no rule or divider crossing content.

### Round 13 — Final scientific and rendering freeze

- Confirmed every displayed value, baseline, seed count, scope statement, and author name/order in the final PPTX.
- Confirmed that the four conflicting contextual severe-drift values remain absent.
- Confirmed that all bank claims are descriptive because the supplied four-seed summaries contain no uncertainty estimates.
- Independent LibreOffice re-export is pixel-identical to the delivered preview (absolute pixel error = 0).
- Final package remains one 59.9987 × 89.9971 cm slide with embedded media, no external relationships, a valid PPTX archive, embedded PDF fonts, and correct title/author metadata.

## 11. Revision 4 — First-column enrichment and whole-poster review

### Additional user requirements

- Use the remaining first-column space to strengthen the argument and content, not merely to enlarge decoration or repeat the right-column results.
- Preserve the restrained two-column paper structure, all no-overlap/no-crossing constraints, and the template's original lower blue-purple color band.
- After the local edit, reassess the complete poster for logical coherence, scientific accuracy, clarity, beauty, and balance; continue refining if the edit creates density, hierarchy, or readability problems elsewhere.

### Chosen narrative addition

The real gap was between the RQ3 study definition and the later bank ablation: the poster stated what was varied but not how the online bank worked. The first column therefore now adds the paper's three-step mechanism:

1. **Generate:** candidates cover memory, timing, control, and regime roles, with sparse semantic mixtures and lightweight horizon/step-size mutation.
2. **Score:** short-horizon streaming evidence rewards decision/decoding gains and uncertainty reduction while penalizing temporal-difference error and redundancy.
3. **Retain + expose:** diversity-aware selection keeps a compact bank of complementary GVFs, replenishes missing roles online, and exposes `[o_t, bank, 1]` to the streaming linear policy.

A compact readout map then closes the experiment-design loop: decoding diagnoses preservation, post-switch performance diagnoses control utility, and recovery diagnoses adaptation. POMDP, GVF, and RFF are expanded on first use so the richer column remains accessible.

## 12. Revision 4 QA log

### Round 14 — First-column logic and density

- Added the online-bank mechanism immediately after the RQ1/RQ2/RQ3 study map, where it connects the RQ3 intervention to the right-column ablation rather than interrupting the motivation or running example.
- Used typography, thin rules, and two small arrows instead of new cards, icons, or decorative containers; the poster remains visually restrained.
- Rebalanced the controls and sequence-rationale blocks and added the readout mapping, replacing unused vertical space with experiment logic while retaining breathing room before the conclusion.
- Inspected a 144-dpi first-column crop after each substantive edit; all method stages, labels, arrows, and explanatory lines remain legible and separated.

### Round 15 — Whole-poster scientific and visual review

- Re-audited the full argument as a one-to-one chain: core RL question → preservation/exposure/adaptation bottlenecks → three controlled RQs → three bounded answers → interface-level conclusion.
- Confirmed the new method content comes from `useful_GVF/main.tex` and does not introduce claims beyond the supplied paper: semantic-role generation, control-oriented scoring, diversity-aware retention, and online replenishment.
- Rechecked the selected results and interpretation boundaries: RQ1 remains descriptive at three seeds per condition, RQ2 uses ten paired seeds and the fixed-prediction adapter intervention, and RQ3 reports only supplied four-seed means without significance language.
- Inspected the final full page, both column crops, an A4-scaled overview, and a grayscale rendering. The title/problem/three RQs/conclusion remain visible at overview scale; the main paired-seed figure still owns the strongest visual emphasis; color is not required to recover the argument.
- Expanded partially observable Markov decision process (POMDP), general value function (GVF), and residual random Fourier features (RFF) on first use; removed an avoidable readout-line wrap and separated the T-maze branch rule from the junction box.

### Round 16 — Final technical and rendering freeze

- Final PPTX: one 59.9987 × 89.9971 cm slide, 139 objects, 108 text objects, two embedded media files (template background and paired-seed result figure), zero out-of-bounds objects, zero text-to-text overlaps, zero rule/text crossings, zero external relationships, and a valid ZIP archive.
- Final PDF: one 60 × 90 cm page with embedded fonts, correct title and author metadata, and no occurrence of the four excluded conflicting values (0.7231, 0.7809, 0.6212, 0.8661).
- Final preview: 2268 × 3402 pixels. An independent LibreOffice export rendered pixel-identically to the delivered preview (absolute pixel error = 0).
- Source-template hashes remain `7c3e921f…` for `poster_template.pptx` and `9e528c40…` for `poster_template_base.pptx`; neither source template was overwritten.

## 13. Revision 5 — Divider alignment and multi-role audit

### Additional user requirements

- Extend the divider below **RQ3 · Bank structure under drift** leftward so that it is the same overall length as the other study dividers.
- Go beyond a local correction and interrogate the complete poster from several perspectives: a reader with no RL background, a reader with basic RL knowledge, a Sutton/Alberta Plan expert, a strict reviewer, and a visual/print reviewer.
- Use the combined audit to keep improving content, logic, clarity, professionalism, aesthetics, and typography rather than merely reporting possible concerns.

### Multi-role findings and implemented responses

| Reader role | Main concern found | Implemented response | Resulting assessment |
|---|---|---|---|
| No RL background | The T-maze could be mistaken for a classification diagram; GVF, oracle, decodability, and the control objective were not plain enough | Added a compact RL-task line (cue/aliased corridor/junction action/correctness feedback/continuing objective), described GVFs as learned forecasts of cue/timing/regime, labeled the oracle as a direct-cue condition, added chance to the 0.50 result, and changed the opening to “Accurate prediction ≠ useful control state” | The main problem, intervention, strongest result, and conclusion are understandable without reading the equation; RFF/SEM remain optional technical detail |
| Introductory RL knowledge | It was possible to miss what was held fixed and why the RQs form a causal sequence | Kept seed counts beside each study, shortened designs to emphasize the varied factor, retained “same `g_t` and learner; only `f` changes,” and clarified the RQ1→RQ2→RQ3 rationale | A reader can now explain environment, intervention, baseline, metric, and answer for each RQ |
| Sutton/Alberta Plan/GVF expert | The poster needed to show value beyond “one method scored higher” and to admit where autonomy is still limited | Centered the Alberta Plan state question, one-pass continual interaction, fixed-prediction accessibility intervention, k=4 decoding/control counterexample, and diversity ablation; added “hand-structured GVF roles” to scope and joint bank/controller adaptation as the next step | Scientifically meaningful as a focused empirical/mechanism study and diagnostic counterexample, while explicitly not presented as a universal theorem or fully autonomous discovery system |
| Strict scientific reviewer | The categorical conclusion, “best explains” wording, single-row k=3 highlight, and low-seed RQ3 evidence could overstate the result | Scoped the conclusion to “these streaming POMDPs,” changed RQ3 to “supplied means favor,” highlighted both tied 0.5565 rows, retained uncertainty-not-supplied beside RQ3, and kept n=3/4 results descriptive | Claims now match the interventions and supplied uncertainty; the main remaining weakness is acknowledged small-sample, structured-benchmark evidence |
| Visual / print reviewer | RQ3's divider was visibly shorter; text density was high; a few secondary labels approached the lower readable bound | Set all study dividers to `x=0.92 in`, `width=8.92 in`; reduced extracted text from about 855 to 792 words; enlarged table/answer/control text; retained a 51 pt title, 22–27 pt major statements, 14.8–16.6 pt primary body text, and 13.2–14.5 pt secondary labels | The two columns are balanced, the central paired-seed plot remains the dominant figure, and the argument survives A4 and grayscale viewing without relying on decorative cards |

### Consolidated judgment

- **No-RL reader:** can understand the delayed-memory problem and headline conclusion; the detailed adapter and uncertainty notation is intentionally secondary.
- **Introductory-RL reader:** can follow the controlled-comparison logic and should find the “decodable but unusable” result instructive.
- **Expert reader:** the value lies in separating state content from learner accessibility and showing that more decodable predictive state can still reduce control; the poster is honest that the bank uses hand-structured roles and small supplied seed sets.
- **Strict reviewer:** the poster is professional and evidence-bounded; it makes mechanism-level claims supported by controlled counterexamples rather than significance or universality claims.
- **Visual reviewer:** the page is denser than a purely promotional poster but appropriate for an academic project poster; one main plot, two compact tables, restrained color, and open separators maintain hierarchy.

## 14. Revision 5 QA log

### Round 17 — Divider and geometry correction

- Changed the shared study-row divider to span the complete first-column width and aligned all three at `x=0.92 in`, `width=8.92 in`; RQ1, RQ2, and RQ3 now end at the same position.
- The first RL-task-caption attempt touched the lower T-maze labels; shortened the lower branch and repositioned `turn R` / `aliased corridor` instead of hiding the problem with a smaller body font.
- Rebuilt and re-audited until there were zero text overlaps and zero rule/text crossings.

### Round 18 — Accessibility and reviewer rigor

- Replaced the abstract “Prediction quality is not representation utility” with “Accurate prediction ≠ useful control state.”
- Added plain-language task, forecast, chance, and oracle explanations while preserving POMDP/GVF/RFF expansions.
- Reworded RQ1 from “better-looking geometry” to the testable intervention “reshaping predictive features.”
- Recast the RQ2 answer around local sparse features and the fixed learner, and bounded RQ3/conclusion language to the supplied means and streaming POMDP scope.
- Highlighted both `k=3 full` and `k=3, no novelty`, since they tie at 0.5565; this makes the no-observed-novelty-effect result visually honest.

### Round 19 — Density and typography

- Compared both supplied example posters at their common 60 × 90 cm page size and used them as density/hierarchy references without copying their visual systems.
- Removed repeated prose from motivation, controls, study descriptions, answer blocks, and sequence rationale; extracted word count fell from approximately 855 to 792 while every selected numeric result and evidence boundary remained.
- Increased geometry/bank table text, controls, RQ answers, result bullets, conclusion evidence, and scope text. The smallest editable text is 13.2 pt and is limited to compact T-maze labels; primary body text is predominantly 14.8–16.6 pt.
- Re-inspected the full page, both 144-dpi columns, A4 overview, and grayscale view; reading order and the visual dominance of the paired-seed result remain intact.

### Round 20 — Final technical freeze

- Final PPTX remains one 59.9987 × 89.9971 cm slide with 139 objects, 108 text objects, two embedded media files, zero out-of-bounds objects, zero text overlaps, zero rule/text crossings, zero external relationships, and a valid archive.
- Final PDF is one 60 × 90 cm page with embedded fonts and correct title/author metadata; the four excluded conflicting values remain absent.
- Final preview is 2268 × 3402 pixels. A fresh independent LibreOffice export is pixel-identical to the delivered preview (absolute pixel error = 0).
- Template header/logos and the original lower blue-purple gradient remain unchanged; both source templates retain their recorded hashes.

## 15. Revision 6 — Whole-poster spacing and line-balance pass

### Additional user requirements

- Correct the visibly oversized gap below the motivation paragraph.
- Check and refine the spacing of all other content and visual elements across the poster.
- Let explanatory copy use the available line width naturally, but never add generic or redundant text merely to fill a line.

### Spacing system and implemented changes

- Rewrote the motivation paragraph as four balanced lines that state a substantive chain: Alberta Plan framing → POMDP hidden information → controller accessibility → the preservation/accessibility/adaptation decomposition.
- Moved the three-stage bottleneck directly beneath that paragraph and shifted the running example, study map, online-bank mechanism, controls, and sequence rationale upward as a coordinated group. This removed the isolated blank band without compressing any single block.
- Rebalanced the RQ1/RQ2/RQ3 study descriptions around information that matters for interpretation: within-environment comparison for non-commensurate metrics, the fixed representation/learner in the adapter intervention, and the bank factors plus raw/single-GVF baselines under drift.
- Balanced the GVF/RFF definitions, experimental-control lines, and RQ sequence explanation so their last lines no longer appear as accidental fragments.
- Kept a repeatable vertical rhythm: ordinary divider-to-label transitions are approximately 0.26–0.27 in; larger method transitions are approximately 0.34–0.39 in; heading-to-body gaps are approximately 0.04–0.10 in; answer-to-next-divider gaps remain approximately 0.10–0.24 in.
- Reviewed the right-column result tables, paired-seed figure, captions, answer blocks, conclusion band, and footer independently. No decorative block or filler sentence was added; all additional wording clarifies the intervention, comparison, or interpretation.

## 16. Revision 6 QA log

### Round 21 — Render-driven overflow correction

- The first line-balancing attempt passed the geometric audit but LibreOffice reflowed the motivation text into the bottleneck labels. The rendered page, rather than the object coordinates alone, exposed the issue.
- Rewrote the paragraph to a stable four-line form, increased its effective text allowance, and repositioned the downstream blocks. A fresh render shows clear separation between the paragraph and the preserve/expose/adapt chain.

### Round 22 — Full-page visual spacing review

- Inspected the full 144-dpi poster, a dedicated first-column crop, a dedicated right-column crop, the conclusion/footer crop, an A4-scale overview, and a grayscale rendering.
- Confirmed that the header, problem statement, motivation, running example, three study definitions, online-bank mechanism, result table/plot hierarchy, conclusion, and footer each have distinct visual boundaries.
- Confirmed that RQ1/RQ2/RQ3 retain consistent question → evidence → bounded-answer spacing and that the paired-seed figure remains the dominant result rather than being crowded by surrounding text.
- Confirmed that the conclusion remains visually separated from both columns and from the original blue-purple footer, while the footer's three provenance blocks remain aligned and readable.

### Round 23 — Final geometry and content targets

- Confirmed package: one 59.9987 × 89.9971 cm slide, 139 objects, 108 non-empty text objects, and two embedded media files.
- Confirmed geometry: zero out-of-bounds objects, zero text-to-text overlaps, zero rule/text crossings, zero external relationships, and a valid PPTX archive.
- The revised poster contains approximately 832 extracted words; the increase from Revision 5 is limited to meaningful experimental logic and interpretation, not filler.
- Preserve all source-locked values, author order, title, template header/logos, and lower blue-purple gradient; keep the four conflicting contextual values absent.
- Confirmed PDF/preview: one 60 × 90 cm PDF page with embedded fonts and correct title/author metadata, plus a 2268 × 3402 PNG preview.
- A fresh isolated LibreOffice export is pixel-identical to the prior spacing-review export at 144 dpi (absolute pixel error = 0).
- Revision 6 artifact hashes: PPTX `a574275c35265a913e548587e111d1bd30e48d51e06cf7829df089f3be4dba41`; PDF `bc009a8afd5a7f2ee1028a0da3552e243bdbe67fff8f96dfede37e792a6ef3c6`; preview `161566b109629d21aedb41ad56a04801a05a68850ddf94dd58c821ecd5e49184`.

## 17. Revision 7 — Second-column rhythm and two-line answers

### Additional user requirements

- Increase the gap between the RQ1 table and its answer.
- Remove the excessive gap before the RQ3 answer and reassess spacing throughout the second column.
- Add a few substantive words where useful so that each RQ answer fills exactly two lines without wrapping to a third.

### Implemented answer copy

- **RQ1:** makes the three-seed boundary do interpretive work: the results support counterexamples to a universal geometry ranking rather than a general ranking claim.
- **RQ2:** states the controlled mechanism more explicitly: local sparse features expose the retained cue to the fixed linear learner, so the gain is accessibility rather than added predictive information.
- **RQ3:** makes the k=4 counterexample explicit: higher decodability can still add redundancy or interference instead of improving control.
- Manual line breaks lock each answer to two semantically complete, visually balanced lines in LibreOffice/PDF output.

### Rebalanced second-column spacing

- Measured from the PDF's rendered text bounds, the last evidence line → answer first line gaps are now **0.268 in (RQ1)**, **0.298 in (RQ2)**, and **0.294 in (RQ3)**.
- Increased the RQ1 answer → section-divider gap from approximately 0.12 in to **0.281 in**.
- Shifted RQ2 and RQ3 downward together by 0.16 in rather than moving isolated objects; RQ2 retains its full-size central plot and its answer → divider gap is **0.343 in**.
- The RQ3 answer ends **0.404 in** above the full-width conclusion rule, giving the final result block a clear close without reopening the earlier empty band.
- Kept the conclusion and preserved template footer visually separated; the lower blue-purple gradient remains unchanged.

## 18. Revision 7 QA log

### Round 24 — Rendered line-count and spacing audit

- Used PDF word bounding boxes rather than PowerPoint textbox coordinates to verify the visible line count and spacing after LibreOffice reflow.
- Confirmed all three answers render as exactly two lines with no orphaned sample-size line and no third-line wrap.
- Inspected the high-resolution right-column crop, full-page render, A4-scale overview, and grayscale rendering; RQ1/RQ2/RQ3 retain a consistent question → evidence → answer → transition rhythm.

### Round 25 — Hidden-boundary correction

- The first geometric pass found a 0.08 in overlap between the RQ3 bullet textbox boundary and the answer textbox boundary, even though the visible glyphs were separated.
- Reduced only the unused height of the three-line bullet textbox. The before/after 144-dpi renders are pixel-identical (absolute pixel error = 0), while the final geometry audit returns zero text overlaps.

### Round 26 — Final freeze

- Final package: one 59.9987 × 89.9971 cm slide, 139 objects, 108 non-empty text objects, and two embedded media files.
- Final geometry: zero out-of-bounds objects, zero text-to-text overlaps, zero rule/text crossings, zero external relationships, and a valid PPTX archive.
- Final PDF: one 60 × 90 cm page with embedded fonts and correct title/author metadata; extracted word count is approximately 847 and the four excluded contextual values remain absent.
- A fresh isolated LibreOffice export is pixel-identical at both 144 dpi and 96 dpi (absolute pixel error = 0).
- Final artifact hashes: PPTX `02ec569ee3c4a5118e90b225b73be51eb602fbc9e2726e446cf18625b852b6e2`; PDF `f0334dc765eb6bfa63966b2b4bf7f6a77e27f09b432884832263b23c4bac64ad`; preview `2ca8251d748bb9f6839a204b450b812d2121b4a14ccfe283e89897aa9c868bc5`.

## 19. Revision 8 — Full-page composition and colored-band review

### Additional user requirement

- Perform another deep independent review of the complete poster and implement useful improvements, including the upper and lower colored regions, content spacing, narrative logic, visual balance, and aesthetics.

### Full-page findings and responses

| Area | Finding | Implemented response |
|---|---|---|
| Upper template band | The logo row, title, authors, and lower color boundary were already well balanced, but the two 51 pt title lines were slightly tight | Preserved every template logo/color element and all x/y anchors; increased title line spacing from 0.90 to 0.94. Rendered title-to-author and author-to-boundary gaps remain approximately 0.86 in and 0.99 in |
| Opening question | “Become useful state” was grammatically awkward and less precise for both RL and non-RL readers | Recast the question as “When does predictive knowledge become a useful state representation for replay-free streaming control?” and aligned the hypothesis to action-relevant distinctions |
| Two-column body | The preceding revision had already normalized RQ evidence/answer spacing and exact two-line answers | Preserved the body geometry instead of introducing low-value movement; rechecked both columns at full, crop, A4, and grayscale scales |
| Conclusion | The evidence sentence was accurate but syntactically dense | Rewrote it as a parallel contrast: same cue information, better access (0.5165 → 0.9780); more decodability, worse control (k=4 versus k=3) |
| Lower template band | Three multi-line footer boxes were vertically centered independently, so their headings appeared at three different heights and the complete group sat too high in the gradient | Split each footer block into a bold heading plus body, aligned all headings, and moved the group to the visual center without changing the original blue-purple gradient or provenance content |

### Multi-role judgment after the revision

- **No-RL reader:** the displayed question now defines the target as a state representation rather than assuming “state” is self-explanatory; the preserve/expose/adapt chain still provides the plain-language reading path.
- **Introductory RL reader:** the question, controlled interventions, paired-seed evidence, and scoped answers remain connected without adding another conceptual layer.
- **Alberta Plan/GVF expert:** the interface-level claim, streaming constraints, k=4 counterexample, hand-structured-role limitation, and adaptation next step remain explicit.
- **Strict reviewer:** no uncertainty or universality claim was strengthened; the revised conclusion is shorter but retains both empirical counterexamples.
- **Visual/print reviewer:** the template bands now function as balanced anchors, the body remains the main reading field, and grayscale/A4 views preserve hierarchy and contrast.

## 20. Revision 8 QA log

### Round 27 — Colored-band geometry

- PDF text bounds place both title lines at 2.337–4.056 in, authors at 4.913–5.473 in, and the color boundary at 6.46 in; the title remains clear of the institutional logos and visually centered in the original header.
- All footer headings now share the exact rendered y-range 33.525–33.774 in.
- The complete footer text group spans 33.525–34.499 in inside the 32.58–35.43 in gradient, leaving approximately 0.945 in above and 0.931 in below: effectively centered.

### Round 28 — Full-page narrative and scale review

- Inspected the high-resolution full page, upper band, opening, both body columns, conclusion/lower band, A4-scale overview, and grayscale rendering.
- Confirmed that the new question stays on one line, the hypothesis stays on one line, the three RQ answers remain exactly two lines, and the conclusion evidence remains one concise line.
- Confirmed that the central paired-seed plot remains the dominant evidence and that the stronger footer hierarchy does not compete with the scientific body.

### Round 29 — Final freeze

- Final package: one 59.9987 × 89.9971 cm slide, 142 objects, 111 non-empty text objects, and two embedded media files.
- Final geometry: zero out-of-bounds objects, zero text-to-text overlaps, zero rule/text crossings, zero external relationships, and a valid PPTX archive.
- Final PDF: one 60 × 90 cm page with embedded fonts, correct title/author metadata, approximately 845 extracted words, and none of the four excluded contextual values.
- Independent isolated LibreOffice exports are pixel-identical at both 144 dpi and 96 dpi (absolute pixel error = 0).
- Source templates remain unchanged at `7c3e921f…` and `9e528c40…`.
- Final artifact hashes: PPTX `25a119b14b040dc5ed4099b810747ade8bf8b810a75d30a881e7891b7be9f57d`; PDF `820ff88d64b12f7d0d54dd131ca8c778682a5fe53366250545ac3dd60dbf2879`; preview `e851f6ac5033721a371b3f90ccc0b95951e9bbf56f884a00d2f760d9175b2dba`.
