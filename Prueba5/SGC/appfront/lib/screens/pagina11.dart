import 'package:flutter/material.dart';
import 'package:appfront/api_service.dart';

class Pagina11 extends StatefulWidget {
  @override
  _Pagina11State createState() => _Pagina11State();
}

class _Pagina11State extends State<Pagina11> {
  ApiService apiService = ApiService();
  TextEditingController _descripcionController = TextEditingController();

  void _addTipo() async {
    bool success = await apiService.addTipoIdentificacion(_descripcionController.text);
    if (success) {
      Navigator.pop(context);
    } else {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error al agregar')));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Agregar Tipo de Identificación'),
      ),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          children: <Widget>[
            TextField(
              controller: _descripcionController,
              decoration: InputDecoration(labelText: 'Descripción'),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: _addTipo,
              child: Text('Agregar'),
            ),
            ElevatedButton(
              onPressed: () {
                Navigator.pop(context);
              },
              child: Text('Cancelar'),
            ),
          ],
        ),
      ),
    );
  }
}
