import 'package:flutter/material.dart';
import 'package:appfront/api_service.dart';

class Pagina12 extends StatefulWidget {
  final dynamic tipo;

  Pagina12({required this.tipo});

  @override
  _Pagina12State createState() => _Pagina12State();
}

class _Pagina12State extends State<Pagina12> {
  ApiService apiService = ApiService();
  TextEditingController _descripcionController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _descripcionController.text = widget.tipo['Descripcion'];
  }

  void _updateTipo() async {
    bool success = await apiService.updateTipoIdentificacion(widget.tipo['TipoIdentificacionID'], _descripcionController.text);
    if (success) {
      Navigator.pop(context);
    } else {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error al actualizar')));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Modificar Tipo de Identificación'),
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
              onPressed: _updateTipo,
              child: Text('Guardar Cambios'),
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
