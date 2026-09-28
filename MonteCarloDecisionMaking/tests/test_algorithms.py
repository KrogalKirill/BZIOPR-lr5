"""Автоматические тесты для проверки корректности генератора LFSR и модели Монте-Карло."""

import unittest
from src.models import VariantConfig
from src.lfsr import LFSR32Generator
from src.optimizer import MonteCarloOptimizer


class TestLFSR32Generator(unittest.TestCase):
    """Тестирование генератора LFSR."""

    def test_seed_zero_raises_error(self):
        with self.assertRaises(ValueError):
            LFSR32Generator(seed=0)

    def test_range_of_next_double(self):
        rng = LFSR32Generator(seed=0x12345678)
        for _ in range(5000):
            val = rng.next_double()
            self.assertGreaterEqual(val, 0.0)
            self.assertLess(val, 1.0)

    def test_independence_and_uniformity(self):
        """Проверка равномерности: среднее распределения в [0, 1) должно быть близко к 0.5."""
        rng = LFSR32Generator(seed=0xACE1ACE1)
        samples = [rng.next_double() for _ in range(50000)]
        mean = sum(samples) / len(samples)
        # По закону больших чисел среднее должно быть в пределах 0.50 ± 0.01
        self.assertAlmostEqual(mean, 0.5, delta=0.01)

    def test_correlation_between_consecutive_draws(self):
        """Проверка отсутствия автокорреляции между соседними r1 и r2."""
        rng = LFSR32Generator(seed=0xCAFEBABE)
        # Доля событий, когда оба числа попали в интервал < 0.5 должна быть около 0.25 (0.5 * 0.5)
        n = 20000
        joint_count = 0
        for _ in range(n):
            r1 = rng.next_double()
            r2 = rng.next_double()
            if r1 < 0.5 and r2 < 0.5:
                joint_count += 1
        joint_prob = joint_count / n
        self.assertAlmostEqual(joint_prob, 0.25, delta=0.02)


class TestMonteCarloOptimizer(unittest.TestCase):
    """Тестирование сходимости метода Монте-Карло с аналитической теорией."""

    def setUp(self):
        self.config = VariantConfig(
            defect_rate=0.15,
            cost_inspection=7.0,
            cost_adjustment=50.0,
            cost_replacement=125.0,
            trials_per_step=10000
        )
        self.rng = LFSR32Generator(seed=0x1337BEEF)

    def test_theoretical_formula_monotonicity(self):
        """Тест монотонности функции: для варианта 6 затраты строго убывают при росте контроля."""
        costs = []
        for p in range(0, 101, 10):
            p_val = p / 100.0
            theo = (
                (p_val * self.config.cost_inspection)
                + (p_val * self.config.defect_rate * self.config.cost_adjustment)
                + ((1.0 - p_val) * self.config.defect_rate * self.config.cost_replacement)
            ) * self.config.trials_per_step
            costs.append(theo)

        # Проверка, что каждый следующий шаг строго дешевле предыдущего
        for i in range(len(costs) - 1):
            self.assertGreater(costs[i], costs[i + 1])

    def test_monte_carlo_convergence(self):
        """Тест сходимости: погрешность моделирования не должна превышать 5% от теории."""
        results = MonteCarloOptimizer.run(self.config, self.rng, step=10)

        for row in results:
            relative_error = row.delta_cost / row.theoretical_cost
            self.assertLess(
                relative_error,
                0.05,
                f"На доле {row.percent}% погрешность {relative_error:.3%} превысила допустимые 2%!"
            )

    def test_optimal_decision_is_100_percent(self):
        """Тест выбора оптимума: для Варианта 6 минимум затрат обязан быть на 100% контроля."""
        results = MonteCarloOptimizer.run(self.config, self.rng, step=5)
        optimal_row = next(r for r in results if r.is_optimal)
        self.assertEqual(
            optimal_row.percent,
            100,
            f"Оптимальный процент {optimal_row.percent}%, ожидалось 100%!"
        )


if __name__ == "__main__":
    unittest.main()