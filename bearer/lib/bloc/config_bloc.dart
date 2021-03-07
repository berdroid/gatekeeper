import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:stargate/bloc/bloc.dart';
import 'package:stargate/bloc/network_bloc.dart';
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

  NetworkBLoC _networkBloc;
  StreamSubscription<String> _neworkSubs;
  String _wifiName;

  Stream<List<GateConfig>> get configStream => _configController.stream;

  void _update() {
    _configController.add(_configs
        .map((e) => GateConfig(
              configJSON: utf8.decode(e.codeUnits),
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

  ConfigBLoC._() {
    try {
      _load().then((_) {
        _update();
      });
    } on PlatformException catch (e) {
      print(e);
    }

    _networkBloc = NetworkBLoC.instance();
    _neworkSubs = _networkBloc.networkStream.listen((wifiName) {
      _wifiName = wifiName;
      _update();
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
    _networkBloc.dispose();
    _neworkSubs.cancel();
  }
}
