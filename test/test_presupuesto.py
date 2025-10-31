import os
import unittest
from decimal import Decimal

from flask import current_app

from app import create_app, db
from app.service import PresupuestoService, UsuarioService
from test.presupuesto_service import PresupuestoServiceTest
from test.usuario_service import UsuarioServiceTest


class PresupuestoTest(unittest.TestCase):
    def setUp(self):
        os.environ["FLASK_CONTEXT"] = "testing"
        os.environ["A3500_FALLBACK"] = "1150.50"
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        db.create_all()

        usuario = UsuarioServiceTest.usuario_creation()
        self.usuario = UsuarioService.create(usuario)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app(self):
        self.assertIsNotNone(current_app)

    def test_presupuesto_creation(self):
        presupuesto = PresupuestoServiceTest.presupuesto_creation(self.usuario.id)
        presupuesto = PresupuestoService.create(presupuesto)

        self.assertIsNotNone(presupuesto)
        self.assertGreater(presupuesto.id, 0)
        self.assertEqual(presupuesto.estado, "finalizado")
        self.assertEqual(presupuesto.moneda, "USD")
        self.assertEqual(presupuesto.total, 1000.0)
        self.assertEqual(presupuesto.detalle, "Detalle del presupuesto")

    def test_presupuesto_read(self):
        presupuesto = PresupuestoServiceTest.presupuesto_creation(self.usuario.id)
        presupuesto = PresupuestoService.create(presupuesto)

        fetched = PresupuestoService.get_by_id(presupuesto.id)

        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.estado, "finalizado")
        self.assertEqual(fetched.moneda, "USD")

    def test_presupuesto_read_all(self):
        p1 = PresupuestoServiceTest.presupuesto_creation(self.usuario.id)
        p1 = PresupuestoService.create(p1)

        p2 = PresupuestoServiceTest.presupuesto_creation(self.usuario.id)
        p2.moneda = "ARS"
        p2 = PresupuestoService.create(p2)

        all_presupuestos = PresupuestoService.read_all()

        self.assertIsNotNone(all_presupuestos)
        self.assertGreater(len(all_presupuestos), 0)

    def test_calcular_modo_cif(self):
        articulo = PresupuestoServiceTest.articulo_notebook_cif()

        cif, metadata = PresupuestoService.calcular_cif(articulo)

        self.assertEqual(cif, articulo.valor_usd)
        self.assertEqual(metadata["modo"], "CIF")

    def test_calcular_impuestos_sin_courier(self):
        cif = Decimal("1000.00")
        origen = "US"
        tipo = "celulares"
        es_courier = False

        impuestos = PresupuestoService.calcular_impuestos(
            cif, origen, tipo, es_courier
        )

        self.assertIn("di", impuestos)
        self.assertIn("tasa_est", impuestos)
        self.assertIn("iva", impuestos)
        self.assertIn("percep_iva", impuestos)
        self.assertIn("percep_gan", impuestos)

        self.assertEqual(impuestos["di"], Decimal("80.00"))
        self.assertEqual(impuestos["tasa_est"], Decimal("30.00"))

        base_esperada = cif + impuestos["di"] + impuestos["tasa_est"]
        iva_esperado = PresupuestoService._round(
            base_esperada * Decimal("0.21")
        )
        self.assertEqual(impuestos["iva"], iva_esperado)

    def test_calcular_impuestos_con_courier(self):
        cif = Decimal("1000.00")
        origen = "US"
        tipo = "celulares"
        es_courier = True

        impuestos = PresupuestoService.calcular_impuestos(
            cif, origen, tipo, es_courier
        )

        self.assertEqual(impuestos["di"], Decimal("500.00"))
        self.assertEqual(impuestos["tasa_est"], Decimal("30.00"))

    def test_calcular_completo(self):
        articulo = PresupuestoServiceTest.articulo_celular_fob()

        resultado = PresupuestoService.calcular(articulo)

        self.assertIn("bases", resultado)
        self.assertIn("unitario", resultado)
        self.assertIn("total", resultado)
        self.assertIn("fuentes", resultado)

        self.assertEqual(resultado["bases"]["tipo_producto"], "celulares")
        self.assertEqual(resultado["bases"]["unidades"], 2)

        self.assertIn("cif_usd", resultado["unitario"])
        self.assertIn("impuestos_usd", resultado["unitario"])
        self.assertIn("costo_final_usd", resultado["unitario"])

        self.assertIn("costo_final_usd", resultado["total"])
        self.assertIn("costo_final_ars", resultado["total"])


if __name__ == "__main__":
    unittest.main()
