import 'package:flutter/material.dart';
import 'package:appfront/screens/welcome_screen.dart';
import 'package:appfront/screens/admin_auth_screen.dart';
import 'package:appfront/screens/dashboard_screen.dart';
// Importa las demás pantallas según las vayas necesitando

class Routes {
  static const welcome = '/';
  static const adminAuth = '/admin-auth';
  static const playerAuth = '/player-auth';
  static const dashboard = '/dashboard';
  static const tournaments = '/tournaments';
  static const teams = '/teams';
  static const fixture = '/fixture';
  static const settings = '/settings';

  static Map<String, WidgetBuilder> getRoutes() {
    return {
      welcome: (context) => WelcomeScreen(),
      adminAuth: (context) => AdminAuthScreen(),
      //playerAuth: (context) => PlayerAuthScreen(),
      dashboard: (context) => DashboardScreen(),
      // Agregar más rutas según sea necesario
    };
  }
}