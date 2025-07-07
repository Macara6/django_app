
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User , AbstractUser# type: ignore


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    entrep_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    adress= models.CharField(max_length=40, null=True, blank=True)
    rccm_number= models.CharField(max_length=40)
    impot_number= models.CharField(max_length=255)

    
class Category(models.Model):

    name = models.CharField(max_length=50)
    user_created =  models.ForeignKey(User, on_delete=models.CASCADE)
   

    def __str__(self):
        return self.name

class Product(models.Model):
   name = models.CharField(max_length=50)
   stock = models.PositiveIntegerField(default=0)
   user_created = models.ForeignKey(User, on_delete=models.CASCADE)
   created_at = models.DateTimeField(auto_now_add=True)

   def __str__(self):
       created_at= self.created_at.strftime('%Y-%m-%d %H:%M')
       return f"{self.name} - {created_at}"                                                                                                                                     
   
class Bureau(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class DeliveryNote(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    bureau = models.ForeignKey(Bureau,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f"Bon de livraison #{self.id} - {self.created_at.strftime('%Y-%m-%d')}"
    
    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())
    
class DeliveryNoteItem(models.Model):
        delivery_note = models.ForeignKey(DeliveryNote,related_name='items' ,on_delete=models.CASCADE)
        product= models.ForeignKey(Product, on_delete=models.CASCADE)
        quantity = models.PositiveBigIntegerField()

    
        def __str__(self):
            return f"{self.product.name} x {self.quantity}"        


class CashOut(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now= True)
    motif = models.CharField(max_length=30, default="Aucun motif")
    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    @property
    def total_amount(self):
        return sum(detail.amount for detail in self.details.all())

class CashOutDetail(models.Model):
    cashout = models.ForeignKey(CashOut, related_name='details', on_delete=models.CASCADE)
    reason = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
       return f"{self.reason} - {self.amount}"   


class PDFDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='pdf_documents/')
    created_at = models.DateTimeField(auto_now=True)

    def __srt__(self):
        return f"{self.title}  -  {self.created_at.strftime('%Y-%m-%d %H:%M')}"