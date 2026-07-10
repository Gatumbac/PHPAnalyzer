from src.parser import PhpParser
from src.utils.logger import PhpLogger
from pathlib import Path

def run_analyzer():

    algorithms = [
        ("tests/algorithm_darwin.php", "DarwinDiaz"),
        ("tests/algorithm_gabriel.php", "GabrielTumbaco"),
    ]

    parser = PhpParser()

    for path_str, member in algorithms:

        path_algorithm = Path(path_str)

        if not path_algorithm.exists():
            print(f"Error: File not found {path_algorithm}")
            continue

        with open(path_algorithm, "r", encoding="utf-8") as file:
            text = file.read()

        parser.lexer.input(text)

        sintactic_errors, semantic_errors = parser.parse(text)

        sintactic_logger = PhpLogger(member_name=member, analysis_type="sintactico")

        if not sintactic_errors:
            sintactic_errors = ["Análisis sintáctico exitoso. Código sin errores de estructura."]

        sintactic_logger.save_logs(sintactic_errors)
        print(f"Log sintáctico generado con éxito: {sintactic_logger.file_path}")

        if "Análisis sintáctico exitoso" not in sintactic_errors[0]:
            print(f"Fase semántica omitida para {member} debido a errores sintácticos previos.")

        semantic_logger = PhpLogger(member_name=member, analysis_type="semantico")

        if not semantic_errors:
            semantic_errors = ["Análisis semántico exitoso. Variables y contextos correctos."]
        semantic_logger.save_logs(semantic_errors)
        print(f"Log semántico generado con éxito: {semantic_logger.file_path}")

if __name__ == "__main__":
    run_analyzer()
