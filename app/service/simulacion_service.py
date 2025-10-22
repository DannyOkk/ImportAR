from app.models import Simulacion
from app.repositories import SimulacionRepository
from typing import List
from app.service.simulacion_tareas import Task, CalculateTask, BudgetTask, EmailTask
from app.service.usuario_service import UsuarioService
from app.service.presupuesto_service import PresupuestoService
from datetime import datetime
from random import randint

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
    def execute(dto: Simulacion) -> bool:
        """
        Execute a simulation task.
        :param simulacion: Simulacion object to be executed.
        :return: True if the task was executed successfully, else False.
        DTO: Data Transfer Object
        """

        #TODO: refactorizar
        simulacion = Simulacion()
        simulacion.usuario = UsuarioService.get_by_id(dto.usuario.id)
        simulacion.estado = "procesando"
        simulacion.fecha_creacion = datetime.now()
        simulacion.num_escenario = randint(1, 100)
        task = Task()
        calculate = CalculateTask()
        budget = BudgetTask()
        email = EmailTask()
        task.add(calculate)
        task.add(budget)
        task.add(email)

        result = task.execute(simulacion)
        if result:
            simulacion.estado = "finalizado"
            simulacion.fecha_finalizacion = datetime.now()
            PresupuestoService.create(simulacion.presupuesto)
            SimulacionService.create(simulacion)
        else:
            simulacion.estado = "error"
            simulacion.fecha_finalizacion = datetime.now()
        return result
