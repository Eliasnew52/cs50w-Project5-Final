from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.utils.html import format_html



#User Model

class User_Credentials(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)

# Art Model
class Art(models.Model):
    Owner_ID = models.ForeignKey(User_Credentials, on_delete=models.CASCADE, related_name='arts')
    Creation_Date = models.DateTimeField(auto_now_add=True)
    title = models.TextField(max_length=100 ,default="Untitled")
    Description = models.TextField(max_length=500)
    image = CloudinaryField('image')

    def __str__(self) -> str:
        return self.title
    
# Tag List Model

class Tag_List(models.Model):
    Tag_ID = models.AutoField(primary_key=True)
    Tag_Name = models.TextField(max_length=30, unique=True)

    def __str__(self) -> str:
        return self.Tag_Name


#Art Tags Model

class Art_Tags(models.Model):
    Tag1 = models.ForeignKey(Tag_List,on_delete=models.CASCADE, related_name='Tag1', default='No Tag')
    Tag2 = models.ForeignKey(Tag_List,on_delete=models.CASCADE, related_name='Tag2',default='No Tag')
    Tag3 = models.ForeignKey(Tag_List,on_delete=models.CASCADE, related_name='Tag3',default='No Tag')
    arts_id = models.ForeignKey(Art, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.arts_id.title)

# User Info Model

class User_Info(models.Model):
    First_Name = models.TextField(max_length=20)
    Last_Name = models.TextField(max_length=20)
    About_Me = models.TextField(max_length=500)
    User_ID = models.OneToOneField(User_Credentials, on_delete=models.CASCADE, related_name='info')

    def __str__(self):
        return f"{self.User_ID.username}'s Info"

# User Social Media Model   
class User_Social(models.Model):
    Whatsapp = models.IntegerField(default='No Available')
    Facebook = models.TextField(max_length=500, default='No Available')
    Instagram = models.TextField(max_length=500, default='No Available')
    Social_Owner = models.OneToOneField(User_Credentials, on_delete=models.CASCADE, related_name='social')

    #Function to Return Href Content = Redirects to Whatsapp Chat
    def whatsapp_link(self):
        return format_html("https://wa.me/{}",self.Whatsapp)


    def __str__(self):
        return f"{self.Social_Owner.username}'s Socials"

    # Art Rating Model
class Art_Rating(models.Model):
    Rating = models.PositiveBigIntegerField([MaxValueValidator(5), MinValueValidator(1)])
    Art_ID = models.ForeignKey(Art, on_delete=models.CASCADE, related_name='image_id')
    Reviewer_ID = models.ForeignKey(User_Credentials, on_delete=models.CASCADE, related_name='reviewer')


# Deals Model

class Deal(models.Model):
    buyer = models.ForeignKey(User_Credentials, on_delete=models.CASCADE, related_name='buyer')
    seller = models.ForeignKey(User_Credentials, on_delete=models.CASCADE, related_name='seller')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=50, blank=True, null=True)
    Message = models.TextField(max_length=500, default="Nothing")
    status = models.CharField(max_length=20, default='Pending')
    timestamp = models.DateTimeField(auto_now_add=True)
        