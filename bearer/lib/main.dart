import 'dart:io';

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:path_provider/path_provider.dart';
import 'package:stargate/add_gate.dart';
import 'package:stargate/bloc/bloc_provider.dart';
import 'package:stargate/bloc/config_bloc.dart';
import 'package:stargate/gate.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  final title = 'Stargate';

  final picker = ImagePicker();

  MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      bloc: ConfigBLoC.instance,
      child: MaterialApp(
        title: title,
        theme: ThemeData(
          primarySwatch: Colors.blue,
        ),
        home: const GatesPage(),
      ),
    );
  }
}

class GatesPage extends StatefulWidget {
  const GatesPage({Key? key}) : super(key: key);

  @override
  _GatesPageState createState() => _GatesPageState();
}

class _GatesPageState extends State<GatesPage> {
  File? _bgImage;

  @override
  void initState() {
    super.initState();
    _readBackgroundImage();
    WidgetsBinding.instance!.addPostFrameCallback((_) {
      final configProvider = BlocProvider.of<ConfigBLoC>(context);
      configProvider.load().then((_) {
        if (configProvider.numConfigs == 0) {
          _getGateConfig(context, configProvider);
        }
      });
    });
  }

  _getGateConfig(BuildContext context, ConfigBLoC configProvider) async {
    String? config = await Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => const AddGate()),
    );
    if (config != null) configProvider.addConfig(config);
  }

  Future<String> get _bgImagePath async {
    final appDir = await getApplicationDocumentsDirectory();
    return '${appDir.path}/app_background';
  }

  _pickBackGroundImage() async {
    final pickedFile = await (ImagePicker().pickImage(source: ImageSource.gallery));
    if (pickedFile != null) {
      final File image = File(pickedFile.path);
      final File bgImage = await image.copy(await _bgImagePath);

      setState(() {
        imageCache!.clear();
        _bgImage = bgImage;
      });
    }
  }

  _readBackgroundImage() async {
    final File bgImage = File(await _bgImagePath);

    if (await bgImage.exists()) {
      setState(() {
        _bgImage = bgImage;
      });
    }
  }

  _deleteBackgroundImage() async {
    if (_bgImage != null && await _bgImage!.exists()) {
      _bgImage!.delete();
      setState(() {
        _bgImage = null;
      });
    }
  }

  Widget gateCard(BuildContext context, GateConfig gate) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 25, vertical: 12.5),
      child: Gate(gateConfig: gate),
    );
  }

  @override
  Widget build(BuildContext context) {
    final configBloc = BlocProvider.of<ConfigBLoC>(context);
    return StreamBuilder<List<GateConfig>>(
      stream: configBloc.configStream,
      builder: (context, snapshot) {
        final gates = snapshot.data ?? [];
        return Scaffold(
          appBar: AppBar(
            leading: Image.asset('res/images/app_icon_transp.png'),
            title: const Text('Stargate'),
          ),
          body: Container(
            decoration: BoxDecoration(
              image: DecorationImage(
                image: _bgImage != null
                    ? FileImage(_bgImage!) as ImageProvider<Object>
                    : const AssetImage('res/images/background.jpg'),
                fit: BoxFit.cover,
              ),
            ),
            constraints: const BoxConstraints.expand(),
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 25, vertical: 37.5),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.start,
                children: gates.map((e) => gateCard(context, e)).toList(),
              ),
            ),
          ),
          drawer: Drawer(
            child: Column(
              children: <Widget>[
                const DrawerHeader(child: Text('Actions')),
                const Spacer(flex: 25),
                ListTile(
                  leading: const Icon(Icons.landscape),
                  title: const Text('Background'),
                  onTap: () {
                    Navigator.pop(context);
                    _pickBackGroundImage();
                  },
                  onLongPress: () {
                    Navigator.pop(context);
                    _deleteBackgroundImage();
                  },
                ),
                const Spacer(flex: 1),
                ListTile(
                  leading: const Icon(Icons.add_location),
                  title: const Text('Add Gate'),
                  onTap: () {
                    Navigator.pop(context);
                    _getGateConfig(context, configBloc);
                  },
                ),
                const Spacer(flex: 1),
                ListTile(
                  leading: const Icon(Icons.delete),
                  title: const Text('Delete All'),
                  onTap: () {
                    Navigator.pop(context);
                  },
                  onLongPress: () async {
                    Navigator.pop(context);
                    configBloc.clearConfigs();
                    _deleteBackgroundImage();
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
