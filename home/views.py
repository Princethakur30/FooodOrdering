from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from decimal import Decimal

from .models import Food, Contact, Order, OrderItem


# =========================
# HOME PAGE
# =========================

def home(request):

    foods = Food.objects.filter(
        available=True,
        show_on_home=True
    )

    customer_username = request.session.get(
        "customer_username"
    )

    return render(
        request,
        "home/home.html",
        {
            "foods": foods,
            "customer_username": customer_username
        }
    )


# =========================
# ABOUT PAGE
# =========================

def about(request):

    customer_username = request.session.get(
        "customer_username"
    )

    return render(
        request,
        "home/about.html",
        {
            "customer_username": customer_username
        }
    )


# =========================
# ADD TO CART
# =========================

def add_to_cart(request, food_id):

    cart = request.session.get(
        "cart",
        {}
    )

    food_id = str(food_id)

    if food_id in cart:

        cart[food_id] += 1

    else:

        cart[food_id] = 1

    request.session["cart"] = cart

    return redirect("home")


# =========================
# CART PAGE
# =========================

def cart(request):

    cart = request.session.get(
        "cart",
        {}
    )

    foods = Food.objects.filter(
        id__in=cart.keys()
    )

    cart_items = []

    for food in foods:

        quantity = cart[str(food.id)]

        item_total = (
            food.price * quantity
        )

        delivery_charge = (
            food.delivery_charge
        )

        cart_items.append({

            "food": food,

            "quantity": quantity,

            "total": item_total,

            "delivery_charge": delivery_charge

        })


    # =========================
    # ITEM SUBTOTAL
    # =========================

    grand_total = sum(
        item["total"]
        for item in cart_items
    )


    # =========================
    # TOTAL DELIVERY CHARGES
    # =========================

    total_delivery = sum(
        item["delivery_charge"]
        for item in cart_items
    )


    # =========================
    # FINAL TOTAL
    # =========================

    final_total = (
        grand_total + total_delivery
    )


    customer_username = request.session.get(
        "customer_username"
    )


    return render(
        request,
        "home/cart.html",
        {
            "cart_items": cart_items,

            "grand_total": grand_total,

            "total_delivery": total_delivery,

            "final_total": final_total,

            "customer_username": customer_username
        }
    )


# =========================
# REMOVE ONE ITEM FROM CART
# =========================

def remove_from_cart(request, food_id):

    cart = request.session.get(
        "cart",
        {}
    )

    food_id = str(food_id)

    if food_id in cart:

        if cart[food_id] > 1:

            cart[food_id] -= 1

        else:

            del cart[food_id]

    request.session["cart"] = cart

    return redirect("cart")


# =========================
# FOOD DETAIL
# =========================

def food_detail(request, food_id):

    selected_food = Food.objects.get(
        id=food_id
    )

    related_foods = Food.objects.filter(
        category=selected_food.category,
        available=True
    ).exclude(
        id=selected_food.id
    )

    return render(
        request,
        "home/food_detail.html",
        {
            "selected_food": selected_food,
            "related_foods": related_foods
        }
    )


# =========================
# CONTACT
# =========================

def contact(request):

    if request.method == "POST":

        name = request.POST.get(
            "name"
        )

        email = request.POST.get(
            "email"
        )

        message = request.POST.get(
            "message"
        )


        Contact.objects.create(

            name=name,

            email=email,

            message=message

        )


        return render(
            request,
            "home/contact.html",
            {
                "success": True
            }
        )


    return render(
        request,
        "home/contact.html"
    )


# =========================
# SIGNUP
# =========================

def signup(request):

    if request.method == "POST":

        username = request.POST.get(
            "username"
        )

        email = request.POST.get(
            "email"
        )

        password = request.POST.get(
            "password"
        )


        # Check username

        if User.objects.filter(
            username=username
        ).exists():

            return render(
                request,
                "home/signup.html",
                {
                    "error":
                    "Username already exists."
                }
            )


        # Create customer

        user = User.objects.create_user(

            username=username,

            email=email,

            password=password

        )


        # Save customer information in session

        request.session[
            "customer_id"
        ] = user.id

        request.session[
            "customer_username"
        ] = user.username


        return redirect("home")


    return render(
        request,
        "home/signup.html"
    )


# =========================
# LOGIN
# =========================

def user_login(request):

    if request.method == "POST":

        username = request.POST.get(
            "username"
        )

        password = request.POST.get(
            "password"
        )


        user = authenticate(

            request,

            username=username,

            password=password

        )


        if user is not None:

            # Save logged-in customer ID

            request.session[
                "customer_id"
            ] = user.id

            request.session[
                "customer_username"
            ] = user.username


            return redirect("home")


        return render(
            request,
            "home/login.html",
            {
                "error":
                "Invalid username or password."
            }
        )


    return render(
        request,
        "home/login.html"
    )


# =========================
# LOGOUT
# =========================

def user_logout(request):

    request.session.pop(
        "customer_id",
        None
    )

    request.session.pop(
        "customer_username",
        None
    )

    return redirect("home")


# =========================================================
# CHECKOUT
# =========================================================

# =========================================================
# CHECKOUT
# =========================================================

def checkout(request):

    cart = request.session.get(
        "cart",
        {}
    )

    # If cart is empty
    if not cart:
        return redirect("cart")

    # Get foods from cart
    foods = Food.objects.filter(
        id__in=cart.keys()
    )

    cart_items = []

    subtotal = Decimal("0.00")

    for food in foods:

        quantity = cart[str(food.id)]

        item_total = food.price * quantity

        subtotal += item_total

        cart_items.append({
            "food": food,
            "quantity": quantity,
            "total": item_total
        })

    # =========================
    # DELIVERY CHARGE
    # =========================

    delivery_charge = Decimal("40.00")

    # =========================
    # GRAND TOTAL
    # =========================

    grand_total = subtotal + delivery_charge

    # =====================================================
    # PLACE ORDER
    # =====================================================

    if request.method == "POST":

        # -------------------------
        # CHECK LOGIN
        # -------------------------

        customer_id = request.session.get(
            "customer_id"
        )

        if not customer_id:
            return redirect("login")

        # -------------------------
        # GET CUSTOMER
        # -------------------------

        customer = get_object_or_404(
            User,
            id=customer_id
        )

        # -------------------------
        # GET CHECKOUT DATA
        # -------------------------

        customer_name = request.POST.get(
            "customer_name"
        )

        phone = request.POST.get(
            "phone"
        )

        email = request.POST.get(
            "email"
        )

        address = request.POST.get(
            "address"
        )

        city = request.POST.get(
            "city"
        )

        pincode = request.POST.get(
            "pincode"
        )

        payment_method = request.POST.get(
            "payment_method"
        )

        # =================================================
        # CREATE ORDER
        # =================================================

        order = Order.objects.create(

            customer=customer,

            customer_name=customer_name,

            phone=phone,

            email=email,

            address=address,

            city=city,

            pincode=pincode,

            payment_method=payment_method,

            subtotal=subtotal,

            delivery_charge=delivery_charge,

            grand_total=grand_total

        )

        # =================================================
        # CREATE ORDER ITEMS
        # =================================================

        for item in cart_items:

            OrderItem.objects.create(

                order=order,

                food=item["food"],

                quantity=item["quantity"],

                price=item["food"].price,

                total=item["total"]

            )

        # =================================================
        # EMAIL ITEMS
        # =================================================

        email_items = ""

        for item in cart_items:

            email_items += (
                f"{item['food'].name} "
                f"x {item['quantity']} "
                f"= ₹{item['total']}\n"
            )

        # =================================================
        # SEND ORDER CONFIRMATION EMAIL
        # =================================================

        if email:

            email_subject = (
                f"Foodie - Order Confirmation #{order.id}"
            )

            email_message = f"""
Hello {customer_name},

Thank you for ordering from Foodie! 🎉

Your order has been successfully placed.

--------------------------------
ORDER DETAILS
--------------------------------

Order ID: #{order.id}

Order Status: {order.status}

Payment Method: {payment_method}

Order Date:
{order.created_at.strftime("%d-%m-%Y %I:%M %p")}


--------------------------------
ORDER ITEMS
--------------------------------

{email_items}

--------------------------------
PAYMENT SUMMARY
--------------------------------

Subtotal: ₹{subtotal}

Delivery Charge: ₹{delivery_charge}

Grand Total: ₹{grand_total}


--------------------------------
DELIVERY DETAILS
--------------------------------

Name: {customer_name}

Phone: {phone}

Address: {address}

City: {city}

Pincode: {pincode}


Your order is currently being processed.

You can check your order status from
the "My Orders" section of the Foodie website.

Thank you for choosing Foodie! ❤️

Regards,
Foodie Team
"""

            try:

                send_mail(
                    subject=email_subject,
                    message=email_message,
                    from_email=None,
                    recipient_list=[email],
                    fail_silently=False
                )

                print(
                    f"Order confirmation email sent to {email}"
                )

            except Exception as e:

                print(
                    f"EMAIL ERROR: {e}"
                )

        # =================================================
        # CLEAR CART
        # =================================================

        request.session["cart"] = {}

        request.session.modified = True

        # =================================================
        # ORDER SUCCESS PAGE
        # =================================================

        return render(
            request,
            "home/order_success.html",
            {
                "order": order
            }
        )

    # =====================================================
    # SHOW CHECKOUT PAGE
    # =====================================================

    return render(
        request,
        "home/checkout.html",
        {
            "cart_items": cart_items,

            "subtotal": subtotal,

            "delivery_charge": delivery_charge,

            "grand_total": grand_total
        }
    )

# =========================================================
# MY ORDERS
# =========================================================

def orders(request):

    customer_id = request.session.get(
        "customer_id"
    )

    if not customer_id:
        return redirect("login")

    customer_orders = Order.objects.filter(
        customer_id=customer_id
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "home/orders.html",
        {
            "orders": customer_orders
        }
    )


# =========================================================
# ORDER DETAILS
# =========================================================

def order_detail(request, order_id):

    customer_id = request.session.get(
        "customer_id"
    )

    if not customer_id:
        return redirect("login")

    order = get_object_or_404(
        Order,
        id=order_id,
        customer_id=customer_id
    )

    order_items = order.items.select_related(
        "food"
    )

    return render(
        request,
        "home/order_detail.html",
        {
            "order": order,
            "order_items": order_items
        }
    )


# =========================================================
# CANCEL ORDER
# =========================================================

def cancel_order(request, order_id):

    customer_id = request.session.get(
        "customer_id"
    )

    if not customer_id:
        return redirect("login")

    order = get_object_or_404(
        Order,
        id=order_id,
        customer_id=customer_id
    )

    if request.method == "POST":

        if order.status in [
            "Pending",
            "Confirmed"
        ]:

            order.status = "Cancelled"
            order.save()

    return redirect(
        "order_detail",
        order_id=order.id
    )