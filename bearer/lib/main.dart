import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
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
  Future frontGate = rootBundle.loadString('res/front.json');
  Future backDoor = rootBundle.loadString('res/back.json');

  String username = 'bernhard';

  _MyHomePageState();

  Widget gateCard(Future future) {
    return FutureBuilder<String>(
      future: future,
      builder: (BuildContext context, AsyncSnapshot<String> snapshot) {
        if (snapshot.hasData) {
          return Gate(
            user: username,
            config: snapshot.data,
          );
        } else {
          return SizedBox(
            child: CircularProgressIndicator(),
            width: 60,
            height: 60,
          );
        }
      },
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
          children: <Widget>[
            gateCard(frontGate),
            gateCard(backDoor),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        child: Icon(Icons.add),
      ), // This trailing comma makes auto-formatting nicer for build methods.
    );
  }
}
