# garden · 两院一径 R1

Pure static Three.js garden study, no backend or CDN runtime dependency.

## Open locally

Unzip, enter this folder, and run:

    python -m http.server 8000

Open http://localhost:8000. Do not open index.html via file://: browser security prevents GLB/JSON loading that way.

## Deliverables

- index.html / main.js / style.css: responsive Three.js viewer.
- models/garden.glb: recommended B, Year 3, summer. Metres, Y up; +X south, +Z west.
- models/existing-site.glb: clean calibrated existing site.
- models/design-A-year*.glb, design-B-year1/5.glb, design-C-year*.glb: all alternatives and years.
- docs/design.html: complete printable design document; includes site reconstruction, uncertainties, alternatives, climate sources, planting schedule, group quantities/spacing, privacy, drainage, seasons and annual care.
- assets/plan-existing.svg, plan-A/B/C.svg: matching vector plans.
- assets/masterplan-B.png: readable raster master plan.
- plants.json / layouts.json / site-config.json: plant information, exact model coordinates and dimension evidence.
- models/validation.json: scope and results of data/geometry verification; no browser/device test claim.

The outer dimensions follow the owner's annotated diagram. Local planter dimensions, passage width, door/window positions, levels and drainage are still explicit assumptions. The garden is a concept master plan, not a surveyed construction model.

## Viewer

Orbit by one finger/left drag, zoom with pinch/wheel, pan with two fingers/right drag or arrow keys when the canvas has focus. Select plants by tapping or use the text dropdown. Switch Existing/A/B/C, Year 1/3/5 and seasonal appearance. Shadows are optional; full building is hidden by default for a readable cutaway. Geometry loads only when selected. GLBs keep names, PBR materials and plant metadata; seasonal variants are controlled by tagged groups in this viewer. Generic GLB viewers show the default summer state.

## Deploy elsewhere

Upload this folder's static contents to a static host. index.html must be at its public root. GitHub Pages can publish this folder/repository root; on Netlify/Cloudflare Pages/Vercel select a static project and the folder containing index.html as output. No API keys or environment variables are required. All runtime imports and assets use relative local paths, including at a repository subpath. Hosting availability and account restrictions in mainland China have not been tested.

## Rebuild the models

Node.js and Python 3 are needed only for rebuilding, not for hosting. Three.js is vendored.

    python source/prepare-design.py
    node source/build-model.mjs
    node source/build-designs.mjs
    python source/build-docs-r1.py
    node source/validate.mjs

Edit the dimensions and planting definitions in source/prepare-design.py before rebuilding. It regenerates the JSON design inputs. The measured/assumed distinction must be maintained. Existing geometry is in source/build-model.mjs and proposed geometry in source/build-designs.mjs. Preview PNGs are supplied snapshots; updating GLBs does not automatically redraw those PNGs.

Materials are procedural solid PBR colors, with brick joints represented geometrically; no photographed texture is missing. Plant forms and growth are schematic. Three.js r180 is supplied under the MIT license in vendor/THREE-LICENSE.txt. Property photographs belong to the supplied evidence.
