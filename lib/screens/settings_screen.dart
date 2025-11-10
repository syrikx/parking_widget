import 'package:flutter/material.dart';
import '../models/parking_location.dart';
import '../services/parking_service.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  final ParkingService _parkingService = ParkingService();
  List<ParkingLocation> _locations = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadLocations();
  }

  Future<void> _loadLocations() async {
    setState(() => _isLoading = true);
    final locations = await _parkingService.getAvailableLocations();
    setState(() {
      _locations = locations;
      _isLoading = false;
    });
  }

  Future<void> _addLocation() async {
    final result = await showDialog<ParkingLocation>(
      context: context,
      builder: (context) => const _LocationDialog(),
    );

    if (result != null) {
      await _parkingService.addLocation(result);
      _loadLocations();
    }
  }

  Future<void> _editLocation(ParkingLocation location) async {
    final result = await showDialog<ParkingLocation>(
      context: context,
      builder: (context) => _LocationDialog(location: location),
    );

    if (result != null) {
      await _parkingService.updateLocation(location.id, result);
      _loadLocations();
    }
  }

  Future<void> _deleteLocation(ParkingLocation location) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('위치 삭제'),
        content: Text('"${location.name}"을(를) 삭제하시겠습니까?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('취소'),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, true),
            child: const Text('삭제'),
          ),
        ],
      ),
    );

    if (confirmed == true) {
      await _parkingService.removeLocation(location.id);
      _loadLocations();
    }
  }

  Future<void> _resetToDefault() async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('기본값으로 초기화'),
        content: const Text('모든 위치를 기본값으로 되돌리시겠습니까?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('취소'),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, true),
            child: const Text('초기화'),
          ),
        ],
      ),
    );

    if (confirmed == true) {
      await _parkingService.saveAvailableLocations(
        ParkingService.defaultLocations,
      );
      _loadLocations();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('주차 위치 관리'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _resetToDefault,
            tooltip: '기본값으로 초기화',
          ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _locations.isEmpty
              ? const Center(
                  child: Text('주차 위치가 없습니다.\n아래 버튼으로 추가해주세요.'),
                )
              : ListView.builder(
                  itemCount: _locations.length,
                  itemBuilder: (context, index) {
                    final location = _locations[index];
                    return Card(
                      margin: const EdgeInsets.symmetric(
                        horizontal: 16,
                        vertical: 8,
                      ),
                      child: ListTile(
                        leading: const Icon(Icons.local_parking),
                        title: Text(
                          location.name,
                          style: const TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        subtitle: Text('ID: ${location.id}'),
                        trailing: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            IconButton(
                              icon: const Icon(Icons.edit),
                              onPressed: () => _editLocation(location),
                            ),
                            IconButton(
                              icon: const Icon(Icons.delete),
                              onPressed: () => _deleteLocation(location),
                            ),
                          ],
                        ),
                      ),
                    );
                  },
                ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: _addLocation,
        icon: const Icon(Icons.add),
        label: const Text('위치 추가'),
      ),
    );
  }
}

class _LocationDialog extends StatefulWidget {
  final ParkingLocation? location;

  const _LocationDialog({this.location});

  @override
  State<_LocationDialog> createState() => _LocationDialogState();
}

class _LocationDialogState extends State<_LocationDialog> {
  late TextEditingController _idController;
  late TextEditingController _nameController;

  @override
  void initState() {
    super.initState();
    _idController = TextEditingController(text: widget.location?.id ?? '');
    _nameController = TextEditingController(text: widget.location?.name ?? '');
  }

  @override
  void dispose() {
    _idController.dispose();
    _nameController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: Text(widget.location == null ? '위치 추가' : '위치 수정'),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          TextField(
            controller: _idController,
            decoration: const InputDecoration(
              labelText: 'ID',
              hintText: 'b2_l',
              border: OutlineInputBorder(),
            ),
            enabled: widget.location == null,
          ),
          const SizedBox(height: 16),
          TextField(
            controller: _nameController,
            decoration: const InputDecoration(
              labelText: '이름',
              hintText: 'B2(L)',
              border: OutlineInputBorder(),
            ),
          ),
        ],
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context),
          child: const Text('취소'),
        ),
        TextButton(
          onPressed: () {
            if (_idController.text.isNotEmpty &&
                _nameController.text.isNotEmpty) {
              Navigator.pop(
                context,
                ParkingLocation(
                  id: _idController.text.trim(),
                  name: _nameController.text.trim(),
                ),
              );
            }
          },
          child: const Text('저장'),
        ),
      ],
    );
  }
}
