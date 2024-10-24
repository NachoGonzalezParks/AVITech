import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:appfront/api_service.dart';
import 'package:appfront/screens/landing_screen.dart';
import 'package:appfront/screens/login_screen.dart';
import 'package:appfront/screens/register_screen.dart';
import 'package:appfront/screens/home_screen.dart';

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
        theme: ThemeData(
          useMaterial3: true,
          colorScheme: ColorScheme.fromSeed(
            seedColor: const Color(0xFF0D1321), // Color primario (azul oscuro)
            secondary: Color.fromRGBO(209, 95, 13, 1), // Color secundario (naranja complementario)
          ),
        ),
        initialRoute: '/landing',
        routes: {
          '/landing': (context) => const LandingScreen(),
          '/login': (context) => const LoginScreen(),
          '/register': (context) => const RegisterScreen(),
          '/home': (context) => const HomeScreen(),
        },
      ),      

    );
  }
}


class ZeusAppState extends ChangeNotifier {

}