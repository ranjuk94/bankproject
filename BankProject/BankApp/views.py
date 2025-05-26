import random
import string
from django.contrib.auth import login,logout
from decimal import Decimal
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from .models import CustomUser
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from .models import Customer, Transaction


def index(request):
    return render(request,'index.html')
def home(request):
    customer = request.user.customer_profile
    return render(request, 'home.html', {
        'account_number': customer.account_number,
        'balance': customer.balance+customer.initial_amount,
        'customer': customer,

    })

def banker_home(request):
    customers = Customer.objects.all()
    active_users_count = Customer.objects.filter(user__is_active=True).count()

    for customer in customers:
        customer.total_balance = customer.balance + customer.initial_amount

    return render(request, 'banker_home.html', {'customers': customers,'active_users_count': active_users_count
    })

def view_users(request):
    query = request.GET.get('search')
    if query:
        # Filter customers by username (case-insensitive search)
        customers = Customer.objects.filter(user__username__icontains=query)
    else:
        customers = Customer.objects.all()

    return render(request, 'view_users.html', {'customers': customers})

def generate_account_number():
    # Generate a random 10-digit account number
    return ''.join(random.choices(string.digits, k=10))


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        name = request.POST.get('name')
        dob = request.POST.get('dob')
        age = request.POST.get('age')
        pan_number = request.POST.get('pan_number')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        aadhar_number = request.POST.get('aadhar_number')
        initial_amount = request.POST.get('initial_amount')
        profile_image = request.FILES.get('profile_image')

        if password != confirm_password:
            return render(request, 'register.html', {'error': 'Passwords do not match.'})

        user = CustomUser(
            username=username,
            email=email,
            is_customer=True
        )
        user.set_password(password)
        user.save()
        account_number = "ACC" + str(user.id)

        customer = Customer(
            user=user,
            name=name,
            email=email,
            account_number=account_number,
            dob=dob,
            age=age,
            pan_number=pan_number,
            address=address,
            phone=phone,
            aadhar_number=aadhar_number,
            initial_amount=initial_amount,
            profile_image=profile_image,
        )
        customer.save()
        login(request, user)
        return redirect('login')
    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_banker:
                return redirect('banker_home')
            elif user.is_customer:
                return redirect('home')
            else:
                return render(request, 'login.html', {'error': 'User role not assigned.'})
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials. Please try again.'})

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def deposit(request):
    if request.method == 'POST':


        amount = Decimal(request.POST.get('amount'))
        branch_name = request.POST.get('branch')

        if amount <= 0:
            return render(request, 'deposit.html', {'error': 'Amount must be positive.'})

        customer = request.user.customer_profile

        bank_name = "PDC Bank"
        ifsc_code = "PDCB0000348"

        customer.balance += amount
        customer.save()

        # Save the transaction details
        Transaction.objects.create(
            customer=customer,
            branch=branch_name,
            amount=amount,
            bank=bank_name,
            ifsc=ifsc_code,
            balance=customer.balance+customer.initial_amount,
            details="Credited"
        )

        return redirect('home')

    customer = request.user.customer_profile
    return render(request, 'deposit.html', {
        'account_number': request.user.customer_profile.account_number,
        'bank': "PDC Bank",
        'account_name': customer.name,
    })

def withdraw(request):
    if request.method == 'POST':

        amount = Decimal(request.POST.get('amount'))
        branch_name = request.POST.get('branch')

        # Validate the deposit amount
        if amount <= 0:
            return render(request, 'withdraw.html', {'error': 'Amount must be positive.'})

        customer = request.user.customer_profile

        bank_name = "PDC Bank"
        ifsc_code = "PDC0000348"

        customer.balance -= amount
        customer.save()

        Transaction.objects.create(
            customer=customer,
            branch=branch_name,
            amount=amount,
            bank=bank_name,
            ifsc=ifsc_code,
            balance=customer.balance+customer.initial_amount,
            details="Debited"
        )

        return redirect('home')

    customer = request.user.customer_profile
    return render(request, 'withdraw.html', {
        'account_number': request.user.customer_profile.account_number,
        'bank': "PDC Bank",
        'account_name': customer.name,
    })

def profile_view(request, user_id):
    # Retrieve the customer profile using the user_id
    customer = get_object_or_404(Customer, user__id=user_id)

    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You are not authorized to view this page.")

    if request.user.is_customer:
        # Customer can only view their own profile
        if request.user.id != user_id:
            return HttpResponseForbidden("You are not authorized to view this page.")
        return render(request, 'profile.html', {'customer': customer})

    if request.user.is_banker:
        # Banker can view any customer's profile
        return render(request, 'banker_profile.html', {'customer': customer})

    return HttpResponseForbidden("You are not authorized to view this page.")


def edit_profile(request):
    customer = get_object_or_404(Customer, user=request.user)

    if request.method == "POST":
        # Update fields from the form
        # customer.name = request.POST.get('name')
        # customer.dob = request.POST.get('dob')
        # customer.dob = request.POST.get('age')
        # customer.aadhar_number = request.POST.get('aadhar_number')
        # customer.pan_number = request.POST.get('pan_number')
        # customer.address = request.POST.get('address')
        # customer.phone = request.POST.get('phone')

        # Update profile image if a new one is uploaded
        if 'profile_image' in request.FILES:
            customer.profile_image = request.FILES['profile_image']

        # Update user email
        user = request.user
        user.email = request.POST.get('email')
        user.save()

        # Save customer changes
        customer.save()
        messages.success(request, "Your profile has been updated successfully!")
        return redirect('profile', user_id=user.id)

    return render(request, 'edit_profile.html', {'customer': customer, 'user': request.user})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Customer, Transaction

# def customer_transaction_history(request, account_number):
    # customer = get_object_or_404(Customer, account_number=account_number)
    #
    # # Fetch transactions, ordered by latest date and time
    # transactions = customer.transactions.all().order_by('-date', '-time')
    #
    # # Fetch initial credited amount (either from customer or first transaction)
    # initial_credited_amount = customer.initial_amount
    #
    # # If the initial balance isn't stored in the Customer model, get it from the first transaction
    # first_transaction = customer.transactions.order_by('date', 'time').first()
    # if first_transaction and first_transaction.transaction_type == 'credit':  # Adjust based on your model
    #     initial_credited_amount = first_transaction.amount
    #
    # if request.user.is_customer:
    #     if request.user.id != customer.user.id:
    #         messages.error(request, "You are not authorized to view this page.")
    #         return redirect('home')
    #     return render(request, 'transaction_history.html', {
    #         'customer': customer,
    #         'transactions': transactions,
    #         'initial_credited_amount': initial_credited_amount
    #     })
    #
    # if request.user.is_banker:
    #     return render(request, 'banker_transaction.html', {
    #         'customer': customer,
    #         'transactions': transactions,
    #         'initial_credited_amount': initial_credited_amount
    #     })
    #
    # messages.error(request, "You are not authorized to view this page.")
    # return redirect('home')

def customer_transaction_history(request, account_number):
    # Retrieve the customer using their account number
    customer = get_object_or_404(Customer, account_number=account_number)

    # Fetch the customer's transactions, ordered by date and time
    transactions = customer.transactions.all().order_by('-date', '-time')

    # Check if the user is a customer or a banker
    if request.user.is_customer:
        # If the user is a customer, they can only view their own transaction history
        if request.user.id != customer.user.id:
            return HttpResponseForbidden("You are not authorized to view this page.")
        return render(request, 'transaction_history.html', {
            'customer': customer,
            'transactions': transactions
        })

    elif request.user.is_banker:
        # If the user is a banker, they can view any customer's transaction history
        return render(request, 'banker_transaction.html', {
            'customer': customer,
            'transactions': transactions
        })

    # If the user is neither a customer nor a banker, return a forbidden response
    return HttpResponseForbidden("You are not authorized to view this page.")

def more_details(request):
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        messages.error(request, "Customer profile not found.")
        return redirect('home')

    transactions = Transaction.objects.filter(customer=customer).values(
        'bank', 'branch', 'ifsc'
    ).distinct()

    context = {
        'transactions': transactions,
        'customer': customer,
    }
    return render(request, 'more.html', context)