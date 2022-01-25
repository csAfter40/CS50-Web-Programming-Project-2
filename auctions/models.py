from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.expressions import Case


class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=64)

    def __str__(self):
        return self.category_name

class Listing(models.Model):
    ACTIVE = 1
    CLOSED = 0
    STATUS_CHOICES = [
        (ACTIVE, "Active"),
        (CLOSED, "Closed")
    ]


    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    category = models.ForeignKey(Category, on_delete=SET_NULL, related_name="listings", blank=True, null=True)
    starting_bid = models.DecimalField(max_digits=11, decimal_places=2)
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="listings")
    image_url = models.URLField(max_length=256, null=True, blank=True)
    create_time = models.DateTimeField(auto_now=True)
    max_bid = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    winner = models.ForeignKey(User, blank=True, null=True, on_delete=SET_NULL)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=ACTIVE)

    def __str__(self):
        return self.title

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    listing = models.ForeignKey(Listing, on_delete=CASCADE, related_name="bids")
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.amount)

class Comment(models.Model):
    text = models.CharField(max_length=512)
    listing = models.ForeignKey(Listing, on_delete=CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="comments")
    time = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"listing #{self.id}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="watchlists")
    listing = models.ForeignKey(Listing, on_delete=CASCADE, related_name="watchlists")
