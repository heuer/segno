from django.db import models


class Ticket(models.Model):
    """Example which stores an alphanumeric name and the name as QR code.
    """
    name = models.CharField(max_length=150, unique=True)
    qrcode = models.ImageField(upload_to='ticket-qrcodes/')
