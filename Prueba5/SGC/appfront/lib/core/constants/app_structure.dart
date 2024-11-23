import 'package:flutter/material.dart';
import 'package:appfront/core/constants/navbar.dart';
import 'package:appfront/core/constants/footer.dart';

class AppStructure extends StatelessWidget {

  final Widget bodyContent;
  const AppStructure({super.key, required this.bodyContent});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const NavBar(), // Simply add NavBar without actions parameter
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: bodyContent,
        ),
      ),
      bottomNavigationBar: const FooterBar(),
    );
  }
}
