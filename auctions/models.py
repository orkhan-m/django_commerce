from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    categories = [
    ("Strength", "Strength"),
    ("Intelligence", "Intelligence"), 
    ("Agility", "Agility")
    ]

    category = models.CharField(max_length=20, choices=categories, default="Strength", unique=True)

    def __str__(self):
        return f"{self.category}"

class Auction(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    image_url = models.CharField(max_length=2000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="auction_category", null=True, blank=True)
    initial_price = models.FloatField()
    last_price = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, related_name="auction_watchlist")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction_user")
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_user")
    bid = models.FloatField(default=0)
    auction = models.ForeignKey(Auction, related_name="bid_auction", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.auction} bid ${self.bid}'

class Comment(models.Model):
    text = models.CharField(max_length=2000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user")
    item = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comment_item")
    date = models.DateTimeField(auto_now=True)

