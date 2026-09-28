"""Модуль имитационного моделирования методом Монте-Карло."""

from typing import List
from src.models import VariantConfig, SimulationRow
from src.lfsr import LFSR32Generator


class MonteCarloOptimizer:
    @staticmethod
    def run(config: VariantConfig, rng: LFSR32Generator, step: int = 5) -> List[SimulationRow]:
        raw_results = []

        for p_int in range(0, 101, step):
            p = p_int / 100.0
            total_sim_cost = 0.0

            for _ in range(config.trials_per_step):
                r1 = rng.next_double()
                r2 = rng.next_double()

                if r1 < p:
                    total_sim_cost += config.cost_inspection
                    if r2 < config.defect_rate:
                        total_sim_cost += config.cost_adjustment
                else:
                    if r2 < config.defect_rate:
                        total_sim_cost += config.cost_replacement

            expected_cost_per_item = (
                (p * config.cost_inspection)
                + (p * config.defect_rate * config.cost_adjustment)
                + ((1.0 - p) * config.defect_rate * config.cost_replacement)
            )
            theoretical_cost = expected_cost_per_item * config.trials_per_step
            delta = abs(total_sim_cost - theoretical_cost)

            raw_results.append({
                "percent": p_int,
                "simulated_cost": total_sim_cost,
                "theoretical_cost": theoretical_cost,
                "delta_cost": delta,
            })

        min_cost = min(item["simulated_cost"] for item in raw_results)

        results: List[SimulationRow] = []
        for item in raw_results:
            is_optimal = item["simulated_cost"] == min_cost
            results.append(SimulationRow(
                percent=item["percent"],
                simulated_cost=item["simulated_cost"],
                theoretical_cost=item["theoretical_cost"],
                delta_cost=item["delta_cost"],
                is_optimal=is_optimal,
            ))

        return results