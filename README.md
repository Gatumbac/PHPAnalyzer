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
| `BOOLEAN` | Valores booleanos | `true`, `FALSE` |
| `COMMENT` | Comentarios | `// ...`, `# ...`, `/* ... */` |

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
│   ├── algorithm_darwin.php   # Archivo PHP de prueba
│   ├── algorithm_gabriel.php
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

Esto analiza el archivo `tests/algorithm_darwin.php` y genera un log con los tokens detectados en `tests/logs/`.

## Integrantes

- Darwin Díaz — Variables, datos primitivos y comentarios
- Gabriel Tumbaco
