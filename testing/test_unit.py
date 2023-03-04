# Імпортувати бібліотеку unittest та нашу функцію
import unittest
from prime import is_prime

# Клас, що містить всі наші тести 
class Tests(unittest.TestCase):
    # Назви функцій починаються з test_, для автоматичного запуску функцій за викликом unittest.main().
    def test_1(self):
        """Перевірити, чи 1 не просте число."""
        self.assertFalse(is_prime(1))
    # Кожен тест приймає аргумент self, що є звичайним при написанні методів у класах Python.
    def test_2(self):
        """Перевірити, чи 2 просте число."""
        self.assertTrue(is_prime(2))

    def test_8(self):
        # Містить docstring, або ж рядок документації. Коли ми запустимо тести, коментар буде показаний як опис тесту в разі його невдачі.
        """Перевірити, що 8 не просте число."""
        self.assertFalse(is_prime(8))

    def test_11(self):
        """Перевірити, що 11 просте число."""
        # Наступний рядок кожної функції містив припущення у формі self.assertSOMETHING. 
        self.assertTrue(is_prime(11))

    def test_25(self):
        """Перевірити, що 25 не просте число."""
        self.assertFalse(is_prime(25))

    def test_28(self):
        """Перевірити, що 28 не просте число."""
        self.assertFalse(is_prime(28))


# Запустити кожну функцію тестування 
if __name__ == "__main__":
    unittest.main()