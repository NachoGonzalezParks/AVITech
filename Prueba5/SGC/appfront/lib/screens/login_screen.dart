import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:appfront/api_service.dart';
import 'package:appfront/widgets/page_structure01.dart';
import 'package:appfront/widgets/custom_text_field.dart';

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

    return PageStructure01(
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

              if (response['success']) {

                  var userDetails = {
                    'first_name': response['first_name'],
                    'last_name': response['last_name'],
                    'username': response['username'],
                    'email': response['email'],
                    'groups': response['groups'],
                  };
                
                Navigator.pushReplacementNamed(
                  currentContext,
                  '/home',
                  arguments: userDetails,
                );
              } else {
                // Si hay un error, muestra el mensaje del error
                messenger.showSnackBar(
                  SnackBar(content: Text(response['message'])),
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
