
import 'package:flutter/material.dart';
import 'package:stargate/add_gate.dart';
import 'package:stargate/bloc/bloc_provider.dart';
import 'package:stargate/bloc/config_bloc.dart';
import 'package:stargate/gate.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  final title = 'Stargate';

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      bloc: ConfigBLoC(),
      child: MaterialApp(
        title: title,
        theme: ThemeData(
          primarySwatch: Colors.blue,
        ),
        home: GatesPage(),
      ),
    );
  }
}

class GatesPage extends StatelessWidget {

  Widget gateCard(BuildContext context, GateConfig gate) {
    return Gate(
      user: BlocProvider.of<ConfigBLoC>(context).username,
      gateConfig: gate,
    );
  }

  @override
  Widget build(BuildContext context) {
    final configProvider = BlocProvider.of<ConfigBLoC>(context);
    return StreamBuilder<List<GateConfig>>(
      stream: configProvider.configStream,
      builder: (context, snapshot) {
        final gates = snapshot.data ?? [];
        return Scaffold(
          appBar: AppBar(
            title: Text('Stargate'),
          ),
          body: Padding(
            padding: EdgeInsets.symmetric(horizontal: 25, vertical: 10),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              children: gates.map((e) => gateCard(context, e)).toList(),
            ),
          ),
          floatingActionButton: FloatingActionButton(
            child: Icon(Icons.add),
            onPressed: () async {
              String config = await Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => AddGate())
              );
              configProvider.addConfig(config);            },
          ),
        );
      },
    );
  }
}

