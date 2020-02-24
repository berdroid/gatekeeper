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

  String get username {
    if (_storageValues != null)
      return _storageValues['username'];
    else
      return null;
  }

  set username(String text) {
    if (_storageValues != null) {
      _storageValues['username'] = text;
      _storage.write(key: 'username', value: text);
      _update();
    }
  }

  void _update() {
    _configController.add(_configs
        .map((e) => GateConfig(
              configJSON: e,
              username: username,
              wifiName: _wifiName,
            ))
        .toList());
  }

  void addConfig(String config) {
    _configs.add(config);
    _update();
  }

  void clearConfigs() {
    _storage.deleteAll().then((value) {
      _storageValues?.clear();
      _configs.clear();
      _update();
    });
  }

  ConfigBLoC() {
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

      try {
        _storage.readAll().then((value) {
          _storageValues = Map.from(value);
          _update();
        });
      } on PlatformException catch (e) {
        print(e);
      }
    });
  }

  @override
  void dispose() {
    _configController.close();
    _wlanStatus.cancel();
  }
}
