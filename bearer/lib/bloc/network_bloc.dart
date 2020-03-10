import 'dart:async';

import 'package:connectivity/connectivity.dart';
import 'package:flutter/material.dart';
import 'package:stargate/bloc/bloc.dart';


class NetworkBLoC extends Bloc with WidgetsBindingObserver {

  String _wifiName;

  StreamSubscription _wlanStatus;

  final _networkController = StreamController<String>();

  Stream<String> get networkStream => _networkController.stream;

  void _update() {
    _networkController.add(_wifiName);
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

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    print('$state');
    if (state == AppLifecycleState.resumed)
      Connectivity().checkConnectivity().then(_updateWiFi);
  }

  NetworkBLoC._() {
    _wlanStatus = Connectivity().onConnectivityChanged.listen(_updateWiFi);

    Connectivity().checkConnectivity().then(_updateWiFi);

    WidgetsBinding.instance.addObserver(this);
  }

  static NetworkBLoC _instance;

  factory NetworkBLoC.instance() {
    if (_instance == null) {
      _instance = NetworkBLoC._();
    }
    return _instance;
  }

  @override
  void dispose() {
    _wlanStatus.cancel();

    WidgetsBinding.instance.removeObserver(this);
  }
}


