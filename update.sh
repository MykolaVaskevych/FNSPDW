#!/usr/bin/env bash
# Sync the paper both ways: local -> Overleaf, then Overleaf -> local.
#
# Overleaf and GitHub keep each other in step by themselves (two GitHub Actions),
# but nothing can push into a working tree, so the last hop has to be pulled. This
# does the whole chain and asks for any commit message it needs.
#
# Needs: gh, authenticated. No Overleaf token - the token lives in GitHub secrets
# and only the Actions use it.
set -uo pipefail

REPO=MykolaVaskevych/Paper
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PAPER="$ROOT/paper"

say() { printf '\n== %s\n' "$*"; }
die() { printf '\n!! %s\n' "$*" >&2; exit 1; }

command -v gh >/dev/null || die "gh is not installed"
gh auth status >/dev/null 2>&1 || die "gh is not logged in - run: gh auth login"
[ -d "$PAPER/.git" ] || [ -f "$PAPER/.git" ] || die "no paper submodule at $PAPER"

# ---------------------------------------------------------------- local -> Overleaf
if [ -n "$(git -C "$PAPER" status --porcelain)" ]; then
  say "paper/ has uncommitted changes"
  git -C "$PAPER" status --short | sed 's/^/   /'
  printf '\n   commit message (empty to skip and leave them uncommitted): '
  read -r msg
  if [ -n "$msg" ]; then
    git -C "$PAPER" add -A
    git -C "$PAPER" commit -q -m "$msg" || die "commit failed"
    echo "   committed: $(git -C "$PAPER" log --oneline -1)"
  else
    echo "   skipped - they stay local, and will not reach Overleaf"
  fi
fi

if ! git -C "$PAPER" diff --quiet HEAD "@{upstream}" 2>/dev/null; then
  say "pushing paper/ to GitHub, which fires Push to Overleaf"
  git -C "$PAPER" push origin HEAD:main || die "push rejected - run this again to pull first"
fi

# ---------------------------------------------------------------- Overleaf -> GitHub
say "asking GitHub to pull from Overleaf"
gh workflow run "Pull from Overleaf" --repo "$REPO" --ref main >/dev/null \
  || die "could not start the workflow"
sleep 5
id=$(gh run list --repo "$REPO" --workflow "Pull from Overleaf" --limit 1 \
       --json databaseId -q '.[0].databaseId')
echo "   run $id"
if ! gh run watch "$id" --repo "$REPO" --exit-status --interval 5 >/dev/null 2>&1; then
  printf '\n!! that job did not succeed. Most likely Overleaf and GitHub both changed,\n'
  printf '   so it opened a pull request and left main alone. Look at:\n'
  printf '     gh run view %s --repo %s --log\n' "$id" "$REPO"
  printf '     gh pr list --repo %s\n\n' "$REPO"
  exit 1
fi

# ---------------------------------------------------------------- GitHub -> local
say "pulling into paper/"
git -C "$PAPER" pull --ff-only origin main 2>&1 | sed 's/^/   /'

# ---------------------------------------------------------------- parent pointer
head_now=$(git -C "$PAPER" rev-parse HEAD)
recorded=$(git -C "$ROOT" rev-parse HEAD:paper 2>/dev/null || echo none)
if [ "$head_now" != "$recorded" ]; then
  say "FNSPDW still points at the old paper commit"
  git -C "$PAPER" log --oneline "${recorded}..${head_now}" 2>/dev/null | sed 's/^/   /'
  printf '\n   commit message for the pointer update (empty to skip): '
  read -r msg2
  if [ -n "$msg2" ]; then
    git -C "$ROOT" add paper
    git -C "$ROOT" commit -q -m "$msg2" || die "commit failed"
    git -C "$ROOT" push -q origin HEAD || die "push failed"
    echo "   pointer updated and pushed"
  else
    echo "   skipped - FNSPDW will keep showing 'M paper' until you commit it"
  fi
fi

say "done"
printf '   paper local  %s\n' "$(git -C "$PAPER" rev-parse --short HEAD)"
printf '   paper GitHub %s\n' "$(git -C "$PAPER" rev-parse --short origin/main 2>/dev/null)"
printf '   FNSPDW points at %s\n' "$(git -C "$ROOT" rev-parse --short HEAD:paper 2>/dev/null)"
