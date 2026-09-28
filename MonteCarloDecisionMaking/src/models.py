"""Модуль моделей данных предметной области и результатов расчёта."""

from dataclasses import dataclass


@dataclass(frozen=True)
class VariantConfig:
    """Параметры варианта 6:
    A: доля брака (15% = 0.15)
    B: стоимость входного контроля (7 руб.)
    C: стоимость подгонки на контроле (50 руб.)
    D: стоимость замены в готовом изделии (125 руб.)
    trials_per_step: число деталей в партии (10 000 шт.)
    """
    defect_rate: float = 0.15
    cost_inspection: float = 7.0
    cost_adjustment: float = 50.0
    cost_replacement: float = 125.0
    trials_per_step: int = 10000


@dataclass(frozen=True)
class SimulationRow:
    """Строка результата имитационного эксперимента для фиксированного процента контроля."""
    percent: int
    simulated_cost: float
    theoretical_cost: float
    delta_cost: float
    is_optimal: bool = False