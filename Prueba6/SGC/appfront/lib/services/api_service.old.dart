// api_service.dart
import 'dart:convert';
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

  // ==================== Auth ====================

  
  Future<Map<String, dynamic>> login(String email, String password) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/login/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'username': email, 'password': password}),
    );

    if (response.statusCode == 200) {
      _token = jsonDecode(response.body)['token'];
      await _saveToken(_token!);
      return jsonDecode(response.body);
    } else {
      throw Exception('Error en login: ${response.statusCode}');
    }
  }
  

  

  Future<void> _saveToken(String token) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('authToken', token);
  }

  // ==================== Registro ====================
  Future<Map<String, dynamic>> registroUsuario(Map<String, dynamic> data) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/registro/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(data),
    );

    return _handleResponse(response);
  }

  // ==================== Utilidades ====================
  dynamic _handleResponse(http.Response response) {
    if (response.statusCode >= 200 && response.statusCode < 300) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Error ${response.statusCode}: ${response.body}');
    }
  }

  // ==================== Listados ====================
  Future<List<String>> listarPaises() async {
    final response = await http.post(
      Uri.parse('$_baseUrl/listar_paises/'),
      headers: _headers,
    );
    return List<String>.from(jsonDecode(response.body)['paises']);
  }

  Future<List<String>> listarTiposIdentificacion(String pais) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/listar_tipos_identificacion_por_pais/'),
      headers: _headers,
      body: jsonEncode({'nombre_pais': pais}),
    );
    return List<String>.from(jsonDecode(response.body)['tipos_identificacion']);
  }

  Future<List<String>> listarSexos() async {
    final response = await http.post(
      Uri.parse('$_baseUrl/listar_sexos/'),
      headers: _headers,
    );
    return List<String>.from(jsonDecode(response.body)['sexos']);
  }

  // ==================== Password ====================
  Future<void> solicitarResetPassword(String email) async {
    await http.post(
      Uri.parse('$_baseUrl/mail_password_reset/'),
      body: jsonEncode({'email': email}),
    );
  }

  Future<void> confirmarResetPassword(String uid, String token, String newPassword) async {
    await http.post(
      Uri.parse('$_baseUrl/reset/$uid/$token/'),
      body: jsonEncode({'new_password': newPassword}),
    );
  }

  // ==================== User Management ====================
  Future<Map<String, dynamic>> getUsuarioActual() async {
    final response = await http.get(
      Uri.parse('$_baseUrl/api/auth/user/'),
      headers: _headers,
    );
    return _handleResponse(response);
  }

  Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('authToken');
    _token = null;
  }
}