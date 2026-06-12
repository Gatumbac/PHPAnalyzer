from src.lexer import PhpLexer
from src.utils.logger import LexerLogger
from pathlib import Path

def run_analyzer():

    path_algorithm = Path("tests") / "algorithm_darwin.php"
    
    if not path_algorithm.exists():
        print(f"Error: File not found {path_algorithm}")
        return

    lexer = PhpLexer()
    
    logger = LexerLogger(member_name="DarwinDiaz")

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

if __name__ == "__main__":
    run_analyzer()