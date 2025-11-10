#!/usr/bin/env python3
"""위젯 크기 변경 로그"""

from code_changelog_tracker import CodeChangeLogger

# 로거 생성
logger = CodeChangeLogger(
    "Parking Widget - 위젯 크기 최소화",
    user_request="parking_widget 최소 크기를 1x1 또는 1x2부터 가능하게 간략화"
)

# Android 위젯 크기 설정 수정
logger.log_file_modification(
    "android/app/src/main/res/xml/parking_widget_info.xml",
    """    android:minWidth="180dp"
    android:minHeight="110dp" """,
    """    android:minWidth="40dp"
    android:minHeight="40dp" """,
    "Android 위젯 최소 크기를 3x2에서 1x1로 변경 (40dp = 약 1칸)"
)

# Android 위젯 레이아웃 간략화
logger.log_file_modification(
    "android/app/src/main/res/layout/parking_widget.xml",
    """    <ImageView
        android:layout_width="48dp"
        android:layout_height="48dp"
        android:src="@android:drawable/ic_menu_mylocation"
        android:tint="#2196F3"
        android:contentDescription="@string/parking_icon" />

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/current_parking"
        android:textSize="12sp"
        android:textColor="#666666"
        android:layout_marginTop="8dp" />

    <TextView
        android:id="@+id/parking_location_text"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/no_location"
        android:textSize="24sp"
        android:textStyle="bold"
        android:textColor="#2196F3"
        android:layout_marginTop="4dp" />""",
    """    <TextView
        android:id="@+id/parking_location_text"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/no_location"
        android:textSize="16sp"
        android:textStyle="bold"
        android:textColor="#2196F3"
        android:gravity="center" />""",
    "Android 위젯 레이아웃 간략화: 아이콘 제거, 라벨 제거, 주차 위치만 표시, padding 축소 (16dp→4dp)"
)

# iOS 위젯 레이아웃 반응형 수정
logger.log_file_modification(
    "ios/ParkingWidget/ParkingWidget.swift",
    """struct ParkingWidgetEntryView : View {
    var entry: Provider.Entry

    var body: some View {
        ZStack {
            Color.white

            VStack(spacing: 8) {
                Image(systemName: "car.fill")
                    .font(.system(size: 32))
                    .foregroundColor(.blue)

                Text("현재 주차 위치")
                    .font(.caption)
                    .foregroundColor(.gray)

                Text(entry.parkingLocation)
                    .font(.title2)
                    .fontWeight(.bold)
                    .foregroundColor(.blue)
            }
            .padding()
        }
    }
}""",
    """struct ParkingWidgetEntryView : View {
    var entry: Provider.Entry
    @Environment(\.widgetFamily) var family

    var body: some View {
        ZStack {
            Color.white

            VStack(spacing: 4) {
                // 작은 크기일 때는 아이콘과 라벨 제거
                if family == .systemMedium || family == .systemLarge {
                    Image(systemName: "car.fill")
                        .font(.system(size: 24))
                        .foregroundColor(.blue)

                    Text("현재 주차 위치")
                        .font(.caption2)
                        .foregroundColor(.gray)
                }

                Text(entry.parkingLocation)
                    .font(family == .systemSmall ? .body : .title2)
                    .fontWeight(.bold)
                    .foregroundColor(.blue)
                    .minimumScaleFactor(0.5)
                    .lineLimit(1)
            }
            .padding(family == .systemSmall ? 4 : 8)
        }
    }
}""",
    "iOS 위젯 레이아웃 반응형 수정: systemSmall은 주차 위치만 표시, systemMedium/Large는 아이콘+라벨+주차위치 표시, 텍스트 자동 축소 기능 추가"
)

# 저장 및 빌드
logger.save_and_build()

print("\n" + "="*60)
print("✅ 위젯 크기 변경 사항이 changelog에 기록되었습니다!")
print("="*60)
