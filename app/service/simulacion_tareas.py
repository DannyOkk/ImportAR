from abc import ABC, abstractmethod
import logging
from faker import Faker
from app.models import Articulo, Simulacion, Presupuesto

class Command(ABC):
    @abstractmethod
    def execute(self, simulacion: Simulacion,*args, **kwargs)-> bool:
        raise NotImplementedError("You should implement this method.")
    
class CalculateTask(Command):
    def execute(self, simulacion: Simulacion, *args, **kwargs) -> bool:
        # Aquí iría la lógica para ejecutar la tarea de simulación.
        logging.info(f"Ejecutando tarea de simulación")
        fake = Faker()
        presupuesto = Presupuesto()
        presupuesto.estado = "finalizado"
        presupuesto.moneda = "USD"
        articulo = Articulo()
        articulo.codigo = fake.unique.ean(length=8)
        articulo.nombre = fake.name()
        articulo.descripcion = fake.text(max_nb_chars=200)
        articulo.precio = round(fake.pyfloat(left_digits=3, right_digits=2, positive=True, min_value=10, max_value=1000),2)
        presupuesto.total = articulo.precio * 1.21  # Suponiendo un IVA del 21%
        presupuesto.detalle = f"Artículo: {articulo.nombre}, Precio: {articulo.precio}, IVA: 21%"
        simulacion.presupuesto = presupuesto
        return True

class BudgetTask(Command):

    def execute(self, simulacion: Simulacion, *args, **kwargs) -> bool:
        # Aquí iría la lógica para ejecutar la tarea de presupuesto.
        logging.info(f"Ejecutando tarea de presupuesto")
        return True

class EmailTask(Command):
    def execute(self, simulacion: Simulacion, *args, **kwargs) -> bool:
        # Aquí iría la lógica para enviar el correo electrónico.
        logging.info(f"Enviando correo electrónico")
        return True

class Task(Command):
    def __init__(self):
        self.tasks = []

    def add(self, task: Command):
        self.tasks.append(task)

    def remove(self, task: Command):
        self.tasks.remove(task)

    def execute(self, simulacion: Simulacion, *args, **kwargs) -> bool:
        # Aquí iría la lógica para guardar los resultados.
        logging.info(f"Executando tareas...")
        result = True
        for task in self.tasks:
            result = task.execute(simulacion) and result 
        return result 
    
        
