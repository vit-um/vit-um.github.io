import math

def is_prime(n):
    # Ми знаємо, що числа менші за 2, не належать до простих
    if n < 2: 
        return False
    # Перевіряємо дільники до sqrt(n)
    for i in range(2, int(math.sqrt(n))):  # закладена помилка, це взятий на одиницю менший діапазон для перевірки: int(math.sqrt(n) + 1 )
        # Якщо i  - дільник, повернути false
        if n % i == 0:
            return False
    
    # Якщо дільники не знайдені, повернути true
    return True