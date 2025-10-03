from abc import ABC, abstractmethod
import logging

class Command(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs)-> bool:
        raise NotImplementedError("You should implement this method.")
    
class CalculateTask(Command):
    def execute(self, *args, **kwargs) -> bool:
        # Aquí iría la lógica para ejecutar la tarea de simulación.
        logging.info(f"Ejecutando tarea de simulación")
        return True

class BudgetTask(Command):

    def execute(self, *args, **kwargs) -> bool:
        # Aquí iría la lógica para ejecutar la tarea de presupuesto.
        logging.info(f"Ejecutando tarea de presupuesto")
        return True

class EmailTask(Command):
    def execute(self, *args, **kwargs) -> bool:
        # Aquí iría la lógica para enviar el correo electrónico.
        logging.info(f"Enviando correo electrónico")
        return True

class Task(Command):
    def __init__(self, simulacion=None):
        self.simulacion= simulacion
        self.tasks = []

    def add(self, task: Command):
        self.tasks.append(task)

    def remove(self, task: Command):
        self.tasks.remove(task)

    def execute(self, *args, **kwargs) -> bool:
        # Aquí iría la lógica para guardar los resultados.
        logging.info(f"Executando tareas...")
        result = True
        for task in self.tasks:
            result = task.execute(self.simulacion) and result 
        return result 
    
        
