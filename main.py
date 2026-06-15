from src.lexer import PhpLexer
from src.utils.logger import LexerLogger
from pathlib import Path

def run_analyzer():

    algorithms = [
        ("tests/algorithm_darwin.php", "DarwinDiaz"),
        ("tests/algorithm_gabriel.php", "GabrielTumbaco"),
    ]

    lexer = PhpLexer()

    for path_str, member in algorithms:
        path_algorithm = Path(path_str)

        if not path_algorithm.exists():
            print(f"Error: File not found {path_algorithm}")
            continue

        logger = LexerLogger(member_name=member)

        with open(path_algorithm, "r", encoding="utf-8") as file:
            text = file.read()

        lexer.input(text)

        tokens_detectados = []
        while True:
            tok = lexer.token()
            if not tok:
                break
            tokens_detectados.append(tok)

        logger.save_tokens(tokens_detectados)
        print(f"Log generado: {logger.file_path}")

if __name__ == "__main__":
    run_analyzer()
