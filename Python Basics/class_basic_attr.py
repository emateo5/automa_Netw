# Clase con atributos y métodos básicos de matemáticas

class BasicMathAttr():
    def __init__(self, a: int, b: int):
        self.a = a
        self.b = b

    def add(self) -> int:
        return self.a + self.b
    
    def subtract(self) -> int:
        return self.a - self.b