from django.contrib import admin
from .models import Transaction, PettyCash, Bill, Sale, CalendarEvent

# Register your models here.
admin.site.register(Transaction)
admin.site.register(PettyCash)
admin.site.register(Bill)
admin.site.register(Sale)
admin.site.register(CalendarEvent)