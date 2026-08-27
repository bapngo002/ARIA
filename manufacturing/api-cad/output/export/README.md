# CAD exports

Manufacturing releases stay empty until final-release preflight and every final-critical validation check PASS. Layout/review exports may be stored in a clearly separated `not-for-manufacture/` subdirectory when useful; they must preserve placeholder labels and cannot be mistaken for released print files.

Each release uses a versioned subdirectory and includes:

- release manifest;
- source commit and final FCStd SHA-256;
- constraint/object-map versions;
- approved validation report;
- neutral STEP assembly;
- only the approved STL/3MF parts and their export tolerances.

Exploratory geometry must be labeled `NOT FOR MANUFACTURE` and must not be placed here.
