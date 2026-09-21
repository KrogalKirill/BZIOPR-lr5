namespace MonteCarloDecisionMaking.Models;

/// <summary>
/// Параметры предметной области (Вариант 6).
/// </summary>
/// <param name="DefectRate">Доля брака A (15% = 0.15).</param>
/// <param name="CostInspection">Затраты на входной контроль B (7 руб.).</param>
/// <param name="CostAdjustment">Затраты на подгонку на контроле C (50 руб.).</param>
/// <param name="CostReplacement">Затраты на замену в готовом изделии D (125 руб.).</param>
/// <param name="TrialsPerStep">Число деталей для каждого шага эксперимента (10 000).</param>
public sealed record VariantConfig(
    double DefectRate = 0.15,
    double CostInspection = 7.0,
    double CostAdjustment = 50.0,
    double CostReplacement = 125.0,
    int TrialsPerStep = 10000
);