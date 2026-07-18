from django.test import TestCase
from .calculators import calculate_economic_optimization

class EconomicOptimizationTests(TestCase):
    def test_standard_optimization(self):
        # a=150, b=0.1, c=30, d=0.05, F=1000
        # q* = (150 - 30) / (2 * (0.1 + 0.05)) = 120 / 0.3 = 400
        res = calculate_economic_optimization(a=150.0, b=0.1, c=30.0, d=0.05, F=1000.0)
        self.assertTrue(res['is_valid'])
        self.assertEqual(res['optimal_q'], 400.0)
        self.assertEqual(res['optimal_price'], 110.0) # 150 - 0.1 * 400 = 110
        self.assertEqual(res['revenue_at_opt'], 44000.0) # 400 * 110 = 44000
        self.assertEqual(res['cost_at_opt'], 21000.0) # 1000 + 30*400 + 0.05*(400^2) = 1000 + 12000 + 8000 = 21000
        self.assertEqual(res['max_profit'], 23000.0) # 44000 - 21000 = 23000

    def test_non_profitable_market(self):
        # Precio de reserva menor al costo variable base: a=20, c=30
        res = calculate_economic_optimization(a=20.0, b=0.1, c=30.0, d=0.05, F=500.0)
        self.assertEqual(res['optimal_q'], 0.0)
        self.assertEqual(res['max_profit'], -500.0) # Solo se pierde el costo fijo

    def test_capacity_limitation(self):
        # q* teórico = 400, pero capacidad máxima = 200
        res = calculate_economic_optimization(a=150.0, b=0.1, c=30.0, d=0.05, F=1000.0, max_capacity=200)
        self.assertEqual(res['optimal_q'], 200.0)
        self.assertIn("supera la capacidad máxima operativa", res['message'])

    def test_invalid_coefficients(self):
        # b + d = 0 (Evita división por cero)
        res = calculate_economic_optimization(a=100.0, b=0.0, c=20.0, d=0.0, F=100.0)
        self.assertFalse(res['is_valid'])
        self.assertEqual(res['optimal_q'], 0.0)

