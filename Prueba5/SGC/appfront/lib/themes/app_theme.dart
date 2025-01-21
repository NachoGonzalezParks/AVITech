import 'package:flutter/material.dart';

class AppTheme {
  static ThemeData buildTheme() {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: const Color.fromRGBO(13, 19, 33, 1),
        primary:   const Color.fromARGB(255, 31, 53, 106), // Primary (dark blue)
        secondary: const Color.fromRGBO(209, 95, 13, 1), // Secondary (orange)
        tertiary:  const Color.fromARGB(255, 135, 61, 8), // Secondary (orange)
      ),
    );
  }
}
