import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  final String baseUrl = 'http://localhost:8000/api/';

  Future<List<dynamic>> getTiposIdentificacion() async {
    final response = await http.get(Uri.parse('${baseUrl}tipos-identificacion/'));
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Error al cargar los tipos de identificación');
    }
  }

  Future<bool> addTipoIdentificacion(String descripcion) async {
    final response = await http.post(
      Uri.parse('${baseUrl}tipos-identificacion/'),
      body: {'Descripcion': descripcion},
    );
    return response.statusCode == 201;
  }

  Future<bool> updateTipoIdentificacion(int id, String descripcion) async {
    final response = await http.put(
      Uri.parse('${baseUrl}tipos-identificacion/$id/'),
      body: {'Descripcion': descripcion},
    );
    return response.statusCode == 200;
  }

  Future<bool> deleteTipoIdentificacion(int id) async {
    final response = await http.delete(
      Uri.parse('${baseUrl}tipos-identificacion/$id/'),
    );
    return response.statusCode == 204;
  }
}
