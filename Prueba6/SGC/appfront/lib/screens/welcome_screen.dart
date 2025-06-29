import 'package:flutter/material.dart';
import 'package:appfront/routes.dart';

class WelcomeScreen extends StatelessWidget {
  const WelcomeScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [Color(0xFF1E5799), Color(0xFF207CCA)],
          ),
        ),
        child: Center(
          child: SingleChildScrollView(
            child: Card(
              elevation: 5,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(10),
              ),
              margin: const EdgeInsets.all(20),
              child: Container(
                padding: const EdgeInsets.all(32),
                width: 500,
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Image.asset('assets/images/Zeus.jpg', width: 150),
                    const SizedBox(height: 16),
                    const Text(
                      'Bienvenido a Zeus',
                      style: TextStyle(
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                        color: Color(0xFF1E5799),
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'Plataforma para administración de torneos deportivos ',
                      style: TextStyle(color: Colors.grey[600]),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 32),
                    Column(
                      children: [
                        ElevatedButton(
                          style: ElevatedButton.styleFrom(
                            //primary: Color(0xFF1E5799),
                            backgroundColor: const Color(0xFF1E5799),
                            foregroundColor: const Color.fromARGB(255, 255, 255, 255),
                            minimumSize: const Size(double.infinity, 50),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(5),
                            ),
                          ),
                          onPressed: () {
                            // Navegar a pantalla de administradores
                            // Navigator.push(context, MaterialPageRoute(builder: (_) => AdminAuthScreen()));
                            Navigator.pushNamed(context, Routes.adminAuth);
                          },
                          child: const Text('Administradores'),
                        ),
                        const SizedBox(height: 16),
                        ElevatedButton(
                          style: ElevatedButton.styleFrom(
                            //primary: Colors.green,
                            backgroundColor: Colors.green,
                            foregroundColor: const Color.fromARGB(255, 255, 255, 255),                            
                            minimumSize: const Size(double.infinity, 50),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(5),
                            ),
                          ),
                          onPressed: () {
                            // Navegar a pantalla de jugadores
                            // Navigator.push(context, MaterialPageRoute(builder: (_) => PlayerAuthScreen()));
                            //Navigator.pushNamed(context, Routes.playerAuth);
                          },
                          child: const Text('Jugadores'),
                        ),
                      ],
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