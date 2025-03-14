// FLUTTER
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
// API_SERVICE
import 'package:appfront/data/repositories/api_service.dart';

class LoginForm extends StatefulWidget {
  const LoginForm({super.key});

  @override
  LoginFormState createState() => LoginFormState();
}

class LoginFormState extends State<LoginForm> {
  final TextEditingController emailController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();
  final _formKey = GlobalKey<FormState>();
  
  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        children: [
          TextFormField(
            controller: emailController,
            decoration: InputDecoration(labelText: 'Email'),
            keyboardType: TextInputType.emailAddress,
            validator: (value) {
              if (value == null || value.isEmpty) {
                return 'Por favor ingrese su email';
              } else if (!RegExp(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$").hasMatch(value)) {
                return 'Ingrese un email válido';
              } else {
              return null;
              }
            },
          ),
          TextFormField(
            controller: passwordController,
            decoration: InputDecoration(labelText: 'Contraseña'),
            obscureText: true,
            validator: (value) {
              if (value == null || value.isEmpty) {
                return 'Por favor ingrese su contraseña';
              } else if (value.length < 6) {
                return 'La contraseña debe tener al menos 6 caracteres';
              } else {
              return null;
              }
            },
          ),
          SizedBox(height: 20),
          ElevatedButton(
            onPressed: () async {
              if (_formKey.currentState!.validate()) {
                String email = emailController.text;
                String password = passwordController.text;
                final messenger = ScaffoldMessenger.of(context);
                final currentContext = context;

                try {
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
                    messenger.showSnackBar(
                      SnackBar(content: Text(response['message'])),
                    );
                  }
                } catch (e) {
                  messenger.showSnackBar(
                    SnackBar(content: Text('Error al conectar con el servidor. Inténtelo de nuevo.')),
                  );
                }
              }
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: Theme.of(context).colorScheme.secondary,
              foregroundColor: Theme.of(context).colorScheme.onSecondary,
              padding: const EdgeInsets.symmetric(horizontal: 50, vertical: 15),
            ),
            child: const Text('Iniciar Sesión'),
          ),
        ],
      ),
    );
  }
}
