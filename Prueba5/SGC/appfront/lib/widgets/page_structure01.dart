// File: widgets/page_structure01.dart
import 'package:flutter/material.dart';
import 'package:appfront/widgets/navbar.dart';
import 'package:appfront/widgets/footer.dart';

class PageStructure01 extends StatelessWidget {
  final Widget bodyContent;

  const PageStructure01({super.key, required this.bodyContent});

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
