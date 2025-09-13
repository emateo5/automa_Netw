# Script con funciones matematicas básicas

def multiplica(a: int, b: int) -> int:
    """
    Multiplica dos números.
    Args:
        a (int): Primer número.
        b (int): Segundo número.

    Returns:
        int: El producto de a y b.
    """
    return a * b

def divide(a: int, b: int) -> float:
    """
    Divide dos números.
    Args:
        a (int): Primer número.
        b (int): Segundo número.

    Returns:
        float: El cociente de a y b.
    """
    if b != 0:
        return a / b
    print ("Error: División por cero.")
    return 0