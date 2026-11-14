# STATUS (2026-11-15) -- boot frontier

30 fps black CLEAR-only. Two draws per frame, both CLEAR(0,0,0,1), zero geometry.
Continue path: DataCheck=1, D3D12 set_shader/bind_texture/VP ready/GCM2D fire, no flip.

## Proven with evidence

- SPU delivery works end-to-end (route A exonerated): chain job (image 3010, 68 KB
  @0x0070D080) dispatches 51x HIT / 0 MISS, RETURNED rc=0; jc_signal_done pushes to
  guest q1+q2 rc=0; Job Manager (002E07CC, tid=2) consumes q1 and dispatches.
- q1 handler table is NULL: 43/43 indirect calls at lr=0x002E0894 target 0x00000000;
  mgr=0x11005900, slot +0x20 never written (page-guard 90 s: zero writes to the
  whole 0x11005000 page). Manager exists (+0=1 +0xC=2), fill code never executes.
- The main wait is INVERTED: DCC78 ret==0 (flags CLEAR) leads to D160/advance,
  ret!=0 leads to churn/pump. Flags frozen at 0x29 = work never completes, not
  work never started. Each flag set ONCE per run, never cleared:
  bit 0x20: submitted once by 002D36A8 (caller 0x000B06D0; pool allocs + list
  insert + ADA0 set), clearer 002DABB8 runs ZERO times (callers unreachable).
  bits 0x8/0x1: same one-shot pattern.
- File pipeline is HEALTHY (log-cap lesson: [fs] logs only first 50 reads;
  FS_READ_ALL=1 shows the truth): 74 reads/60 s, 7.5 MB from common.dat
  (2.3 MB DDS + structs) scattered to work buffers incl. 11x460928 B chunks at
  0x14001840/0x14072100/0x140E29C0.../0x14466FC0, then ep01 FILT 55 KB.
  Phase 1+2 complete; no I/O for 90+ s after (timeline run: reads stuck at 74).
- Chain job is innocent: single GET ea=0x10033780 size=4 per run, RETURNED rc=0.
- ep01 FILT 55 KB lands at 0x102D75D8; phase-3 request never issued.

## Route (Wayfinder map in workspace .scratch/siren-first-frame/)

- Route A (fix delivery) executed and exonerated at mechanism level.
- Refined next: the 3 one-shot flags completers -- who should invoke the
  0x20/0x8/0x1 clearers (002DABB8 et al.) and what completion they wait on.
  File-thread dispatch (00330278, all selectors, return-value pairing) and
  the FILT consumer are the two live observation points.
- Ticket 04 (repro pack): BASE.log/BASE-err.log/base.png/rsxcap/ are the 对照物.

## Method notes

- PS3_CALLTRACE_TO=<fn> traces callers with no rebuild; PPU_GUARD_EA=<addr>
  catches guest-side writers (host fread bypasses it -- file data arrives via
  host, invisible to the guard); [fs] has a 50-line cap, use FS_READ_ALL=1.
- REQDUMP/REQRET pair file-thread selector (r4) with return value in order;
  selector 6 = chunked fs reader (0033A288 via populated slot table).