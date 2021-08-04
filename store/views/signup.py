from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from store.models.product import Product
from store.models.customer import Customer
from django.views import View


# CLASS FOR RENDRING THE SIGNUP IN PAGE
class Signup(View):

    def get(self, request):
        return render(request, 'signup.htm')

    def post(self, request):
        post_data = request.POST
        first_name = post_data.get('firstname')
        last_name = post_data.get('lastname')
        phone = post_data.get('phone')
        email = post_data.get('email')
        password = post_data.get('password')

        # FOR VALIDATION

        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            phone=phone,
                            email=email,
                            password=password)

        error_msg = self.validateCustomer(customer)

        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email,
        }

        # saving
        if not error_msg:
            print(first_name, last_name, phone, email, password)

            customer.password = make_password(customer.password)
            customer.register()

            return redirect('/')

        else:
            data = {
                'error': error_msg,
                'values': value,
            }
            return render(request, 'signup.htm', data)

        # METHOD FOR VALIDATING THE CUSTOMER

    def validateCustomer(self, customer):
        error_msg = None

        # FOR FIRST NAME
        if (not customer.first_name):
            error_msg = "First Name Required!!"

        elif len(customer.first_name) < 4:
            error_msg = "First Name must be 4 char long or more"

        # FOR LAST NAME
        elif (not customer.last_name):
            error_msg = "Last Name Required!!"

        elif len(customer.last_name) < 4:
            error_msg = "Last Name must be 4 char long or more"

        # FOR PHONE
        elif (not customer.phone):
            error_msg = "Phone Number Required!!"

        elif len(customer.phone) < 11:
            error_msg = "Phone Number must be 11 char long"

        # FOR PASSWORD
        elif (not customer.password):
            error_msg = "Password Required!!"

        elif len(customer.phone) < 6:
            error_msg = "Password must be 6 char long"

        # FOR EMAIL
        elif len(customer.email) < 5:
            error_msg = "Email must be 5 char long"

        # CHECKING IF EMAIL ALREADY EXISTS IN THE DATABASE
        elif customer.isExists():
            error_msg = 'Email Address Already Registered..'

        return error_msg
