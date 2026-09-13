# ARIA custom sculpt workspace

## Human-base preparation

`aria-human-base.blend` now contains an unsculpted adult-female MPFB base plus the packed references. This is a different human base from the rejected pixiv anime draft; it does not yet match the concept. Separate eyeballs, hair, clothing, custom head sculpt and facial rig are pending. The original reference-only file remains unchanged.

Open `tools/avatar/Open-ARIA-Blender.cmd` from Explorer to use Blender with the isolated D-drive profile and enabled MPFB. Opening Blender normally may use a different profile without MPFB. Both the source package and extension data are stored under `D:/UserData/ARIA/tools/`; they are not bundled in this repository.

MPFB 2.0.17 source: https://github.com/makehumancommunity/mpfb2/tree/v2.0.17, commit `80919fa4682335c41847f761a4d79dcad4124732`. Base assets use CC0, retained in `MPFB-ASSETS-LICENSE.md`. MPFB code is separately GPL-licensed; it is not embedded in the model. Setup report is in `mpfb-setup.json`. Setup builder expects this pinned source under `D:/UserData/ARIA/tools/mpfb2-source`; do not rerun it over later manual sculpt revisions.

Open `aria-custom-sculpt.blend` with Blender 5.2. The file embeds the original concept and approximate three-view reference. Reference objects are locked against accidental selection; the custom-sculpt collection is empty.

**This is setup only, not a character model.** No new head geometry, hair, rig or facial animation exists here yet. The generated views are not calibrated orthographic measurements. The rejected stock model remains separately preserved.

Builder: `tools/avatar/prepare_sculpt_workspace.py`. Running it again replaces this setup file; save later manual sculpt work under a new revision name before rebuilding.
