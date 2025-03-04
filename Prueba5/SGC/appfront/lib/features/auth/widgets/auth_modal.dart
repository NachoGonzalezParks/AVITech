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

  @override
  Widget build(BuildContext context) {
    return Dialog(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          TabBar(
            controller: _tabController,
            tabs: [
              Tab(text: 'Crear cuenta'),
              Tab(text: 'Iniciar sesión'),
            ],
          ),
          Container(
            height: 600,
            padding: EdgeInsets.all(16),
            child: TabBarView(
              controller: _tabController,
              children: [
                RegisterForm(),
                LoginForm(),
              ],
            ),
          ),
        ],
      ),
    );
  }
}