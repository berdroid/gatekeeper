

import 'package:flutter/cupertino.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';

class Notify {

  final FlutterLocalNotificationsPlugin ntf;

  final cbMap = Map<String,VoidCallback>();

  Notify._() :
  ntf = FlutterLocalNotificationsPlugin()
  {
    //initialise the plugin. app_icon needs to be a added as a drawable resource to the Android head project
    var initAndroid = AndroidInitializationSettings('ic_launcher');
    var initIOS = IOSInitializationSettings(
        onDidReceiveLocalNotification: onReceiveNotify);
    var init = InitializationSettings(initAndroid, initIOS);
    ntf.initialize(init, onSelectNotification: onSelectNotify);
  }

  static Notify _instance;

  factory Notify.instance() {
    if (_instance == null) {
      _instance = Notify._();
    }
    return _instance;
  }

  Future onSelectNotify(String id) async {
    if (id != null) {
      debugPrint('notification payload: $id');
      cbMap[id]();
    }
  }

  Future onReceiveNotify(
  int id, String title, String body, String payload) async {

  }

  void showNotify(int id, String title, String body, VoidCallback cb) {
    var android = AndroidNotificationDetails(
        'your channel id', 'your channel name', 'your channel description',
        importance: Importance.Max, priority: Priority.High,
      timeoutAfter: 10000,
    );
    var ios = IOSNotificationDetails();
    var platformChannelSpecifics = NotificationDetails(android, ios);
    cbMap['$id'] = cb;
    ntf.show(
        id, title, body, platformChannelSpecifics,
        payload: '$id');
  }

  void cancelAll() {
    ntf.cancelAll();
  }
}