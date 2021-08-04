from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from store.models.product import Product
from store.models.customer import Customer
from django.views import View


# CLASS FOR RENDRING THE LOG IN PAGE
class Login(View):

    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, 'login.htm')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id

                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('/')
            else:
                error_message = "Email or Password is Invalid !!"

        else:
            error_message = "Email or Password is Invalid !!"
        print(email + '\n' + password)
        return render(request, 'login.htm', {'error': error_message})


# FUNCTION FOR LOG OUT
def logout(request):
    request.session.clear()
    return redirect('login')
