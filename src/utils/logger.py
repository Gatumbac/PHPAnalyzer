from pathlib import Path
from datetime import datetime

class LexerLogger:
    
    def __init__(self, member_name="DarwinDiaz"):
        self.member = member_name
        self.folder_logs = Path("tests") / "logs"
        self.folder_logs.mkdir(parents=True, exist_ok=True)
        self.file_path = self.generate_file_path()

    def generate_file_path(self):
        fecha_hora = datetime.now().strftime("%d-%m-%Y-%Hh%M")
        name_log = f"lexico-{self.member}-{fecha_hora}.txt"
        return self.folder_logs / name_log

    def save_tokens(self, lista_tokens):
        with open(self.file_path, "w", encoding="utf-8") as file:
            for tok in lista_tokens:
                file.write(str(tok) + "\n")