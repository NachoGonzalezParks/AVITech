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
          // Logo
          Expanded(
            flex: 2, // Equivalente al 20% del ancho
            child: Align(
              alignment: Alignment.centerLeft,
              child: IconButton(
                icon: Icon(Icons.menu), // Puedes reemplazar con tu logo
                onPressed: () {
                  // Acción del logo
                },
              ),
            ),
          ),
          // Título en el centro
          Expanded(
            flex: 4, // Equivalente al 40% del ancho
            child: Center(
              child: Text(
                'Zeus', // Tu texto del título
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: Colors.white, // Color del texto
                ),
              ),
            ),
          ),
          // Botones a la derecha (recibidos como parámetro)
          Expanded(
          flex: 2, // Equivalente al 40% del ancho
          child: Row(
            mainAxisAlignment: MainAxisAlignment.end,
            children: actions),
          )],
      ),
    );
  }

  @override
  Size get preferredSize => const Size.fromHeight(60.0);
}