import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final args = ModalRoute.of(context)!.settings.arguments as Map<String, dynamic>;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Pantalla Principal'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('Hola, Bienvenido ${args['first_name']} ${args['last_name']}!'),
            const SizedBox(height: 20),
            //Text('Grupos: ${args['groups'].map((g) => g['name']).join(", ")}'),
          ],
        ),
      ),
    );
  }
}
