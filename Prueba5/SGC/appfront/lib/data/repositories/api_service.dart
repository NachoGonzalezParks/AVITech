import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class ApiService extends ChangeNotifier {
  static const String baseUrl = 'http://127.0.0.1:8000/';
  
  bool _isLoading = false;

  bool get isLoading => _isLoading;

  void _setLoading(bool loading) {
    _isLoading = loading;
    notifyListeners();
  }

  Future<Map<String, dynamic>> login(String email, String password) async {
    _setLoading(true);
    final response = await http.post(
      Uri.parse('$baseUrl/login/'),
      body: {
        'username': email,
        'password': password,
      },
    );
    _setLoading(false);

    // Decodificar la respuesta JSON
    final responseBody = json.decode(response.body);

    // Verificar si la clave 'success' es true
    if (responseBody['success'] == true) {
      return responseBody; // Respuesta exitosa
    } else {
      // Si hay un error, devuelve el mensaje de error del servidor
      return {
        'success': false,
        'message': responseBody['message'] ?? 'Error al iniciar sesión.',
      };
    }
  }

  Future<Map<String, dynamic>> getUserDetails(String token) async {
    final response = await http.get(
      Uri.parse('$baseUrl/auth/user/'),
      headers: {
        'Authorization': 'Token $token',
      },
    );
    

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to load user details');
    }
  }


  Future<Map<String, dynamic>> register(String email, String password1, String password2, String nombre, String apellido, String alias, String sexo, String tipoIdentificacion, String numeroIdentificacion, String fechaNacimiento, String telefono, String pais) async {
    _setLoading(true);
    final response = await http.post(

      Uri.parse('$baseUrl/registro/'),
      body: {
        'email': email,
        'password1': password1,
        'password2': password2,
        'nombre' : nombre,
        'apellido' : apellido,
        'alias' : alias, 
        'sexo' : sexo,       
        'tipo_identificacion' : tipoIdentificacion,
        'numero_identificacion' : numeroIdentificacion,
        'fecha_nacimiento' : fechaNacimiento,
        'telefono' : telefono,
        'pais': pais,
      },

    );
    _setLoading(false);

    print(response);

    final responseData = json.decode(response.body);

    if (response.statusCode == 200 || response.statusCode == 201) {
      return responseData;
    } else {
      return {
        'success': false,
        'message': 'Se produjo un error al registrar el usuario: ${responseData['message'] ?? 'Error desconocido'}',
      };
    }
  }

  Future<List<String>> listarSexos() async {
  final response = await http.post(Uri.parse('$baseUrl/listar_sexos/'));

  if (response.statusCode == 200) {
    // Decodificar la respuesta JSON
    final Map<String, dynamic> responseBody = json.decode(response.body);

    // Verificar si la respuesta contiene la clave "paises"
    if (responseBody.containsKey('sexos')) {
      // Extraer la lista de países como una lista de strings
      return List<String>.from(responseBody['sexos']);
    } else {
      throw Exception('La respuesta no contiene la clave "sexos"');
    }
  } else {
    throw Exception('Error al cargar países: ${response.statusCode}');
  }
}


  Future<List<String>> listarPaises() async {
  final response = await http.post(Uri.parse('$baseUrl/listar_paises/'));

  if (response.statusCode == 200) {
    // Decodificar la respuesta JSON
    final Map<String, dynamic> responseBody = json.decode(response.body);

    // Verificar si la respuesta contiene la clave "paises"
    if (responseBody.containsKey('paises')) {
      // Extraer la lista de países como una lista de strings
      return List<String>.from(responseBody['paises']);
    } else {
      throw Exception('La respuesta no contiene la clave "paises"');
    }
  } else {
    throw Exception('Error al cargar países: ${response.statusCode}');
  }
}

Future<List<String>> listarTiposIdentificacionPorPais(String nombrePais) async {
  final response = await http.post(
    Uri.parse('$baseUrl/listar_tipos_identificacion_por_pais/'),
    body: {
      'nombre_pais': nombrePais, // Enviar el nombre del país en el cuerpo
    },
  );

  if (response.statusCode == 200) {
    // Decodificar la respuesta JSON
    final Map<String, dynamic> responseBody = json.decode(response.body);

    // Verificar si la respuesta contiene la clave "tipos_identificacion"
    if (responseBody.containsKey('tipos_identificacion')) {
      // Extraer la lista de tipos de identificación
      return List<String>.from(responseBody['tipos_identificacion']);
    } else {
      throw Exception('La respuesta no contiene la clave "tipos_identificacion"');
    }
  } else {
    throw Exception('Error al cargar tipos de identificación: ${response.statusCode}');
  }
}
}