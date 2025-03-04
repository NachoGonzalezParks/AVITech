import 'package:flutter/material.dart';
import 'package:appfront/core/utils/responsive.dart'; // Importa tu ResponsiveWidget

class NavBar extends StatelessWidget implements PreferredSizeWidget {
  final Function(bool) onAdminSelected;

  const NavBar({super.key, required this.onAdminSelected});

  List<Widget> _getActions(BuildContext context) {
    return [
      TextButton(
        onPressed: () => onAdminSelected(false),
        child: Text('Jugadores', style: TextStyle(color: Theme.of(context).colorScheme.onSecondary)),
      ),
      TextButton(
        onPressed: () => onAdminSelected(true),
        child: Text('Administradores', style: TextStyle(color: Theme.of(context).colorScheme.onSecondary)),
      ),
    ];
  }

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;

    return AppBar(
      backgroundColor: colorScheme.primary,
      elevation: 0,
      leading: IconButton(
        icon: const Icon(Icons.arrow_back, color: Colors.white),
        onPressed: () {
          Navigator.maybePop(context);
        },
      ),
      title: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Expanded(
            flex: 4,
            child: Text(
              'ZEUS',
              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white),
              textAlign: TextAlign.left,
            ),
          ),
          Expanded(
            flex: 3,
            child: ResponsiveWidget(
              mobile: _mobileMenu(context), // Menú en móviles
              tablet: Row(
                mainAxisAlignment: MainAxisAlignment.end,
                children: _getActions(context),
              ),
              desktop: Row(
                mainAxisAlignment: MainAxisAlignment.end,
                children: _getActions(context),
              ),
            ),
          ),
        ],
      ),
    );
  }

  /// Menú desplegable para móviles
  Widget _mobileMenu(BuildContext context) {
    return PopupMenuButton<String>(
      icon: Icon(Icons.menu, color: Colors.white),
      onSelected: (String value) {
        if (value == 'jugadores') {
          onAdminSelected(false);
        } else if (value == 'administradores') {
          onAdminSelected(true);
        }
      },
      itemBuilder: (BuildContext context) => [
        PopupMenuItem<String>(
          value: 'jugadores',
          child: Text('Jugadores'),
        ),
        PopupMenuItem<String>(
          value: 'administradores',
          child: Text('Administradores'),
        ),
      ],
    );
  }

  @override
  Size get preferredSize => const Size.fromHeight(60.0);
}
