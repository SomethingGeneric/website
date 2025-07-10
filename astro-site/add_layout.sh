#!/bin/bash
find . -type f -name "*.md" -print0 | while IFS= read -r -d $'\0' file; do
  # Check if the file already contains a layout property
  if ! grep -q "layout:" "$file"; then
    echo "Adding layout to: $file"
    # Check if the file already has a frontmatter section (starts with ---)
    if [[ -s "$file" && "$(head -n 1 "$file")" == "---" ]]; then
      # If frontmatter exists, add the layout property after the opening ---
      sed -i '1a\layout: /src/layouts/MarkdownLayout.astro' "$file"
    else
      # If no frontmatter, create it and prepend it to the file
      (echo "---"; echo "layout: /src/layouts/MarkdownLayout.astro"; echo "---"; cat "$file") > "${file}.tmp" && mv "${file}.tmp" "$file"
    fi
  fi
done
