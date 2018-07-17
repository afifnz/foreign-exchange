from django.views import generic
from django.http import JsonResponse

from . import forms, models


class ExchangeAdd(generic.FormView):
    ''' add exchange view'''

    http_method_names = (u'post',)
    form_class = forms.ExchangeForm

    def form_valid(self, form):
        self.object = form.save()
        data = {'message': 'add exchange rate success'}
        return JsonResponse(data)

    def form_invalid(self, form):
        data = form.errors
        return JsonResponse(data, status=400)


class ExchangeDelete(generic.DeleteView):
    ''' delete exchange view '''

    model = models.Exchange
    http_method_names = (u'delete')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        data = {'message': 'delete exchange rate success'}
        return JsonResponse(data)


class RateAdd(generic.FormView):
    ''' add daily rate'''

    http_method_names = (u'post')
    form_class = forms.RateForm

    def form_valid(self, form):
        self.object = form.save()
        data = {'message': 'add daily rate success'}
        return JsonResponse(data)

    def form_invalid(self, form):
        data = form.errors
        return JsonResponse(data, status=400)


class RateTrace(generic.FormView):
    ''' Trace avarage rate in 7 days '''

    http_method_names = (u'post',)
    form_class = forms.RateTraceForm

    def form_valid(self, form):
        data = {'result': form.trace()}
        return JsonResponse(data)

    def form_invalid(self, form):
        data = form.errors
        return JsonResponse(data, status=400)


class CurrencyList(generic.ListView):
    ''' currency list view '''

    http_method_names = (u'get',)
    model = models.Currency

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        data = []
        for objek in self.object_list:
            data.append({
                'pk': objek.pk,
                'currency_code': objek.currency_code,
                'description': objek.description
            })

        if data:
            data = {'result': data}
        else:
            data = {'message': 'currency data is empty'}

        return JsonResponse(data)


class CurrencyAdd(generic.CreateView):
    ''' add currency view'''

    http_method_names = (u'post',)
    form_class = forms.CurrencyForm

    def form_valid(self, form):
        self.object = form.save()
        data = {'message': 'add currency success'}
        return JsonResponse(data)

    def form_invalid(self, form):
        data = form.errors
        return JsonResponse(data, status=400)


class CurrencyUpdate(generic.UpdateView):
    ''' update currency view '''

    http_method_names = (u'post', u'put')
    model = models.Currency
    fields = ('currency_code', 'description',)

    def form_valid(self, form):
        self.object = form.save()
        data = {'message': 'update currency success'}
        return JsonResponse(data)

    def form_invalid(self, form):
        data = form.errors
        return JsonResponse(data, status=400)


class CurrencyDelete(generic.DeleteView):
    ''' delete currency view '''

    model = models.Currency

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        data = {'message': 'delete currency success'}
        return JsonResponse(data)
