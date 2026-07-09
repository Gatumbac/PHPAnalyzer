class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def put(self, name, attributes):
        self.symbols[name] = attributes

    def get(self, name):
        return self.symbols.get(name)

    def exists(self, name):
        return name in self.symbols
