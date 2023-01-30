from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, resolve
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
        # NOTE to pass a foreign to Auction table, we need to retrieve it through Primary Key table
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
            "items" : Auction.objects.filter(is_active=True)
        })

def filter(request):
    if request.method == "POST":
        category_filtered = request.POST['selected_category']

        if category_filtered == "all":
            activeItems = Auction.objects.filter(is_active=True)
            return render(request, "auctions/index.html", {
                "items" : activeItems,
                "categories" : Category.objects.all()
            })
        else:
            category_filtered_pk = Category.objects.get(category=category_filtered)
            activeItems = Auction.objects.filter(is_active=True, category=category_filtered_pk)
            return render(request, "auctions/index.html", {
                "items" : activeItems,
                "categories" : Category.objects.all()}) 

def filter_watchlist(request):
    if request.method == "POST":
        category_filtered = request.POST['selected_category']
        currentUser = request.user
        if category_filtered == "all":
            # NOTE here we have an access to foreign key through Users and then filter by Auction field
            watchlistItems = currentUser.auction_watchlist.filter(is_active=True)
            print(watchlistItems)
            return render(request, "auctions/watchlist.html", {
                "watchlistItems" : watchlistItems,
                "categories" : Category.objects.all()
            })
        else:
            category_filtered_pk = Category.objects.get(category=category_filtered)
            watchlistItems = currentUser.auction_watchlist.filter(is_active=True, category = category_filtered_pk)
            return render(request, "auctions/watchlist.html", {
                "watchlistItems" : watchlistItems,
                "categories" : Category.objects.all()}) 

def watchlist(request):
    currentUser = request.user
    # NOTE auction_watchlist is RELATED_NAME. We use to access foreign key data for User (different models)
    items = currentUser.auction_watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watchlistItems" : items,
        "categories" : Category.objects.all()
    })

# NOTE Use "render(request, ..." when you want to return a template with passed data
# Use HttpResonse... when you want to redirect user to different URL or/and just make database changes
def addWatchlist(request, id):
    item = Auction.objects.get(pk=id)
    currentUser = request.user
    item.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("auction_details", args=(id, )))


def removeWatchlist(request, id):
    item = Auction.objects.get(pk=id)
    currentUser = request.user
    item.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("auction_details", args=(id, )))

def index(request):
    # NOTE return PATH, e.g., for index "/", for auction_details for the third item result = "auction_details/3" 
    # print(request.path) 
    items = Auction.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "items" : items,
        "categories" : Category.objects.all()
    })

# NOTE auction_detailse(request, ID - id is taken from HTML
# NOTE id here is taken from HTML, however HTML gets the id here: href="{% url 'auction_details' id=item.id %}"
# which means that the id should be first passed to HTML through Django views.py
def auction_details(request, id):
    item = Auction.objects.get(pk=id)
    currentUser = request.user
    if currentUser in item.watchlist.all():
        isWatchlist = True
    else:
        isWatchlist = False
    return render(request, "auctions/auction_details.html", {
        "item" : item,
        "isWatchlist" : isWatchlist
    })

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
