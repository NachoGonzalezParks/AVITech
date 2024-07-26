import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:flutter_app_3/api_service.dart'; 
import 'package:flutter_app_3/screens/login_screen.dart';
import 'package:flutter_app_3/screens/register_screen.dart';
import 'package:flutter_app_3/screens/home_screen.dart';

void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => ApiService()),
      ],
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SGC',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      initialRoute: '/login',
      routes: {
        '/login': (context) => const LoginScreen(),
        '/register': (context) => const RegisterScreen(),
        '/home': (context) => const HomeScreen(),
      },
    );
  }
}
