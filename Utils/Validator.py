"""
Archivo: `validators.py`

Funciones de validación y parseo para usar en el proyecto:
- is_non_empty_string, clean_string
- is_valid_name
- is_positive_int_str / parse_positive_int
- is_positive_decimal_str / parse_positive_decimal
- is_unique_name
- format_decimal
- parse_bool
"""

import re
from typing import Iterable, Optional

def is_non_empty_string(value: Optional[str]) -> bool:
    """True si value es un string no vacío después de strip()."""
    return isinstance(value, str) and bool(value.strip())


def clean_string(value: Optional[str]) -> str:
    """Devuelve value.strip() o cadena vacía si es None."""
    return (value or "").strip()


_NAME_RE = re.compile(r"^(?!\d)[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9\s\-\._']+$")


def is_valid_name(value: Optional[str], min_len: int = 1, max_len: int = 100) -> bool:
    """
    Válida un nombre de producto básico:
    - no vacío (según min_len)
    - longitud entre min_len y max_len
    - no empieza por dígito
    - solo caracteres razonables (letras, números, espacios, - . _ ')
    """
    s = clean_string(value)
    if not (min_len <= len(s) <= max_len):
        return False
    return bool(_NAME_RE.match(s))

def is_valid_number(value: Optional[float]) -> bool:
    """
    Válida si el valor es un número (int o float).
    """
    return isinstance(value, (int, float))


def is_positive_int(value: int) -> bool:
    """True si value representa un entero positivo (>0)."""
    try:
        n = int(value)
        return n > 0
    except Exception:
        return False

def is_positive_int_str(value: str) -> bool:
    """True si value es un string que representa un entero positivo (>0)."""
    if not isinstance(value, str):
        return False
    s = value.strip()
    if not s.isdigit():
        return False
    try:
        return int(s) > 0
    except Exception:
        return False


def parse_positive_int(value: str) -> int:
    """
    Convierte value a int positivo (>0).
    Lanza ValueError si no es válido.
    """
    try:
        n = int(value)
    except Exception:
        raise ValueError("No es un entero válido.")
    if n <= 0:
        raise ValueError("El entero debe ser mayor que 0.")
    return n


_DECIMAL_RE = re.compile(r"^[+-]?\d+([.,]\d+)?$")


def is_positive_decimal(value: str) -> bool:
    """True si value es decimal u entero positivo (acepta ',' o '.')."""
    if not isinstance(value, str):
        return False
    s = value.strip().replace(" ", "")
    if not _DECIMAL_RE.match(s):
        return False
    try:
        return float(s.replace(",", ".")) > 0
    except Exception:
        return False

def is_valid_decimal(value: str) -> bool:
    """True si value es decimal o entero (acepta ',' o '.')."""
    if not isinstance(value, str):
        return False
    s = value.strip().replace(" ", "")
    if not _DECIMAL_RE.match(s):
        return False
    try:
        float(s.replace(",", "."))
        return True
    except Exception:
        return False


def parse_positive_decimal(value: str) -> float:
    """
    Convierte value a float positivo (>0). Acepta coma o punto como separador.
    Lanza ValueError si no es válido.
    """
    if not isinstance(value, str):
        raise ValueError("Valor no es una cadena.")
    s = value.strip().replace(" ", "")
    if not _DECIMAL_RE.match(s):
        raise ValueError("Formato decimal inválido.")
    f = float(s.replace(",", "."))
    if f <= 0:
        raise ValueError("El número debe ser mayor que 0.")
    return f


def is_unique_name(name: str, container: Iterable[str]) -> bool:
    """
    Comprueba si name no está en container (case-insensitive).
    container puede ser keys de un dict o lista de nombres.
    """
    if not is_non_empty_string(name):
        return False
    name_norm = clean_string(name).lower()
    return all(name_norm != clean_string(c).lower() for c in container)


def format_decimal(value: float, decimals: int = 2, decimal_sep: str = ",") -> str:
    """
    Formatea un número con `decimals` decimales y usa `decimal_sep`
    (por ejemplo \",\") como separador decimal.
    """
    fmt = f"{{:.{decimals}f}}".format(value)
    if decimal_sep != ".":
        fmt = fmt.replace(".", decimal_sep)
    return fmt


def parse_bool(value: str) -> Optional[bool]:
    """
    Interpreta respuestas yes/no en múltiples idiomas.
    Devuelve True/False o None si no puede interpretarse.
    Acepta: y/n, s/n, yes/no, true/false (case-insensitive).
    """
    if not isinstance(value, str):
        return None
    v = value.strip().lower()
    true_set = {"y", "yes", "s", "si", "true", "t", "1"}
    false_set = {"n", "no", "false", "f", "0"}
    if v in true_set:
        return True
    if v in false_set:
        return False
    return None


Soy GitHub Copilot Chat Assistant.

Aquí tienes una propuesta de README.md para tu repositorio PruebaPython basada en la estructura que has compartido.

--------------------------------------------------

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
- Dependencias estándar (si en el futuro se añaden externas, agrégalas aquí).

## Instalación

1. Clona el repositorio:
   ```
   git clone https://github.com/Danieloid3/PruebaPython.git
   cd PruebaPython
   ```
2. (Opcional) Crea y activa un entorno virtual:
   ```
   python -m venv .venv
   source .venv/bin/activate        # Linux / macOS
   .venv\Scripts\activate           # Windows
   ```
3. Verifica que los archivos CSV existen en la carpeta Archivos/. Si deseas iniciar limpio puedes vaciarlos manteniendo la cabecera (si la hubiera).

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

Si el archivo menu.py ofrece opciones numeradas, simplemente sigue las instrucciones en pantalla.

## Formato esperado de CSV (sugerido)

Aunque puede variar según la implementación interna, un formato típico podría ser:

Inventario.csv:
```
id,nombre,precio,cantidad
1,Teclado,25.99,10
```

Sales.csv:
```
id_venta,id_producto,cantidad,total,fecha
1,1,2,51.98,2025-11-24
```

Users.csv:
```
id_usuario,nombre,rol
1,Ana,admin
```

Ajusta estos ejemplos si tus archivos ya tienen un esquema diferente.

## Extensiones futuras

- Reemplazo de CSV por SQLite o PostgreSQL.
- Autenticación y control de roles más robusto.
- Exportación de reportes (PDF/Excel).
- API REST usando FastAPI o Flask.
- Tests automatizados (PyTest).

## Buenas prácticas sugeridas

- Agregar un archivo requirements.txt si se añaden dependencias.
- Incluir manejo de excepciones centralizado en los servicios.
- Evitar lógica compleja dentro de los modelos (moverla a Services).
- Añadir docstrings y type hints para mejorar mantenimiento.
- Implementar unit tests en una carpeta tests/.

## Contribuir

1. Crear rama:
   ```
   git checkout -b feature/nueva-funcionalidad
   ```
2. Hacer cambios y commits descriptivos:
   ```
   git commit -m "Agrega validación de stock negativo"
   ```
3. Abrir Pull Request hacia main o master.

## Licencia

Especifica aquí la licencia (por ejemplo MIT, GPL, etc.). Si aún no tienes una, puedes crear un archivo LICENSE y aclararlo.

## Autor

Proyecto mantenido por Danieloid3.

---

Si quieres que adapte el README a otro estilo (más técnico, más comercial, en inglés, con badges, etc.) házmelo saber y lo ajusto.