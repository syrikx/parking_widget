#!/bin/bash
# Flutter Android APK 릴리스 빌드
# parking_widget 프로젝트 빌드

echo "Flutter 의존성 설치 중..."
flutter pub get

echo ""
echo "Flutter Android APK 릴리스 빌드 중..."
flutter build apk --release

echo ""
echo "빌드 완료!"
echo "APK 위치: build/app/outputs/flutter-apk/app-release.apk"
ls -lh build/app/outputs/flutter-apk/app-release.apk
