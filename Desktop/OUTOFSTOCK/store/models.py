from django.db import models
from django.contrib.auth.models import User


# extra info attached to every user account
class Profile(models.Model):
    ROLE_CHOICES = [
        ('buyer',  'Buyer'),
        ('seller', 'Seller'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')

    def __str__(self):
        return f'{self.user.username} - {self.role}'


# product categories
class Category(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


# a product listing created by a seller or admin
class Product(models.Model):
    owner       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    category    = models.ForeignKey(Category, on_delete=models.CASCADE)
    name        = models.CharField(max_length=150)
    brand       = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    price       = models.DecimalField(max_digits=8, decimal_places=2)
    image       = models.ImageField(upload_to='products/', blank=True, null=True)
    stock       = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


# a review left by a logged-in user on a product
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    rating  = models.IntegerField(default=5)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.username} reviewed {self.product.name}'


# one item sitting in a user's cart
class CartItem(models.Model):
    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'


# a product saved to a user's wishlist
class WishlistItem(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} saved {self.product.name}'


# a completed simulated purchase — one row per cart item at checkout
class Order(models.Model):
    buyer       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product     = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    quantity    = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.buyer.username} bought {self.product.name}'


# tracks which discount codes a user has already redeemed
# this stops a code from being used more than once per account
class UsedCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=50)

    class Meta:
        unique_together = ('user', 'code')

    def __str__(self):
        return f'{self.user.username} used {self.code}'
