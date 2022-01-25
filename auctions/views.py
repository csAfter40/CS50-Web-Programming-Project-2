from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, response
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse


from .models import User, Category, Listing, Watchlist, Bid, Comment
from .forms import ListingForm
from . import urls

def get_category_names():
    category_names = []
    categories = Category.objects.all()
    for category in categories:
        category_names.append(category.category_name)
    return category_names

def get_user_watchlist(user):
    watchlists = Watchlist.objects.filter(user=user)
    listings = [watchlist.listing for watchlist in watchlists]
    return listings


# def get_current_bid(listing):
#     if listing.max_bid:
#         return listing.max_bid
#     else:
#         return listing.starting_bid

def index(request, listings=None, title="Active Listings"):
    if not listings:
        if title == "Active Listings":
            listings = Listing.objects.filter(status=1)
    if request.user.is_authenticated:
        watchlist_listings = get_user_watchlist(request.user)
    else:
        watchlist_listings = []
    context = {
        "listings": listings,
        "title": title,
        "user": request.user,
        "watchlist": watchlist_listings,
        "categories": Category.objects.all()
        
    }
    return render(request, "auctions/index.html", context)

def detail_view(request, id):
    listing = Listing.objects.filter(id=id).first()
    if request.method == "POST" and request.user.is_authenticated:
        # print(request.POST["bid"])
        amount = request.POST["bid"]
        bid = Bid(user=request.user, amount=amount, listing=listing)
        bid.save()
        listing.max_bid = amount
        listing.save()
    
    if request.user.is_authenticated:
        watchlist_listings = get_user_watchlist(request.user)
    else:
        watchlist_listings = []
    
    comments = Comment.objects.filter(listing=listing).order_by("time")

    context = {
            "listing": listing,
            "id": id,
            "is_in_watchlist": listing in watchlist_listings,
            "current_bid": listing.max_bid,
            "comments": comments,
            "categories": Category.objects.all()
    }
    return render(request, "auctions/listing.html", context)

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
                "message": "Invalid username and/or password.",
                "categories": Category.objects.all()
            })
    else:
        return render(request, "auctions/login.html", {
            "categories": Category.objects.all()
        })


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
                "message": "Passwords must match.",
                "categories": Category.objects.all()
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken.",
                "categories": Category.objects.all()
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html", {
            "categories": Category.objects.all()})

def create1(request):
    pass

def create(request, listing=None):
    
    if isinstance(request.user, AnonymousUser):
        return HttpResponseRedirect(reverse("register"))

    if request.method == "POST":
        category = Category.objects.get(category_name=request.POST["category"])

        listing = Listing(title=request.POST["title"], description=request.POST["description"], starting_bid=float(request.POST["bid"]),
                            image_url=request.POST["picture"], category=category, user=request.user, max_bid=float(request.POST["bid"]))
        listing.save()
        return HttpResponseRedirect(reverse("index"))

    else:
        context = {
            "category_names": get_category_names(),
            "categories": Category.objects.all()
        }
        return render(request, "auctions/create.html", context)

def my_listings(request):
    listings = Listing.objects.filter(user=request.user)
    return index(request, listings=listings, title="My Listings")

def update_listing(request, id):
    listing = get_object_or_404(Listing, id=id)

    form = ListingForm(request.POST or None, instance=listing)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("detail", kwargs={"id":id}))
    
    context = {
        "form": form,
        "categories": Category.objects.all()
    }

    return render(request, "auctions/update.html", context)

def toggle_watchlist(request, id):
    referer = request.META.get("HTTP_REFERER")
    user = request.user
    listing = Listing.objects.filter(id=id).first()
    watchlist = Watchlist.objects.filter(user=request.user, listing=listing).first()
    if watchlist:
        watchlist.delete()
    else:
        watchlist = Watchlist(user=user, listing=listing)
        watchlist.save()
    return redirect(referer)

def my_watchlist(request):
    watchlists = Watchlist.objects.filter(user=request.user)
    listings = [watchlist.listing for watchlist in watchlists]
    return index(request, listings=listings, title="My Watchlist")

def close_bid(request, id):
    listing = Listing.objects.filter(id=id).first()
    if request.user == listing.user:
        bid = listing.bids.all().order_by("-amount").first()
        if bid:
            listing.winner = bid.user
        listing.status = 0
        listing.save()

    return HttpResponseRedirect(reverse("detail", kwargs={"id":id})) 

def won(request):
    if request.user.is_authenticated:
        listings = Listing.objects.filter(winner=request.user)
        return index(request, listings=listings, title="Auctions I Won")
    return index(request)

def comment(request, id):
    if request.method == "POST":
        text = request.POST["comment"]
        user = request.user
        listing = get_object_or_404(Listing, id=id)
        comment = Comment(text=text, user=user, listing=listing)
        comment.save()
    return HttpResponseRedirect(reverse("detail", kwargs={"id":id}))

def category(request, category):
    category = get_object_or_404(Category, category_name=category)
    listings = Listing.objects.filter(category=category)
    return index(request, listings=listings, title=category)