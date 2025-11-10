# 주차 위치 위젯 앱

Flutter로 만든 주차 위치 표시 앱입니다. 홈 화면 위젯을 통해 현재 주차 위치를 빠르게 확인할 수 있습니다.

## 기능

- 홈 화면 위젯을 통한 주차 위치 표시
- 위젯 클릭으로 앱 열기 및 위치 변경
- 기본 주차 위치: B2(L), B2(R), B3(L), B3(R), B4(L), B4(R)
- 사용자 정의 위치 추가/수정/삭제 기능
- Android 및 iOS 지원

## 설치 및 실행

### 1. 의존성 설치

```bash
flutter pub get
```

### 2. Android에서 실행

```bash
flutter run
```

Android에서는 위젯이 자동으로 등록됩니다. 앱 실행 후:
1. 홈 화면 길게 누르기
2. 위젯 메뉴 선택
3. "주차 위치" 위젯 찾기
4. 홈 화면에 드래그하여 추가

### 3. iOS에서 실행 (추가 설정 필요)

iOS 위젯을 사용하려면 Xcode에서 Widget Extension을 추가해야 합니다:

#### iOS 위젯 설정 방법

1. Xcode에서 프로젝트 열기:
   ```bash
   open ios/Runner.xcworkspace
   ```

2. File → New → Target 선택

3. "Widget Extension" 검색 및 선택

4. 다음 정보 입력:
   - Product Name: `ParkingWidget`
   - Team: 본인의 Apple Developer Team 선택
   - Include Configuration Intent: 체크 해제

5. Activate scheme 다이얼로그가 나오면 "Activate" 클릭

6. 생성된 ParkingWidget 폴더의 파일들을 삭제하고, 미리 준비된 파일 사용:
   - `ios/ParkingWidget/ParkingWidget.swift` 파일이 이미 준비되어 있습니다
   - `ios/ParkingWidget/Info.plist` 파일이 이미 준비되어 있습니다

7. App Groups 설정:
   - Runner 타겟 선택
   - Signing & Capabilities 탭
   - "+ Capability" 클릭
   - "App Groups" 추가
   - `group.com.example.parkingWidget` 추가

   - ParkingWidget 타겟도 동일하게 설정
   - `group.com.example.parkingWidget` 추가

8. Flutter 앱 실행:
   ```bash
   flutter run -d ios
   ```

9. iOS 홈 화면에서:
   - 홈 화면 길게 누르기
   - 왼쪽 상단 "+" 버튼
   - "주차 위치" 위젯 검색
   - 원하는 크기 선택하여 추가

## 사용 방법

### 주차 위치 설정

1. 앱을 실행합니다
2. 메인 화면에서 원하는 주차 위치를 탭합니다
3. 선택한 위치가 위젯에 자동으로 표시됩니다

### 위치 목록 커스터마이징

1. 앱 상단의 설정(⚙️) 아이콘을 탭합니다
2. 오른쪽 하단의 "위치 추가" 버튼을 탭합니다
3. ID와 이름을 입력하여 새 위치를 추가합니다
4. 기존 위치를 수정하거나 삭제할 수 있습니다
5. "기본값으로 초기화" 아이콘을 탭하면 원래 위치 목록으로 되돌릴 수 있습니다

## 기술 스택

- **Flutter**: 크로스 플랫폼 앱 프레임워크
- **home_widget**: 네이티브 홈 화면 위젯 지원
- **shared_preferences**: 로컬 데이터 저장
- **Kotlin**: Android 네이티브 위젯 구현
- **Swift/SwiftUI**: iOS 네이티브 위젯 구현

## 프로젝트 구조

```
lib/
├── main.dart                    # 앱 진입점
├── models/
│   └── parking_location.dart    # 주차 위치 데이터 모델
├── services/
│   └── parking_service.dart     # 주차 위치 관리 서비스
└── screens/
    ├── home_screen.dart         # 메인 화면
    └── settings_screen.dart     # 설정 화면

android/
└── app/src/main/
    ├── kotlin/.../
    │   └── ParkingWidgetProvider.kt  # Android 위젯
    ├── res/
    │   ├── layout/
    │   │   └── parking_widget.xml    # 위젯 레이아웃
    │   ├── xml/
    │   │   └── parking_widget_info.xml  # 위젯 메타데이터
    │   └── drawable/
    │       └── widget_background.xml  # 위젯 배경
    └── AndroidManifest.xml

ios/
└── ParkingWidget/
    ├── ParkingWidget.swift      # iOS 위젯
    └── Info.plist              # iOS 위젯 설정
```

## 문제 해결

### Android

- 위젯이 업데이트되지 않으면 위젯을 제거하고 다시 추가해보세요
- 앱을 재설치한 경우 위젯도 다시 추가해야 합니다

### iOS

- 위젯이 나타나지 않으면 Xcode에서 Widget Extension이 제대로 추가되었는지 확인하세요
- App Groups가 양쪽 타겟에 모두 설정되어 있는지 확인하세요
- 시뮬레이터를 재시작하거나 기기를 재부팅해보세요
