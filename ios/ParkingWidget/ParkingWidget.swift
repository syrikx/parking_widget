import WidgetKit
import SwiftUI

struct Provider: TimelineProvider {
    func placeholder(in context: Context) -> SimpleEntry {
        SimpleEntry(date: Date(), parkingLocation: "위치 없음")
    }

    func getSnapshot(in context: Context, completion: @escaping (SimpleEntry) -> ()) {
        let parkingLocation = UserDefaults(suiteName: "group.com.example.parkingWidget")?.string(forKey: "widget_parking_location") ?? "위치 없음"
        let entry = SimpleEntry(date: Date(), parkingLocation: parkingLocation)
        completion(entry)
    }

    func getTimeline(in context: Context, completion: @escaping (Timeline<Entry>) -> ()) {
        let parkingLocation = UserDefaults(suiteName: "group.com.example.parkingWidget")?.string(forKey: "widget_parking_location") ?? "위치 없음"
        let entry = SimpleEntry(date: Date(), parkingLocation: parkingLocation)
        let timeline = Timeline(entries: [entry], policy: .never)
        completion(timeline)
    }
}

struct SimpleEntry: TimelineEntry {
    let date: Date
    let parkingLocation: String
}

struct ParkingWidgetEntryView : View {
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
}

@main
struct ParkingWidget: Widget {
    let kind: String = "ParkingWidget"

    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: Provider()) { entry in
            ParkingWidgetEntryView(entry: entry)
        }
        .configurationDisplayName("주차 위치")
        .description("현재 주차 위치를 표시합니다")
        .supportedFamilies([.systemSmall, .systemMedium])
    }
}

struct ParkingWidget_Previews: PreviewProvider {
    static var previews: some View {
        ParkingWidgetEntryView(entry: SimpleEntry(date: Date(), parkingLocation: "B2(L)"))
            .previewContext(WidgetPreviewContext(family: .systemSmall))
    }
}
