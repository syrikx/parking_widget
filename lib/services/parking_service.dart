import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:home_widget/home_widget.dart';
import '../models/parking_location.dart';

class ParkingService {
  static const String _currentLocationKey = 'current_parking_location';
  static const String _availableLocationsKey = 'available_parking_locations';
  static const String _widgetLocationKey = 'widget_parking_location';

  // 기본 주차 위치 목록
  static final List<ParkingLocation> defaultLocations = [
    ParkingLocation(id: 'b2_l', name: 'B2(L)'),
    ParkingLocation(id: 'b2_r', name: 'B2(R)'),
    ParkingLocation(id: 'b3_l', name: 'B3(L)'),
    ParkingLocation(id: 'b3_r', name: 'B3(R)'),
    ParkingLocation(id: 'b4_l', name: 'B4(L)'),
    ParkingLocation(id: 'b4_r', name: 'B4(R)'),
  ];

  // 현재 주차 위치 가져오기
  Future<String?> getCurrentLocation() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_currentLocationKey);
  }

  // 현재 주차 위치 저장
  Future<void> setCurrentLocation(String locationName) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_currentLocationKey, locationName);

    // 위젯 업데이트
    await updateWidget(locationName);
  }

  // 위젯 업데이트
  Future<void> updateWidget(String locationName) async {
    await HomeWidget.saveWidgetData<String>(_widgetLocationKey, locationName);
    await HomeWidget.updateWidget(
      name: 'ParkingWidgetProvider',
      androidName: 'ParkingWidgetProvider',
      iOSName: 'ParkingWidget',
    );
  }

  // 사용 가능한 위치 목록 가져오기
  Future<List<ParkingLocation>> getAvailableLocations() async {
    final prefs = await SharedPreferences.getInstance();
    final jsonString = prefs.getString(_availableLocationsKey);

    if (jsonString == null) {
      return defaultLocations;
    }

    try {
      final List<dynamic> jsonList = json.decode(jsonString);
      return jsonList.map((json) => ParkingLocation.fromJson(json)).toList();
    } catch (e) {
      return defaultLocations;
    }
  }

  // 사용 가능한 위치 목록 저장
  Future<void> saveAvailableLocations(List<ParkingLocation> locations) async {
    final prefs = await SharedPreferences.getInstance();
    final jsonString = json.encode(locations.map((loc) => loc.toJson()).toList());
    await prefs.setString(_availableLocationsKey, jsonString);
  }

  // 위치 추가
  Future<void> addLocation(ParkingLocation location) async {
    final locations = await getAvailableLocations();
    if (!locations.any((loc) => loc.id == location.id)) {
      locations.add(location);
      await saveAvailableLocations(locations);
    }
  }

  // 위치 삭제
  Future<void> removeLocation(String locationId) async {
    final locations = await getAvailableLocations();
    locations.removeWhere((loc) => loc.id == locationId);
    await saveAvailableLocations(locations);
  }

  // 위치 수정
  Future<void> updateLocation(String oldId, ParkingLocation newLocation) async {
    final locations = await getAvailableLocations();
    final index = locations.indexWhere((loc) => loc.id == oldId);
    if (index != -1) {
      locations[index] = newLocation;
      await saveAvailableLocations(locations);
    }
  }
}
