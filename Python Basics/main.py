# Script principal que utiliza (importa) las clases y scripts

from class_oper_basic_math import Basicas
from class_oper_advance_math import Advance
from class_basic_attr import BasicMathAttr
from script_basic import multiplica, divide

if __name__ == "__main__":
    basic = Basicas()
    advance = Advance()
    basic_math = BasicMathAttr(10, 5)
    print ("Suma: ", basic.suma(5, 5))
    print ("Resta: ", basic.resta(5, 5))
    print ("Multiplica: ", basic.multiplica(5, 5))
    print ("Divide: ", basic.divide(5, 5))
    print ("Potencia: ", advance.potencia(5, 2))
    print ("Raíz Cuadrada: ", advance.raiz_cuadrada(25))
    print ("Clase Suma: ", basic_math.add())
    print ("Clase Resta: ", basic_math.subtract())
    print ("Script Multiplica: ", multiplica(10, 5))
    print ("Script Divide: ", divide(10, 5))