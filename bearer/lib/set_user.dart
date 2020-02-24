import 'package:flutter/material.dart';

class SetUser extends StatefulWidget {
  @override
  _SetUserState createState() => _SetUserState();
}

class _SetUserState extends State<SetUser> {
  final _username = TextEditingController();

  @override
  void initState() {
    super.initState();
    _username.clear();
  }

  @override
  void dispose() {
    super.dispose();
    _username.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Enter User Name'),
      ),
      body: Padding(
        padding: EdgeInsets.symmetric(horizontal: 100, vertical: 25),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: <Widget>[
            Text(
              'Enter User Name:',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            TextField(
              controller: _username,
              autofocus: true,
              onChanged: (_) => setState(() {}),
            ),
            RaisedButton(
              child: Text('Next'),
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.all(Radius.circular(5))),
              color: Colors.green,
              onPressed: _username.text.length < 5
                  ? null
                  : () {
                      Navigator.pop(context, _username.text);
                    },
            ),
          ],
        ),
      ),
    );
  }
}
