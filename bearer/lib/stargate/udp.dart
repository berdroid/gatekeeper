import 'dart:io';

import 'package:flutter/cupertino.dart';
import 'package:udp/udp.dart';
import 'package:dotp/dotp.dart';

typedef GateCallback = void Function(bool);

class StarGateUDP {
  StarGateUDP(
    this.gate, {
    @required this.user,
    @required secret,
    @required this.hostName,
    @required this.port,
  }) : _totp = TOTP(secret);

  final String gate;
  final String hostName;
  final int port;
  final String user;
  final TOTP _totp;

  void openGate({GateCallback onResult}) async {
    try {
      final code = _totp.now();
      var sender = await UDP.bind(Endpoint.any());
      List<InternetAddress> address = await InternetAddress.lookup(hostName);
      Endpoint endpoint = Endpoint.unicast(address[0], port: Port(port));
      String msg = 'open@$gate:$user:$code:\n';

      sender.send(msg.codeUnits, endpoint);
      print('sending $code => $address done.');
      if (onResult != null) onResult(true);
    } catch (e) {
      print(e);
      if (onResult != null) onResult(false);
    }
  }
}
