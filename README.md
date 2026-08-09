# fluxopt-evaluation — `usb_ethernet` measurement CI

This repository holds **measurement infrastructure only**. It builds the
embassy-net `usb_ethernet` example under a set of named configurations, measures
each resulting binary (section sizes and panic call-sites), and uploads the
results as CI artifacts. It does **not** write Flux annotations, prove anything,
or modify the embassy / xarxa sources — the forks are cloned and built exactly
as they ship.

## What is measured

The example is `examples/nrf52840`, binary `usb_ethernet`, in the
`ninehusky/embassy` fork. That example path-depends on:

- **xarxa** — vendored by the embassy fork as the `third_party/xarxa` git
  submodule (`ninehusky/xarxa`), and
- **flux-rs** — vendored as `third_party/flux` (`ninehusky/flux`); only the
  lightweight `lib/flux-rs` + `lib/flux-attrs` proc-macro crates are pulled in,
  so an ordinary `cargo build` compiles it with no Flux toolchain involved.

The target triple (`thumbv7em-none-eabi`) is **read from the example's
`.cargo/config.toml`** and never guessed or overridden.

## Configurations (`configs.toml`)

All four configurations are implemented; adding another requires editing only
`configs.toml`.

| name | description | enabled |
|---|---|---|
| `baseline` | Default `Cargo.toml` settings, unmodified upstream deps | ✅ |
| `immediate-abort` | Baseline plus `panic=immediate-abort` | ✅ |
| `xarxa-nopanic` | Baseline against the panic-free xarxa fork | ❌ |
| `xarxa-embassy-nopanic` | `xarxa-nopanic` plus the panic-free embassy fork | ❌ |

- **`baseline`** builds the example exactly as the embassy fork ships it. Its
  xarxa is the commit the fork pins as a submodule (`xarxa_ref = "@submodule"`),
  which is recorded — resolved SHA **and** merge-base against upstream
  `embassy-rs/xarxa` — in every run, since the fork is actively pushed to.
- **`immediate-abort`** is the oracle lower bound: total panic-infrastructure
  removal by fiat. See the mechanism note below.
- **`xarxa-nopanic` / `xarxa-embassy-nopanic`** are disabled but fully wired:
  they override the xarxa submodule with `remove-explicit-panics`. There is
  currently no separate panic-free *embassy* branch (`ninehusky/embassy` has
  only `main`), so config 4's `embassy_ref` is left at `main`; enabling it once
  such a branch exists is a one-line edit.

### `immediate-abort` — mechanism note (important)

The task specified building this config with
`-Z build-std=core,alloc -Z build-std-features=panic_immediate_abort`.

On the pinned nightly (`nightly-2026-07-25`, rustc 1.99.0-nightly) that
`build-std-features` value **no longer exists** — the compiler rejects it with a
`compile_error!`:

> `panic_immediate_abort is now a real panic strategy! Enable it with
> panic = "immediate-abort" in Cargo.toml, or with the compiler flags
> -Zunstable-options -Cpanic=immediate-abort. In both cases, you still need to
> build core, e.g. with -Zbuild-std`

The workflow therefore uses the compiler's own sanctioned replacement:
`-Z build-std=core,alloc` **plus** `RUSTFLAGS="-Zunstable-options
-Cpanic=immediate-abort"`. The goal is unchanged (rebuild `core` with panics
lowered directly to `abort`, no formatting machinery). CI does **not** assume
the flag worked because the build succeeded: it verifies the panic-formatting
symbols (`panic_fmt` / `core::panicking`) are **absent** from the linked binary
and fails the run if they are still present.

## What each run records

Per configuration, uploaded as an artifact:

- `<config>/results.json` — everything below, with **both build passes recorded
  separately**;
- `<config>/disasm.txt` — full disassembly;
- `<config>/cargo-tree.txt` — dependency graph;
- `<config>/build.log` — every command and its output.

Plus a top-level `summary.json` keyed by configuration, carrying `.text` size
and panic-site count per config for cross-run diffing.

`results.json` contains:

- **Environment / provenance** (verbatim): `rustc --version --verbose`; the
  embassy fork's `rust-toolchain.toml`; the target triple and the file it was
  read from; runner image label; `llvm-size`/`llvm-objdump`/`llvm-nm` versions;
  and for **each** dependency repo (embassy, xarxa, flux) the resolved commit
  SHA of the ref built **and** its merge-base against upstream.
- **Effective profile**: `opt-level`, `lto`, `codegen-units`, `panic`,
  `debug-assertions`, `overflow-checks`, `strip`, `debug` — each with its value
  and where the value came from (`emitted` by cargo/rustc, or a documented
  default). Unset values are resolved to the applicable default, never left as
  "unset".
- **Dependency graph**: `cargo tree`, plus a check that xarxa resolves to the
  `third_party/xarxa` **path** dependency. If it ever resolves to a crates.io
  registry version, the run fails (no patch section is added to paper over it).
- **Size**: `.text`, `.rodata`, `.data`, `.bss`, and total via `llvm-size -A`
  (**section sizes**, never the ELF file length). `.text` is the primary figure.
- **Panic sites**, extracted from the disassembly: count of branch instructions
  targeting panic-related symbols; the distinct panic symbols with a per-symbol
  count; the total call-site count; the **exact match patterns used**; and an
  `unclassified_candidates` field for symbols that look panic-related but match
  no explicit pattern (neither silently counted nor dropped).
- **Determinism**: `.text` size and panic-site count from pass 1 and pass 2
  (build → measure → `cargo clean` → rebuild → re-measure). They must be
  identical; if they differ the run fails and reports the delta.

### Cross-config invariant

`debug-assertions` and `overflow-checks` generate panic sites directly, so they
must be identical across all measured configurations or the comparison is
meaningless. The `summarize` job asserts this and fails the run if it does not
hold.

## Toolchain provisioning

The workflow installs its own pinned toolchain — it does not rely on anything
preinstalled on the runner beyond `rustup` (the installer) and Python:

- nightly pinned to a fixed date (`nightly-2026-07-25`, from `configs.toml`),
- the `rust-src` component (required for `-Z build-std`),
- `llvm-tools` (gives `llvm-size` / `llvm-objdump` / `llvm-nm` pinned to the
  toolchain's own LLVM),
- the target triple, added from the value read out of `.cargo/config.toml`.

Runner image is pinned to `ubuntu-24.04` (never `ubuntu-latest`); action
versions and Python (`3.12`) are pinned too.

> No number in this repo is a committed baseline, expected value, or fixture.
> Every measured value comes from a CI run. Numbers produced while iterating on
> the workflow locally are for debugging only and are never checked in.

## Triggers

- `push` and `pull_request` — run all enabled configurations.
- `workflow_dispatch` — optional `config` input runs a single named
  configuration (any of the four, enabled or not); blank runs all enabled.

## Layout

```
configs.toml                         # the four configurations + toolchain/upstreams
ci/list_configs.py                   # enabled-config matrix for Actions
ci/run_config.py                     # per-config: setup, build x2, measure x2, provenance
ci/measure.py                        # size + panic-site measurement primitives
ci/summarize.py                      # summary.json + profile-equality assertion
.github/workflows/measure-usb-ethernet.yml
```
