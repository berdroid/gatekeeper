import 'package:flutter/material.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:stargate/add_gate.dart';
import 'package:stargate/bloc/bloc_provider.dart';
import 'package:stargate/bloc/config_bloc.dart';
import 'package:stargate/gate.dart';
import 'package:stargate/set_user.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  final title = 'Stargate';

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      bloc: ConfigBLoC.instance(),
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

class GatesPage extends StatefulWidget {
  @override
  _GatesPageState createState() => _GatesPageState();
}

class _GatesPageState extends State<GatesPage> {
  @override
  void initState() {
    super.initState();
    _getPermission();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final configProvider = BlocProvider.of<ConfigBLoC>(context);
      configProvider.load().then((value) async {
        if (await _getUsernameIfNeeded(context, configProvider) ||
            configProvider.numConfigs == 0)
          _getGateConfigIfPossible(context, configProvider);
      });
    });
  }

  Future<bool> _getUsernameIfNeeded(BuildContext context, ConfigBLoC configProvider) async {
    return Future<bool>(() async {
      if (configProvider.username == null) {
        String username = await Navigator.push(
          context, MaterialPageRoute(builder: (context) => SetUser())
        );
        if (username != null) {
          await configProvider.setUsername(username);
          return true;
        }
      }
      return false;
    });
  }

  _getGateConfigIfPossible(BuildContext context, ConfigBLoC configProvider) async {
    if (configProvider.username != null) {
      String config = await Navigator.push(
          context, MaterialPageRoute(builder: (context) => AddGate()));
      if (config != null) await configProvider.addConfig(config);
    }
  }

  _getPermission() async {
    Map<PermissionGroup, PermissionStatus> permissions = await PermissionHandler().requestPermissions([
      PermissionGroup.location,
      PermissionGroup.locationAlways,
    ]);
    print(permissions);
  }

  Widget gateCard(BuildContext context, GateConfig gate) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 25, vertical: 12.5),
      child: Gate(
        user: BlocProvider.of<ConfigBLoC>(context).username,
        gateConfig: gate,
      ),
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
            leading: Container(height: 1),
            title: Text('Stargate'),
          ),
          body: Padding(
            padding: EdgeInsets.symmetric(horizontal: 25, vertical: 37.5),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,

              children: gates.map((e) => gateCard(context, e)).toList(),
            ),
          ),
          drawer: Drawer(
            child: Column(
              children: <Widget>[
                DrawerHeader(child: Text('Actions')),
                Spacer(flex: 25),
                ListTile(
                  leading: Icon(Icons.add_location),
                  title: Text('Add Gate'),
                  onTap: () {
                    Navigator.pop(context);
                    _getUsernameIfNeeded(context, configProvider);
                    _getGateConfigIfPossible(context, configProvider);
                  },
                ),
                Spacer(flex: 1),
                ListTile(
                  leading: Icon(Icons.delete),
                  title: Text('Delete All'),
                  onLongPress: () {
                    Navigator.pop(context);
                    configProvider.clearConfigs();
                  },
                ),
              ],
            ),
          ),

        );
      },
    );
  }
}
