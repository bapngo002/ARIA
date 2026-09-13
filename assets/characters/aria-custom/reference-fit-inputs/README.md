# Reference fitting experiments R8-R17

WORK IN PROGRESS, NOT AN APPROVED AVATAR. R6 was rejected; R4 remains the previous selected baseline. The owner asks to continue until resemblance is achieved.

R8 fits 142 front-view landmark constraints on the existing mesh and projects the original reference photo. R9 stock hair was unsatisfactory. R10-R16 explore actual curved hair geometry with front/profile image projections and segmentation. R17 restricts hair texture sampling to classified hair pixels to reduce skin-colored contamination. Intermediate files are historical experiments, preserved for recovery, not finished alternatives.

The face, eyes and hair are real meshes. Appearance currently relies heavily on low-resolution photographic projections, with baked reference lighting, seams and view-dependent distortions. Hair is a shell, not a finished strand groom. Latest appearance study has no validated facial rig, teeth or animation/export deliverable. R6's previously exported rig is unrelated to approval of these studies. No ARIA runtime, selected launcher or hardware changes.

Reproduction: Blender 5.2 with MPFB profile at D:/UserData/ARIA/tools/blender-profile, run tools/avatar/fit_head_r8.py then refine_r9.py through refine_r17.py in sequence. Scripts currently reference local D:/UserData/ARIA/tools/avatar-fit-data; JSON landmark and NPY segmentation inputs are preserved here. Restore them to that location or adjust script paths. Stock long01 hair used only in early experiments remains at D:/UserData/ARIA/tools/avatar-assets/hair/long01. Original photo is ../r6-candidate/reference-three-views.png and packed in saved Blender scenes. Base assets are the existing R7/R4 studies.

Landmark/segmentation inputs were generated locally using Google's MediaPipe face_landmarker float16 model and selfie_multiclass_256x256 float32 model. Segmentation channels: background, hair, body, face, clothes, other. No external upload or paid API. Projected 2D fitting residuals do not measure 3D accuracy or likeness. All geometric adjustments are mathematical edits, not claimed manual sculpting.

R18-R23 continuation: skin validity masking, complete hair topology, profile depth correction, lateral smoothing and expanded skin-edge projection. Run refine_r18.py through refine_r23.py after the earlier chain. These experiments are not approval or completion evidence.

R24-R26: normalized per-pixel hair mixing, skin-edge color extension and central-face projection mask. These still show material-boundary defects; no successful three-view likeness claim. Run scripts in numerical order.
