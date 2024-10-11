import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class ApiService extends ChangeNotifier {
  static const String baseUrl = 'http://127.0.0.1:8000';
  
  bool _isLoading = false;

  bool get isLoading => _isLoading;

  void _setLoading(bool loading) {
    _isLoading = loading;
    notifyListeners();
  }



  Future<Map<String, dynamic>> login(String email, String password) async {
    _setLoading(true);
    final response = await http.post(
      Uri.parse('$baseUrl/auth/login/'),
      body: {
        'email': email,
        'password': password,
      },
    );
    _setLoading(false);

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      return {
        'success': false,
        'message': 'Failed to login (en Api_service)',
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

  Future<Map<String, dynamic>> register(String email, String password1, String password2) async {
    _setLoading(true);
    final response = await http.post(
      Uri.parse('$baseUrl/auth/registration/'),
      body: {
        'email': email,
        'password1': password1,
        'password2': password2,
      },
    );
    _setLoading(false);

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      return {
        'success': false,
        'message': 'Failed to register',
      };
    }
  }
}