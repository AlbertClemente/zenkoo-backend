import uuid
from django.db import models

class Cripto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10, unique=True)
    """
    Para evitar fallos de conversión entre el API de CoinGecko y Django, debemos cambiar el price:
    
    issue: Si tienes por ejemplo max_digits=10 y un número como 76241 con decimal_places=8, Django no puede representarlo 
    (porque ocuparía 13 dígitos).
    """
    # price = models.DecimalField(max_digits=10, decimal_places=8)
    price = models.DecimalField(max_digits=20, decimal_places=8)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.symbol})"