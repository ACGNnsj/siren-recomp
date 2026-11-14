# siren-recomp -- Siren: Blood Curse (BCJS30020) PC port

PC port of Siren: New Translation / Blood Curse (PS3 BCJS30020, JP retail dump)
built on ps3recomp (runtime v0.19.0, upstream de4f0903 -- see runtime-patches/upstream-head.txt).
First-ever PC port attempt for this title (first-party exclusive, no port on record).

## Layout

- siren/ -- the port project: CMakeLists.txt, main.cpp, lift scripts
  (gen_pm_registry.py, findstub*.py, ...) and machine-lifted SPU sources in
  siren/spu/ (13 SPUs: Wws_Job pm_416BED + 12 Sony Scream audio PMs +
  13 WWS job modules jobmod_*, lifted with wrap_spu_elf + --auto-functions
  --return-entries --merge-chunks; Wws_Job additionally --base 0xA00
  --extra-funcs 0xA2C --force-indirect 0x277C).
- runtime-patches/siren-probes.patch -- diff of the ps3recomp checkout used
  (19 files: SPU dispatch/drain/DMA probes, Spurs walker + guard +
  event-queue delivery, HLE stubs, RSX capture, lift_jobmods.py engine support).
- docs/STATUS.md -- where the boot currently stands and what is next.

## Reproduce

1. Decrypt EBOOT.BIN to EBOOT.elf, lift PPU (analysis/lifted/).
2. SPU_DUMP_MISS run to collect the 13 PMs, lift, register via gen_pm_registry.py
   (image ids 3001+, job modules 200-212).
3. Apply runtime-patches/siren-probes.patch, build (VS + clang-cl).
4. Baseline env: PS3_HEAPRETRY=1 PS3_JOINFAKE=1 PS3_FORCE_FORK=1 SIREN_PUMPFAKE=1.
   Diagnose: SPURS_PM_PIPE=1, PS3_TBLDUMP=1, PS3_CALLTRACE_LR=0x2E0894, RSX_CAP.

## What is NOT here

No game bytes: no EBOOT, no spudump bins, no lifted PPU output, no build tree.
Bring your own dump.