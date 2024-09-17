import 'package:flutter/material.dart';

class Home extends StatelessWidget {
  const Home({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('ZEUS'),
        actions: [
          // Adding the button to open the modal at the right side of the AppBar
          TextButton(
            onPressed: () {
              // Show the modal when the button is pressed
              showModalBottomSheet(
                context: context,
                isScrollControlled: true,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
                ),
                builder: (context) => AuthModal(),
              );
            },
            child: Text(
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
      padding: EdgeInsets.all(16.0),
      child: Column(
        children: [
          TabBar(
            controller: _tabController,
            labelColor: Colors.blue,
            unselectedLabelColor: Colors.grey,
            indicatorColor: Colors.blue,
            tabs: [
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
  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Column(
        children: [
          TextField(
            decoration: InputDecoration(labelText: 'Nombre'),
          ),
          TextField(
            decoration: InputDecoration(labelText: 'Apellido'),
          ),
          TextField(
            decoration: InputDecoration(labelText: 'Email'),
          ),
          TextField(
            decoration: InputDecoration(labelText: 'Código de área'),
          ),
          TextField(
            decoration: InputDecoration(labelText: 'Teléfono'),
          ),
          TextField(
            decoration: InputDecoration(labelText: 'Contraseña'),
            obscureText: true,
          ),
          TextField(
            decoration: InputDecoration(labelText: 'Repite tu contraseña'),
            obscureText: true,
          ),
          Row(
            children: [
              Checkbox(value: false, onChanged: (value) {}),
              GestureDetector(
                onTap: () {
                  // Handle terms and conditions link
                },
                child: Text('Acepto los Términos y condiciones'),
              ),
            ],
          ),
          SizedBox(height: 20),
          ElevatedButton(
            onPressed: () {
              // Handle Register action
            },
            child: Text('Crear cuenta'),
          ),
        ],
      ),
    );
  }
}

class LoginForm extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Column(
        children: [
          TextField(
            decoration: InputDecoration(labelText: 'Email'),
          ),
          TextField(
            decoration: InputDecoration(labelText: 'Contraseña'),
            obscureText: true,
          ),
          SizedBox(height: 10),
          GestureDetector(
            onTap: () {
              // Handle forgot password link
            },
            child: Text('¿Olvidaste tu contraseña?', style: TextStyle(color: Colors.blue)),
          ),
          SizedBox(height: 20),
          ElevatedButton(
            onPressed: () {
              // Handle Login action
            },
            child: Text('Iniciar sesión'),
          ),
          SizedBox(height: 10),
          GestureDetector(
            onTap: () {
              // Handle account creation
            },
            child: Text('¿No tenés cuenta de organizador? Creá tu cuenta'),
          ),
        ],
      ),
    );
  }
}






