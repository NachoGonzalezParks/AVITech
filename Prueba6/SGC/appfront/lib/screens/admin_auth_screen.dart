import 'package:flutter/material.dart';
import 'package:appfront/widgets/auth_tab.dart';

class AdminAuthScreen extends StatelessWidget {
  const AdminAuthScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [Color(0xFF1E5799), Color(0xFF207CCA)],
          ),
        ),
        child: Center(
          child: Container(
            constraints: BoxConstraints(
              maxWidth: 600,
              maxHeight: MediaQuery.of(context).size.height * 0.9,
            ),
            child: Card(
              margin: const EdgeInsets.all(16),
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Text(
                      'Acceso Administradores',
                      style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 20),
                    // Widget AuthTab simplificado sin parámetros de pestaña
                    const Expanded(
                      child: AuthTab(userType: 'admin'),
                    ),
                    TextButton(
                      onPressed: () => Navigator.pop(context),
                      child: const Text('Volver'),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}