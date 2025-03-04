import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import 'package:appfront/data/repositories/api_service.dart';

class RegisterForm extends StatefulWidget {
  const RegisterForm({super.key});

  @override
  RegisterFormState createState() => RegisterFormState();
}

class RegisterFormState extends State<RegisterForm> {
  final TextEditingController emailController = TextEditingController();
  final TextEditingController password1Controller = TextEditingController();
  final TextEditingController password2Controller = TextEditingController();
  final TextEditingController nombreController = TextEditingController();
  final TextEditingController apellidoController = TextEditingController();
  final TextEditingController aliasController = TextEditingController();
  final TextEditingController sexoController = TextEditingController();
  final TextEditingController numeroIdentificacionController = TextEditingController();
  final TextEditingController fechaNacimientoController = TextEditingController();
  final TextEditingController telefonoController = TextEditingController();

  List<String> tipoIdentificacionOptions = []; // Lista de tipos de identificación
  String? selectedTipoIdentificacion;
  String? selectedPais; // Variable para almacenar el país seleccionado
  List<String> paises = []; // Lista de países
  final _formKey = GlobalKey<FormState>();
  bool _isRegistering = false;

  @override
  void initState() {
    super.initState();

    // Retrasar la llamada a _cargarPaises hasta que el contexto esté listo
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _cargarPaises();
    });
  }

  // Método para cargar la lista de países desde el backend
  Future<void> _cargarPaises() async {
    try {
      final apiService = Provider.of<ApiService>(context, listen: false);
      final listaPaises = await apiService.listarPaises(); // Obtener la lista de países

      setState(() {
        paises = listaPaises; // Asignar la lista de nombres de países
        selectedPais = paises.isNotEmpty ? paises[0] : null; // Seleccionar el primer país por defecto
      });

      // Cargar los tipos de identificación para el país seleccionado
      if (selectedPais != null) {
        await _cargarTiposIdentificacion(selectedPais!);
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error al cargar países: $e')),
      );
    }
  }

  // Método para cargar los tipos de identificación según el país seleccionado
  Future<void> _cargarTiposIdentificacion(String nombrePais) async {
    try {
      final apiService = Provider.of<ApiService>(context, listen: false);
      final tiposIdentificacion = await apiService.listarTiposIdentificacionPorPais(nombrePais);

      setState(() {
        tipoIdentificacionOptions = tiposIdentificacion; // Asignar la lista de tipos de identificación
        selectedTipoIdentificacion = tipoIdentificacionOptions.isNotEmpty ? tipoIdentificacionOptions[0] : null; // Seleccionar el primer tipo por defecto
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error al cargar tipos de identificación: $e')),
      );
    }
  }

  String _convertDateFormat(String date) {
    try {
      DateTime parsedDate = DateFormat('dd/MM/yyyy').parse(date);
      return DateFormat('yyyy-MM-dd').format(parsedDate);  // Convierte a formato backend
    } catch (e) {
      return date;  // Devuelve la fecha sin cambios si hay error
    }
  }

  Future<void> _selectDate(BuildContext context) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: DateTime.now(),
      firstDate: DateTime(1900),
      lastDate: DateTime.now(),
    );
    if (picked != null) {
      setState(() {
        fechaNacimientoController.text = DateFormat('dd/MM/yyyy').format(picked);
        fechaNacimientoController.value = TextEditingValue(
          text: DateFormat('dd/MM/yyyy').format(picked),
          selection: TextSelection.collapsed(offset: fechaNacimientoController.text.length),
        );
      });
    }
  }

  bool _validateFields() {
    if (emailController.text.isEmpty ||
        password1Controller.text.isEmpty ||
        password2Controller.text.isEmpty ||
        nombreController.text.isEmpty ||
        apellidoController.text.isEmpty ||
        aliasController.text.isEmpty ||
        selectedTipoIdentificacion == null ||
        numeroIdentificacionController.text.isEmpty ||
        fechaNacimientoController.text.isEmpty ||
        telefonoController.text.isEmpty ||
        selectedPais == null) { // Validar que se seleccione un país
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Todos los campos son obligatorios.')),
      );
      return false;
    }

    if (password1Controller.text != password2Controller.text) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Las contraseñas no coinciden.')),
      );
      return false;
    }

    return true;
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Form(
          key: _formKey,
          child: Column(
            children: [
              Row(
                children: [
                  Expanded(
                    child: TextFormField(
                      controller: nombreController,
                      decoration: const InputDecoration(labelText: 'Nombre'),
                    ),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: TextFormField(
                      controller: apellidoController,
                      decoration: const InputDecoration(labelText: 'Apellido'),
                    ),
                  ),
                ],
              ),
              TextFormField(
                controller: aliasController,
                decoration: const InputDecoration(labelText: 'Alias'),
              ),
              TextFormField(
                controller: sexoController,
                decoration: const InputDecoration(labelText: 'Sexo'),
              ),
              TextFormField(
                controller: emailController,
                decoration: const InputDecoration(labelText: 'Email'),
              ),
              // Desplegable de países
              DropdownButtonFormField<String>(
                value: selectedPais,
                decoration: const InputDecoration(labelText: 'País'),
                items: paises.map((pais) {
                  return DropdownMenuItem<String>(
                    value: pais,
                    child: Text(pais),
                  );
                }).toList(),
                onChanged: (String? newValue) async {
                  setState(() {
                    selectedPais = newValue;
                  });

                  // Cargar los tipos de identificación para el nuevo país seleccionado
                  if (newValue != null) {
                    await _cargarTiposIdentificacion(newValue);
                  }
                },
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Por favor, selecciona un país';
                  }
                  return null;
                },
              ),
              Row(
                children: [
                  Expanded(
                    child: DropdownButtonFormField<String>(
                      value: selectedTipoIdentificacion,
                      decoration: const InputDecoration(labelText: 'Tipo de Documento'),
                      items: tipoIdentificacionOptions.map((String option) {
                        return DropdownMenuItem<String>(
                          value: option,
                          child: Text(option),
                        );
                      }).toList(),
                      onChanged: (String? newValue) {
                        setState(() {
                          selectedTipoIdentificacion = newValue;
                        });
                      },
                    ),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: TextFormField(
                      controller: numeroIdentificacionController,
                      decoration: const InputDecoration(labelText: 'Documento'),
                    ),
                  ),
                ],
              ),
              Row(
                children: [
                  Expanded(
                    child: TextFormField(
                      controller: telefonoController,
                      decoration: const InputDecoration(labelText: 'Teléfono'),
                    ),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: GestureDetector(
                      onTap: () => _selectDate(context),
                      child: AbsorbPointer(
                        child: TextFormField(
                          controller: fechaNacimientoController,
                          decoration: const InputDecoration(labelText: 'Fecha de Nacimiento'),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
              TextFormField(
                controller: password1Controller,
                decoration: const InputDecoration(labelText: 'Contraseña'),
                obscureText: true,
              ),
              TextFormField(
                controller: password2Controller,
                decoration: const InputDecoration(labelText: 'Repite tu contraseña'),
                obscureText: true,
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: _isRegistering
                    ? null
                    : () async {
                        if (_validateFields()) {
                          setState(() {
                            _isRegistering = true;
                          });

                          String email = emailController.text;
                          String password1 = password1Controller.text;
                          String password2 = password2Controller.text;
                          String nombre = nombreController.text;
                          String apellido = apellidoController.text;
                          String alias = aliasController.text;
                          String sexo = sexoController.text;
                          String tipoIdentificacion = selectedTipoIdentificacion ?? '';
                          String numeroIdentificacion = numeroIdentificacionController.text;
                          String fechaNacimiento = _convertDateFormat(fechaNacimientoController.text);
                          String telefono = telefonoController.text;
                          String pais = selectedPais ?? ''; // Agregar el país seleccionado
                          
                          final messenger = ScaffoldMessenger.of(context);
                          final currentContext = context;

                          try {
                            var response = await Provider.of<ApiService>(currentContext, listen: false)
                                .register(email, password1, password2, nombre, apellido, alias, tipoIdentificacion, numeroIdentificacion, fechaNacimiento, telefono, pais);

                            if (!context.mounted) return;

                            if (response['success']) {
                              messenger.showSnackBar(
                                const SnackBar(content: Text('Cuenta registrada')),
                              );
                            } else {
                              messenger.showSnackBar(
                                SnackBar(content: Text(response['message'] ?? 'Error desconocido')),
                              );
                            }
                          } catch (e) {
                            messenger.showSnackBar(
                              SnackBar(content: Text('Error al conectar con el servidor: $e')),
                            );
                          } finally {
                            setState(() {
                              _isRegistering = false;
                            });
                          }
                        }
                      },
                style: ElevatedButton.styleFrom(
                  backgroundColor: Theme.of(context).colorScheme.secondary,
                  foregroundColor: Theme.of(context).colorScheme.onSecondary,
                  padding: const EdgeInsets.symmetric(horizontal: 50, vertical: 15),
                ),
                child: const Text('Registrarse'),
              ),
            ],
          ),
        ),
      ],
    );
  }
}