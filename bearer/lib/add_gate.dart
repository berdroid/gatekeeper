import 'dart:io';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class AddGate extends StatefulWidget {
  const AddGate({Key? key}) : super(key: key);

  @override
  _AddGateState createState() => _AddGateState();
}

class _AddGateState extends State<AddGate> {
  final _code = TextEditingController();

  late bool _started;

  @override
  void initState() {
    super.initState();
    _code.clear();
    _started = false;
  }

  @override
  void dispose() {
    super.dispose();
    _code.dispose();
  }

  void downloadConfig(context) async {
    final uri = Uri.https('file.io', _code.text);
    print('starting with $uri');
    final http.Response r = await http.get(uri);
    print('${r.statusCode}');
    if (r.statusCode == HttpStatus.ok) {
      Navigator.pop(context, r.body);
    }
    setState(() {
      _code.clear();
      _started = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Add New Gate'),
      ),
      body: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 100, vertical: 25),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: <Widget>[
            const Text(
              'Enter Download Code:',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            TextField(
              controller: _code,
              enabled: !_started,
              autofocus: true,
              onChanged: (_) => setState(() {}),
            ),
            ElevatedButton(
              child: const Text('Next'),
              style: ElevatedButton.styleFrom(
                primary: Colors.green,
                shape: const RoundedRectangleBorder(borderRadius: BorderRadius.all(Radius.circular(5))),
              ),
              onPressed: _started || _code.text.length < 5
                  ? null
                  : () async {
                      setState(() => _started = true);
                      downloadConfig(context);
                    },
            ),
            const SizedBox(height: 40),
            if (_started) const CircularProgressIndicator(),
          ],
        ),
      ),
    );
  }
}
