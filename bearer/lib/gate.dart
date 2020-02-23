import 'dart:convert';

import 'stargate/udp.dart';
import 'package:flutter/material.dart';

class Gate extends StatefulWidget {
  Gate({Key key, this.user, this.config}) : super(key: key);

  final String user;
  final String config;

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
  StarGateUDP gate;
  String name;
  String description;
  GateState state = GateState.accessible;

  @override
  void initState() {
    super.initState();
    print(widget.config);

    final Map<String, dynamic> config = json.decode(widget.config);
    name = config['name'];
    description = config['desc'];
    gate = StarGateUDP(
      config['gate'],
      user: widget.user,
      secret: config['TOTP']['secret'],
      hostName: config['UDP']['host'],
      port: config['UDP']['port'],
    );
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
            )
          ],
        ),
      ),
    );
  }
}
