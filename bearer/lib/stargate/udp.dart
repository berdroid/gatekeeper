
import 'dart:io';

import 'package:udp/udp.dart';


class StarGateUDP {

  StarGateUDP(this.gate) {

  }

  final String gate;

  void openGate(int idx, {onResult: Function}) async {
    try {
      var sender = await UDP.bind(Endpoint.any());
      List<InternetAddress> address = await InternetAddress.lookup('melber.ddnss.eu');
      Endpoint endpoint = Endpoint.unicast(address[0], port: Port(4242));
      String msg = 'open $gate: $idx\n';

      sender.send(msg.codeUnits, endpoint);
      print('sending $idx => $address done.');
      if (onResult != null)
        onResult(true);
    } catch (e) {
      print(e);
      if (onResult != null)
        onResult(false);
    } finally {}
  }
}