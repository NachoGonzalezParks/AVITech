import 'package:flutter/material.dart';
import 'package:appfront/widgets/nav_drawer.dart';
//import 'package:appfront/screens/fixture_screen.dart';
//import 'package:appfront/screens/settings_screen.dart';
//import 'package:appfront/screens/teams_screen.dart';
//import 'package:appfront/screens/tournaments_screen.dart';
//import 'package:appfront/widgets/nav_drawer.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({Key? key}) : super(key: key);

  @override
  _DashboardScreenState createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  int _selectedIndex = 0;

  final List<Widget> _screens = [
    HomeTab(),
    //TournamentsScreen(),
    //TeamsScreen(),
    //FixtureScreen(),
    //SettingsScreen(),
  ];

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      drawer: NavDrawer(
        currentIndex: _selectedIndex,
        onItemSelected: _onItemTapped,
      ),
      appBar: AppBar(
        title: const Text('Torneos App'),
      ),
      body: IndexedStack(
        index: _selectedIndex,
        children: _screens,
      ),
    );
  }
}

class HomeTab extends StatelessWidget {
  const HomeTab({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Bienvenido al Panel de Control',
            style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 16),
          const Text('Selecciona una opción del menú para comenzar.'),
          const SizedBox(height: 24),
          GridView.count(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            crossAxisCount: MediaQuery.of(context).size.width > 600 ? 3 : 1,
            childAspectRatio: 2,
            crossAxisSpacing: 16,
            mainAxisSpacing: 16,
            children: [
              StatCard(title: 'Torneos activos', value: '3', color: Colors.blue),
              StatCard(title: 'Equipos registrados', value: '12', color: Colors.green),
              StatCard(title: 'Próximos partidos', value: '5', color: Colors.orange),
            ],
          ),
        ],
      ),
    );
  }
}

class StatCard extends StatelessWidget {
  final String title;
  final String value;
  final Color color;

  const StatCard({Key? key, required this.title, required this.value, required this.color}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 2,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              title,
              style: TextStyle(color: Colors.grey[600]),
            ),
            const SizedBox(height: 8),
            Text(
              value,
              style: TextStyle(
                fontSize: 28,
                fontWeight: FontWeight.bold,
                color: color,
              ),
            ),
          ],
        ),
      ),
    );
  }
}