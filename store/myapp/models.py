from django.db import models

# Create your models here.


class Product(models.Model):
    CAT=((1,"Protein"),(2,"Gainer"),(3,"Creatine"),(4,"BCAA"),(5,"EAA"),(6,"Fish Oil"),(7,"Pre-Workout"),(8,"Peanut-Butter"),(9,"Oats"),(10,"Muesli"),(11,"Muesli"),(12,"Shaker"),(13,"Sandbag"),(14,"Weightlifting Belt"),(15,"Hand-Glooves"))
    pname=models.CharField(max_length=50,verbose_name="Product Name")
    price1=models.FloatField(default=0.0)
    price=models.FloatField()
    seller=models.CharField(max_length=50,verbose_name="seller", default="Default Name") 
    category=models.IntegerField(choices=CAT ,verbose_name="Category")
    description=models.CharField(max_length=300 , verbose_name="Details")
    is_active=models.BooleanField(default=True, verbose_name="Is_Available")
    pimage=models.ImageField(upload_to='image')
    pimage1=models.ImageField(upload_to='image', default='default.jpg')
    pimage2=models.ImageField(upload_to='image', default='default.jpg')


    def __str__(self):
        return self.pname
    

    def discount_percentage(self):
        if self.price1 > 0:
            return round(((self.price1 - self.price) / self.price1) * 100, 2)
        return 0
   
        

class cart(models.Model):
    userid=models.ForeignKey('auth.User',on_delete=models.CASCADE,db_column='userid')
    pid=models.ForeignKey('Product',on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)

  




class Address(models.Model):
    user_id=models.ForeignKey("auth.User",on_delete=models.CASCADE, db_column="user_id")
    address=models.CharField(max_length=200)
    fullname=models.CharField(max_length=40)
    city=models.CharField(max_length=30)
    pincode=models.CharField(max_length=10)
    state=models.CharField(max_length=30)
    mobile=models.CharField(max_length=10)



class Order(models.Model):
    order_id=models.CharField(max_length=50)
    user_id=models.ForeignKey("auth.User",on_delete=models.CASCADE, db_column="user_id")
    p_id=models.ForeignKey("Product",on_delete=models.CASCADE,db_column="p_id")
    qty=models.IntegerField(default=1)
    amt=models.FloatField()  
    payment_status=models.CharField(max_length=30,default='unpaid')




class BMIRecord(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    height = models.FloatField(help_text="Height in cm")
    weight = models.FloatField(help_text="Weight in kg")
    bmi = models.FloatField()
    category = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Guest'} - BMI: {self.bmi:.2f}"
