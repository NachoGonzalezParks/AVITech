import 'package:flutter/material.dart';
//import 'package:appfront/routes.dart';
//import 'package:appfront/screens/welcome_screen.dart';
// ROUTES
import 'package:appfront/routes.dart';


void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Torneos App',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      //Configuración de rutas
      initialRoute: Routes.welcome, // Ruta inicial
      routes: Routes.getRoutes(), // Todas las rutas definidas      
      //home: WelcomeScreen(), // Esta es tu pantalla de inicio
    );
  }
}