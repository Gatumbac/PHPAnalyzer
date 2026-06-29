class SymbolTable:
    
    def __init__(self):
        # Para almacenar variables y funciones.
        self.symbols = {}
    
    def put(self, name, attributes):
        # Registra un nuevo símbolo junto con sus atributos.
        self.symbols[name] = attributes
    
    def get(self, name):
        # Retorna los atributos de un símbolo. Si no existe, devuelve None.
        return self.symbols.get(name)
    
    def exists(self, name):
        # Verifica si un símbolo existe en la tabla.
        return name in self.symbols