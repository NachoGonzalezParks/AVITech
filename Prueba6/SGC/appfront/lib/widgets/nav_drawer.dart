import 'package:flutter/material.dart';

class NavDrawer extends StatelessWidget {
  final int currentIndex;
  final Function(int) onItemSelected;

  const NavDrawer({Key? key, required this.currentIndex, required this.onItemSelected}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Drawer(
      child: Column(
        children: [
          const DrawerHeader(
            decoration: BoxDecoration(
              color: Color(0xFF1E5799),
            ),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                CircleAvatar(
                  radius: 30,
                  backgroundColor: Colors.white,
                  child: Icon(Icons.person, size: 40, color: Color(0xFF1E5799)),
                ),
                SizedBox(height: 8),
                Text(
                  'Nombre Usuario',
                  style: TextStyle(color: Colors.white),
                ),
              ],
            ),
          ),
          Expanded(
            child: ListView(
              padding: EdgeInsets.zero,
              children: [
                _buildNavItem(context, Icons.home, 'Inicio', 0),
                _buildNavItem(context, Icons.sports_soccer, 'Torneos', 1),
                _buildNavItem(context, Icons.people, 'Equipos', 2),
                _buildNavItem(context, Icons.calendar_today, 'Fixture', 3),
                _buildNavItem(context, Icons.settings, 'Configuración', 4),
              ],
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(16),
            child: ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.red,
                minimumSize: const Size(double.infinity, 50),
              ),
              onPressed: () {
                // Cerrar sesión
                Navigator.pushNamedAndRemoveUntil(
                  context, 
                  '/', 
                  (route) => false
                );
              },
              child: const Text('Cerrar sesión'),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildNavItem(BuildContext context, IconData icon, String title, int index) {
    return ListTile(
      leading: Icon(icon),
      title: Text(title),
      selected: currentIndex == index,
      selectedTileColor: Colors.blue[50],
      onTap: () {
        Navigator.pop(context);
        onItemSelected(index);
      },
    );
  }
}