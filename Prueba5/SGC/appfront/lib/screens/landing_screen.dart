import 'package:flutter/material.dart';
import 'package:appfront/widgets/navbar.dart';
import 'package:appfront/widgets/footer.dart';

class LandingScreen extends StatelessWidget {
  const LandingScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;

    return Scaffold(
      appBar: NavBar(
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pushReplacementNamed(context, '/login');
            },
            child: Text('Login', style: TextStyle(color: colorScheme.onPrimary)),
          ),
          TextButton(
            onPressed: () {
              Navigator.pushReplacementNamed(context, '/register');
            },
            child: Text('Register', style: TextStyle(color: colorScheme.onPrimary)),
          ),
        ],
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            // Sección de promoción
            Container(
              padding: const EdgeInsets.symmetric(vertical: 50, horizontal: 20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  const Text(
                    'Bienvenido a Zeus',
                    style: TextStyle(
                      fontSize: 32,
                      fontWeight: FontWeight.bold,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 20),
                  Text(
                    'Gestiona tus canchas de manera eficiente con nuestra app. '
                    'Reserva, organiza y administra todas tus actividades deportivas desde un solo lugar.',
                    style: TextStyle(
                      fontSize: 18,
                      color: Colors.grey[700], // Texto gris para detalles
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 40),
                  ElevatedButton(
                    onPressed: () {
                      // Acción para descargar app o más información
                    },
                    style: ElevatedButton.styleFrom(
                      backgroundColor: colorScheme.secondary, // Botón con color secundario (naranja)
                      foregroundColor: colorScheme.onSecondary, // Texto sobre botón
                      padding: const EdgeInsets.symmetric(horizontal: 50, vertical: 15),
                    ),
                    child: const Text('Descargar la App'),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
      bottomNavigationBar: const FooterBar(),
    );
  }
}
