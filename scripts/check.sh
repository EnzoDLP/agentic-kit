#!/bin/sh
# Maintainer check, run before committing. Reports, never fixes. Needs python3.
#   sh scripts/check.sh
# Private terms that must never appear (client, product, person names) go one per line in
# .sensitive-terms at the repository root: git-ignored, never committed.
cd "$(dirname "$0")/.." || exit 2
fail=0
err() { printf 'FAIL %s\n' "$*"; fail=1; }

# Layers: valid permissions.json, known required layers.
for f in layers/*/permissions.json; do
  python3 -c "import json,sys; d=json.load(open(sys.argv[1]))['permissions']; \
assert set(d) <= {'ask','deny'}" "$f" 2>/dev/null || err "invalid permissions file: $f"
done
for f in layers/*/requires; do
  [ -f "$f" ] || continue
  while IFS= read -r dep; do
    [ -z "$dep" ] || [ -d "layers/$dep" ] || err "$f requires unknown layer '$dep'"
  done <"$f"
done

# Rules files: no frontmatter (always loaded), and a size that stays cheap in context.
for f in layers/*/rules/*.md; do
  size=$(wc -c <"$f" | tr -d ' ')
  [ "$size" -lt 9000 ] || err "$f is $size characters (limit 9000)"
  [ "$(head -1 "$f")" != "---" ] || err "$f has frontmatter"
done

# Skills and agents: a name that is the link link.py creates, and a description.
for s in layers/*/skills/*/; do
  f="${s}SKILL.md"; [ -f "$f" ] || { err "$s has no SKILL.md"; continue; }
  layer=$(echo "$s" | cut -d/ -f2)
  name=$(sed -n 's/^name: *//p' "$f" | head -1)
  [ "$name" = "$layer-$(basename "$s")" ] || err "$f: name '$name' != $layer-$(basename "$s")"
  grep -q '^description: ' "$f" || err "$f has no description"
done
for f in layers/*/agents/*.md; do
  name=$(sed -n 's/^name: *//p' "$f" | head -1)
  [ "$name.md" = "$(basename "$f")" ] || err "$f: name '$name' != file name"
done

# Kit files named by their path in a project (.claude/agentic-kit/...) exist here.
for f in $(grep -rl '\.claude/agentic-kit/' layers README.md AGENTS.md); do
  for ref in $(grep -o '\.claude/agentic-kit/[A-Za-z0-9_./-]*' "$f" | sed 's#\.claude/agentic-kit/##; s/[.]$//' | sort -u); do
    case "$ref" in *'<'*|*'*'*|'') continue ;; esac
    [ -e "$ref" ] || err "$f references missing $ref"
  done
done

# Namespaced skill names from the plugin era (expo:revenuecat) are gone.
grep -rnE '\b(workflow|typescript|react|expo|supabase):[a-z]' layers README.md AGENTS.md \
  | grep -v 'Bash(' && err "plugin-style skill name above (use workflow-review)"

# Sensitive content: personal paths, email addresses, private terms.
files=$(git ls-files --cached --others --exclude-standard | grep -v -x scripts/check.sh | while IFS= read -r f; do [ -f "$f" ] && echo "$f"; done)
grep -n -E '/Users/|/home/[a-z]|~/Desktop|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(com|fr|io|net|org)' $files \
  | grep -v -E 'users\.noreply\.github\.com|noreply@' && err "personal path or email address above"
if [ -f .sensitive-terms ]; then
  grep -v -E '^\s*(#|$)' .sensitive-terms | while IFS= read -r t; do
    grep -n -i -F -w -- "$t" $files && echo "FAIL private term: $t"
  done | grep -q . && err "private terms found (rerun: grep -n -i -w -F -f .sensitive-terms)"
fi

[ "$fail" -eq 0 ] && echo ok
exit "$fail"
