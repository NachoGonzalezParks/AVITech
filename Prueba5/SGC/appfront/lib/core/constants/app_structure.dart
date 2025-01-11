import 'package:flutter/material.dart';
import 'package:appfront/core/constants/navbar.dart';
import 'package:appfront/features/auth/screens/landing_screen.dart';

class AppStructure extends StatelessWidget {
  final Widget bodyContent;
  const AppStructure({super.key, required this.bodyContent});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: NavBar(
        onAdminSelected: (isAdmin) {
          final state = context.findAncestorStateOfType<LandingScreenState>();
          state?.toggleContent(isAdmin);
        },
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: bodyContent,
        ),
      ),
    );
  }
}
