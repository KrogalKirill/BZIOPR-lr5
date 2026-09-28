"""Модуль генератора псевдослучайных чисел на основе 32-битного LFSR."""

from abc import ABC, abstractmethod


class IRandomGenerator(ABC):
    @abstractmethod
    def next_double(self) -> float:
        pass


class LFSR32Generator(IRandomGenerator):
    """32-битный регистр сдвига с линейной обратной связью (LFSR) по полиному №15.

    Полином №15:
    X^32 + X^30 + X^27 + X^26 + X^25 + X^23 + X^22 + X^21 + X^20 +
    X^19 + X^18 + X^17 + X^13 + X^6 + X^5 + X^4 + 1
    """

    TAPS = (30, 27, 26, 25, 23, 22, 21, 20, 19, 18, 17, 13, 6, 5, 4)

    def __init__(self, seed: int = 0xACE1ACE1):
        if seed == 0:
            raise ValueError("Seed LFSR не может быть равен нулю.")
        self.initial_seed = seed & 0xFFFFFFFF
        self._state: int = self.initial_seed
        self._mask: int = self._calculate_mask()

    def reset(self):
        """Сброс состояния регистра к начальному seed."""
        self._state = self.initial_seed

    def _calculate_mask(self) -> int:
        mask = 1 << 31  # Степень 32 (бит 31)
        for tap in self.TAPS:
            mask |= 1 << (tap - 1)
        return mask

    def clock_bit(self) -> int:
        """Один такт LFSR: возвращает 1 выходной бит."""
        feedback = self._state & self._mask
        bit = bin(feedback).count("1") % 2
        out_bit = self._state & 1
        self._state = (self._state >> 1) | (bit << 31)
        return out_bit

    def next_uint32(self) -> int:
        """Генерация полноценного независимого 32-битного числа за 32 такта сдвига."""
        num = 0
        for _ in range(32):
            num = (num << 1) | self.clock_bit()
        return num

    def next_double(self) -> float:
        """Нормализация в полуинтервал [0.0, 1.0)."""
        return self.next_uint32() / 4294967296.0