
import 'package:flutter/material.dart';
import 'package:stargate/add_gate.dart';
import 'package:stargate/gate.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  final title = 'Stargate';

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: title,
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(title: title),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  var gates = <String>[];

  String username = 'bernhard';

  _MyHomePageState();

  Widget gateCard(String config) {
    return Gate(
      user: username,
      config: config,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: Padding(
        padding: EdgeInsets.symmetric(horizontal: 25, vertical: 10),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: gates.map((f) => gateCard(f)).toList(),
        ),
      ),
      floatingActionButton: FloatingActionButton(
        child: Icon(Icons.add),
        onPressed: () async {
          String config = await Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => AddGate())
          );
          setState(() => gates.add(config));
        },
      ),
    );
  }
}
