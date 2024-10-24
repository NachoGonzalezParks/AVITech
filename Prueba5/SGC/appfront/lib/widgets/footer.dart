import 'package:flutter/material.dart';

class FooterBar extends StatelessWidget {
  const FooterBar({super.key});

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    return BottomAppBar(
      color: colorScheme.primary,
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              '© 2024 Zeus App',
              style: TextStyle(color: colorScheme.onPrimary),
            ),
            Row(
              children: [
                TextButton(
                  onPressed: () {
                    // Acción para ir a términos y condiciones
                  },
                  child: Text(
                    'Términos y Condiciones',
                    style: TextStyle(color: colorScheme.onPrimary),
                  ),
                ),
                TextButton(
                  onPressed: () {
                    // Acción para ir a política de privacidad
                  },
                  child: Text(
                    'Política de Privacidad',
                    style: TextStyle(color: colorScheme.onPrimary),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}