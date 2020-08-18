import io
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.base import ContentFile
from django.shortcuts import render
import segno
from .models import Ticket
from .forms import TicketForm


def index(request):
    """Renders the form to create a ticket"""
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            qr = segno.make_qr(name)
            buff = io.BytesIO()
            qr.save(buff, kind='png', scale=3, dark='darkblue')
            ticket = Ticket(name=name)
            ticket.qrcode.save(name + '.png', ContentFile(buff.getvalue()),
                               save=True)
            return HttpResponseRedirect('/thanks/')
    else:
        form = TicketForm()
    return render(request, 'qrcode/example.html', {'form': form})


def thanks(request):
    return HttpResponse('Thanks, a new ticket was created')
