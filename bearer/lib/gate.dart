import 'dart:async';

import 'package:flutter/material.dart';
import 'package:stargate/bloc/config_bloc.dart';

import 'stargate/udp.dart';

class Gate extends StatefulWidget {
  Gate({Key key, this.user, this.gateConfig}) : super(key: key);

  final String user;
  final GateConfig gateConfig;

  @override
  _GateState createState() => _GateState();
}

enum GateState {
  idle,
  blocked,
  pending,
  success,
  failed,
}

class _GateState extends State<Gate> {
  StarGateUDP get gate => widget.gateConfig.gate;

  Map<String, dynamic> get config => widget.gateConfig.config;

  String get name => widget.gateConfig.name;

  String get description => widget.gateConfig.description;

  bool get accessible => widget.gateConfig.accessible;

  GateState _state = GateState.idle;

  GateState get state => accessible ? _state : GateState.blocked;

  set state(s) {
    if (mounted) {
      setState(() {
        if (accessible) _state = s;
      });
    }
  }

  @override
  void initState() {
    super.initState();
    print('${widget.user}@${widget.gateConfig.name}');
  }

  @override
  void dispose() {
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    Widget trail;

    switch (state) {
      case GateState.blocked:
        trail = Icon(Icons.block, size: 32, color: Colors.red);
        break;
      case GateState.idle:
        trail = SizedBox(width: 32, height: 32);
        break;
      case GateState.pending:
        trail = CircularProgressIndicator();
        break;
      case GateState.success:
        trail = Icon(Icons.check, size: 32, color: Colors.lightGreen[900]);
        break;
      case GateState.failed:
        trail = Icon(Icons.warning, size: 32, color: Colors.orange);
        break;
    }

    return Center(
      child: Card(
        color: Colors.white54,
        child: Column(
          children: <Widget>[
            ListTile(
              enabled: state == GateState.idle,
              leading: Icon(Icons.vpn_key, size: 32),
              trailing: trail,
              title: Text(name),
              subtitle: Text(description),
              onTap: _open,
              onLongPress: () {},
            )
          ],
        ),
      ),
    );
  }

  void _open() {
    state = GateState.pending;
    gate.openGate(onResult: (result) {
      state = result ? GateState.success : GateState.failed;
      Future.delayed(Duration(seconds: 3)).then((_) {
        state = GateState.idle;
      });
    });
  }

}