import 'package:flutter/material.dart';
import 'package:appfront/routes.dart';
import 'package:appfront/services/api_service.dart';
import 'package:flutter/services.dart';
import 'package:intl/intl.dart';

class AuthTab extends StatefulWidget {
  final String userType;

  const AuthTab({Key? key, required this.userType}) : super(key: key);

  @override
  _AuthTabState createState() => _AuthTabState();
}

class _AuthTabState extends State<AuthTab> with SingleTickerProviderStateMixin {
  late TabController _tabController;
  final ApiService _apiService = ApiService();

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        TabBar(
          controller: _tabController,
          labelColor: Colors.orange,
          unselectedLabelColor: Colors.grey,
          tabs: const [
            Tab(text: 'Ingresar'),
            Tab(text: 'Crear Usuario'),
          ],
        ),
        Expanded(
          child: TabBarView(
            controller: _tabController,
            children: [
              _LoginForm(userType: widget.userType),
              _RegisterForm(userType: widget.userType),
            ],
          ),
        ),
      ],
    );
  }
}

class _LoginForm extends StatefulWidget {
  final String userType;

  const _LoginForm({Key? key, required this.userType}) : super(key: key);

  @override
  __LoginFormState createState() => __LoginFormState();
}

class __LoginFormState extends State<_LoginForm> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final ApiService _apiService = ApiService();

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Form(
        key: _formKey,
        child: Column(
          children: [
            TextFormField(
              controller: _emailController,
              decoration: const InputDecoration(labelText: 'Email'),
              keyboardType: TextInputType.emailAddress,
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Por favor ingrese su email';
                }
                if (!value.contains('@')) {
                  return 'Ingrese un email válido';
                }
                return null;
              },
            ),
            const SizedBox(height: 12),
            TextFormField(
              controller: _passwordController,
              decoration: const InputDecoration(labelText: 'Contraseña'),
              obscureText: true,
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Por favor ingrese su contraseña';
                }
                if (value.length < 6) {
                  return 'La contraseña debe tener al menos 6 caracteres';
                }
                return null;
              },
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: widget.userType == 'admin' 
                  ? const Color.fromARGB(255, 189, 101, 29) 
                  : Colors.green,
                minimumSize: const Size(double.infinity, 50),
              ),
              onPressed: _submitForm,
              child: const Text('Ingresar'),
            ),
          ],
        ),
      ),
    );
  }

  void _submitForm() async {
    if (_formKey.currentState!.validate()) {
      try {
        showDialog(
          context: context,
          barrierDismissible: false,
          builder: (context) => const Center(child: CircularProgressIndicator()),
        );

        final response = await _apiService.login(
          _emailController.text.trim(),
          _passwordController.text.trim(),
        );

        Navigator.pop(context);

        if (response['success'] == true) {
          Navigator.pushNamedAndRemoveUntil(
            context, 
            Routes.dashboard, 
            (route) => false,
          );
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(response['message'] ?? 'Error desconocido'),
              backgroundColor: Colors.red,
              duration: const Duration(seconds: 60),
              action: SnackBarAction(
                label: 'Aceptar',
                textColor: Colors.white,
                onPressed: () {
                  ScaffoldMessenger.of(context).hideCurrentSnackBar();
                },
              ),
            ),
          );
        }
      } on PlatformException catch (e) {
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error: ${e.message ?? "Falló la conexión con el servidor"}'),
            backgroundColor: Colors.red,
            duration: const Duration(seconds: 60),
            action: SnackBarAction(
              label: 'Aceptar',
              textColor: Colors.white,
              onPressed: () {
                ScaffoldMessenger.of(context).hideCurrentSnackBar();
              },
            ),          
          ),
        );
      } catch (e) {
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error inesperado: ${e.toString()}'),
            backgroundColor: Colors.red,
            duration: const Duration(seconds: 60),
            action: SnackBarAction(
              label: 'Aceptar',
              textColor: Colors.white,
              onPressed: () {
                ScaffoldMessenger.of(context).hideCurrentSnackBar();
              },
            ),          
          ),
        );
      }
    }
  }

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }
}

class _RegisterForm extends StatefulWidget {
  final String userType;

  const _RegisterForm({Key? key, required this.userType}) : super(key: key);

  @override
  __RegisterFormState createState() => __RegisterFormState();
}

class __RegisterFormState extends State<_RegisterForm> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _confirmPasswordController = TextEditingController();
  final _firstNameController = TextEditingController();
  final _lastNameController = TextEditingController();
  final _idNumberController = TextEditingController();
  final _birthDateController = TextEditingController();
  final _aliasController = TextEditingController();
  final _phoneController = TextEditingController();
  
  String? _selectedCountry;
  String? _selectedIdType;
  String? _selectedGender;
  
  List<String> _countries = [];
  List<String> _idTypes = [];
  List<String> _genders = [];
  
  bool _emailChecking = false;
  bool _emailExists = false;
  final ApiService _apiService = ApiService();

  @override
  void initState() {
    super.initState();
    _loadInitialData();
  }

  Future<void> _loadInitialData() async {
    try {
      // Cargar países
      _countries = await _apiService.listarPaises();
      setState(() {
        _selectedCountry = _countries.contains('Argentina') 
            ? 'Argentina' 
            : _countries.isNotEmpty ? _countries.first : null;
      });
      
      // Cargar tipos de identificación para el país seleccionado
      if (_selectedCountry != null) {
        try {
          _idTypes = await _apiService.listarTiposIdentificacion(_selectedCountry!);
          setState(() {
            _selectedIdType = _idTypes.isNotEmpty ? _idTypes.first : null;
          });
        } catch (e) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Error al cargar tipos de identificación: $e'),
              backgroundColor: Colors.red,
            ),
          );
        }
      }
      
      // Cargar géneros
      try {
        _genders = await _apiService.listarSexos();
        setState(() {
          _selectedGender = _genders.isNotEmpty ? _genders.first : null;
        });
      } catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error al cargar géneros: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Error al cargar datos iniciales: $e'),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  Future<void> _checkEmail() async {
    if (_emailController.text.isEmpty) return;
    
    setState(() => _emailChecking = true);
    try {
      final exists = await _apiService.checkEmailExists(_emailController.text);
      setState(() => _emailExists = exists);
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error al verificar email: $e')),
      );
    } finally {
      setState(() => _emailChecking = false);
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
        _birthDateController.text = DateFormat('yyyy-MM-dd').format(picked);
      });
    }
  }


  
  Future<void> _register() async {
    if (_formKey.currentState!.validate()) {
      if (_selectedCountry == null || 
          _selectedIdType == null || 
          _selectedGender == null) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Complete todos los campos obligatorios')),
        );
        return;
      }
      
      final userData = {
        'email': _emailController.text,
        'password1': _passwordController.text,
        'password2': _confirmPasswordController.text,
        'nombre': _firstNameController.text,
        'apellido': _lastNameController.text,
        'pais': _selectedCountry,
        'tipo_identificacion': _selectedIdType,
        'numero_identificacion': _idNumberController.text,
        'sexo': _selectedGender,
        'fecha_nacimiento': _birthDateController.text,
        'alias': _aliasController.text,
        'telefono': _phoneController.text,
      };
      
      try {
        showDialog(
          context: context,
          barrierDismissible: false,
          builder: (context) => const Center(child: CircularProgressIndicator()),
        );

        final result = await _apiService.registroUsuario(userData);
        
        Navigator.pop(context);
        
        if (result['success'] == true) {
          showDialog(
            context: context,
            builder: (ctx) => AlertDialog(
              title: const Text('Registro Exitoso'),
              content: const Text('Registro completado. Se ha enviado un email para validar tu cuenta.'),
              actions: [
                TextButton(
                  onPressed: () {
                    Navigator.pop(ctx);
                    Navigator.pop(context); // Cerrar diálogo y volver al login
                  },
                  child: const Text('OK'),
                )
              ],
            ),
          );
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(result['message']),
              duration: const Duration(seconds: 30), // 30 segundos
              action: SnackBarAction(
                label: 'Aceptar',
                textColor: Colors.white,
                onPressed: () {
                  ScaffoldMessenger.of(context).hideCurrentSnackBar();
                },
              ),
            ),
          );
        }
      } catch (e) {
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error de conexión: $e'),
            duration: const Duration(seconds: 30), // 30 segundos
            action: SnackBarAction(
              label: 'Aceptar',
              textColor: Colors.white,
              onPressed: () {
                ScaffoldMessenger.of(context).hideCurrentSnackBar();
              },
            ),
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        children: [
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              child: Column(
                children: [
                  // Email
                  TextFormField(
                    controller: _emailController,
                    decoration: InputDecoration(
                      labelText: 'Email',
                      suffixIcon: _emailChecking
                          ? const CircularProgressIndicator()
                          : _emailExists
                              ? const Icon(Icons.error, color: Colors.red)
                              : null,
                    ),
                    keyboardType: TextInputType.emailAddress,
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Campo obligatorio';
                      }
                      if (!RegExp(r'^[^@]+@[^@]+\.[^@]+').hasMatch(value)) {
                        return 'Formato de email inválido';
                      }
                      if (_emailExists) {
                        return 'Email ya registrado';
                      }
                      return null;
                    },
                    onChanged: (value) => _checkEmail(),
                  ),
                  const SizedBox(height: 12),
                  
                  // Contraseña
                  TextFormField(
                    controller: _passwordController,
                    obscureText: true,
                    decoration: const InputDecoration(labelText: 'Contraseña'),
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Campo obligatorio';
                      }
                      if (value.length < 6) {
                        return 'Mínimo 6 caracteres';
                      }
                      return null;
                    },
                  ),
                  const SizedBox(height: 12),
                  
                  // Confirmar contraseña
                  TextFormField(
                    controller: _confirmPasswordController,
                    obscureText: true,
                    decoration: const InputDecoration(labelText: 'Confirmar Contraseña'),
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Campo obligatorio';
                      }
                      if (value != _passwordController.text) {
                        return 'Las contraseñas no coinciden';
                      }
                      return null;
                    },
                  ),
                  const SizedBox(height: 12),
                  
                  // Nombre y Apellido
                  TextFormField(
                    controller: _firstNameController,
                    decoration: const InputDecoration(labelText: 'Nombre'),
                    validator: (value) => _validateRequired(value, 'Nombre'),
                  ),
                  const SizedBox(height: 12),
                  
                  TextFormField(
                    controller: _lastNameController,
                    decoration: const InputDecoration(labelText: 'Apellido'),
                    validator: (value) => _validateRequired(value, 'Apellido'),
                  ),
                  const SizedBox(height: 12),
                  
                  // País
                  DropdownButtonFormField<String>(
                    value: _selectedCountry,
                    items: _countries.map((country) {
                      return DropdownMenuItem(
                        value: country,
                        child: Text(country),
                      );
                    }).toList(),
                    onChanged: (value) async {
                      setState(() => _selectedCountry = value);
                      if (value != null) {
                        try {
                          final types = await _apiService.listarTiposIdentificacion(value);
                          setState(() {
                            _idTypes = types;
                            _selectedIdType = types.isNotEmpty ? types.first : null;
                          });
                        } catch (e) {
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(content: Text('Error al cargar tipos de identificación: $e')),
                          );
                        }
                      }
                    },
                    decoration: const InputDecoration(labelText: 'País'),
                    validator: (value) => _validateRequired(value, 'País'),
                  ),
                  const SizedBox(height: 12),
                  
                  // Tipo de identificación
                  DropdownButtonFormField<String>(
                    value: _selectedIdType,
                    items: _idTypes.map((type) {
                      return DropdownMenuItem(
                        value: type,
                        child: Text(type),
                      );
                    }).toList(),
                    onChanged: (value) => setState(() => _selectedIdType = value),
                    decoration: const InputDecoration(labelText: 'Tipo de Identificación'),
                    validator: (value) => _validateRequired(value, 'Tipo de Identificación'),
                  ),
                  const SizedBox(height: 12),
                  
                  // Número de identificación
                  TextFormField(
                    controller: _idNumberController,
                    decoration: const InputDecoration(labelText: 'Número de Identificación'),
                    validator: (value) => _validateRequired(value, 'Número de Identificación'),
                  ),
                  const SizedBox(height: 12),
                  
                  // Sexo
                  DropdownButtonFormField<String>(
                    value: _selectedGender,
                    items: _genders.map((gender) {
                      return DropdownMenuItem(
                        value: gender,
                        child: Text(gender),
                      );
                    }).toList(),
                    onChanged: (value) => setState(() => _selectedGender = value),
                    decoration: const InputDecoration(labelText: 'Sexo'),
                    validator: (value) => _validateRequired(value, 'Sexo'),
                  ),
                  const SizedBox(height: 12),
                  
                  // Fecha de nacimiento
                  TextFormField(
                    controller: _birthDateController,
                    decoration: InputDecoration(
                      labelText: 'Fecha de Nacimiento',
                      suffixIcon: IconButton(
                        icon: const Icon(Icons.calendar_today),
                        onPressed: () => _selectDate(context),
                      ),
                    ),
                    readOnly: true,
                    validator: (value) => _validateRequired(value, 'Fecha de Nacimiento'),
                  ),
                  const SizedBox(height: 12),
                  
                  // Alias (opcional)
                  TextFormField(
                    controller: _aliasController,
                    decoration: const InputDecoration(labelText: 'Alias (opcional)'),
                  ),
                  const SizedBox(height: 12),
                  
                  // Teléfono (opcional)
                  TextFormField(
                    controller: _phoneController,
                    decoration: const InputDecoration(labelText: 'Teléfono (opcional)'),
                    keyboardType: TextInputType.phone,
                  ),
                ],
              ),
            ),
          ),
          
          // Botones de acción
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              children: [
                ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: widget.userType == 'admin' 
                      ? const Color.fromARGB(255, 189, 101, 29) 
                      : Colors.green,
                    minimumSize: const Size(double.infinity, 50),
                  ),
                  onPressed: _register,
                  child: const Text('Registrarse'),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  String? _validateRequired(String? value, String field) {
    if (value == null || value.isEmpty) {
      return '$field es obligatorio';
    }
    return null;
  }

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    _confirmPasswordController.dispose();
    _firstNameController.dispose();
    _lastNameController.dispose();
    _idNumberController.dispose();
    _birthDateController.dispose();
    _aliasController.dispose();
    _phoneController.dispose();
    super.dispose();
  }
}