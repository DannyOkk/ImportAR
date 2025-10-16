from dataclasses import dataclass

@dataclass(init=False)
class Articulo():
    codigo = ""
    nombre = ""
    descripcion = ""    
    precio = 0.0
