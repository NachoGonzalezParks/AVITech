import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:appfront/api_service.dart';  // Servicio API que se conecta con el backend Django

class Home extends StatelessWidget {
  const Home({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('ZEUS'),
        actions: [
          TextButton(
            onPressed: () {
              showModalBottomSheet(
                context: context,
                isScrollControlled: true,
                shape: const RoundedRectangleBorder(
                  borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
                ),
                builder: (context) => AuthModal(),
              );
            },
            child: const Text(
              'Login/Registro',
              style: TextStyle(color: Colors.black),
            ),
          ),
        ],
      ),
      bottomNavigationBar: BottomAppBar(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              TextButton(
                onPressed: () {
                  // Acción para Política de Privacidad
                },
                child: const Text('Política de Privacidad'),
              ),
              TextButton(
                onPressed: () {
                  // Acción para Términos de Uso
                },
                child: const Text('Términos de Uso'),
              ),
              TextButton(
                onPressed: () {
                  // Acción para Contacto
                },
                child: const Text('Contacto'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class AuthModal extends StatefulWidget {
  @override
  _AuthModalState createState() => _AuthModalState();
}

class _AuthModalState extends State<AuthModal> with SingleTickerProviderStateMixin {
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      height: MediaQuery.of(context).size.height * 0.75,
      padding: const EdgeInsets.all(16.0),
      child: Column(
        children: [
          TabBar(
            controller: _tabController,
            labelColor: Colors.blue,
            unselectedLabelColor: Colors.grey,
            indicatorColor: Colors.blue,
            tabs: const [
              Tab(text: 'Crear cuenta'), // Register tab
              Tab(text: 'Iniciar sesión'), // Login tab
            ],
          ),
          Expanded(
            child: TabBarView(
              controller: _tabController,
              children: [
                RegisterForm(), // Registration Form
                LoginForm(), // Login Form
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class RegisterForm extends StatelessWidget {
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _surnameController = TextEditingController();
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _phoneController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  final TextEditingController _confirmPasswordController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Column(
        children: [
          TextField(
            controller: _nameController,
            decoration: const InputDecoration(labelText: 'Nombre'),
          ),
          TextField(
            controller: _surnameController,
            decoration: const InputDecoration(labelText: 'Apellido'),
          ),
          TextField(
            controller: _emailController,
            decoration: const InputDecoration(labelText: 'Email'),
          ),
          TextField(
            controller: _phoneController,
            decoration: const InputDecoration(labelText: 'Teléfono'),
          ),
          TextField(
            controller: _passwordController,
            decoration: const InputDecoration(labelText: 'Contraseña'),
            obscureText: true,
          ),
          TextField(
            controller: _confirmPasswordController,
            decoration: const InputDecoration(labelText: 'Repite tu contraseña'),
            obscureText: true,
          ),
          Row(
            children: [
              Checkbox(value: false, onChanged: (value) {}),
              GestureDetector(
                onTap: () {
                  // Handle terms and conditions link
                },
                child: const Text('Acepto los Términos y condiciones'),
              ),
            ],
          ),
          const SizedBox(height: 20),
          ElevatedButton(
            onPressed: () async {
              if (_passwordController.text == _confirmPasswordController.text) {
                var response = await Provider.of<ApiService>(context, listen: false).register(
                  _nameController.text,
                  _surnameController.text,
                  _emailController.text,
                  _phoneController.text,
                  _passwordController.text,
                );

                if (response != null && response['token'] != null) {
                  Navigator.pushReplacementNamed(context, '/home');
                } else {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Error al crear la cuenta')),
                  );
                }
              } else {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Las contraseñas no coinciden')),
                );
              }
            },
            child: const Text('Crear cuenta'),
          ),
        ],
      ),
    );
  }
}

class LoginForm extends StatelessWidget {
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Column(
        children: [
          TextField(
            controller: _emailController,
            decoration: const InputDecoration(labelText: 'Email'),
          ),
          TextField(
            controller: _passwordController,
            decoration: const InputDecoration(labelText: 'Contraseña'),
            obscureText: true,
          ),
          const SizedBox(height: 10),
          GestureDetector(
            onTap: () {
              // Handle forgot password link
            },
            child: const Text('¿Olvidaste tu contraseña?', style: TextStyle(color: Colors.blue)),
          ),
          const SizedBox(height: 20),
          ElevatedButton(
            onPressed: () async {
              var response = await Provider.of<ApiService>(context, listen: false).login(
                _emailController.text,
                _passwordController.text,
              );

              if (response != null && response['token'] != null) {
                Navigator.pushReplacementNamed(context, '/home');
              } else {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Error de inicio de sesión')),
                );
              }
            },
            child: const Text('Iniciar sesión'),
          ),
          const SizedBox(height: 10),
          GestureDetector(
            onTap: () {
              // Handle account creation
            },
            child: const Text('¿No tenés cuenta de organizador? Creá tu cuenta'),
          ),
        ],
      ),
    );
  }
}
