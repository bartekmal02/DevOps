#!/bin/bash

if [[ $# -lt 1 ]]; then
    echo "Użycie: $0 <nazwa_projektu> [katalog1 katalog2 ...] [--no-readme]"
    exit 1
fi

project_name="$1"
shift

default_dirs=("src" "tests" "docs" "config")
dirs=()
create_readme_flag=true

for arg in "$@"; do
    if [[ "$arg" == "--no-readme" ]]; then
        create_readme_flag=false
    else
        dirs+=("$arg")
    fi
done

if [[ ${#dirs[@]} -eq 0 ]]; then
    dirs=("${default_dirs[@]}")
fi

create_dir() {
    local dir="$1"
    if [[ -d "$dir" ]]; then
        echo "⚠ Katalog $dir już istnieje"
        return 1
    fi
    if mkdir -p "$dir"; then
        echo "✅ Utworzono katalog $dir"
        return 0
    else
        echo "❌ Błąd przy tworzeniu $dir"
        return 1
    fi
}

create_readme() {
    local project="$1"
    cat > "$project/README.md" << EOF
# $project

## O projekcie
Opis projektu.

## Struktura
$(for dir in "${dirs[@]}"; do echo "- \`$dir/\`"; done)

## Instalacja
\`\`\`bash
git clone <repo-url>
cd $project
\`\`\`
EOF
    echo "✅ Utworzono README.md"
}

echo "🚀 Tworzenie struktury projektu: $project_name"

if ! create_dir "$project_name"; then
    echo "❌ Nie można utworzyć projektu"
    exit 1
fi

for dir in "${dirs[@]}"; do
    create_dir "$project_name/$dir"
done

if $create_readme_flag; then
    create_readme "$project_name"
else
    echo "ℹ Pominięto tworzenie README.md"
fi

if command -v git &>/dev/null; then
    (
        cd "$project_name" &&
        git init >/dev/null &&
        echo "✅ Zainicjalizowano repozytorium Git"
    )
else
    echo "⚠ Git nie jest zainstalowany — pomijam inicjalizację repozytorium."
fi

echo "✨ Projekt $project_name został pomyślnie utworzony!"