from django.db import models
from django.contrib.auth.models import User


# extra information attached to every user account
# role is either buyer or seller
class Profile(models.Model):
    ROLE_CHOICES = [
        ('buyer',  'Buyer'),
        ('seller', 'Seller'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')

    def __str__(self):
        return self.user.username + ' as ' + self.role


# product category like Electronics or Furniture
# parent is null for top level categories like Electronics
# parent points to another category for sub categories like Phones under Electronics
class Category(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    parent      = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subcategories'
    )

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        # show parent name before child name so admin lists are easy to read
        if self.parent:
            return self.parent.name + ' > ' + self.name
        return self.name

    def is_top_level(self):
        # returns True if this category has no parent
        return self.parent is None


# a product that is listed for sale on the site
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


# extra images attached to a product listing
# the first image uploaded is considered the cover image
# is_cover is set to True on the first image and False on the rest
class ProductImage(models.Model):
    product  = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image    = models.ImageField(upload_to='products/')
    is_cover = models.BooleanField(default=False)
    order    = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return 'Image for ' + self.product.name


# a star rating and comment left by a logged in user on a product
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    rating  = models.IntegerField(default=5)
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.user.username + ' reviewed ' + self.product.name


# one item sitting in a users cart before checkout
class CartItem(models.Model):
    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.name + ' x' + str(self.quantity)


# a product saved to a users wishlist
class WishlistItem(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' saved ' + self.product.name


# a completed simulated purchase saved after checkout
# one row is created for each cart item at the time of checkout
class Order(models.Model):
    buyer       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product     = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    quantity    = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.buyer.username + ' bought ' + self.product.name


# tracks which discount codes a user has already redeemed
# the unique together rule stops the same code being used twice by one account
class UsedCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=50)

    class Meta:
        unique_together = ('user', 'code')

    def __str__(self):
        return self.user.username + ' used ' + self.code


# stores the last 10 products a logged in user has visited
# each time they open a product page we update or create a row for that product
class RecentlyViewed(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recently_viewed')
    product    = models.ForeignKey(Product, on_delete=models.CASCADE)
    viewed_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-viewed_at']

    def __str__(self):
        return self.user.username + ' viewed ' + self.product.name
