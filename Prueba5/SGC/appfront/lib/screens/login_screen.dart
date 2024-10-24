import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:appfront/api_service.dart';
import 'package:appfront/widgets/navbar.dart'; // Incluimos el NavBar modularizado
import 'package:appfront/widgets/footer.dart'; // Incluimos el FooterBar modularizado

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  LoginScreenState createState() => LoginScreenState();
}

class LoginScreenState extends State<LoginScreen> {
  final TextEditingController emailController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;

    return Scaffold(
      appBar: NavBar(
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pushReplacementNamed(context, '/landing');
            },
            child: Text('Home', style: TextStyle(color: colorScheme.onPrimary)),
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const Text(
              'Bienvenido',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 20),
            TextField(
              controller: emailController,
              decoration: const InputDecoration(
                labelText: 'Email',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 10),
            TextField(
              controller: passwordController,
              decoration: const InputDecoration(
                labelText: 'Password',
                border: OutlineInputBorder(),
              ),
              obscureText: true,
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () async {
                String email = emailController.text;
                String password = passwordController.text;

                final messenger = ScaffoldMessenger.of(context);
                final currentContext = context;

                var response = await Provider.of<ApiService>(currentContext, listen: false).login(email, password);

                if (!context.mounted) return;

                /*
                if (response['key'] != null) {
                  String token = response['key'];
                  // Llamar a la función para obtener los detalles del usuario
                  var userDetails = await Provider.of<ApiService>(currentContext, listen: false).getUserDetails(token);

                  Navigator.pushReplacementNamed(
                    currentContext,
                    '/home',
                    arguments: {
                      'first_name': userDetails['first_name'],
                      'last_name': userDetails['last_name'],
                    },
                  );
                }
                */
                /*
                if (response['key'] != null) {
                    Navigator.pushReplacementNamed(
                      currentContext,
                      '/home',
                      arguments: {
                        'first_name': response['first_name'],
                        'last_name': response['last_name'],
                        'groups': response['groups'], 
                      },
                    );
                } */
                if (response['key'] != null) {
                    String token = response['key'];
                    var userDetails = await Provider.of<ApiService>(currentContext, listen: false).getUserDetails(token);
                    Navigator.pushReplacementNamed(
                      currentContext,
                      '/home',
                      arguments: {
                        'first_name': userDetails['first_name'],
                        'last_name': userDetails['last_name'],
                        //'groups': userDetails['groups'], 
                      },
                    );
                }else {
                    messenger.showSnackBar(
                      const SnackBar(content: Text('Error de inicio de sesión (algo salió mal)')),
                    );
                }
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: colorScheme.secondary,
                foregroundColor: colorScheme.onSecondary,
                padding: const EdgeInsets.symmetric(horizontal: 50, vertical: 15),
              ),
              child: const Text('Iniciar Sesión'),
            ),
            TextButton(
              onPressed: () {
                Navigator.pushNamed(context, '/register');
              },
              child: const Text('Registrarse'),
            ),
          ],
        ),
      ),
      bottomNavigationBar: const FooterBar(),
    );
  }
}
