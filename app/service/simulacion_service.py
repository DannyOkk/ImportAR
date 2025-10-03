from app.models import Simulacion
from app.repositories import SimulacionRepository
from typing import List
from app.service import Task, CalculateTask, BudgetTask, EmailTask

class SimulacionService:
    @staticmethod
    def create(simulacion:Simulacion)-> Simulacion: 
        """
        Create a new simulation in the database.
        :param simulacion: Simulacion object to be created.   
        :return: The created Simulacion object.
        """
        SimulacionRepository.create(simulacion)

        return simulacion
    def get_by_id(id: int) -> Simulacion:
        """
        Retrieve a simulation by its ID.
        :param id: The ID of the simulation to retrieve.
        :return: The Simulacion object if found, else None.
        """
        return SimulacionRepository.get_by_id(id)

    @staticmethod   
    def read_all() -> list[Simulacion]:
        """
        Retrieve all simulations from the database.
        :return: A list of all Simulacion objects.
        """
        return SimulacionRepository.read_all()

    @staticmethod
    def execute(simulacion: Simulacion) -> bool:
        """
        Execute a simulation task.
        :param simulacion: Simulacion object to be executed.
        :return: True if the task was executed successfully, else False.
        """
        task = Task(simulacion)
        calculate = CalculateTask()
        budget = BudgetTask()
        email = EmailTask()
        task.add(calculate)
        task.add(budget)
        task.add(email)

        result = task.execute()
        return result
