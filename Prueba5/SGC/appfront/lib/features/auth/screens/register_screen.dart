import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import 'package:appfront/data/repositories/api_service.dart';
import 'package:appfront/core/constants/app_structure.dart';
import 'package:appfront/core/widgets/custom_text_field.dart';
import 'package:appfront/core/widgets/custom_dropdown.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  RegisterScreenState createState() => RegisterScreenState();
}

class RegisterScreenState extends State<RegisterScreen> {
  final TextEditingController emailController = TextEditingController();
  final TextEditingController password1Controller = TextEditingController();
  final TextEditingController password2Controller = TextEditingController();
  final TextEditingController nombreController = TextEditingController();
  final TextEditingController apellidoController = TextEditingController();
  final TextEditingController aliasController = TextEditingController();
  final TextEditingController numeroIdentificacionController = TextEditingController();
  final TextEditingController fechaNacimientoController = TextEditingController();
  final TextEditingController telefonoController = TextEditingController();

  // Opciones para el campo tipoIdentificacion
  final List<String> tipoIdentificacionOptions = [
    'DNI',
    'RUC',
    'Pasaporte',
  ];

  String? selectedTipoIdentificacion;

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;

    return AppStructure(
      bodyContent: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: <Widget>[
          CustomTextField(
            controller: emailController,
            labelText: 'Email',
            keyboardType: TextInputType.emailAddress,
          ),
          CustomTextField(
            controller: password1Controller,
            labelText: 'Contraseña',
            obscureText: true,
          ),
          CustomTextField(
            controller: password2Controller,
            labelText: 'Confirmar Contraseña',
            obscureText: true,
          ),
          CustomTextField(
            controller: nombreController,
            labelText: 'Nombre',
          ),
          CustomTextField(
            controller: apellidoController,
            labelText: 'Apellido',
          ),
          CustomTextField(
            controller: aliasController,
            labelText: 'Alias',
          ),
          // Utilizamos el widget CustomDropdown
          CustomDropdown(
            labelText: 'Tipo de identificación',
            options: tipoIdentificacionOptions,
            value: selectedTipoIdentificacion,
            onChanged: (String? newValue) {
              setState(() {
                selectedTipoIdentificacion = newValue;
              });
            },
          ),
          CustomTextField(
            controller: numeroIdentificacionController,
            labelText: 'Número de identificación',
            keyboardType: TextInputType.number,
            inputFormatters: [FilteringTextInputFormatter.digitsOnly],
          ),
          GestureDetector(
            onTap: () async {
              DateTime? pickedDate = await showDatePicker(
                context: context,
                initialDate: DateTime.now(),
                firstDate: DateTime(1900),
                lastDate: DateTime(2100),
              );
              if (pickedDate != null) {
                setState(() {
                  fechaNacimientoController.text = "${pickedDate.toLocal()}".split(' ')[0];
                });
              }
            },
            child: AbsorbPointer(
              child: CustomTextField(
                controller: fechaNacimientoController,
                labelText: 'Fecha de nacimiento',
                keyboardType: TextInputType.datetime,
                readOnly: true,
              ),
            ),
          ),
          CustomTextField(
            controller: telefonoController,
            labelText: 'Teléfono',
            keyboardType: TextInputType.phone,
            inputFormatters: [FilteringTextInputFormatter.digitsOnly],
          ),
          const SizedBox(height: 20),
          ElevatedButton(
            onPressed: () async {
              String email = emailController.text;
              String password1 = password1Controller.text;
              String password2 = password2Controller.text;
              String nombre = nombreController.text;
              String apellido = apellidoController.text;
              String alias = aliasController.text;
              String tipoIdentificacion = selectedTipoIdentificacion ?? '';
              String numeroIdentificacion = numeroIdentificacionController.text;
              String fechaNacimiento = fechaNacimientoController.text;
              String telefono = telefonoController.text;

              if (password1 != password2) {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Las contraseñas no coinciden')),
                );
                return;
              }

              try {
                var currentContext = context;
                var response = await Provider.of<ApiService>(currentContext, listen: false)
                    .register(email, password1, password2, nombre, apellido, alias, tipoIdentificacion, numeroIdentificacion, fechaNacimiento, telefono)
                    .timeout(const Duration(seconds: 10));  // Timeout de 10 segundos

                if (!context.mounted) return;

                if (response['success']) {
                  Navigator.pushReplacementNamed(context, '/login');
                } else {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text(response['message'])),
                  );
                }
              } catch (e) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Error durante el registro: $e')),
                );
              }
            },

            style: ElevatedButton.styleFrom(
              backgroundColor: colorScheme.secondary,
              foregroundColor: colorScheme.onSecondary,
              padding: const EdgeInsets.symmetric(horizontal: 50, vertical: 15),
            ),
            child: const Text('Registrarse'),
          ),
          TextButton(
            onPressed: () {
              Navigator.pushNamed(context, '/login');
            },
            child: const Text('Ya tienes una cuenta? Inicia sesión'),
          ),
        ],
      ),
    );
  }
}
