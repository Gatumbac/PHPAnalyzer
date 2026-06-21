# PHPAnalyzer

Analizador léxico y sintáctico para código PHP desarrollado en Python usando [PLY (Python Lex-Yacc)](https://www.dabeaz.com/ply/).

## Descripción

PHPAnalyzer tokeniza y analiza sintácticamente archivos PHP. El análisis se realiza en dos fases:

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

Los resultados se guardan como archivos de log en `tests/logs/`, tanto del análisis léxico como sintáctico.

## Estructura del proyecto

```
PHPAnalyzer/
├── main.py                  # Punto de entrada
├── src/
│   ├── __init__.py
│   ├── lexer.py             # Analizador léxico (PhpLexer)
│   ├── parser.py            # Analizador sintáctico (PhpParser)
│   └── utils/
│       ├── __init__.py
│       └── logger.py        # Logger (PhpLogger)
├── tests/
│   ├── algorithm_darwin.php     # Archivo PHP de prueba (Darwin Díaz)
│   ├── algorithm_gabriel.php    # Archivo PHP de prueba (Gabriel Tumbaco)
│   └── logs/                    # Salida de los análisis
│       ├── lexico-*.txt
│       └── sintactico-*.txt
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

Esto ejecuta el análisis sintáctico sobre los archivos PHP en `tests/`, generando logs en `tests/logs/` con los errores de estructura encontrados. Si el código es válido, se registra un mensaje de éxito.

Para usar únicamente el analizador léxico de forma interactiva:

```python
from src.lexer import PhpLexer

lexer = PhpLexer()
lexer.input("<?php $x = 10 + 5; ?>")
for tok in lexer.lexer:
    print(tok)
```

## Integrantes

- Darwin Díaz — Variables, datos primitivos, comentarios, `while`/`break`, arreglos indexados, funciones con retorno, `echo`
- Gabriel Tumbaco — Operadores, palabras reservadas, delimitadores, `if`/`else`, arreglos asociativos, llamadas a funciones, captura de datos (`readline`/`$_POST`), manejo de errores sintácticos
