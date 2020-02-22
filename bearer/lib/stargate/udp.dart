
import 'dart:io';

import 'package:udp/udp.dart';


class StarGateUDP {

  StarGateUDP(this.gate) {

  }

  final String gate;

  void openGate(int idx) async {
    var sender = await UDP.bind(Endpoint.any());
    List<InternetAddress> address = await InternetAddress.lookup('melber.ddnss.eu');
    Endpoint endpoint = Endpoint.unicast(address[0], port: Port(4242));
    String msg = 'open stargate: $idx\n';

    sender.send(msg.codeUnits, endpoint);
  }
}