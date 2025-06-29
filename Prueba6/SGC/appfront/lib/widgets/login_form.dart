import 'package:flutter/material.dart';
import 'package:appfront/routes.dart';
import 'package:appfront/services/api_service.dart';
import 'package:flutter/services.dart';

class LoginForm extends StatefulWidget {
  final String userType;

  const LoginForm({Key? key, required this.userType}) : super(key: key);

  @override
  _LoginFormState createState() => _LoginFormState();
}

class _LoginFormState extends State<LoginForm> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final ApiService _apiService = ApiService();

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Form(
        key: _formKey,
        child: Column(
          children: [
            TextFormField(
              controller: _emailController,
              decoration: const InputDecoration(labelText: 'Email'),
              keyboardType: TextInputType.emailAddress,
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Por favor ingrese su email';
                }
                if (!value.contains('@')) {
                  return 'Ingrese un email válido';
                }
                return null;
              },
            ),
            const SizedBox(height: 12),
            TextFormField(
              controller: _passwordController,
              decoration: const InputDecoration(labelText: 'Contraseña'),
              obscureText: true,
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Por favor ingrese su contraseña';
                }
                if (value.length < 6) {
                  return 'La contraseña debe tener al menos 6 caracteres';
                }
                return null;
              },
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: widget.userType == 'admin' 
                  ? const Color.fromARGB(255, 189, 101, 29) 
                  : Colors.green,
                minimumSize: const Size(double.infinity, 50),
              ),
              onPressed: _submitForm,
              child: const Text('Ingresar'),
            ),
          ],
        ),
      ),
    );
  }

  void _submitForm() async {
    if (_formKey.currentState!.validate()) {
      try {
        showDialog(
          context: context,
          barrierDismissible: false,
          builder: (context) => const Center(child: CircularProgressIndicator()),
        );

        final response = await _apiService.login(
          _emailController.text.trim(),
          _passwordController.text.trim(),
        );

        Navigator.pop(context);

        if (response['success'] == true) {
          Navigator.pushNamedAndRemoveUntil(
            context, 
            Routes.dashboard, 
            (route) => false,
          );
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(response['message'] ?? 'Error desconocido'),
              backgroundColor: Colors.red,
              duration: const Duration(seconds: 60),
              action: SnackBarAction(
                label: 'Aceptar',
                textColor: Colors.white,
                onPressed: () {
                  ScaffoldMessenger.of(context).hideCurrentSnackBar();
                },
              ),
            ),
          );
        }
      } on PlatformException catch (e) {
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error: ${e.message ?? "Falló la conexión con el servidor"}'),
            backgroundColor: Colors.red,
            duration: const Duration(seconds: 60),
            action: SnackBarAction(
              label: 'Aceptar',
              textColor: Colors.white,
              onPressed: () {
                ScaffoldMessenger.of(context).hideCurrentSnackBar();
              },
            ),          
          ),
        );
      } catch (e) {
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error inesperado: ${e.toString()}'),
            backgroundColor: Colors.red,
            duration: const Duration(seconds: 60),
            action: SnackBarAction(
              label: 'Aceptar',
              textColor: Colors.white,
              onPressed: () {
                ScaffoldMessenger.of(context).hideCurrentSnackBar();
              },
            ),          
          ),
        );
      }
    }
  }

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }
}