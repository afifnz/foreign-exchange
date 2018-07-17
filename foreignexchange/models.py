import datetime

from django.db import models


class Currency(models.Model):
    ''' currency table as master of currency data'''

    currency_code = models.CharField(max_length=3, unique=True)
    description = models.TextField()


class Exchange(models.Model):
    ''' exchange table, register foreign exchange data '''

    from_currency = models.ForeignKey(
        'foreignexchange.Currency',
        related_name='from_currency', on_delete=models.CASCADE)
    to_currency = models.ForeignKey(
        'foreignexchange.Currency',
        related_name='to_currency', on_delete=models.CASCADE)

    def rate_in_aweek(self, date):
        ''' select rate data in 7 days'''

        date_from = date - datetime.timedelta(days=6)
        queryset = self.rate_set.filter(
            date__gte=date_from, date__lte=date)
        return queryset

    def rate(self, date):
        queryset = self.rate_in_aweek(date)

        if not queryset.exists():
            rate = 'insufficient data'
            average = None
            return rate, average

        rate = queryset.latest('date').rate

        average = queryset.aggregate(
            models.Avg('rate')).get('rate__avg')

        return rate, average


class Rate(models.Model):
    ''' rate table, to record daily rate data '''

    exchange = models.ForeignKey(
        'foreignexchange.Exchange', on_delete=models.CASCADE)
    rate = models.FloatField()
    date = models.DateField()
