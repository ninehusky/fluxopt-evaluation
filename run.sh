#!/usr/bin/env bash
#
# Build the nRF52840 `usb_ethernet` example twice -- once against upstream
# embassy+xarxa, once against the ninehusky forks -- and measure both ELFs.
#
#   ./run.sh
#
# Everything lands in ./work (clones + cargo target dirs, gitignored) and
# ./results (the numbers, committed).  Re-running reuses the clones.
set -euo pipefail

# ---------------------------------------------------------------------------
# The two configurations under test.
#
# baseline = upstream embassy at 7c2eac8a1, the commit ninehusky/embassy was
#   forked from.  Its embassy-net/Cargo.toml pins upstream xarxa at
#   rev 1f332ac32cc33d86aefc8e1c1a9749b93234a6de as a git dependency, so cargo
#   fetches upstream xarxa on its own -- there is nothing to pin here.
#
# modified = ninehusky/embassy main, which replaces that git dependency with
#   the third_party/xarxa submodule, pinned at ninehusky/xarxa
#   f42ae2866a63f32b3230a8dc24c95f209ccc22ad (branch remove-explicit-panics,
#   also merged to that fork's main).  `git submodule update --init` below is
#   what selects the xarxa under test; we never edit xarxa or embassy sources.
# ---------------------------------------------------------------------------
BASE_URL=https://github.com/embassy-rs/embassy
BASE_REV=7c2eac8a1450dbfbcc138a03c79aef4b880aff7b

MOD_URL=https://github.com/ninehusky/embassy
MOD_REV=460e274e50c0d799eceedd8e6192f31f6ded5c35

# Identical for both builds.  1.97 is what both repos' rust-toolchain.toml asks
# for; we name it explicitly so neither build can drift onto another toolchain.
TOOLCHAIN=1.97
TARGET=thumbv7em-none-eabi
EXAMPLE_DIR=examples/nrf52840
BIN=usb_ethernet

HERE="$(cd "$(dirname "$0")" && pwd)"
WORK="${WORK:-$HERE/work}"
RESULTS="$HERE/results"

# llvm-size / llvm-objdump from the same toolchain that compiles the binaries.
HOST="$(rustc "+$TOOLCHAIN" -vV | awk '/^host:/{print $2}')"
LLVM_BIN="$(rustc "+$TOOLCHAIN" --print sysroot)/lib/rustlib/$HOST/bin"
export LLVM_BIN

mkdir -p "$WORK" "$RESULTS"

# build <name> <url> <rev>  ->  prints the path of the linked ELF on stdout
build() {
  local name=$1 url=$2 rev=$3
  local dir="$WORK/$name"

  if [ ! -d "$dir/.git" ]; then
    git init -q "$dir"
    git -C "$dir" remote add origin "$url"
  fi
  git -C "$dir" fetch -q --depth 1 origin "$rev"
  git -C "$dir" checkout -q --detach FETCH_HEAD
  # No-op for the upstream checkout (it has no submodules); for the fork this
  # is what pulls in third_party/xarxa and third_party/flux at their pins.
  git -C "$dir" submodule update --init -q

  # CARGO_INCREMENTAL=0 because the fork's .cargo/config.toml sets
  # incremental = false and upstream's does not.  Pinning it here makes the two
  # builds agree on the one setting that would otherwise differ.
  ( cd "$dir/$EXAMPLE_DIR" \
    && CARGO_INCREMENTAL=0 cargo "+$TOOLCHAIN" build --release --bin "$BIN" \
         --target "$TARGET" >&2 )

  echo "$dir/$EXAMPLE_DIR/target/$TARGET/release/$BIN"
}

echo "== building baseline (upstream embassy $BASE_REV + upstream xarxa)"
BASE_ELF="$(build baseline "$BASE_URL" "$BASE_REV")"

echo "== building modified (ninehusky/embassy $MOD_REV + ninehusky/xarxa)"
MOD_ELF="$(build modified "$MOD_URL" "$MOD_REV")"

echo "== measuring"
python3 "$HERE/measure.py" "$BASE_ELF" "$RESULTS/baseline"
python3 "$HERE/measure.py" "$MOD_ELF"  "$RESULTS/modified"

# Record exactly what was built, so the table can be traced back.  The baseline
# xarxa rev is read out of upstream's own Cargo.toml rather than hardcoded.
{
  echo "toolchain      $TOOLCHAIN   target $TARGET   profile release   bin $BIN"
  echo "baseline  embassy $BASE_URL @ $(git -C "$WORK/baseline" rev-parse HEAD)"
  echo "baseline  xarxa   https://github.com/embassy-rs/xarxa @ $(
    sed -n 's/.*rev = "\([0-9a-f]*\)".*/\1/p' "$WORK/baseline/embassy-net/Cargo.toml" | head -1)"
  echo "modified  embassy $MOD_URL @ $(git -C "$WORK/modified" rev-parse HEAD)"
  echo "modified  xarxa   https://github.com/ninehusky/xarxa @ $(git -C "$WORK/modified/third_party/xarxa" rev-parse HEAD)"
} > "$RESULTS/refs.txt"

{
  echo "# usb_ethernet, nRF52840: upstream vs ninehusky"
  echo
  echo "Produced by \`./run.sh\`. See ../README.md for what the numbers mean."
  echo
  echo '```'
  cat "$RESULTS/refs.txt"
  echo '```'
  echo
  python3 "$HERE/compare.py" "$RESULTS/baseline.json" "$RESULTS/modified.json"
} > "$RESULTS/RESULTS.md"
cat "$RESULTS/RESULTS.md"
