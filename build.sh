#!/usr/bin/env bash
set -euo pipefail

# =========================================================
# Gradle-style Nuitka Onefile Builder
# =========================================================

APP_NAME="${APP_NAME:-16kbs}"
VERSION="${VERSION:-dev}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT_DIR="$SCRIPT_DIR/dist"

GRADLE_TASK=":nuitkaBuild"

# =========================================================
# Logger (Gradle-like)
# =========================================================

log_header() {
    echo ""
    echo "> Task $GRADLE_TASK"
}

log_step() {
    echo "> $1"
}

log_info() {
    echo "  - $1"
}

die() {
    echo ""
    echo "> Task $GRADLE_TASK FAILED"
    echo "> Reason: $1"
    exit 1
}

# =========================================================
# start
# =========================================================

log_header
log_step "Initializing build environment"

command -v python3 >/dev/null 2>&1 || die "python3 not found"

python3 -c "import nuitka" 2>/dev/null || die "Nuitka not installed"
python3 -c "import PySide6" 2>/dev/null || die "PySide6 not installed"

mkdir -p "$OUT_DIR"

# =========================================================
# platform detection
# =========================================================

log_step "Detecting platform"

OS="$(uname -s)"
case "$OS" in
    Linux*)   PLATFORM="linux" ;;
    Darwin*)  PLATFORM="macos" ;;
    MINGW*|MSYS*|CYGWIN*) PLATFORM="windows" ;;
    *)        PLATFORM="unknown" ;;
esac

log_info "$PLATFORM"

# =========================================================
# Nuitka configuration
# =========================================================

log_step "Configuring compilation flags"

NUITKA_FLAGS=(
    --onefile
    --standalone
    --enable-plugin=pyside6

    --output-dir="$OUT_DIR"
    --output-filename="${APP_NAME}-${PLATFORM}-${VERSION}"

    --follow-imports

    --include-package=ui
    --include-module=constants
    --include-module=ffmpeg_utils
    --include-module=encoders
    --include-module=workers
    --include-module=commands

    --jobs="$(nproc 2>/dev/null || sysctl -n hw.ncpu)"

    --assume-yes-for-downloads

    --onefile-tempdir-spec="{CACHE_DIR}/16kbs"
)

if [[ "$PLATFORM" == "windows" ]]; then
    NUITKA_FLAGS+=(--windows-console-mode=disable)
fi

if [[ "$PLATFORM" == "macos" ]]; then
    NUITKA_FLAGS+=(--macos-create-app-bundle)
fi

# =========================================================
# build
# =========================================================

log_step "Starting compilation pipeline"

echo ""
echo "> Task $GRADLE_TASK"
echo "> Running Nuitka compiler"
echo "> Mode: standalone onefile"
echo ""

python3 -m nuitka "${NUITKA_FLAGS[@]}" "$SCRIPT_DIR/__main__.py"

# =========================================================
# finish
# =========================================================

echo ""
echo "> Task $GRADLE_TASK"
echo "> BUILD SUCCESSFUL"
echo "> Output: $OUT_DIR/$APP_NAME"
echo ""
echo "Done"