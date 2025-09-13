# Clase Operaciones matemáticas avanzadas

class Advance():
    def potencia(base: int, exponente: int) -> int:
        """
        Calcula la potencia de un número.
        Args:
            base (int): La base.
            exponente (int): El exponente.
        Returns:
            int: El resultado de base elevado a exponente.
        """
        return base ** exponente

    def raiz_cuadrada(numero: int) -> float:
        """
        Calcula la raíz cuadrada de un número.
        Args:
            numero (int): El número del cual se desea calcular la raíz cuadrada.
        Returns:
            float: La raíz cuadrada de numero.
        """
        return numero ** 0.5