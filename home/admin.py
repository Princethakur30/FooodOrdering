from django.contrib import admin
from .models import Food, Contact, Order, OrderItem


# =========================
# FOOD ADMIN
# =========================

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "price",
        "category",
        "available",
        "show_on_home",
    )

    list_filter = (
        "category",
        "available",
        "show_on_home",
    )

    search_fields = (
        "name",
        "description",
    )


# =========================
# CONTACT ADMIN
# =========================

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "email",
        "message",
        "created_at",
    )

    search_fields = (
        "name",
        "email",
        "message",
    )

    ordering = (
        "-created_at",
    )


# =========================
# ORDER ADMIN
# =========================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    # What will be shown in the Orders list
    list_display = (
        "id",
        "customer_name",
        "phone",
        "grand_total",
        "payment_method",
        "status",
        "order_date",
    )

    # Status will be a dropdown for EVERY order
    list_editable = (
        "status",
    )

    # Filters on the right side
    list_filter = (
        "status",
        "payment_method",
        "created_at",
    )

    # Search box
    search_fields = (
        "customer_name",
        "phone",
        "email",
    )

    # Newest orders first
    ordering = (
        "-created_at",
    )

    # Show date + month + year + time
    @admin.display(
        description="Created At",
        ordering="created_at"
    )
    def order_date(self, obj):
        return obj.created_at.strftime(
            "%d-%m-%Y %I:%M %p"
        )


# =========================
# ORDER ITEM ADMIN
# =========================

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order",
        "food",
        "quantity",
        "price",
        "total",
    )

    search_fields = (
        "food__name",
    )

    list_filter = (
        "food",
    )