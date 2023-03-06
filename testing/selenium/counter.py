import os
import pathlib
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By

# Знаходить URI файлу 
def file_uri(filename):
    return pathlib.Path(os.path.abspath(filename)).as_uri()

# Налаштовує веб-драйвер на використання Google chrome
driver = webdriver.Chrome()


# Стандартний вигляд класу тестування
class WebpageTests(unittest.TestCase):

    def test_title(self):
        """Перевірити правильність назви сторінки"""
        driver.get(file_uri("counter.html"))
        self.assertEqual(driver.title, "Обрахунок")

    def test_increase(self):
        """Перевірити, що заголовок оновлено на 1 після одного натискання кнопки збільшення"""
        driver.get(file_uri("counter.html"))
        increase = driver.find_element(By.ID, "increase")
        increase.click()
        self.assertEqual(driver.find_element(By.TAG_NAME,"h1").text, "1")

    def test_decrease(self):
        """Перевірити, що заголовок оновлено на -1 після одного натискання на кнопку зменшення"""
        driver.get(file_uri("counter.html"))
        decrease = driver.find_element(By.ID, "decrease")
        decrease.click()
        self.assertEqual(driver.find_element(By.TAG_NAME,"h1").text, "-1")

    def test_multiple_increase(self):
        """Перевірити, що заголовок оновлено на 3 після трьох натискань на кнопку збільшення"""
        driver.get(file_uri("counter.html"))
        increase = driver.find_element(By.ID, "increase")
        for i in range(5):
            increase.click()
        self.assertEqual(driver.find_element(By.TAG_NAME, "h1").text, "5")

if __name__ == "__main__":
    unittest.main()
    
