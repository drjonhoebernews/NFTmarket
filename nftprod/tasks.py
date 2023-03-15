import requests
from django_rq import job
from .models import Currency

@job
def update_currencies():
    currencies = Currency.objects.filter(is_active=True)
    for currency in currencies:
        try:
            response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={currency.name.lower()}&vs_currencies=usd,eur,try')
            prices = response.json()[currency.name.lower()]
            currency.usd_value = prices['usd']
            currency.eur_value = prices['eur']
            currency.try_value = prices['try']
            currency.save()
        except Exception as e:
            print(f'Error updating {currency.name}: {e}')
