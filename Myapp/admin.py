from django.contrib import admin

from .models import *



admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Bureau)
admin.site.register(DeliveryNote)
admin.site.register(DeliveryNoteItem)
admin.site.register(UserProfile)

admin.site.register(CashOut)
admin.site.register(CashOutDetail),
admin.site.register(PDFDocument)