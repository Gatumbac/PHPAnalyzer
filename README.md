# PHPAnalyzer

Analizador léxico, sintáctico y semántico para código PHP desarrollado en Python usando [PLY (Python Lex-Yacc)](https://www.dabeaz.com/ply/).

Setup Local: [SETUP](./docs/SETUP.md)

## Descripción

PHPAnalyzer tokeniza y analiza archivos PHP en tres fases:

### 1. Análisis Léxico (PhpLexer)

Identifica los siguientes elementos léxicos:

| Token | Descripción | Ejemplo |
|-------|-------------|---------|
| `VARIABLE` | Variables PHP | `$nombre`, `$edad_usuario` |
| `INTEGER` | Números enteros | `25`, `-5` |
| `FLOAT` | Números de punto flotante | `19.99`, `-120.45` |
| `STRING` | Cadenas de texto | `'texto'`, `"texto"` |
| `TRUE` / `FALSE` | Booleanos | `true`, `false` |
| `COMMENT` | Comentarios | `// ...`, `# ...`, `/* ... */` |
| `ID` | Identificadores | `sumar`, `calcular` |
| `IF`, `ELSE`, `WHILE`, `BREAK`, `FUNCTION`, `RETURN`, `ECHO` | Palabras reservadas | `if`, `while`, `function` |
| `PLUS`, `MINUS`, `TIMES`, `DIVIDE`, `MODULO` | Operadores aritméticos | `+`, `-`, `*`, `/`, `%` |
| `EQ`, `NEQ`, `LT`, `GT`, `LE`, `GE` | Operadores relacionales | `==`, `!=`, `<`, `>`, `<=`, `>=` |
| `AND`, `OR`, `NOT` | Operadores lógicos | `&&`, `\|\|`, `!` |
| `ASSIGN`, `PLUS_ASSIGN`, `MINUS_ASSIGN` | Operadores de asignación | `=`, `+=`, `-=` |
| `SEMICOLON`, `LBRACE`, `RBRACE`, `LPAREN`, `RPAREN` | Delimitadores | `;`, `{`, `}`, `(`, `)` |
| `LBRACKET`, `RBRACKET`, `COMMA`, `COLON`, `ARROW` | Delimitadores | `[`, `]`, `,`, `:`, `=>` |
| `PHP_OPEN`, `PHP_CLOSE` | Etiquetas PHP | `<?php`, `?>` |
| `POST`, `READLINE` | Captura de datos | `$_POST`, `readline` |

### 2. Análisis Sintáctico (PhpParser)

Valida la estructura del código PHP según reglas gramaticales definidas:

| Regla | Descripción |
|-------|-------------|
| Declaraciones simples | Asignación de variables (`$x = expr;`) y arreglos |
| Declaraciones compuestas | Asignación con operadores `+=` y `-=` |
| Expresiones | Operaciones aritméticas, lógicas y relacionales con precedencia |
| Estructuras de control | `if`/`else`, `while`, `break` |
| Arreglos indexados y asociativos | `[1, 2, 3]`, `["key" => value]` |
| Funciones | Definición (`function foo(...) { }`), retorno y llamadas |
| Captura de datos | `readline(...)`, `$_POST["key"]` |
| Impresión | `echo expr;` |

### 3. Análisis Semántico (SemanticAnalyzer)

Valida coherencia lógica del código luego de pasar la fase sintáctica:

| Regla | Descripción |
|-------|-------------|
| Variables inicializadas | Detecta uso de variables no declaradas/inicializadas |
| Contexto de `break` | Reporta `break` fuera de bucles |
| Tipos aritméticos | Valida operaciones `+`, `-`, `*`, `/`, `%` entre tipos numéricos |
| Redeclaración de funciones | Detecta funciones definidas más de una vez |

Los resultados se guardan como archivos de log en `tests/logs/` para análisis sintáctico y semántico.

## Estructura del proyecto

```
PHPAnalyzer/
├── main.py                  # Punto de entrada
├── apps/
│   └── web/                 # Workspace reservado para frontend web (Vite)
├── docs/
│   └── specs/               # Especificaciones de arquitectura y comportamiento UI
├── packages/
│   └── analyzer/
│       └── php_analyzer/    # Core reusable del analizador (sin IO de archivos)
├── src/
│   └── utils/
│       ├── __init__.py
│       └── logger.py        # Logger de CLI
├── tests/
│   ├── algorithm_darwin.php     # Archivo PHP de prueba (Darwin Díaz)
│   ├── algorithm_gabriel.php    # Archivo PHP de prueba (Gabriel Tumbaco)
│   ├── unit/                     # Tests unitarios del core
│   └── logs/                    # Salida de los análisis
│       ├── lexico-*.txt
│       ├── sintactico-*.txt
│       └── semantico-*.txt
├── pnpm-workspace.yaml
├── package.json
├── requirements.txt
└── README.md
```

## Requisitos previos

- Python 3.10 o superior

## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/Gatumbac/PHPAnalyzer.git
cd PHPAnalyzer
```

2. Crear y activar el entorno virtual:

```bash
python -m venv .venv
```

- Linux / macOS:
```bash
source .venv/bin/activate
```

- Windows:
```bash
.venv\Scripts\activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Uso

```bash
python main.py
```

Esto ejecuta el análisis sobre los archivos PHP en `tests/` y genera logs en `tests/logs/`:

- `sintactico-*.txt` con errores de estructura o mensaje de éxito.
- `semantico-*.txt` con errores lógicos/contextuales o mensaje de éxito.

Para usar el analizador reusable desde Python:

```python
from packages.analyzer import analyze_php

result = analyze_php("<?php $x = 10 + 5; ?>")
print(result.status)
print(result.tokens[0])
```

## Integrantes

- Darwin Díaz — Variables, datos primitivos, comentarios, `while`/`break`, arreglos indexados, funciones con retorno, `echo`
- Gabriel Tumbaco — Operadores, palabras reservadas, delimitadores, `if`/`else`, arreglos asociativos, llamadas a funciones, captura de datos (`readline`/`$_POST`), manejo de errores sintácticos
