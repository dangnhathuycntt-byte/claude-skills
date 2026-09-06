#!/usr/bin/env bash
set -e

TARGET_DIR="${HOME}/.claude/skills"
mkdir -p "${TARGET_DIR}"

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 Installing Claude Skills into ${TARGET_DIR}..."

for skill_path in "${REPO_DIR}"/skills/*; do
  if [ -d "${skill_path}" ]; then
    skill_name="$(basename "${skill_path}")"
    echo "  → Installing ${skill_name}..."
    rm -rf "${TARGET_DIR}/${skill_name}"
    cp -r "${skill_path}" "${TARGET_DIR}/"
    find "${TARGET_DIR}/${skill_name}" -type f -name "*.py" -exec chmod +x {} +
    find "${TARGET_DIR}/${skill_name}" -type f -name "*.sh" -exec chmod +x {} +
  fi
done

echo "✅ All skills installed successfully!"
echo "You can now use these skills inside Claude Code, Claude Desktop, and Cowork."
