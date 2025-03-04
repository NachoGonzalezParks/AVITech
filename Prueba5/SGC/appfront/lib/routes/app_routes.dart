import 'package:appfront/features/auth/screens/landing_screen.dart';
import 'package:appfront/features/dashboard/screens/home_screen.dart';

class AppRoutes {
  static const initialRoute = '/landing';

  static final routes = {
    '/landing': (context) => const LandingScreen(),
    '/home': (context) => const HomeScreen(),
  };
}
