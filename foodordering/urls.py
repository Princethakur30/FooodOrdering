from django.contrib import admin
from django.urls import path
from home import views


urlpatterns = [

    # =========================
    # ADMIN
    # =========================

    path(
        "admin/",
        admin.site.urls
    ),


    # =========================
    # HOME
    # =========================

    path(
        "",
        views.home,
        name="home"
    ),


    # =========================
    # ABOUT
    # =========================

    path(
        "about/",
        views.about,
        name="about"
    ),


    # =========================
    # CONTACT
    # =========================

    path(
        "contact/",
        views.contact,
        name="contact"
    ),


    # =========================
    # LOGIN
    # =========================

    path(
        "login/",
        views.user_login,
        name="login"
    ),


    # =========================
    # SIGNUP
    # =========================

    path(
        "signup/",
        views.signup,
        name="signup"
    ),


    # =========================
    # LOGOUT
    # =========================

    path(
        "logout/",
        views.user_logout,
        name="logout"
    ),


    # =========================
    # CART
    # =========================

    path(
        "cart/",
        views.cart,
        name="cart"
    ),


    # =========================
    # ADD TO CART
    # =========================

    path(
        "add-to-cart/<int:food_id>/",
        views.add_to_cart,
        name="add_to_cart"
    ),


    # =========================
    # REMOVE FROM CART
    # =========================

    path(
        "remove-from-cart/<int:food_id>/",
        views.remove_from_cart,
        name="remove_from_cart"
    ),


    # =========================
    # FOOD DETAIL
    # =========================

    path(
        "food/<int:food_id>/",
        views.food_detail,
        name="food_detail"
    ),


    # =========================
    # CHECKOUT
    # =========================

    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),


    # =================================================
    # MY ORDERS
    # =================================================

    path(
        "orders/",
        views.orders,
        name="orders"
    ),


    # =================================================
    # ORDER DETAIL
    # =================================================

    path(
        "orders/<int:order_id>/",
        views.order_detail,
        name="order_detail"
    ),


    # =================================================
    # CANCEL ORDER
    # =================================================

    path(
        "orders/<int:order_id>/cancel/",
        views.cancel_order,
        name="cancel_order"
    ),

]