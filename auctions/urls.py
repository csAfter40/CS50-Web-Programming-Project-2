from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("create1/", views.create1, name="create1"),
    path("my_listings", views.my_listings, name="my_listings"),
    path("my_watchlist", views.my_watchlist, name="my_watchlist"),
    path("won", views.won, name="won"),
    path("<int:id>/", views.detail_view, name="detail"),
    path("<int:id>/close", views.close_bid, name="close"),
    path("<int:id>/update", views.update_listing, name="update"),
    path("<int:id>/comment", views.comment, name="comment"),
    path("<int:id>/watchlist", views.toggle_watchlist, name="watchlist"),
    path("category/<str:category>", views.category, name="category")
]
