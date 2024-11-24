import 'package:flutter/material.dart';

class AppTheme {
  static ThemeData buildTheme() {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: const Color(0xFF0D1321), // Primary (dark blue)
        secondary: const Color.fromRGBO(209, 95, 13, 1), // Secondary (orange)
      ),
    );
  }
}
