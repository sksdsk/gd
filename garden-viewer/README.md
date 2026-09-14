# Wuhan garden — existing-site review R0

This is the Phase 1–3 review package, NOT the final garden design.
All local dimensions are assumptions. The supplied 25 × 10 m extent still needs confirmation.
Open docs/review.html for the evidence, uncertainties, and measurements requested.

## Run locally

From this folder:

    python -m http.server 8000

Then open http://localhost:8000 . Use a static server rather than opening index.html as a file.
No npm installation, backend, API key or CDN connection is needed.

## Deploy

Upload this folder's contents as static assets. Keep relative paths and filename case.
Works at a root or a subdirectory, including GitHub Pages. No SPA rewrite is needed.

## Files

- index.html, main.js, style.css: responsive Three.js viewer.
- models/existing-site.glb: the review model, metres, embedded PBR materials, named groups.
- site-config.json: feature evidence and provisional dimensions; north is unknown.
- docs/review.html: printable review document, with an uncertainty register.
- assets/plan.svg: schematic review plan, NOT a survey.
- assets/measurement-sheet.svg: mark-up sheet.
- vendor/: Three.js r180 and compatible modules, local imports; MIT license included.
- source/generate-model.mjs: reproducible GLB generator using the vendored exporter.

To regenerate the model after changing dimensions:

    node source/generate-model.mjs

The plan.svg, measurement sheet, report dimension table, and main.js camera/label positions are
review illustrations and must also be revised when geometry changes. They do not auto-update
from site-config.json. The model is deliberately a editable approximation, not a photogrammetric survey.

## Current scope

Clean existing geometry; selectable evidence notes; courtyard and top views; optional full-height
building proxy; existing vegetation layer; optional illustrative shadows; touch orbit/zoom/pan.
A/B/C landscape layouts, final plant schedules and Year 1/3/5 states are not yet authored:
the user requested a geometry review before the landscape design is fixed. The final principal
landscape model will be garden.glb after that review. No final design is hidden in this package.

## Checks and limits

GLB export and actual GLTFLoader parsing, geometry bounds and required named objects verified.
JavaScript syntax and local file references checked. A static geometry image was inspected.
No browser or physical iPhone/iPad/Android test was performed. Lighting is for legibility,
not solar analysis. Existing grades, underground drainage and retained plant identities are unknown.

Supplied photographs are included as project evidence, not as public stock assets. The hosted
review keeps owner-only access. Choose the audience deliberately if deploying this package elsewhere.
