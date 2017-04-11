from django.db import models
from django.forms import ModelForm, TextInput, Select, HiddenInput, Textarea

class Article(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    sold = models.IntegerField(default=0)
    description = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='products', default='products/none.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class About(models.Model):
    description = models.TextField()

class City(models.Model):
    name = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    delivery_price = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProductOrder(models.Model):
    name = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    email = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    status = models.IntegerField(default=0) #0 = unpaid, 1 = paid, 2 = history
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProductOrderForm(ModelForm):
    class Meta:
        model = ProductOrder
        fields = ['product', 'name', 'city', 'email', 'phone_number', 'address']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'product': HiddenInput(),
            'city': Select(attrs={'class': 'form-control'}),
            'address': TextInput(attrs={'class': 'form-control'}),
            'email': TextInput(attrs={'class': 'form-control'}),
            'phone_number': TextInput(attrs={'class': 'form-control'}),
        }

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'description']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control', 'rows': '20', 'placeholder' : 'Fill a description...'}),
        }

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'quantity', 'description', 'photo']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'price': TextInput(attrs={'class': 'form-control'}),
            'quantity': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'})
        }
