import 'package:flutter/material.dart';
import 'register_form.dart';
import 'login_form.dart';

class AuthModal extends StatefulWidget {
  @override
  AuthModalState createState() => AuthModalState();
}

class AuthModalState extends State<AuthModal> with SingleTickerProviderStateMixin {
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
  }

  // Método para cambiar a la solapa "Iniciar sesión"
  void cambiarASolapaIniciarSesion() {
    _tabController.animateTo(1); // Cambiar a la segunda solapa (índice 1)
  }  

  @override
  Widget build(BuildContext context) {
    return Dialog(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          TabBar(
            controller: _tabController,
            tabs: const [
              Tab(text: 'Crear cuenta'),
              Tab(text: 'Iniciar sesión'),
            ],
          ),
          Container(
            height: 600,
            padding: const EdgeInsets.all(16),
            child: TabBarView(
              controller: _tabController,
              children: [
                RegisterForm(cambiarASolapaIniciarSesion: cambiarASolapaIniciarSesion, // Pasar el método como parámetro
                ),
                const LoginForm(),
              ],
            ),
          ),
        ],
      ),
    );
  }
}