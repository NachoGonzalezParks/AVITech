import 'package:appfront/features/auth/screens/landing_screen.dart';
import 'package:appfront/features/auth/screens/login_screen.dart';
import 'package:appfront/features/auth/screens/register_screen.dart';
import 'package:appfront/features/dashboard/screens/home_screen.dart';

class AppRoutes {
  static const initialRoute = '/landing';

  static final routes = {
    '/landing': (context) => const LandingScreen(),
    '/login': (context) => const LoginScreen(),
    '/register': (context) => const RegisterScreen(),
    '/home': (context) => const HomeScreen(),
  };
}
