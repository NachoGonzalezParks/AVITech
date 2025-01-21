// widgets/custom_text_field.dart
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class CustomTextField extends StatelessWidget {
  final TextEditingController controller;
  final String labelText;
  final TextInputType keyboardType;
  final bool obscureText;
  final List<TextInputFormatter>? inputFormatters;
  final VoidCallback? onTap;
  final bool readOnly;

  const CustomTextField({
    super.key, // Convert 'key' to a super parameter
    required this.controller,
    required this.labelText,
    this.keyboardType = TextInputType.text,
    this.obscureText = false,
    this.inputFormatters,
    this.onTap,
    this.readOnly = false,
  });

  @override
  Widget build(BuildContext context) {
    const double maxWidth = 400.0; // Use 'const' here

    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 10.0),
      child: Center(
        child: Container(
          constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width < maxWidth ? double.infinity : maxWidth),
          child: GestureDetector(
            onTap: onTap,
            child: AbsorbPointer(
              absorbing: readOnly,
              child: TextField(
                controller: controller,
                keyboardType: keyboardType,
                obscureText: obscureText,
                inputFormatters: inputFormatters,
                decoration: InputDecoration(
                  labelText: labelText,
                  border: const OutlineInputBorder(),
                  filled: true,
                  fillColor: Colors.white,
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
