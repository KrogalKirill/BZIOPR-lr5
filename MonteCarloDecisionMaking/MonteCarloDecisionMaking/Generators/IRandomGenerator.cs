namespace MonteCarloDecisionMaking.Generators;

/// <summary>
/// Интерфейс генератора псевдослучайных чисел.
/// </summary>
public interface IRandomGenerator
{
    /// <summary>
    /// Возвращает псевдослучайное вещественное число в полуинтервале [0.0, 1.0).
    /// </summary>
    double NextDouble();
}