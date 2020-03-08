import 'dart:async';
import 'dart:convert';

import 'package:connectivity/connectivity.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:stargate/bloc/bloc.dart';
import 'package:stargate/stargate/otp.dart';
import 'package:stargate/stargate/udp.dart';

class GateConfig {
  final String configJSON;
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
    this.wifiName,
  }) : config = json.decode(configJSON) {
    TOTP totp;
    String id;
    if (config.containsKey('COTP')) {
      totp = COTP(config['COTP']['secret']);
      id = config['COTP']['id'];
    } else {
      totp = TOTP(config['TOTP']['secret']);
      id = config['TOTP']['id'];
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

  final _storage = FlutterSecureStorage();
  Map<String, String> _storageValues;

  String _wifiName;

  StreamSubscription _wlanStatus;

  Stream<List<GateConfig>> get configStream => _configController.stream;

  void _update() {
    _configController.add(_configs
        .map((e) => GateConfig(
              configJSON: e,
              wifiName: _wifiName,
            ))
        .toList());
  }

  Future<void> _load() {
    return Future<void>(() async {
      var data = await _storage.readAll();
      _storageValues = Map.from(data);

      _configs.clear();
      for (var i = 0; _storageValues.keys.contains('gate@$i'); i++) {
        _configs.add(_storageValues['gate@$i']);
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

  Future<void> clearConfigs() {
    return Future<void>(() async {
      await _storage.deleteAll();
      _storageValues?.clear();
      _configs.clear();
      _update();
    });
  }

  void _updateWiFi(ConnectivityResult result) async {
    if (result == ConnectivityResult.wifi) {
      _wifiName = await (Connectivity().getWifiName());
      print('WiFi: $_wifiName');
    } else {
      _wifiName = null;
      print('WiFi: none');
    }
    _update();
  }

  ConfigBLoC._() {
    try {
      _load().then((_) {
        _update();
      });
    } on PlatformException catch (e) {
      print(e);
    }

    _wlanStatus = Connectivity().onConnectivityChanged.listen(_updateWiFi);

    Connectivity().checkConnectivity().then(_updateWiFi);
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
