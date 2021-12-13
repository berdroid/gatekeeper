import 'dart:io';

import 'otp.dart';

typedef GateCallback = void Function(bool);

class StarGateUDP {
  StarGateUDP(
    this.gate, {
    required this.id,
    required this.totp,
    required this.hostName,
    required this.port,
  });

  final String gate;
  final String hostName;
  final int port;
  final String id;
  final TOTP totp;

  void openGate({GateCallback? onResult}) async {
    try {
      final code = totp.genTotp();

      var socket = await RawDatagramSocket.bind(InternetAddress.anyIPv4, 0);
      List<InternetAddress> address = await InternetAddress.lookup(hostName);
      String msg = '$gate:${totp.kind}:$id:$code:\n';

      socket.send(msg.codeUnits, address[0], port);
      print('sending ${totp.kind}:$id => $address done.');
      if (onResult != null) onResult(true);
    } catch (e) {
      print(e);
      if (onResult != null) onResult(false);
    }
  }
}
