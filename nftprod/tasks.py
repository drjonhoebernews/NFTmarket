from background_task import background
from .models import Currency


@background(schedule=60)  # her 60 saniyede bir çalışacak şekilde ayarla
def update_currency_rates():
    Currency.update_currency_rates()
