import 'dart:async';
import 'dart:convert';

import 'package:connectivity/connectivity.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:stargate/bloc/bloc.dart';
import 'package:stargate/stargate/udp.dart';

class GateConfig {
  final String configJSON;
  final String username;
  final String wifiName;
  final Map<String, dynamic> config;

  StarGateUDP gate;

  String get name => config['name'];
  String get description => config['desc'];

  bool get accessible {
    if (config['UDP'].keys.contains('wlan'))
      return wifiName == config['UDP']['wlan'];
    else
      return true;
  }

  GateConfig({
    @required this.configJSON,
    @required this.username,
    this.wifiName,
  }) : config = json.decode(configJSON) {
    gate = StarGateUDP(
      config['gate'],
      user: username,
      secret: config['TOTP']['secret'],
      hostName: config['UDP']['host'],
      port: config['UDP']['port'],
    );
  }
}

class ConfigBLoC implements Bloc {
  final _configs = <String>[];

  final _configController = StreamController<List<GateConfig>>();

  final _storage = FlutterSecureStorage();
  Map<String, String> _storageValues;

  String _wifiName;

  StreamSubscription _wlanStatus;

  Stream<List<GateConfig>> get configStream => _configController.stream;

  String _username;

  void _update() {
    _configController.add(_configs
        .map((e) => GateConfig(
              configJSON: e,
              username: username,
              wifiName: _wifiName,
            ))
        .toList());
  }

  Future<void> _load() {
    return Future<void>(() async {
      var data = await _storage.readAll();
      _storageValues = Map.from(data);
      _username = _storageValues['username'];

      _configs.clear();
      for (var i = 0; _storageValues.keys.contains('gate@$i'); i++) {
        _configs.add(_storageValues['gate@$i']);
      }
    });
  }

  Future<void> _save() {
    return Future<void>(() async {
      await _storage.deleteAll();
      await _storage.write(key: 'username', value: _username);

      for (var i = 0; i < _configs.length; i++) {
        await _storage.write(key: 'gate@$i', value: _configs[i]);
      }
    });
  }

  String get username => _username;

  int get numConfigs => _configs.length;

  Future<void> setUsername(String name) {
    return Future<void>(() async {
      _username = name;
      await _save();
      _update();
    });
  }

  Future<void> addConfig(String config) {
    return Future<void>(() async {
      _configs.add(config);
      await _save();
      _update();
    });
  }

  Future<void> clearConfigs() {
    return Future<void>(() async {
      await _storage.deleteAll();
      _username = null;
      _storageValues?.clear();
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

    _wlanStatus = Connectivity()
        .onConnectivityChanged
        .listen((ConnectivityResult result) async {
      if (result == ConnectivityResult.wifi) {
        _wifiName = await (Connectivity().getWifiName());
        print('WiFi: $_wifiName');
      } else {
        _wifiName = null;
        print('WiFi: none');
      }
   });
  }

  static ConfigBLoC _instance;

  factory ConfigBLoC.instance() {
    if (_instance == null) {
      _instance = ConfigBLoC._();
    }
    return _instance;
  }

  Future<void> load() => _load();

  @override
  void dispose() {
    _configController.close();
    _wlanStatus.cancel();
  }
}
