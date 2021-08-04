from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from store.models.product import Product
from store.models.customer import Customer
from django.views import View


# Create your views here.

# CLASS FOR RENDRING THE HOME PAGE
class Index(View):
    def get(self, request):
        products = Product.get_all_products()
        cart = request.session.get('cart')
        if not cart:
                request.session['cart'] = {}
        print(f"You are : {request.session.get('email')}")
        return render(request, 'index.htm', {'products': products})

    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart: ', request.session['cart'])

        return redirect('/')
