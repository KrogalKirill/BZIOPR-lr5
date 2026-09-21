using System.Numerics;

namespace MonteCarloDecisionMaking.Generators;

/// <summary>
/// 32-битный регистр сдвига с линейной обратной связью (LFSR).
/// Полином №15:
/// X^32 + X^30 + X^27 + X^26 + X^25 + X^23 + X^22 + X^21 + X^20 +
/// X^19 + X^18 + X^17 + X^13 + X^6 + X^5 + X^4 + 1
/// </summary>
public sealed class LFSR32Generator : IRandomGenerator
{
    // Отводы полинома (taps): степени от 4 до 30 (старшая 32 и младшая 0 учитываются отдельно)
    private static readonly int[] Taps = [30, 27, 26, 25, 23, 22, 21, 20, 19, 18, 17, 13, 6, 5, 4];

    private readonly uint _mask;
    private uint _state;

    public LFSR32Generator(uint seed = 0xACE1ACE1)
    {
        if (seed == 0)
        {
            throw new ArgumentException("Начальное состояние LFSR не может быть нулем.", nameof(seed));
        }

        _state = seed;
        _mask = CalculateFeedbackMask();
    }

    private static uint CalculateFeedbackMask()
    {
        uint mask = 1u << 31; // 32-й бит
        foreach (int tap in Taps)
        {
            mask |= 1u << (tap - 1);
        }
        return mask;
    }

    public uint NextUInt32()
    {
        // Вычисление бита обратной связи через чётность единичных битов (XOR)
        uint feedback = _state & _mask;
        uint bit = (uint)(BitOperations.PopCount(feedback) % 2);

        // Сдвиг вправо и запись вычисленного бита в старший разряд
        _state = (_state >> 1) | (bit << 31);
        return _state;
    }

    public double NextDouble()
    {
        // Нормализация 32-битного беззнакового целого в диапазон [0.0, 1.0)
        return NextUInt32() / 4294967296.0;
    }
}