#!/usr/bin/env bash
set -euo pipefail

# =========================================================
# Gradle-Style Nuitka Builder
# =========================================================

APP_NAME="16kbps"
ENTRY_FILE="__main__.py"

echo

log_task() {
    echo "> Task :$1"
}

log_info() {
    echo "  - $1"
}

# =========================================================
# Environment Setup
# =========================================================

log_task "initializeBuild"

echo "> Initializing build environment"

OS="$(uname -s | tr '[:upper:]' '[:lower:]')"
ARCH="$(uname -m)"

case "$OS" in
    linux*)
        OS="linux"
        ;;
    darwin*)
        OS="macos"
        ;;
    msys*|mingw*|cygwin*)
        OS="windows"
        ;;
esac

case "$ARCH" in
    x86_64|amd64)
        ARCH="amd64"
        ;;
    aarch64|arm64)
        ARCH="arm64"
        ;;
esac

EXT=""
if [[ "$OS" == "windows" ]]; then
    EXT=".exe"
fi

FINAL_NAME="${APP_NAME}-${OS}-${ARCH}${EXT}"

log_info "platform: ${OS}"
log_info "architecture: ${ARCH}"
log_info "output: dist/${FINAL_NAME}"

echo

# =========================================================
# Cleanup
# =========================================================

log_task "clean"

echo "> Cleaning build artifacts"

rm -rf build
rm -rf *.build
rm -rf *.dist
mkdir -p dist

log_info "removed temporary build directories"

echo

# =========================================================
# Python Detection
# =========================================================

log_task "resolveEnvironment"

echo "> Resolving Python environment"

if command -v python3 >/dev/null 2>&1; then
    PYTHON="python3"
    log_info "python executable: $(command -v python3)"
else
    echo "FAILURE: Python3 not found"
    exit 1
fi

if command -v pip3 >/dev/null 2>&1; then
    PIP="pip3"
    log_info "pip executable: $(command -v pip3)"
else
    echo "FAILURE: pip3 not found"
    exit 1
fi

echo

# =========================================================
# Dependencies
# =========================================================

log_task "installDependencies"

echo "> Checking build dependencies"

$PIP install --quiet --upgrade pip
$PIP install --quiet \
    nuitka \
    ordered-set \
    zstandard \
    pyside6

log_info "dependencies resolved"

echo

# =========================================================
# CPU Threads
# =========================================================

log_task "configureCompiler"

echo "> Configuring compilation pipeline"

if command -v nproc >/dev/null 2>&1; then
    THREADS="$(nproc)"
elif command -v sysctl >/dev/null 2>&1; then
    THREADS="$(sysctl -n hw.ncpu)"
else
    THREADS="4"
fi

log_info "parallel workers: ${THREADS}"
log_info "mode: standalone onefile"
log_info "plugin: pyside6"
log_info "lto: enabled"

echo

# =========================================================
# Build
# =========================================================

log_task "nuitkaBuild"

echo "> Running Nuitka compiler"

$PYTHON -m nuitka \
    --onefile \
    --standalone \
    --follow-imports \
    --assume-yes-for-downloads \
    --remove-output \
    --enable-plugin=pyside6 \
    --lto=yes \
    --jobs="${THREADS}" \
    --output-dir=dist \
    --output-filename="${FINAL_NAME}" \
    "$ENTRY_FILE"

log_info "binary produced: dist/${FINAL_NAME}"

echo

# =========================================================
# Cleanup Dist Folders
# =========================================================

log_task "cleanupDist"

echo "> Removing extracted distribution folders"

find dist -maxdepth 1 -type d -name "*.dist" -exec rm -rf {} +

log_info "temporary folders removed"

if [[ "$OS" != "windows" ]]; then
    chmod +x "dist/${FINAL_NAME}"
fi

echo
echo "BUILD SUCCESSFUL"
echo "in 1 actionable task(s)"
echo