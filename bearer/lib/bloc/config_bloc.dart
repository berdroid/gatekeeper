

import 'dart:async';

import 'package:flutter/cupertino.dart';
import 'package:stargate/bloc/bloc.dart';

class GateConfig {
  final String config;

  GateConfig({
    @required this.config,
});
}

class ConfigBLoC implements Bloc {

  final _configs = <String>[];

  String _username = 'bernhard';

  final _configController = StreamController<List<GateConfig>>();

  Stream<List<GateConfig>> get configStream => _configController.stream;

  String get username => _username;

  void addConfig(String config) {
    _configs.add(config);
    _configController.add(
        _configs.map((e) => GateConfig(config: e)).toList()
    );
  }

  @override
  void dispose() {
    _configController.close();
  }
}