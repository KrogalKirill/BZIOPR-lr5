namespace MonteCarloDecisionMaking.Models;

/// <summary>
/// Результат моделирования для конкретного процента контроля.
/// </summary>
public sealed record SimulationResult(
    int InspectionPercent,
    double SimulatedCost,
    double TheoreticalCost
);