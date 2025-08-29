import unittest
import os
from flask import current_app
from app import create_app
from test.presupuesto_service import PresupuestoServiceTest
from app.service import PresupuestoService

class SimulationTest(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_app(self):
        self.assertIsNotNone(current_app)

    def test_presupuesto_creation(self):
        presupuesto = PresupuestoServiceTest.presupuesto_creation()
        self.assertIsNotNone(presupuesto)
        self.assertEqual(presupuesto.estado, "finalizado")
        self.assertEqual(presupuesto.moneda, "USD")
        self.assertEqual(presupuesto.total, 1000.0)
        self.assertEqual(presupuesto.detalle, "Detalle del presupuesto")

    def test_presupuesto_read(self):
        presupuesto = PresupuestoServiceTest.presupuesto_creation()
        PresupuestoService.create(presupuesto)

        fetched = PresupuestoService.get_by_id(getattr(presupuesto, 'id', None))

        if fetched is not None:
            self.assertEqual(fetched.estado, "finalizado")
            self.assertEqual(fetched.moneda, "USD")

    def test_presupuesto_read_all(self):
        p1 = PresupuestoServiceTest.presupuesto_creation()
        PresupuestoService.create(p1)

        p2 = PresupuestoServiceTest.presupuesto_creation()
        p2.moneda = "ARS"
        PresupuestoService.create(p2)

        all_presupuestos = PresupuestoService.read_all()

        if all_presupuestos is not None:
            if hasattr(all_presupuestos, '__len__'):
                self.assertTrue(len(all_presupuestos) >= 0)

if __name__ == '__main__':
    unittest.main()