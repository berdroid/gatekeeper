import 'dart:async';

import 'package:connectivity/connectivity.dart';
import 'package:flutter/material.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:stargate/bloc/bloc.dart';
import 'package:wifi_info_flutter/wifi_info_flutter.dart';

class NetworkBLoC extends Bloc with WidgetsBindingObserver {
  late Connectivity _connectivity;
  late WifiInfo _wifi;

  String? _wifiName;

  late StreamSubscription _wlanStatus;

  final _networkController = StreamController<String?>();

  Stream<String?> get networkStream => _networkController.stream;

  void _update() {
    _networkController.add(_wifiName);
  }

  void _updateWiFi(ConnectivityResult result) async {
    if (result == ConnectivityResult.wifi) {
      _wifiName = await _wifi.getWifiName();
      print('WiFi: ${await _wifi.getWifiName()}, IP: ${await _wifi.getWifiIP()}');
    } else if (result == ConnectivityResult.mobile) {
      print('connectivity: mobile');
    } else {
      _wifiName = null;
      print('connectivity: none');
    }
    _update();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    print('$state');
    if (state == AppLifecycleState.resumed) _connectivity.checkConnectivity().then(_updateWiFi);
  }

  NetworkBLoC._() {
    Permission.locationWhenInUse.request().then((permissionStatus) {
      print(permissionStatus);
      if (permissionStatus.isGranted) {
        _connectivity = Connectivity();
        _wifi = WifiInfo();
        _wlanStatus = _connectivity.onConnectivityChanged.listen(_updateWiFi);

        _connectivity.checkConnectivity().then(_updateWiFi);

        WidgetsBinding.instance.addObserver(this);
      }
    });
  }

  static NetworkBLoC instance = NetworkBLoC._();

  @override
  void dispose() {
    _wlanStatus.cancel();

    WidgetsBinding.instance.removeObserver(this);
  }
}
