from src.lexer import PhpLexer
from src.parser import PhpParser
from src.utils.logger import PhpLogger
from pathlib import Path

def run_analyzer():

    algorithms = [
        ("tests/algorithm_darwin.php", "DarwinDiaz"),
        #("tests/algorithm_gabriel.php", "GabrielTumbaco"),
    ]

    parser = PhpParser()

    for path_str, member in algorithms:

        path_algorithm = Path(path_str)

        if not path_algorithm.exists():
            print(f"Error: File not found {path_algorithm}")
            continue

        logger = PhpLogger(member_name=member, analysis_type="sintactico")

        with open(path_algorithm, "r", encoding="utf-8") as file:
            text = file.read()

        parser.lexer.input(text)

        errores_detectados = parser.parse(text)
        
        if not errores_detectados:
            errores_detectados = ["Análisis sintáctico exitoso. Código sin errores de estructura."]

        logger.save_logs(errores_detectados)
        print(f"Log generado con éxito: {logger.file_path}")

if __name__ == "__main__":
    run_analyzer()
