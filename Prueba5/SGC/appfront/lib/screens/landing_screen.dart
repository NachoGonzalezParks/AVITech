import 'package:flutter/material.dart';

class LandingScreen extends StatelessWidget {
  const LandingScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;

    return Scaffold(
      appBar: AppBar(
        backgroundColor: colorScheme.primary, // Fondo con el color primario (azul)
        elevation: 0,
        title: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            // Logo en la izquierda
            Container(
              width: 50, // Cambia el tamaño según la imagen que insertes
              height: 50,
              decoration: const BoxDecoration(
                image: DecorationImage(
                  image: AssetImage('assets/logo.png'), // Ruta del logo
                  fit: BoxFit.cover,
                ),
              ),
            ),
            // Título en el centro
            Text(
              'Zeus',
              style: TextStyle(
                color: colorScheme.onPrimary, // Color de texto sobre color primario
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
            // Botones de Login y Registro a la derecha
            Row(
              children: [
                TextButton(
                  onPressed: () {
                    Navigator.pushNamed(context, '/login');
                  },
                  child: Text('Login', style: TextStyle(color: colorScheme.onPrimary)),
                ),
                TextButton(
                  onPressed: () {
                    Navigator.pushNamed(context, '/register');
                  },
                  child: Text('Register', style: TextStyle(color: colorScheme.onPrimary)),
                ),
              ],
            ),
          ],
        ),
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
      bottomNavigationBar: BottomAppBar(
        color: colorScheme.primary, // Footer con el color primario
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                '© 2024 Zeus App',
                style: TextStyle(color: colorScheme.onPrimary), // Texto con el color adecuado
              ),
              Row(
                children: [
                  TextButton(
                    onPressed: () {
                      // Acción para ir a términos y condiciones
                    },
                    child: Text(
                      'Términos y Condiciones',
                      style: TextStyle(color: colorScheme.onPrimary), // Texto sobre fondo primario
                    ),
                  ),
                  TextButton(
                    onPressed: () {
                      // Acción para ir a política de privacidad
                    },
                    child: Text(
                      'Política de Privacidad',
                      style: TextStyle(color: colorScheme.onPrimary), // Texto sobre fondo primario
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
