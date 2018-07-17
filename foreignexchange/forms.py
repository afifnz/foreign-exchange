import datetime

from django import forms
from . import models


class CurrencyForm(forms.ModelForm):

    class Meta:
        model = models.Currency
        fields = ('currency_code', 'description')


class ExchangeForm(forms.ModelForm):

    class Meta:
        model = models.Exchange
        fields = ('from_currency', 'to_currency')

    def __init__(self, *args, **kwargs):
        super(ExchangeForm, self).__init__(*args, **kwargs)
        self.fields['from_currency'].to_field_name = 'currency_code'
        self.fields['to_currency'].to_field_name = 'currency_code'

    def clean(self):
        from_currency = self.cleaned_data.get('from_currency')
        to_currency = self.cleaned_data.get('to_currency')

        if from_currency == to_currency:
            raise forms.ValidationError(
                'The origin and destination of currency must be different.')
        queryset = self._meta.model.objects.filter(
            from_currency=from_currency, to_currency=to_currency)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise forms.ValidationError(
                'Data with the same exchange rate already exists')

        return self.cleaned_data


class RateForm(forms.Form):

    from_currency = forms.ModelChoiceField(
        required=True,
        queryset=models.Currency.objects.all(),
        to_field_name='currency_code',
    )
    to_currency = forms.ModelChoiceField(
        required=True,
        queryset=models.Currency.objects.all(),
        to_field_name='currency_code',
    )
    rate = forms.FloatField()

    def clean(self):
        from_currency = self.cleaned_data.get('from_currency')
        to_currency = self.cleaned_data.get('to_currency')

        if from_currency == to_currency:
            raise forms.ValidationError(
                'The origin and destination of currency must be different.')

        queryset = models.Exchange.objects.filter(
            from_currency=from_currency, to_currency=to_currency)

        try:
            self.exchange = queryset.get()
        except:
            raise forms.ValidationError(
                'Add %s to %s to the exchange rate list' % (
                    from_currency, to_currency))

        today = datetime.datetime.today()
        queryset = models.Rate.objects.filter(
            date=today, exchange=self.exchange)

        if queryset.exists():
            raise forms.ValidationError(
                'Can only add a data in an exchange rate in a day')

        return self.cleaned_data

    def save(self):
        rate = self.cleaned_data.get('rate')
        date = datetime.date.today()

        objek = models.Rate.objects.create(
            exchange=self.exchange, rate=rate, date=date)
        return objek


class RateTraceForm(forms.Form):

    date = forms.DateField()

    def trace(self):
        date = self.cleaned_data.get('date')
        queryset = models.Exchange.objects.all()
        result = []
        for objek in queryset:
            rate, average = objek.rate(date)
            result.append({
                'from': objek.from_currency.currency_code,
                'to': objek.to_currency.currency_code,
                'rate': rate,
                'avg_rate': average
            })

        return result
