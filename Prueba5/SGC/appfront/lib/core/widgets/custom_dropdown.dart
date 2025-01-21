import 'package:flutter/material.dart';

class CustomDropdown extends StatelessWidget {
  final String labelText;
  final List<String> options;
  final String? value;
  final ValueChanged<String?> onChanged;

  const CustomDropdown({
    super.key,
    required this.labelText,
    required this.options,
    this.value,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    const double maxWidth = 400.0; // Límite máximo de ancho, igual que CustomTextField

    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 10.0), // Espaciado igual que en CustomTextField
      child: Center(
        child: Container(
          constraints: BoxConstraints(
            maxWidth: MediaQuery.of(context).size.width < maxWidth
                ? double.infinity
                : maxWidth,
          ),
          child: InputDecorator(
            decoration: InputDecoration(
              labelText: labelText,
              border: const OutlineInputBorder(), // Borde igual que CustomTextField
              filled: true,
              fillColor: Colors.white,
            ),
            child: DropdownButtonHideUnderline(
              child: DropdownButton<String>(
                value: value,
                isExpanded: true, // Para que ocupe todo el ancho del contenedor
                onChanged: onChanged,
                items: [
                  // Agregamos el placeholder "Seleccionar"
                  const DropdownMenuItem<String>(
                    value: null,
                    child: Text(
                      "Seleccionar", // Texto del placeholder
                      style: TextStyle(color: Colors.grey), // Color gris para diferenciarlo
                    ),
                  ),
                  ...options.map((String option) {
                    return DropdownMenuItem<String>(
                      value: option,
                      child: Text(option),
                    );
                  }),
                ],
                style: Theme.of(context).textTheme.bodyLarge, // Estilo de texto global
                dropdownColor: Colors.white, // Fondo blanco igual que TextField
              ),
            ),
          ),
        ),
      ),
    );
  }
}
