from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("auction_details/<int:id>", views.auction_details, name="auction_details"),
    path("addWatchlist/<int:id>", views.addWatchlist, name="addWatchlist"),
    path("removeWatchlist/<int:id>", views.removeWatchlist, name="removeWatchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("filter", views.filter, name="filter"),
    path("filter_watchlist", views.filter_watchlist, name="filter_watchlist"),
]
