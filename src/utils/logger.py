from pathlib import Path
from datetime import datetime

class PhpLogger:
    
    def __init__(self, member_name="DarwinDiaz", analysis_type="lexico"):
        self.member = member_name
        self.analysis = analysis_type
        self.folder_logs = Path("tests") / "logs"
        self.folder_logs.mkdir(parents=True, exist_ok=True)
        self.file_path = self.generate_file_path()

    def generate_file_path(self):
        fecha_hora = datetime.now().strftime("%d-%m-%Y-%Hh%M")
        name_log = f"{self.analysis}-{self.member}-{fecha_hora}.txt"
        return self.folder_logs / name_log

    def save_logs(self, lista_logs):
        with open(self.file_path, "w", encoding="utf-8") as file:
            for log in lista_logs:
                file.write(str(log) + "\n")