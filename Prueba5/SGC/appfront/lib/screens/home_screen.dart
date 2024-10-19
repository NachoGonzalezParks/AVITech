import 'package:flutter/material.dart';
import 'package:appfront/widgets/navbar.dart';
import 'package:appfront/widgets/footer.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;

    return Scaffold(
      appBar: NavBar(
        actions: [
          TextButton(
            onPressed: () {
              // Lógica para cerrar sesión
              Navigator.pushReplacementNamed(context, '/landing');
            },
            child: Text('Cerrar Sesión', style: TextStyle(color: colorScheme.onPrimary)),
          ),
        ],
      ),
      body: Center(
        child: Text('Bienvenido a la página principal de Zeus'),
      ),
      bottomNavigationBar: const FooterBar(),
    );
  }
}
