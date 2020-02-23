import 'dart:async';
import 'dart:convert';

import 'package:flutter/cupertino.dart';
import 'package:stargate/bloc/bloc.dart';
import 'package:stargate/stargate/udp.dart';

class GateConfig {
  final String configJSON;
  final String username;
  final Map<String, dynamic> config;

  StarGateUDP gate;

  String get name => config['name'];
  String get description => config['desc'];
  bool accessible;

  GateConfig({
    @required this.configJSON,
    @required this.username,
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

  Stream<List<GateConfig>> get configStream => _configController.stream;

  String get username => _username;

  void addConfig(String config) {
    _configs.add(config);
    _configController.add(_configs
        .map((e) => GateConfig(configJSON: e, username: username))
        .toList());
  }

  @override
  void dispose() {
    _configController.close();
  }
}
