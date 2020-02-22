
import 'dart:io';

import 'package:udp/udp.dart';


class StarGateUDP {

  StarGateUDP(this.gate) {

  }

  final String gate;

  void openGate(int idx) async {
    var sender = await UDP.bind(Endpoint.any());
    sender.send('open stargate: $idx\n'.codeUnits, Endpoint.unicast(InternetAddress('192.168.1.30'), port: Port(4242)));
  }
}