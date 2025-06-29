import 'dart:convert';
import 'dart:async';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  static const String _baseUrl = 'http://127.0.0.1:8000';
  String? _token;

  Future<void> init() async {
    final prefs = await SharedPreferences.getInstance();
    _token = prefs.getString('authToken');
  }

  Map<String, String> get _headers {
    return {
      'Content-Type': 'application/json',
      if (_token != null) 'Authorization': 'Token $_token',
    };
  }

  // ==================== Autenticación ====================
  Future<Map<String, dynamic>> login(String email, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/login/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'username': email, 'password': password}),
      ).timeout(const Duration(seconds: 10));

      return _parseResponse(response);
    } on TimeoutException {
      throw PlatformException(
        code: 'TIMEOUT',
        message: 'Tiempo de espera agotado',
      );
    } on http.ClientException {
      throw PlatformException(
        code: 'CONNECTION_ERROR',
        message: 'Error de conexión con el servidor',
      );
    } catch (e) {
      throw PlatformException(
        code: 'UNKNOWN_ERROR',
        message: 'Error desconocido: ${e.toString()}',
      );
    }
  }

  // Función para analizar la respuesta
  Map<String, dynamic> _parseResponse(http.Response response) {
    final contentType = response.headers['content-type'];
    
    if (contentType?.contains('application/json') == true) {
      final responseBody = jsonDecode(utf8.decode(response.bodyBytes));
      
      if (response.statusCode == 200 && responseBody['success'] == true) {
        _token = responseBody['token'];
        _saveToken(_token!);
        return responseBody;
      } else {
        throw PlatformException(
          code: 'API_ERROR_${response.statusCode}',
          message: responseBody['message'] ?? 'Error en las credenciales',
        );
      }
    } else {
      // El servidor devolvió HTML en lugar de JSON
      throw PlatformException(
        code: 'INVALID_RESPONSE',
        message: 'El servidor devolvió una respuesta inesperada (HTML)',
      );
    }
  }

  Future<void> _saveToken(String token) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('authToken', token);
  }

  // ==================== Registro de Usuario ====================
  Future<Map<String, dynamic>> registroUsuario(Map<String, dynamic> data) async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/registro/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(data),
      ).timeout(const Duration(seconds: 15));
      
      return _parseRegistrationResponse(response);
    } on TimeoutException {
      return {
        'success': false,
        'message': 'Tiempo de espera agotado durante el registro'
      };
    } catch (e) {
      return {
        'success': false,
        'message': 'Error en el registro: ${e.toString()}'
      };
    }
  }

  // Función para analizar la respuesta de registro
  Map<String, dynamic> _parseRegistrationResponse(http.Response response) {
    final contentType = response.headers['content-type'];
    
    if (contentType?.contains('application/json') == true) {
      final responseBody = jsonDecode(utf8.decode(response.bodyBytes));
      
      if (response.statusCode == 201) {
        return {
          'success': true,
          'message': 'Registro exitoso. Revisa tu correo para confirmar tu cuenta.'
        };
      } else {
        return {
          'success': false,
          'message': responseBody['message'] ?? 'Error en el registro'
        };
      }
    } else {
      // Analizar respuesta HTML para extraer el mensaje de error
      final errorMessage = _extractErrorMessageFromHtml(response.body);
      return {
        'success': false,
        'message': errorMessage
      };
    }
  }

  // Función para extraer mensaje de error de HTML
  String _extractErrorMessageFromHtml(String html) {
    try {
      final startIndex = html.indexOf('<title>') + 7;
      final endIndex = html.indexOf('</title>', startIndex);
      
      if (startIndex >= 0 && endIndex > startIndex) {
        return html.substring(startIndex, endIndex);
      }
      
      return 'Error en el servidor (${html.length} bytes)';
    } catch (e) {
      return 'Error en el servidor (HTML)';
    }
  }

  // ==================== Listados ====================
  Future<List<String>> listarPaises() async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/listar_paises/'),
        headers: _headers,
      ).timeout(const Duration(seconds: 10));
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return List<String>.from(data['paises']);
      } else {
        throw Exception('Error al obtener países: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error al obtener países: ${e.toString()}');
    }
  }

  Future<List<String>> listarTiposIdentificacion(String pais) async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/listar_tipos_identificacion_por_pais/'),
        headers: _headers,
        body: jsonEncode({'nombre_pais': pais}),
      ).timeout(const Duration(seconds: 10));
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        // Corregido: extraer lista de strings directamente
        return List<String>.from(data['tipos_identificacion']);
      } else {
        throw Exception('Error al obtener tipos de identificación: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error al obtener tipos de identificación: ${e.toString()}');
    }
  }

  Future<List<String>> listarSexos() async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/listar_sexos/'),
        headers: _headers,
      ).timeout(const Duration(seconds: 10));
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return List<String>.from(data['sexos']);
      } else {
        throw Exception('Error al obtener lista de sexos: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error al obtener lista de sexos: ${e.toString()}');
    }
  }

  // ==================== Validación de Email ====================
  Future<bool> checkEmailExists(String email) async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/email_existe/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'email': email}),
      ).timeout(const Duration(seconds: 10));
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['existe'];
      } else {
        throw Exception('Error al verificar email: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error al verificar email: ${e.toString()}');
    }
  }

  // ==================== Gestión de Contraseña ====================
  Future<void> solicitarResetPassword(String email) async {
    try {
      await http.post(
        Uri.parse('$_baseUrl/mail_password_reset/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'email': email}),
      ).timeout(const Duration(seconds: 10));
    } catch (e) {
      throw PlatformException(
        code: 'PASSWORD_RESET_FAILED',
        message: 'Error al solicitar restablecimiento: ${e.toString()}',
      );
    }
  }

  Future<void> confirmarResetPassword(String uid, String token, String newPassword) async {
    try {
      await http.post(
        Uri.parse('$_baseUrl/reset/$uid/$token/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'new_password': newPassword}),
      ).timeout(const Duration(seconds: 10));
    } catch (e) {
      throw PlatformException(
        code: 'PASSWORD_CONFIRM_FAILED',
        message: 'Error al confirmar contraseña: ${e.toString()}',
      );
    }
  }

  // ==================== Gestión de Usuario ====================
  Future<Map<String, dynamic>> getUsuarioActual() async {
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/api/auth/user/'),
        headers: _headers,
      ).timeout(const Duration(seconds: 10));
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Error al obtener usuario: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error al obtener usuario: ${e.toString()}');
    }
  }

  Future<void> logout() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.remove('authToken');
      _token = null;
      
      await http.post(
        Uri.parse('$_baseUrl/logout/'),
        headers: _headers,
      ).timeout(const Duration(seconds: 5));
    } catch (e) {
      throw PlatformException(
        code: 'LOGOUT_ERROR',
        message: 'Error durante el logout: ${e.toString()}',
      );
    }
  }
}