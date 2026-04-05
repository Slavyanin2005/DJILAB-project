#!/usr/bin/env python3
"""
Проверка имён файлов на соответствие стандартам проекта.
"""
import os
import re
import sys

# файлы, которые могут иметь специальные имена (искллючения)
EXCLUDED_PATTERNS = [
    # Python
    r".*/__init__\.py$",
    # Django migrations
    r".*/migrations/\d+_.+\.py$",
    # Frontend entry points
    r"^main\.(tsx?|jsx?|js)$",
    r"^vite-env\.d\.ts$",
    r"^index\.(tsx?|jsx?|js|css|html)$",
    # Конфигурационные файлы с дефисами
    r"^[a-z][a-z0-9-]*\.(json|yaml|yml|toml)$",
    r"^\.[a-z][a-z0-9.-]*$",
    # Docker
    r"^Dockerfile$",
    r"^docker-compose.*\.yml$",
]

# Паттерны для разных типов файлов
PATTERNS = {
    # Backend Python (кроме __init__.py и миграций)
    r"backend/.*(?<!__init__)\.py$": r"^[a-z][a-z0-9_]*\.py$",
    # Frontend React компоненты (PascalCase)
    r"frontend/src/(components|pages)/.*\.tsx$": r"^[A-Z][a-zA-Z0-9]*\.tsx$",
    # Frontend TypeScript утилиты/хуки/сервисы (camelCase)
    r"frontend/src/(hooks|services|types)/.*\.ts$": r"^[a-z][a-zA-Z0-9]*(\.d)?\.ts$",
    # Frontend context (PascalCase)
    r"frontend/src/context/.*\.ts$": r"^[A-Z][a-zA-Z0-9]*(\.context)?\.ts$",
    # HTML шаблоны (backend)
    r"backend/templates/.*\.html$": r"^[a-z][a-z0-9_]*\.html$",
    # CSS файлы
    r".*\.css$": r"^[a-z][a-z0-9_-]*\.css$",
}


def is_excluded(filepath):
    """Проверяет, является ли файл исключением."""
    filename = os.path.basename(filepath)
    for pattern in EXCLUDED_PATTERNS:
        if re.match(pattern, filename) or re.match(
            pattern, filepath.replace("\\", "/")
        ):
            return True
    return False


def check_filename(filepath):
    """Проверяет имя файла на соответствие паттернам."""
    if is_excluded(filepath):
        return True, f"[SKIP] {filepath}: исключение"

    normalized_path = filepath.replace("\\", "/")

    for pattern, filename_rule in PATTERNS.items():
        if re.match(pattern, normalized_path):
            filename = os.path.basename(filepath)
            if not re.match(filename_rule, filename):
                return (
                    False,
                    f"[ERROR] {filepath}: '{filename}' не соответствует стандарту",
                )
            return True, f"[OK] {filepath}"

    return True, f"[SKIP] {filepath}: нет правила"


def main():
    """Главная функция."""
    errors = []

    for filepath in sys.argv[1:]:
        is_valid, message = check_filename(filepath)
        print(message)
        if not is_valid:
            errors.append(filepath)

    if errors:
        print(f"\nНайдено ошибок: {len(errors)}")
        sys.exit(1)
    else:
        print("\nВсе имена файлов корректны")
        sys.exit(0)


if __name__ == "__main__":
    main()
