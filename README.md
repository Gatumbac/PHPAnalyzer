# PHPAnalyzer

Analizador léxico para código PHP desarrollado en Python usando [PLY (Python Lex-Yacc)](https://www.dabeaz.com/ply/).

## Descripción

PHPAnalyzer tokeniza archivos PHP e identifica los siguientes elementos léxicos:

| Token | Descripción | Ejemplo |
|-------|-------------|---------|
| `VARIABLE` | Variables PHP | `$nombre`, `$edad_usuario` |
| `INTEGER` | Números enteros | `25`, `-5` |
| `FLOAT` | Números de punto flotante | `19.99`, `-120.45` |
| `STRING` | Cadenas de texto | `'texto'`, `"texto"` |
| `TRUE` | Booleano verdadero | `true` |
| `FALSE` | Booleano falso | `false` |
| `COMMENT` | Comentarios | `// ...`, `# ...`, `/* ... */` |
| `ID` | Identificadores | `sumar`, `calcular` |
| `IF` | Palabra reservada | `if` |
| `ELSE` | Palabra reservada | `else` |
| `WHILE` | Palabra reservada | `while` |
| `BREAK` | Palabra reservada | `break` |
| `FUNCTION` | Palabra reservada | `function` |
| `RETURN` | Palabra reservada | `return` |
| `ECHO` | Palabra reservada | `echo` |
| `PLUS`, `MINUS`, `TIMES`, `DIVIDE`, `MODULO` | Operadores aritméticos | `+`, `-`, `*`, `/`, `%` |
| `EQ`, `NEQ`, `LT`, `GT`, `LE`, `GE` | Operadores relacionales | `==`, `!=`, `<`, `>`, `<=`, `>=` |
| `AND`, `OR`, `NOT` | Operadores lógicos | `&&`, `\|\|`, `!` |
| `ASSIGN`, `PLUS_ASSIGN`, `MINUS_ASSIGN` | Operadores de asignación | `=`, `+=`, `-=` |
| `SEMICOLON`, `LBRACE`, `RBRACE`, `LPAREN`, `RPAREN` | Delimitadores | `;`, `{`, `}`, `(`, `)` |
| `LBRACKET`, `RBRACKET`, `COMMA`, `COLON`, `ARROW` | Delimitadores | `[`, `]`, `,`, `:`, `=>` |
| `PHP_OPEN`, `PHP_CLOSE` | Etiquetas PHP | `<?php`, `?>` |

Los resultados se guardan en archivos de log dentro de `tests/logs/`.

## Estructura del proyecto

```
PHPAnalyzer/
├── main.py              # Punto de entrada
├── src/
│   ├── __init__.py
│   ├── lexer.py         # Definición del analizador léxico (PhpLexer)
│   └── utils/
│       ├── __init__.py
│       └── logger.py    # Logger de tokens (LexerLogger)
├── tests/
│   ├── algorithm_darwin.php   # Archivo PHP de prueba (Darwin Díaz)
│   ├── algorithm_gabriel.php  # Archivo PHP de prueba (Gabriel Tumbaco)
│   └── logs/                  # Salida de los análisis
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

Esto analiza los archivos `tests/algorithm_darwin.php` y `tests/algorithm_gabriel.php`, generando un log por cada integrante en `tests/logs/`.

## Integrantes

- Darwin Díaz — Variables, datos primitivos y comentarios
- Gabriel Tumbaco — Operadores, palabras reservadas y delimitadores
