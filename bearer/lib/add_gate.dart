
import 'package:flutter/material.dart';


class AddGate extends StatefulWidget {
  @override
  _AddGateState createState() => _AddGateState();
}

class _AddGateState extends State<AddGate> {

  String _code;
  bool _started;

  @override
  void initState() {
    super.initState();
    _code = '';
    _started = false;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Add New Gate'),
      ),
      body: Padding(
        padding: EdgeInsets.symmetric(horizontal: 100, vertical: 25),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: <Widget>[
            Text('Enter Download Code:',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            TextField(
              enabled: !_started,
              onChanged: (value) {
                setState(() => _code = value);
              },
            ),
            RaisedButton(
              child: Text('Next'),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.all(Radius.circular(5))),
              color: Colors.green,
              onPressed: _started || _code.length < 5 ? null : () async {
                setState(() => _started = true);
                await Future.delayed(Duration(seconds: 5));
                Navigator.pop(context);
              },
            ),
            SizedBox(height: 40),
            if (_started) CircularProgressIndicator(),
          ],
        ),
      ),
    );
  }
}
