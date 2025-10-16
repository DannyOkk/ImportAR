import unittest
import os
from flask import current_app
from app import create_app, db
from test.presupuesto_service import PresupuestoServiceTest
from app.service import PresupuestoService

class SimulationTest(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    

    def test_app(self):
        self.assertIsNotNone(current_app)

    def test_presupuesto_creation(self):
        presupuesto = PresupuestoServiceTest.presupuesto_creation()
        presupuesto = PresupuestoService.create(presupuesto)
        self.assertIsNotNone(presupuesto)
        self.assertGreater(presupuesto.id, 0)
        self.assertEqual(presupuesto.estado, "finalizado")
        self.assertEqual(presupuesto.moneda, "USD")
        self.assertEqual(presupuesto.total, 1000.0)
        self.assertEqual(presupuesto.detalle, "Detalle del presupuesto")

    def test_presupuesto_read(self):
        presupuesto = PresupuestoServiceTest.presupuesto_creation()
        presupuesto = PresupuestoService.create(presupuesto)

        fetched = PresupuestoService.get_by_id(presupuesto.id)

        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.estado, "finalizado")
        self.assertEqual(fetched.moneda, "USD")

    def test_presupuesto_read_all(self):
        p1 = PresupuestoServiceTest.presupuesto_creation()
        p1 = PresupuestoService.create(p1)

        p2 = PresupuestoServiceTest.presupuesto_creation()
        p2.moneda = "ARS"
        p2 = PresupuestoService.create(p2)

        all_presupuestos = PresupuestoService.read_all()

        self.assertIsNotNone(all_presupuestos)
        self.assertGreater(len(all_presupuestos), 0)

if __name__ == '__main__':
    unittest.main()