using MonteCarloDecisionMaking.Models;

namespace MonteCarloDecisionMaking.Services;

/// <summary>
/// Сервис вывода результатов и рекомендаций для лица, принимающего решения.
/// </summary>
public static class DecisionSupportReporter
{
    public static void PrintReport(IReadOnlyList<SimulationResult> results)
    {
        ArgumentNullException.ThrowIfNull(results);

        Console.WriteLine(new string('=', 76));
        Console.WriteLine(" РЕЗУЛЬТАТЫ МОДЕЛИРОВАНИЯ МЕТОДОМ МОНТЕ-КАРЛО (ВАРИАНТ 6)");
        Console.WriteLine(new string('=', 76));
        Console.WriteLine($"{"Контроль (%)",-15} | {"Затраты (Монте-Карло)",-25} | {"Теория (мат. ожидание)",-25}");
        Console.WriteLine(new string('-', 76));

        SimulationResult best = results.MinBy(r => r.SimulatedCost)!;

        foreach (var res in results)
        {
            string marker = res.InspectionPercent == best.InspectionPercent ? " <-- ОПТИМУМ" : string.Empty;
            Console.WriteLine(
                $"{res.InspectionPercent,10} %     | " +
                $"{res.SimulatedCost,20:F2} руб. | " +
                $"{res.TheoreticalCost,20:F2} руб.{marker}"
            );
        }

        Console.WriteLine(new string('=', 76));
        Console.WriteLine(" ВЫВОД И РЕКОМЕНДАЦИЯ ДЛЯ ПРИНЯТИЯ РЕШЕНИЙ:");
        Console.WriteLine($"  * Оптимальная стратегия: входной контроль {best.InspectionPercent}% резисторов.");
        Console.WriteLine($"  * Минимальные затраты: {best.SimulatedCost:F2} руб.");

        double initialCost = results[0].SimulatedCost;
        double economicGain = initialCost - best.SimulatedCost;

        if (economicGain > 0)
        {
            Console.WriteLine($"  * Экономический эффект (экономия) по сравнению с 0% контроля: {economicGain:F2} руб.");
        }
        else
        {
            Console.WriteLine("  * Входной контроль экономически невыгоден: минимальные издержки при 0% контроля.");
        }
        Console.WriteLine(new string('=', 76));
    }
}