// FLUTTER
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
// API_SERVICE
import 'package:appfront/data/repositories/api_service.dart';
// ROUTES
import 'package:appfront/routes/app_routes.dart';
// THEME
import 'package:appfront/themes/app_theme.dart';

void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => ApiService()),
      ],
      child: const ZeusApp(),
    ),
  );
}

class ZeusApp extends StatelessWidget {
  const ZeusApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => ZeusAppState(),
      child: MaterialApp(
        title: 'SGC',
        theme: AppTheme.buildTheme(),
        initialRoute: AppRoutes.initialRoute,
        routes: AppRoutes.routes,
      ),
    );
  }
}

class ZeusAppState extends ChangeNotifier {}
