from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Category, Auction, Comment, Bid

@login_required
def create_listing(request):
    if request.method == "GET":
        return render(request, "auctions/create.html", {
            "categories" : Category.objects.all()
        })
    elif request.method == "POST":
        title = request.POST["title"]
        category = Category.objects.get(category=request.POST["category"])
        image_url = request.POST["url"]
        description = request.POST["description"]
        initial_price = request.POST["initial_price"]
        status = request.POST["status"]
        if status == 'on':
            is_active = True
        else:
            is_active = False
        owner = User.objects.get(username=request.POST["owner"])

        new_auction = Auction(
            title=title,
            description = description,
            image_url = image_url,
            category = category,
            initial_price = initial_price,
            is_active = is_active,
            user = owner
        )
        new_auction.save()
        return render(request, "auctions/index.html", {

        })

        new_listing = ListingModel(
                        title=title, 
                        image_url=url, 
                        description=description, 
                        category=category, 
                        price=initial_price, 
                        active=status, 
                        owner=User.objects.get(username = owner))
        new_listing.save()


def watchlist(request):
    pass

def index(request):
    items = Auction.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "items" : items,
        "categories" : Category.categories
    })

def auction_details(request):
    pass

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
