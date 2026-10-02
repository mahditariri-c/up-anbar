name: Build Up Anbar APK

on:
  workflow_dispatch:
  push:
    branches:
      - main
      - master

jobs:
  build-apk:
    runs-on: ubuntu-22.04

    steps:
      # --------------------------------------------------
      # 1. دریافت پروژه
      # --------------------------------------------------
      - name: Checkout repository
        uses: actions/checkout@v4

      # --------------------------------------------------
      # 2. Python
      # --------------------------------------------------
      - name: Setup Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      # --------------------------------------------------
      # 3. Java 17
      # بدون PPA
      # --------------------------------------------------
      - name: Setup Java 17
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: "17"

      # --------------------------------------------------
      # 4. بررسی ساختار واقعی پروژه
      # --------------------------------------------------
      - name: Verify project structure
        shell: bash
        run: |
          set -euxo pipefail

          echo "Current directory:"
          pwd

          echo "Project files:"
          find . -maxdepth 2 -type f | sort

          test -f main.py
          test -f buildozer.spec
          test -f icon.png

          echo "main.py OK"
          echo "buildozer.spec OK"
          echo "icon.png OK"

      # --------------------------------------------------
      # 5. وابستگی‌های لینوکس
      # Ubuntu 22.04 برای جلوگیری از مشکل PPA / resolute
      # --------------------------------------------------
      - name: Install Linux dependencies
        shell: bash
        run: |
          set -euxo pipefail

          sudo apt-get update

          sudo apt-get install -y \
            git \
            zip \
            unzip \
            curl \
            wget \
            autoconf \
            automake \
            libtool \
            pkg-config \
            zlib1g-dev \
            libncurses5-dev \
            libncursesw5-dev \
            libtinfo5 \
            cmake \
            libffi-dev \
            libssl-dev \
            libltdl-dev \
            build-essential \
            ccache

      # --------------------------------------------------
      # 6. Android SDK
      # --------------------------------------------------
      - name: Setup Android SDK
        uses: android-actions/setup-android@v3

      # --------------------------------------------------
      # 7. قبول License ها
      # --------------------------------------------------
      - name: Accept Android licenses
        shell: bash
        run: |
          yes | sdkmanager --licenses >/dev/null || true

      # --------------------------------------------------
      # 8. نصب نسخه‌های هماهنگ با buildozer.spec
      # API 36
      # NDK 29
      # Build Tools 36
      # --------------------------------------------------
      - name: Install Android SDK packages
        shell: bash
        run: |
          set -euxo pipefail

          sdkmanager \
            "platform-tools" \
            "platforms;android-36" \
            "build-tools;36.0.0" \
            "ndk;29.0.13113456"

          yes | sdkmanager --licenses >/dev/null || true

      # --------------------------------------------------
      # 9. تنظیم متغیرهای Buildozer
      # --------------------------------------------------
      - name: Configure Android environment
        shell: bash
        run: |
          set -euxo pipefail

          echo "ANDROIDSDK=$ANDROID_HOME" >> "$GITHUB_ENV"
          echo "ANDROID_HOME=$ANDROID_HOME" >> "$GITHUB_ENV"
          echo "ANDROID_SDK_ROOT=$ANDROID_HOME" >> "$GITHUB_ENV"

          echo "ANDROIDNDK=$ANDROID_HOME/ndk/29.0.13113456" >> "$GITHUB_ENV"
          echo "ANDROID_NDK_HOME=$ANDROID_HOME/ndk/29.0.13113456" >> "$GITHUB_ENV"

          echo "ANDROIDAPI=36" >> "$GITHUB_ENV"
          echo "ANDROIDNDKVER=29.0.13113456" >> "$GITHUB_ENV"

      # --------------------------------------------------
      # 10. بررسی SDK
      # --------------------------------------------------
      - name: Verify Android environment
        shell: bash
        run: |
          set -euxo pipefail

          echo "ANDROID_HOME=$ANDROID_HOME"
          echo "ANDROIDSDK=$ANDROIDSDK"
          echo "ANDROIDNDK=$ANDROIDNDK"

          java -version
          python --version
          sdkmanager --version

          test -d "$ANDROID_HOME/platforms/android-36"
          test -d "$ANDROID_HOME/build-tools/36.0.0"
          test -d "$ANDROID_HOME/ndk/29.0.13113456"

          test -x "$ANDROID_HOME/build-tools/36.0.0/aidl"

          "$ANDROID_HOME/build-tools/36.0.0/aidl" version

      # --------------------------------------------------
      # 11. نصب Buildozer
      # --------------------------------------------------
      - name: Install Buildozer
        shell: bash
        run: |
          set -euxo pipefail

          python -m pip install --upgrade pip setuptools wheel

          python -m pip install \
            buildozer==1.5.0 \
            cython==0.29.37

      # --------------------------------------------------
      # 12. بررسی Buildozer
      # --------------------------------------------------
      - name: Verify Buildozer configuration
        shell: bash
        run: |
          set -euxo pipefail

          test -f buildozer.spec

          echo "===== buildozer.spec ====="
          cat buildozer.spec

          echo "===== Important files ====="
          ls -lah

          echo "===== Source directory ====="
          grep "^source.dir" buildozer.spec

          echo "===== Requirements ====="
          grep "^requirements" buildozer.spec

      # --------------------------------------------------
      # 13. پاک کردن build قبلی
      # --------------------------------------------------
      - name: Clean Buildozer
        shell: bash
        run: |
          set -euxo pipefail

          rm -rf .buildozer
          rm -rf bin

      # --------------------------------------------------
      # 14. ساخت APK
      #
      # خیلی مهم:
      # اینجا عمداً working-directory نداریم.
      # Buildozer باید از ریشه پروژه اجرا شود.
      # --------------------------------------------------
      - name: Build Up Anbar debug APK
        shell: bash
        run: |
          set -euxo pipefail

          pwd
          test -f main.py
          test -f buildozer.spec

          yes | sdkmanager --licenses >/dev/null || true

          buildozer -v android debug

      # --------------------------------------------------
      # 15. پیدا کردن APK
      # --------------------------------------------------
      - name: Find generated APK
        id: find_apk
        shell: bash
        run: |
          set -euxo pipefail

          echo "===== bin directory ====="

          if [ -d bin ]; then
            find bin -type f -maxdepth 2 -print
          else
            echo "ERROR: bin directory was not created."
            exit 1
          fi

          APK="$(find bin -type f -name '*.apk' -print -quit)"

          if [ -z "$APK" ]; then
            echo "ERROR: Build finished but no APK was found."

            echo "===== Debug files ====="
            find . -maxdepth 5 -type f | sort | tail -300

            exit 1
          fi

          echo "APK found:"
          echo "$APK"

          echo "apk=$APK" >> "$GITHUB_OUTPUT"

      # --------------------------------------------------
      # 16. آپلود APK
      # --------------------------------------------------
      - name: Upload Up Anbar APK
        uses: actions/upload-artifact@v4
        with:
          name: up-anbar-debug-apk
          path: ${{ steps.find_apk.outputs.apk }}
          if-no-files-found: error
