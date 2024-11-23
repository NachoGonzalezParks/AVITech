// File: widgets/navbar.dart
import 'package:flutter/material.dart';

class NavBar extends StatelessWidget implements PreferredSizeWidget {
  const NavBar({Key? key}) : super(key: key);

  List<Widget> _getActions(BuildContext context) {
    final currentRoute = ModalRoute.of(context)?.settings.name;

    if (currentRoute == '/login') {
      return [
        TextButton(
          onPressed: () => Navigator.pushReplacementNamed(context, '/landing'),
          child: const Text('Home', style: TextStyle(color: Colors.white)),
        ),
      ];
    } else if (currentRoute == '/register') {
      return [
        TextButton(
          onPressed: () => Navigator.pushReplacementNamed(context, '/login'),
          child: const Text('Login', style: TextStyle(color: Colors.white)),
        ),
        TextButton(
          onPressed: () => Navigator.pushReplacementNamed(context, '/landing'),
          child: const Text('Home', style: TextStyle(color: Colors.white)),
        ),
      ];
    } else if (currentRoute == '/home') {
      return [
        TextButton(
          onPressed: () => Navigator.pushReplacementNamed(context, '/landing'),
          child: const Text('Cerrar Sesión', style: TextStyle(color: Colors.white)),
        ),
      ];
    } else {
      return [
        TextButton(
          onPressed: () => Navigator.pushNamed(context, '/login'),
          child: const Text('Login', style: TextStyle(color: Colors.white)),
        ),
        TextButton(
          onPressed: () => Navigator.pushNamed(context, '/register'),
          child: const Text('Register', style: TextStyle(color: Colors.white)),
        ),
      ];
    }
  }

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    return AppBar(
      backgroundColor: colorScheme.primary,
      elevation: 0,
      leading: IconButton(
        icon: const Icon(Icons.arrow_back, color: Colors.white), // Back arrow icon
        onPressed: () {
          Navigator.maybePop(context); // Go back to the previous screen if possible
        },
      ),
      title: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          // Center title
        // Título alineado a la izquierda
          Expanded(
            flex: 4,
            child: Text(
              'ZEUS',
              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white),
              textAlign: TextAlign.left, // Alineación del texto a la izquierda
            ),
          ),
          // Buttons on the right
          Expanded(
            flex: 3,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.end,
              children: _getActions(context),
            ),
          ),
        ],
      ),
    );
  }

  @override
  Size get preferredSize => const Size.fromHeight(60.0);
}
