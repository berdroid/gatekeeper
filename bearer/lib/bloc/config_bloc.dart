import 'dart:async';
import 'dart:convert';

import 'package:connectivity/connectivity.dart';
import 'package:flutter/cupertino.dart';
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

  String _username = 'bernhard';

  final _configController = StreamController<List<GateConfig>>();

  String _wifiName;

  StreamSubscription _wlanStatus;

  Stream<List<GateConfig>> get configStream => _configController.stream;

  String get username => _username;

  void _update() => _configController.add(_configs
      .map((e) => GateConfig(
            configJSON: e,
            username: username,
            wifiName: _wifiName,
          ))
      .toList());

  void addConfig(String config) {
    _configs.add(config);
    _update();
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
      _update();
    });
  }

  @override
  void dispose() {
    _configController.close();
    _wlanStatus.cancel();
  }
}
