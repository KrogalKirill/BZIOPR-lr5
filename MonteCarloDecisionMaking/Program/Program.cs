using MonteCarloDecisionMaking.Generators;
using MonteCarloDecisionMaking.Models;
using MonteCarloDecisionMaking.Services;

namespace MonteCarloDecisionMaking;

internal static class Program
{
    private static void Main()
    {
        Console.OutputEncoding = System.Text.Encoding.UTF8;

        // 1. Инициализация параметров предметной области (Вариант 6)
        var config = new VariantConfig();

        // 2. Инициализация генератора ПСЧ (LFSR полином №15)
        IRandomGenerator rng = new LFSR32Generator(seed: 0x1337BEEF);

        // 3. Выполнение имитационного эксперимента
        var optimizer = new MonteCarloOptimizer(config, rng);
        var results = optimizer.RunOptimization(step: 5);

        // 4. Формирование отчета
        DecisionSupportReporter.PrintReport(results);
    }
}