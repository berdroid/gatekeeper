import 'dart:io';

import 'package:flutter/cupertino.dart';
import 'package:udp/udp.dart';

class StarGateUDP {
  StarGateUDP(
    this.gate, {
    @required this.hostName,
    @required this.port,
  });

  final String gate;
  final String hostName;
  final int port;

  void openGate(int idx, {onResult: Function}) async {
    try {
      var sender = await UDP.bind(Endpoint.any());
      List<InternetAddress> address = await InternetAddress.lookup(hostName);
      Endpoint endpoint = Endpoint.unicast(address[0], port: Port(port));
      String msg = 'open $gate: $idx\n';

      sender.send(msg.codeUnits, endpoint);
      print('sending $idx => $address done.');
      if (onResult != null) onResult(true);
    } catch (e) {
      print(e);
      if (onResult != null) onResult(false);
    }
  }
}
