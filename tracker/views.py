# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Expense


# login view
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("/")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")

# register view
from django.contrib.auth.models import User

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "User already exists"})

        user = User.objects.create_user(username=username, password=password)
        user.save()

        return redirect("/login")

    return render(request, "register.html")

# logout view
def logout_view(request):
    logout(request)
    return redirect("/login")

# dashboard view
@login_required(login_url="/login")
def index(request):
    data = Expense.objects.filter(user=request.user)  # 🔥 IMPORTANT

    income = sum(i.amount for i in data if i.type == "income")
    expense = sum(i.amount for i in data if i.type == "expense")
    balance = income - expense

    return render(request, "index.html", {
        "data": data,
        "income": income,
        "expense": expense,
        "balance": balance
    })

# add expense view
@login_required(login_url="/login")
def add(request):
    if request.method == "POST":
        title = request.POST["title"]
        amount = request.POST["amount"]
        type_ = request.POST["type"]

        Expense.objects.create(
            user=request.user,   # 🔥 IMPORTANT FIX
            title=title,
            amount=amount,
            type=type_
        )

        return redirect("/")

    return render(request, "add.html")