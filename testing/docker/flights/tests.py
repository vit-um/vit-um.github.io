from django.test import TestCase, Client
from .models import Flight, Airport, Passenger
from django.db.models import Max 

# Create your tests here.
class FlightTestCase(TestCase):

    def setUp(self):

        # Створити аеропорти.
        a1 = Airport.objects.create(code="AAA", city="City A")
        a2 = Airport.objects.create(code="BBB", city="City B")

        # Створити рейси.
        Flight.objects.create(origin=a1, destination=a2, duration=100)
        Flight.objects.create(origin=a1, destination=a1, duration=200)
        Flight.objects.create(origin=a1, destination=a2, duration=-100)
    
    # Перевіримо кількість вильотів та прильотів з аеропорту AAA. Згідно наших записів в БД їх має бути 3 та 1 відповідно:       
    def test_departures_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.departures.count(), 3)

    def test_arrivals_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.arrivals.count(), 1)
        
    # Ми також можемо перевірити функцію is_valid_flight, яку ми додали до нашої моделі Flight. Почнемо з твердження, що функція повертає True, коли політ дійсний:

    def test_valid_flight(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=100)
        self.assertTrue(f.is_valid_flight())
    
    # Далі переконаймось, що рейси з недійсними пунктами призначення й тривалостями повертають False:

    def test_invalid_flight_destination(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)
        self.assertFalse(f.is_valid_flight())

    def test_invalid_flight_duration(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=-100)
        self.assertFalse(f.is_valid_flight())
        
        
    # Тестування на боці користувача
    def test_index(self):

        # Налаштувати client для надсилання запитів
        c = Client()

        # Надіслати запит до сторінки index та зберегти відповідь
        response = c.get("/flights/")

        # Переконатись, що код статусу 200
        self.assertEqual(response.status_code, 200)

        # Переконатись, що три рейси повертаються у контексті відповіді 
        self.assertEqual(response.context["flights"].count(), 3)

    # Переконатись, що отримуємо код відповіді 200 для дійсної сторінки рейсу та код відповіді 404 для сторінки рейсу, яка не існує.

    def test_valid_flight_page(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)

    # def test_invalid_flight_page(self):
    #     max_id = Flight.objects.all().aggregate(Max("id"))["id__max"]

    #     c = Client()
    #     response = c.get(f"/flights/{max_id + 1}")
    #     self.assertEqual(response.status_code, 404)
        
    # Нарешті, додаймо кілька тестів, щоб переконатися, що списки пасажирів і не пасажирів згенеровані як слід:

    def test_flight_page_passengers(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Еліс", last="Адамс")
        f.passengers.add(p)

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["passengers"].count(), 1)

    def test_flight_page_non_passengers(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Еліс", last="Адамс")

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["non_passengers"].count(), 1)