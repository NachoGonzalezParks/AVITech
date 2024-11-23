// FLUTTER
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
// API_SERVICE
// import 'package:appfront/data/repositories/api_service.dart';
// ROUTER
// import 'routes/app_routes.dart';
// THEME
// import 'themes/app_theme.dart';
// SCREENS
// imports?

// void main() => runApp(MaterialApp(
  
// ))

// ARRANQUE DE LA APP
void main() {
  Item itemUno = Item('Pelota', 1);
  itemUno.status();
  print(itemUno.item);
  Item itemDos = Item('Jugadores', 22);
  print(itemDos.item);
  Item itemTres = Item('Cancha', 1);
  print(itemTres.item);
  Match partido = Match('Partido', 1, 90);
  print(partido.item);
  print(partido.tiempo);
  partido.superStatus();
}

class Item {
  
  // ATRIBUTOS
  String item = '';
  int cantidad = 0;

 // CONSTRUCTOR // NOMBRE (PARAMETROS TIPADOS)
  Item (String paramItemNombre, int paramItemCant){
    item = paramItemNombre;
    cantidad = paramItemCant;
  }

  // METODOS
  void status() {
    print('OK!');
  }
}

class Match extends Item { 

  int tiempo = 0;

  // CONSTRUCTOR, PASO LOS PARAM DE CLASE HEREDADA COMO SUPER Y LUEGO LE AGREGO LOS PROPIOS
  Match (super.paramMatchNombre, super.paramMatchCant, int tiempo);


  void superStatus() {
    print('2xOK!');
  }
}