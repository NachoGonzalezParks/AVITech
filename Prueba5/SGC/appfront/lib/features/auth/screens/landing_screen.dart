import 'package:flutter/material.dart';
import 'package:appfront/core/constants/app_structure.dart';
import 'package:appfront/features/auth/widgets/auth_modal.dart';
import 'package:appfront/core/utils/responsive.dart';

class LandingScreen extends StatefulWidget {
  const LandingScreen({super.key});

  @override
  LandingScreenState createState() => LandingScreenState();
}

class LandingScreenState extends State<LandingScreen> {
  bool showAdminContent = false;

  void toggleContent(bool isAdmin) {
    setState(() {
      showAdminContent = isAdmin;
    });
  }

  Widget _accessSection() {
    return Center(
      child: showAdminContent
          ? AuthModal()
          : Text('Descarga la app desde la Play Store usando el QR'),
    );
  }

  Widget _introSection() {
    return Center(
      child: showAdminContent
          ? Text('Descripción de uso para administradores de torneos')
          : Text('Descripción de uso para jugadores, delegados y árbitros '),
    );
  }

  @override
  Widget build(BuildContext context) {
    return AppStructure(
      bodyContent: ResponsiveWidget(
        mobile: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            _accessSection(),
            SizedBox(height: 16),
            _introSection(),
          ],
        ),
        tablet: Row(
          children: [
            Expanded(child: _accessSection()),
            Expanded(child: _introSection()),
          ],
        ),
        desktop: Row(
          children: [
            Expanded(child: _accessSection()),
            Expanded(child: _introSection()),
          ],
        ),
      ),
    );
  }
}
