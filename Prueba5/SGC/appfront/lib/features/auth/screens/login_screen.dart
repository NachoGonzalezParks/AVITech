import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:appfront/data/repositories/api_service.dart';
import 'package:appfront/core/constants/app_structure.dart';
import 'package:appfront/core/widgets/custom_text_field.dart';

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

    return AppStructure(
      bodyContent: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: <Widget>[
          const Text(
            'Bienvenido',
            style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 20),
          CustomTextField(
            controller: emailController,
            labelText: 'Email',
            keyboardType: TextInputType.emailAddress,
          ),
          CustomTextField(
            controller: passwordController,
            labelText: 'Password',
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

              if (response['key'] != null) {
                String token = response['key'];
                var userDetails = await Provider.of<ApiService>(currentContext, listen: false).getUserDetails(token);
                Navigator.pushReplacementNamed(
                  currentContext,
                  '/home',
                  arguments: {
                    'first_name': userDetails['first_name'],
                    'last_name': userDetails['last_name'],
                  },
                );
              } else {
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
    );
  }
}
