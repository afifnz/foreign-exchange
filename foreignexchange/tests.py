from django.test import TestCase, Client
from . import models


class ExchangeTest(TestCase):

    def setUp(self):
        self.client = Client()

        # initial setup add currency master data
        models.Currency.objects.create(
            currency_code='USD', description='United states currency')
        models.Currency.objects.create(
            currency_code='IDR', description='Indonesia states currency')
        models.Currency.objects.create(
            currency_code='JPY', description='Japan currency')

    def test_exchange_add_and_delete(self):
        data = {
            'from_currency': 'IDR',
            'to_currency': 'USD'}

        # test as success add
        response = self.client.post(
            '/foreignexchange/exchange/', data)
        self.assertEqual(response.status_code, 200)

        # test as error, with data already exists
        response = self.client.post(
            '/foreignexchange/exchange/', data)
        self.assertEqual(response.status_code, 400)

        data = {
            'from_currency': 'IDR',
            'to_currency': 'IDR'}

        # test as error, with same from_input and to_input
        response = self.client.post(
            '/foreignexchange/exchange/', data)
        self.assertEqual(response.status_code, 400)

        # test delete exchange rate
        objek = models.Exchange.objects.get()
        url = '/foreignexchange/exchange/%s/' % objek.pk

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        queryset = models.Exchange.objects.filter(pk=objek.pk)
        self.assertEqual(queryset.exists(), False)


class RateTest(TestCase):

    def setUp(self):
        self.client = Client()

        # create initial data of currency
        models.Currency.objects.create(
            currency_code='USD', description='United states currency')
        models.Currency.objects.create(
            currency_code='IDR', description='Indonesia states currency')
        models.Currency.objects.create(
            currency_code='JPY', description='Japan currency')

        # create initial data of exchange rate
        data = {
            'from_currency': 'USD',
            'to_currency': 'IDR'}
        self.client.post(
            '/foreignexchange/exchange/', data)

        self.usd_idr = models.Exchange.objects.get(
            from_currency__currency_code='USD',
            to_currency__currency_code='IDR')

        data = {
            'from_currency': 'JPY',
            'to_currency': 'USD'}
        self.client.post(
            '/foreignexchange/exchange/', data)

        self.jpy_usd = models.Exchange.objects.get(
            from_currency__currency_code='JPY',
            to_currency__currency_code='USD')

    def test_rate_add(self):
        data = {
            'from_currency': 'USD',
            'to_currency': 'IDR',
            'rate': 14366.75
        }

        # test success, add daily rate
        response = self.client.post(
            '/foreignexchange/rate/', data)
        self.assertEqual(response.status_code, 200)

        # test error, can only add an rate in a day
        response = self.client.post(
            '/foreignexchange/rate/', data)
        self.assertEqual(response.status_code, 400)

        data = {
            'from_currency': 'USD',
            'to_currency': 'JPY',
            'rate': 112.37
        }

        # test error, the currency not yet added to exchange rate list
        response = self.client.post(
            '/foreignexchange/rate/', data)
        self.assertEqual(response.status_code, 400)

    def test_rate_trace(self):
        # create example daily rate data
        models.Rate.objects.create(
            exchange=self.usd_idr, rate=14299.89, date='2018-07-20')

        models.Rate.objects.create(
            exchange=self.usd_idr, rate=14366.75, date='2018-07-17')

        models.Rate.objects.create(
            exchange=self.jpy_usd, rate=112.75, date='2018-07-13')

        # enter date format like:
        # 2018-07-20 , 07/20/2018 , 07/20/18
        data = {
            'date': '2018-07-20',
        }
        response = self.client.post(
            '/foreignexchange/rate-trace/', data)
        self.assertEqual(response.status_code, 200)

        result = response.json().get('result')

        for objek in result:
            from_currency = objek.get('from')
            to_currency = objek.get('to')

            if from_currency == 'USD' and to_currency == 'IDR':
                # test last rate data in 7 days
                rate = objek.get('rate')
                self.assertEqual(rate, 14299.89)

                # test averge rate data in 7 days
                avg_rate = objek.get('avg_rate')
                self.assertEqual(avg_rate, (14299.89+14366.75)/2)

            if from_currency == 'JPY' and to_currency == 'USD':

                # result insufficient data, because no rate data in 7 days
                rate = objek.get('rate')
                self.assertEqual(rate, 'insufficient data')


class CurrencyTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.usd = models.Currency.objects.create(
            currency_code='USD', description='United states currency')

    def test_currency_list(self):

        response = self.client.get('/foreignexchange/currency/')
        self.assertEqual(response.status_code, 200)

    def test_currency_add(self):

        data = {
            'currency_code': 'IDR',
            'description': 'indonesia currency'}

        response = self.client.post(
            '/foreignexchange/currency/add/', data)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            '/foreignexchange/currency/add/', data)
        self.assertEqual(response.status_code, 400)

    def test_currency_update(self):

        data = {
            'currency_code': 'JPY',
            'description': 'Japan currency'}
        url = '/foreignexchange/currency/%s/update/' % self.usd.pk

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        queryset = models.Currency.objects.filter(pk=self.usd.pk)
        objek = queryset.get()
        self.assertEqual(
            objek.currency_code, data.get('currency_code'))

    def test_currency_delete(self):

        url = '/foreignexchange/currency/%s/delete/' % self.usd.pk

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        queryset = models.Currency.objects.filter(pk=self.usd.pk)
        self.assertEqual(queryset.exists(), False)
