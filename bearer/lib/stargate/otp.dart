import 'dart:math';
import 'dart:typed_data';

import 'package:base32/base32.dart';
import 'package:crypto/crypto.dart';

abstract class OTP {
  String get kind => 'OTP';

  final String secret;

  final int digits;

  final Hash algo;

  OTP(this.secret, {this.digits = 6, algo}) : algo = algo ?? sha1;

  List<int> _hash(int input) {
    var hmacKey = base32.decode(secret);
    var hmac = Hmac(algo, hmacKey);
    return hmac.convert(_intToBytelist(input)).bytes;
  }

  String _code(List<int> hmac) {
    int offset = hmac[hmac.length - 1] & 0xf;
    int code = ((hmac[offset] & 0x7f) << 24 |
        (hmac[offset + 1] & 0xff) << 16 |
        (hmac[offset + 2] & 0xff) << 8 |
        (hmac[offset + 3] & 0xff));

    String key = (code % pow(10, digits)).toString();
    return key.padLeft(digits, '0');
  }

  String genOtp(int input) {
    var hmac = _hash(input);
    return _code(hmac);
  }

  List<int> _intToBytelist(int input) {
    var result = [0, 0, 0, 0, 0, 0, 0, 0];

    var i = result.length - 1;
    while (input != 0 && -i <= 0) {
      result[i] = input & 0xff;
      input >>= 8;
      i -= 1;
    }

    return result;
  }
}

class TOTP extends OTP {
  @override
  String get kind => 'TOTP';

  final int interval;

  TOTP(secret, {digits = 6, algo, this.interval = 30}) : super(secret, digits: digits, algo: algo);

  String genTotp() {
    return genOtp(_timeCode(_now()));
  }

  DateTime _now() => DateTime.now().toUtc();

  int _timeCode(DateTime pointInTime) {
    return pointInTime.millisecondsSinceEpoch ~/ (interval * 1000);
  }
}

class COTP extends TOTP {
  @override
  String get kind => 'COTP';

  COTP(secret, {digits = 16, algo, interval = 30})
      : super(secret, digits: digits, algo: algo ?? sha256, interval: interval);

  @override
  String _code(List<int> hmac) {
    int offset = hmac[hmac.length - 1] & 0xf;
    return base32.encode(hmac as Uint8List).substring(offset, offset + digits);
  }
}
