# STATUS (2026-11-15) -- boot frontier

30 fps black CLEAR-only. Two draws per frame, both CLEAR(0,0,0,1), zero geometry.
Continue path: DataCheck=1, D3D12 set_shader/bind_texture/VP ready/GCM2D fire, no flip.

## Proven with evidence

- SPU delivery works end-to-end: chain job (image 3010, 68 KB @0x0070D080) dispatches
  51x HIT / 0 MISS, RETURNED rc=0; jc_signal_done pushes to guest q1+q2 rc=0;
  Job Manager (002E07CC, tid=2) consumes q1 and dispatches to handler table.
- Handler table is NULL: 43/43 indirect calls at lr=0x002E0894 target 0x00000000;
  mgr=0x11005900 tbl=0x00000000 after 4-min run (PS3_TBLDUMP). Manager exists
  (+0=1 +0xC=2), table slot never written. Null calls return to caller: consume,
  call NULL, loop -- infinite churn with zero game progress.
- Chain job is innocent: single GET ea=0x10033780 size=4 per run, never PUTs.
- File loading is the furthest-progressing subsystem: 2.3 MB DDS from common.dat,
  then zzdat/ep01 first chunk 55 KB (FILT). Stalls after that -- FILT parse
  never starts its next phase.
- Handler-table NULL is a symptom (init never reaches the fill step), not a
  delivery gap. The blockage moved one layer up: FILT-parse function
  (caller of reader lr=0x0033A3C0) -- what it waits on is the next probe target.

## Route (Wayfinder map in workspace .scratch/siren-first-frame/)

- Route A (fix delivery) executed: PM-exit observation, pipe/joblist dumps,
  q1-vs-q2 audit, exit-chain, handler-target trace. Delivery exonerated.
- Refined next: trace what the FILT parser waits on (observe-only, no wake).
- Ticket 04 (repro pack) open: BASE.log/BASE-err.log/base.png/rsxcap/ are the
 对照物 in siren/build/.