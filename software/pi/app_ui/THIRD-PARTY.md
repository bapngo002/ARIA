# Third-party avatar assets

## pixiv VRM sample

`models/aria-sample.vrm` is an unchanged copy of VRM1_Constraint_Twist_Sample v1.0.1, copyright (c) 2022 pixiv Inc., from:
https://github.com/pixiv/three-vrm/blob/v3.4.2/packages/three-vrm/examples/models/VRM1_Constraint_Twist_Sample.vrm

License: VRM Public License 1.0, https://vrm.dev/licenses/1.0/. The original embedded license settings are preserved in the binary and reproduced in models/aria-sample.metadata.json. This is NOT CC0. Redistribution and modification/redistribution are enabled, everyone may use the avatar, corporate commercial use is allowed, and antisocial/hate use is prohibited by the model settings. No endorsement by pixiv is implied. This is a stock character trial, not a reconstruction of the owner-selected photograph. All model bytes are original; app code changes pose, framing and material colors at runtime, and adds an original flower ornament.

## Runtime libraries

Three.js r180: https://github.com/mrdoob/three.js/tree/r180
- vendor/three.module.min.js and three.core.min.js: original release build files.
- vendor/GLTFLoader.js and BufferGeometryUtils.js: original examples modules with only import paths changed to local modules.
- MIT license retained in vendor/THREE-LICENSE.txt.

@pixiv/three-vrm 3.4.2: https://github.com/pixiv/three-vrm/tree/v3.4.2
- vendor/three-vrm.module.min.js from https://unpkg.com/@pixiv/three-vrm@3.4.2/lib/three-vrm.module.min.js ; bare Three.js import rewritten to the local module.
- MIT license retained in vendor/THREE-VRM-LICENSE.txt.

No CDN or external model request occurs at app runtime. Blob URLs are allowed only for local embedded texture decoding; script sources remain same-origin.

## Shipped SHA-256

- `BufferGeometryUtils.js`: `a34211b841afea271e058713b08b65e007195fef6533aaa4ad961675d6b40839`
- `GLTFLoader.js`: `ba4d3ac753fe446135d4a3c4d6feb42b826ea2420a400194e2ec7da52c02e9c1`
- `THREE-LICENSE.txt`: `bfe119ea4fd413f5f7ca3fcd63adb0c4a073ed39daa2fe7d3e6b769e21272601`
- `THREE-VRM-LICENSE.txt`: `387a46128d34de9d85ea1e07a5a716dba532dbabca6c10adad447f48a29518d3`
- `three-vrm.module.min.js`: `207e7674de023fa05cd8eff0a3b33946c4205f0c553a9c2db8c125beb2fef705`
- `three.core.min.js`: `61ba0df005b05991361d040d8ff670e1aadfd0ce7aeebd1fdb0725957a8957de`
- `three.module.min.js`: `e2b5ee6bccd38fd6d8a2428546b83c5f2426d84b152ef82be8055556e3b40eb6`
- `aria-sample.vrm`: `12c2b97e95e700783a6a550dc0eee2d7880aeedccef9ae67bc4c5a2f0f2631a2` (10776032 bytes)
