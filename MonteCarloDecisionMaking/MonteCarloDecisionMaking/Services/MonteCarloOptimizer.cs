using MonteCarloDecisionMaking.Generators;
using MonteCarloDecisionMaking.Models;

namespace MonteCarloDecisionMaking.Services;

/// <summary>
/// Класс имитационного моделирования методом Монте-Карло.
/// </summary>
public sealed class MonteCarloOptimizer
{
    private readonly VariantConfig _config;
    private readonly IRandomGenerator _rng;

    public MonteCarloOptimizer(VariantConfig config, IRandomGenerator rng)
    {
        _config = config ?? throw new ArgumentNullException(nameof(config));
        _rng = rng ?? throw new ArgumentNullException(nameof(rng));
    }

    /// <summary>
    /// Моделирует совокупные затраты для заданной доли входного контроля.
    /// </summary>
    public double SimulateSingleRate(int inspectionPercent)
    {
        double pInspect = inspectionPercent / 100.0;
        double totalCost = 0.0;

        for (int i = 0; i < _config.TrialsPerStep; i++)
        {
            double r1 = _rng.NextDouble();
            double r2 = _rng.NextDouble();

            if (r1 < pInspect)
            {
                // Деталь поступила на входной контроль
                totalCost += _config.CostInspection;
                if (r2 < _config.DefectRate)
                {
                    // Выявлен брак на этапе контроля -> подгонка
                    totalCost += _config.CostAdjustment;
                }
            }
            else
            {
                // Деталь установлена в изделие без контроля
                if (r2 < _config.DefectRate)
                {
                    // Брак проявился при сборке/тесте изделия -> замена
                    totalCost += _config.CostReplacement;
                }
            }
        }

        return totalCost;
    }

    /// <summary>
    /// Аналитическое вычисление математического ожидания затрат.
    /// </summary>
    public double CalculateTheoreticalCost(int inspectionPercent)
    {
        double p = inspectionPercent / 100.0;
        double expectedUnitCost =
            (p * _config.CostInspection) +
            (p * _config.DefectRate * _config.CostAdjustment) +
            ((1.0 - p) * _config.DefectRate * _config.CostReplacement);

        return expectedUnitCost * _config.TrialsPerStep;
    }

    /// <summary>
    /// Запускает серию симуляций от 0% до 100% с заданным шагом.
    /// </summary>
    public IReadOnlyList<SimulationResult> RunOptimization(int step = 5)
    {
        var results = new List<SimulationResult>();

        for (int percent = 0; percent <= 100; percent += step)
        {
            double simulated = SimulateSingleRate(percent);
            double theoretical = CalculateTheoreticalCost(percent);
            results.Add(new SimulationResult(percent, simulated, theoretical));
        }

        return results.AsReadOnly();
    }
}