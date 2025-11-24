# PruebaPython

Sistema simple de gestión de inventario, ventas y usuarios en Python utilizando archivos CSV como almacenamiento plano.  
El proyecto está organizado en capas: Models, Services y Utils, con una interfaz de menú en consola.

## Características principales

- Gestión de productos (crear, listar, actualizar, eliminar).
- Registro y consulta de ventas.
- Administración de usuarios.
- Persistencia mediante archivos CSV (Inventario.csv, Sales.csv, Users.csv).
- Validaciones y decoradores para mejorar robustez.
- Menú interactivo en consola (archivo Services/menu.py).

## Estructura del proyecto

```
PruebaPython/
├── Archivos/
│   ├── Inventario.csv
│   ├── Sales.csv
│   └── Users.csv
├── Models/
│   ├── Product.py
│   ├── Sale.py
│   └── User.py
├── Services/
│   ├── Inventory.py
│   ├── SaleService.py
│   ├── UserService.py
│   └── menu.py
└── Utils/
    ├── Decorator.py
    └── Validator.py
```

### Archivos (Archivos/)
Contiene los datos persistentes del sistema en formato CSV:  
- Inventario.csv: catálogo de productos con sus cantidades.  
- Sales.csv: historial de ventas realizadas.  
- Users.csv: usuarios registrados (roles o permisos posibles según implementación interna).

### Modelos (Models/)
Representan las entidades del dominio:
- Product.py: define la estructura y posible lógica asociada a productos.
- Sale.py: modela una transacción de venta.
- User.py: representa un usuario del sistema (administrador, vendedor, etc.).

### Servicios (Services/)
Capa donde reside la lógica de negocio:
- Inventory.py: operaciones sobre el inventario (agregar, ajustar stock, consultar).
- SaleService.py: registro y validación de ventas.
- UserService.py: creación y manejo de usuarios.
- menu.py: punto de entrada interactivo; despliega las opciones y coordina las llamadas a los servicios.

### Utilidades (Utils/)
Funciones transversales:
- Validator.py: validaciones de entrada (tipos, rangos, formatos).
- Decorator.py: posibles decoradores para logging, manejo de errores o control de acceso.

## Requisitos

- Python 3.8+ (recomendado)
- No requiere base de datos; utiliza archivos CSV incluidos.

## Instalación

1. Clona el repositorio:
   ```
   git clone https://github.com/Danieloid3/PruebaPython.git
   cd PruebaPython
   ```


## Uso

Ejecuta el menú principal:
```
python Services/menu.py
```

Posibles funcionalidades (según la estructura):
- Listar productos
- Agregar producto
- Registrar venta
- Consultar historial de ventas
- Crear usuario
- Validar datos antes de operaciones

El archivo menu.py ofrece opciones numeradas, simplemente sigue las instrucciones en pantalla.


## Extensiones futuras

- Reemplazo de CSV por SQLite o PostgreSQL.
- Autenticación y control de roles más robusto.
- Exportación de reportes (PDF/Excel).