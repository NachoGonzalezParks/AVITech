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

      final responseBody = jsonDecode(utf8.decode(response.bodyBytes));
      
      if (response.statusCode == 200 && responseBody['success'] == true) {
        _token = responseBody['token']; // Extrae el token
        await _saveToken(_token!);
        return responseBody;
      } else {
        throw PlatformException(
          code: 'LOGIN_FAILED',
          message: responseBody['message'] ?? 'Error en las credenciales',
        );
      }
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
      
      return _handleResponse(response);
    } on TimeoutException {
      throw PlatformException(
        code: 'TIMEOUT',
        message: 'Tiempo de espera agotado durante el registro',
      );
    } catch (e) {
      throw PlatformException(
        code: 'REGISTRATION_FAILED',
        message: 'Error en el registro: ${e.toString()}',
      );
    }
  }

  // ==================== Utilidades de Respuesta ====================
  dynamic _handleResponse(http.Response response) {
    final responseBody = jsonDecode(utf8.decode(response.bodyBytes));
    
    if (response.statusCode >= 200 && response.statusCode < 300) {
      return responseBody;
    } else {
      throw PlatformException(
        code: 'HTTP_ERROR_${response.statusCode}',
        message: responseBody['message'] ?? 'Error en la solicitud',
      );
    }
  }

  // ==================== Listados ====================
  Future<List<String>> listarPaises() async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/listar_paises/'),
        headers: _headers,
      ).timeout(const Duration(seconds: 10));
      
      final data = _handleResponse(response);
      return List<String>.from(data['paises']);
    } catch (e) {
      throw PlatformException(
        code: 'FETCH_ERROR',
        message: 'Error al obtener países: ${e.toString()}',
      );
    }
  }

  Future<List<String>> listarTiposIdentificacion(String pais) async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/listar_tipos_identificacion_por_pais/'),
        headers: _headers,
        body: jsonEncode({'nombre_pais': pais}),
      ).timeout(const Duration(seconds: 10));
      
      final data = _handleResponse(response);
      return List<String>.from(data['tipos_identificacion']);
    } catch (e) {
      throw PlatformException(
        code: 'FETCH_ERROR',
        message: 'Error al obtener tipos de identificación: ${e.toString()}',
      );
    }
  }

  Future<List<String>> listarSexos() async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/listar_sexos/'),
        headers: _headers,
      ).timeout(const Duration(seconds: 10));
      
      final data = _handleResponse(response);
      return List<String>.from(data['sexos']);
    } catch (e) {
      throw PlatformException(
        code: 'FETCH_ERROR',
        message: 'Error al obtener lista de sexos: ${e.toString()}',
      );
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
      
      return _handleResponse(response);
    } catch (e) {
      throw PlatformException(
        code: 'USER_FETCH_ERROR',
        message: 'Error al obtener usuario: ${e.toString()}',
      );
    }
  }

  Future<void> logout() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.remove('authToken');
      _token = null;
      
      // Opcional: Llamar al endpoint de logout del backend si existe
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