import 'dart:async';

import 'package:connectivity/connectivity.dart';
import 'package:stargate/bloc/config_bloc.dart';

import 'stargate/udp.dart';
import 'package:flutter/material.dart';

class Gate extends StatefulWidget {
  Gate({Key key, this.user, this.gateConfig}) : super(key: key);

  final String user;
  final GateConfig gateConfig;

  @override
  _GateState createState() => _GateState();
}

enum GateState {
  blocked,
  accessible,
  pending,
  success,
  failed,
}

class _GateState extends State<Gate> {
  StarGateUDP get gate => widget.gateConfig.gate;
  Map<String, dynamic> get config => widget.gateConfig.config;
  String get name => widget.gateConfig.name;
  String get description => widget.gateConfig.description;
  GateState state = GateState.accessible;
  StreamSubscription wlan;

  @override
  void initState() {
    super.initState();
    print('${widget.user}@${widget.gateConfig.name}');

    if (config['UDP'].keys.contains('wlan')) {
      wlan = Connectivity().onConnectivityChanged.listen((ConnectivityResult result) async {
        var newState = GateState.blocked;
        print(result);
        if (result == ConnectivityResult.wifi) {
          var wifiName = await (Connectivity().getWifiName());
          print(wifiName);
          if (wifiName == config['UDP']['wlan']) {
            newState = GateState.accessible;
          }
        }
        setState(() {
          state = newState;
        });
      });
    }
  }

  @override
  void dispose() {
    wlan?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    Widget trail;

    switch (state) {
      case GateState.blocked:
        trail = Icon(Icons.block, size: 32, color: Colors.red);
        break;
      case GateState.accessible:
        trail = SizedBox(width: 32, height: 32);
        break;
      case GateState.pending:
        trail = CircularProgressIndicator();
        break;
      case GateState.success:
        trail = Icon(Icons.check, size: 32, color: Colors.green);
        break;
      case GateState.failed:
        trail = Icon(Icons.warning, size: 32, color: Colors.orange);
        break;
    }

    return Center(
      child: Card(
        child: Column(
          children: <Widget>[
            ListTile(
              enabled: state == GateState.accessible,
              leading: Icon(Icons.vpn_key, size: 32),
              trailing: trail,
              title: Text(name),
              subtitle: Text(description),
              onTap: () {
                setState(() {
                  state = GateState.pending;
                });
                gate.openGate(onResult: (result) {
                  setState(() {
                    state = result ? GateState.success : GateState.failed;
                  });
                  Future.delayed(Duration(seconds: 3)).then((_) {
                    setState(() {
                      state = GateState.accessible;
                    });
                  });
                });
              },
              onLongPress: () {},
            )
          ],
        ),
      ),
    );
  }
}
