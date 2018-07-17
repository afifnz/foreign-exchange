from django.conf.urls import url
from . import views


urlpatterns = (
    url(
        r'^currency/$',
        views.CurrencyList.as_view()),
    url(
        r'^currency/add/$',
        views.CurrencyAdd.as_view()),
    url(
        r'^currency/(?P<pk>\d+)/update/$',
        views.CurrencyUpdate.as_view()),
    url(
        r'^currency/(?P<pk>\d+)/delete/$',
        views.CurrencyDelete.as_view()),

    url(
        r'^exchange/add/$',
        views.ExchangeAdd.as_view()),
    url(
        r'^exchange/(?P<pk>\d+)/delete/$',
        views.ExchangeDelete.as_view()),
    url(
        r'^rate/add/$',
        views.RateAdd.as_view()),
    url(
        r'^rate-trace/$',
        views.RateTrace.as_view()),
)
