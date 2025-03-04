import 'package:flutter/material.dart';
import 'package:appfront/core/constants/app_structure.dart';
import 'package:appfront/features/auth/widgets/auth_modal.dart';

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
    return Expanded(
      child: Center(
        child: showAdminContent
            ? AuthModal()
            : Text('Descarga la app desde la Play Store usando el QR'),
      ),
    );
  }

  Widget _introSection() {
    return Expanded(
      child: Center(
        child: Text(
          showAdminContent
              ? 'Descripción de uso para administradores (LS)'
              : 'Descripción de uso para jugadores (LS)',
        ),
      ),
    );
  }


  @override
  Widget build(BuildContext context) {
    return AppStructure(
      bodyContent: LayoutBuilder(
        builder: (context, constraints) {
          bool isMobile = MediaQuery.of(context).size.width < 600;

          if (isMobile) {
            return Column(
              children: [
                _accessSection(),
                _introSection(),
              ],
            );
          } else {
            return Row(
              children: [
                Expanded(child: _accessSection()),
                Expanded(child: _introSection()),
              ],
            );
          }
        },
      ),
    );
  }
}
