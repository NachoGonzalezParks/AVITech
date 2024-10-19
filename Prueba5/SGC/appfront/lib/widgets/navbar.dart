import 'package:flutter/material.dart';

class NavBar extends StatelessWidget implements PreferredSizeWidget {
  final List<Widget> actions;

  const NavBar({super.key, required this.actions});

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    return AppBar(
      backgroundColor: colorScheme.primary,
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
              color: colorScheme.onPrimary,
              fontSize: 24,
              fontWeight: FontWeight.bold,
            ),
          ),
          // Botones a la derecha (recibidos como parámetro)
          Row(children: actions),
        ],
      ),
    );
  }

  @override
  Size get preferredSize => const Size.fromHeight(60.0);
}