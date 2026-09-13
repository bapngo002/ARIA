# ARIA custom sculpt workspace

## Current selection: R4 restored

Owner rejected R5 as too dark and requested the first brow correction. Launcher now opens unchanged `aria-head-r4.blend`; R5 remains for comparison. No geometry was regenerated. Next: hair.

## Historical: stronger brow density R5

`aria-head-r5.blend` adds a dark fitted underlayer and 2,200 strands with a wider body following owner rejection of pale/thin R4. Front render inspected; three views saved as `head-r5-*.png`. Static fit only, owner review pending. Builder `tools/avatar/refine_brows_r5.py` overwrites R5 from preserved R4; save later manual edits separately. Launcher opens R5.

## Previous: fuller brows R4

`aria-head-r4.blend` widens and densifies the brows following the owner close-up (1,400 tapered strands), preserving R3 face and lid geometry. Three renders: `head-r4-*.png`; front visually checked. Static fit only; likeness and expression behavior still need review. Builder: `tools/avatar/refine_brows_r4.py`, which overwrites R4 from preserved R3. Launcher opens R4. Next: hair silhouette.

## Previous: brows and eyelid details R3

Owner accepts R2 as the face direction. `aria-head-r3.blend` keeps those proportions unchanged and adds individually tapered surface-fitted brows, subtle lid margins and upper lashes. Three actual Blender renders are `head-r3-front.png`, `head-r3-three-quarter.png` and `head-r3-profile.png`; all inspected. Static fit is partially verified; expression contact and rigging are not. Hair, skin, clothing and final likeness remain pending. Next: long dark hair shape and layered locks.

`tools/avatar/refine_head_r3.py` rebuilds R3 from preserved R2, overwriting R3 only; save later manual work under a different name first. The launcher opens R3 with the isolated MPFB profile. The browser remains the old rejected avatar.

## Previous: eyes and profile R2

`aria-head-r2.blend` preserves R1 and adds static warm-ivory eyeballs, curved brown iris/pupil caps, restrained reflections, bilateral eyelid-height adjustments and small nose-tip/upper-lip targets. Eye centers derive from MPFB joint landmarks; radius and settings are in `head-r2-report.json`. `tools/avatar/refine_head_r2.py` rebuilds this file from R1 and replaces R2, so preserve manual work under a new name before running it.

Front, three-quarter and profile review images are `head-r2-*.png`. These are actual Blender renders with clay skin. Static fitting is only partially verified; eye movement/blink, tearline, eyebrows/eyelashes, hair, skin textures and likeness acceptance remain pending. Procedural iris materials are a study, not final photoreal eye shading. The launcher now opens R2; browser preview remains the earlier rejected model.

## Previous: head proportions R1

Open `aria-head-blockout-r1.blend` or the ARIA Blender launcher. This file keeps 13 editable MPFB face targets, temporary eye-fitting spheres and subdivision smoothing. It is a first proportion study, not an accepted likeness or completed sculpt. Settings are in `head-r1-report.json`; builder is `tools/avatar/sculpt_head_blockout.py`. The builder recreates R1 from the preserved base, so save future manual edits under a new revision before rebuilding.

Compare `head-before-front.png` with `head-r1-front.png` under the same clay material/camera/light; R1 also has `head-r1-three-quarter.png` and `head-r1-profile.png`. The before render resets only the new face targets; it retains the same smoothing and temporary eyes for comparison. Hair, skin textures, fitted eyes, clothing and rigging are not completed. The localhost preview has not been switched to this model.

## Human-base preparation

`aria-human-base.blend` now contains an unsculpted adult-female MPFB base plus the packed references. This is a different human base from the rejected pixiv anime draft; it does not yet match the concept. Separate eyeballs, hair, clothing, custom head sculpt and facial rig are pending. The original reference-only file remains unchanged.

Open `tools/avatar/Open-ARIA-Blender.cmd` from Explorer to use Blender with the isolated D-drive profile and enabled MPFB. Opening Blender normally may use a different profile without MPFB. Both the source package and extension data are stored under `D:/UserData/ARIA/tools/`; they are not bundled in this repository.

MPFB 2.0.17 source: https://github.com/makehumancommunity/mpfb2/tree/v2.0.17, commit `80919fa4682335c41847f761a4d79dcad4124732`. Base assets use CC0, retained in `MPFB-ASSETS-LICENSE.md`. MPFB code is separately GPL-licensed; it is not embedded in the model. Setup report is in `mpfb-setup.json`. Setup builder expects this pinned source under `D:/UserData/ARIA/tools/mpfb2-source`; do not rerun it over later manual sculpt revisions.

Open `aria-custom-sculpt.blend` with Blender 5.2. The file embeds the original concept and approximate three-view reference. Reference objects are locked against accidental selection; the custom-sculpt collection is empty.

**This is setup only, not a character model.** No new head geometry, hair, rig or facial animation exists here yet. The generated views are not calibrated orthographic measurements. The rejected stock model remains separately preserved.

Builder: `tools/avatar/prepare_sculpt_workspace.py`. Running it again replaces this setup file; save later manual sculpt work under a new revision name before rebuilding.
