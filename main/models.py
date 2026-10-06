from django.db import models
from django.contrib.auth.models import User


# =====================================================
# FOOD
# =====================================================

class Food(models.Model):

    CATEGORY_CHOICES = [
        ("Pizza", "Pizza"),
        ("Burger", "Burger"),
        ("Biryani", "Biryani"),
        ("Noodles", "Noodles"),
        ("Dessert", "Dessert"),
        ("Drinks", "Drinks"),
        ("Veg", "Veg"),
    ]

    name = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    image = models.ImageField(
        upload_to="food_images/",
        blank=True,
        null=True
    )

    available = models.BooleanField(
        default=True
    )

    show_on_home = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.name


# =====================================================
# CONTACT
# =====================================================

class Contact(models.Model):

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


# =====================================================
# ORDER
# =====================================================

class Order(models.Model):

    PAYMENT_CHOICES = [
        ("COD", "Cash on Delivery"),
        ("ONLINE", "Online Payment"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Preparing", "Preparing"),
        ("Out for Delivery", "Out for Delivery"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]

    # CUSTOMER USER
    customer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders"
    )

    # CUSTOMER DETAILS
    customer_name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=20
    )

    email = models.EmailField()

    address = models.TextField()

    city = models.CharField(
        max_length=100
    )

    pincode = models.CharField(
        max_length=10
    )

    # PAYMENT
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default="COD"
    )

    # PRICE
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    delivery_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    grand_total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # STATUS
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"


# =====================================================
# ORDER ITEM
# =====================================================

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    food = models.ForeignKey(
        Food,
        on_delete=models.SET_NULL,
        null=True
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):

        if self.food:
            food_name = self.food.name
        else:
            food_name = "Deleted Food"

        return f"{food_name} x {self.quantity}"

# Create your models here.
