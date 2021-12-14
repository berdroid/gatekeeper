import 'dart:async';
import 'dart:convert';

import 'package:flutter/services.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:stargate/bloc/bloc.dart';
import 'package:stargate/bloc/network_bloc.dart';
import 'package:stargate/stargate/otp.dart';
import 'package:stargate/stargate/udp.dart';

class GateConfig {
  final int index;
  final String configJSON;
  final String? wifiName;
  final Map<String, dynamic> config;

  late final StarGateUDP gate;

  String get name => config['name'];
  String get description => config['desc'];

  bool get accessible {
    if (config['UDP'].keys.contains('wlan')) {
      return wifiName == config['UDP']['wlan'];
    } else {
      return true;
    }
  }

  GateConfig({
    required this.index,
    required this.configJSON,
    this.wifiName,
  }) : config = json.decode(configJSON) ?? {} {
    TOTP totp;
    String id;
    if (config.containsKey('COTP')) {
      totp = COTP(config['COTP']['secret'] as String);
      id = config['COTP']['id'] as String;
    } else {
      totp = TOTP(config['TOTP']['secret'] as String);
      id = config['TOTP']['id'] as String;
    }
    gate = StarGateUDP(
      config['gate'],
      id: id,
      totp: totp,
      hostName: config['UDP']['host'],
      port: config['UDP']['port'],
    );
  }
}

class ConfigBLoC implements Bloc {
  final _configs = <String>[];

  final _configController = StreamController<List<GateConfig>>();

  final _storage = const FlutterSecureStorage();
  late Map<String, String> _storageValues;

  late NetworkBLoC _networkBloc;
  late StreamSubscription<String?> _networkSubs;
  String? _wifiName;

  Stream<List<GateConfig>> get configStream => _configController.stream;

  void _update() {
    _configController.add(_configs
        .asMap()
        .map((i, e) => MapEntry<int, GateConfig>(
            i,
            GateConfig(
              index: i,
              configJSON: utf8.decode(e.codeUnits),
              wifiName: _wifiName,
            )))
        .values
        .toList());
  }

  Future<void> _load() {
    return Future<void>(() async {
      var data = await _storage.readAll();
      _storageValues = Map.from(data);

      _configs.clear();
      for (final e in _storageValues.entries) {
        if (e.key.startsWith('gate@')) {
          try {
            final config = GateConfig(
              index: 0,
              configJSON: utf8.decode(e.value.codeUnits),
            );
            print('Loading config: ${e.key}: ${config.name}');
            _configs.add(e.value);
          } on FormatException {
            // ignore invalid entries
          }
        }
      }
    });
  }

  Future<void> _save() {
    return Future<void>(() async {
      await _storage.deleteAll();

      for (var i = 0; i < _configs.length; i++) {
        await _storage.write(key: 'gate@$i', value: _configs[i]);
      }
    });
  }

  int get numConfigs => _configs.length;

  Future<void> addConfig(String config) {
    return Future<void>(() async {
      _configs.add(config);
      await _save();
      _update();
    });
  }

  Future<void> dropConfig(GateConfig config) {
    return Future<void>(() async {
      _configs.removeAt(config.index);
      await _save();
      _update();
    });
  }

  Future<void> clearConfigs() {
    return Future<void>(() async {
      await _storage.deleteAll();
      _storageValues.clear();
      _configs.clear();
      _update();
    });
  }

  ConfigBLoC._() {
    try {
      _load().then((_) {
        _update();
      });
    } on PlatformException catch (e) {
      print(e);
    }

    _networkBloc = NetworkBLoC.instance;
    _networkSubs = _networkBloc.networkStream.listen((wifiName) {
      _wifiName = wifiName;
      _update();
    });
  }

  static ConfigBLoC instance = ConfigBLoC._();

  Future<void> load() => _load();

  @override
  void dispose() {
    _configController.close();
    _networkBloc.dispose();
    _networkSubs.cancel();
  }
}
