import 'package:flutter/material.dart';
import 'package:appfront/api_service.dart';
import 'pagina11.dart';
import 'pagina12.dart';

class Pagina10 extends StatefulWidget {
  @override
  _Pagina10State createState() => _Pagina10State();
}

class _Pagina10State extends State<Pagina10> {
  ApiService apiService = ApiService();
  List<dynamic> tipos = [];

  @override
  void initState() {
    super.initState();
    fetchTipos();
  }

  fetchTipos() async {
    tipos = await apiService.getTiposIdentificacion();
    setState(() {});
  }

  void _deleteTipo(int id) async {
    bool success = await apiService.deleteTipoIdentificacion(id);
    if (success) {
      fetchTipos(); // Actualiza la lista
    }
  }

  void _confirmDelete(int id) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text("Confirmar"),
          content: Text("¿Desea eliminar este registro?"),
          actions: <Widget>[
            TextButton(
              child: Text("No"),
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
            TextButton(
              child: Text("Sí"),
              onPressed: () {
                _deleteTipo(id);
                Navigator.of(context).pop();
              },
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Tipos de Identificación:'),
      ),
      body: ListView.builder(
        itemCount: tipos.length,
        itemBuilder: (context, index) {
          return ListTile(
            title: Text(tipos[index]['Descripcion']),
            trailing: Row(
              mainAxisSize: MainAxisSize.min,
              children: <Widget>[
                IconButton(
                  icon: Icon(Icons.edit),
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => Pagina12(tipo: tipos[index]),
                      ),
                    ).then((_) => fetchTipos());
                  },
                ),
                IconButton(
                  icon: Icon(Icons.delete),
                  onPressed: () => _confirmDelete(tipos[index]['TipoIdentificacionID']),
                ),
              ],
            ),
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => Pagina11()),
          ).then((_) => fetchTipos());
        },
        child: Icon(Icons.add),
      ),
    );
  }
}
