from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

import auctions
from .models import User, AuctionListing, Bid, Comment

categories = ["electronics", "sex toy", "groceries", "jan", "other"]


def index(request):
    return render(request, "auctions/index.html", {
        "title": "Active listings:",
        "listings": AuctionListing.objects.all()
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


def create(request):
    return render(request, "auctions/create.html", {
        "categories": categories
    })


def create_error(request):
    pass


def create_submit(request):
    if request.method == "POST":
        title = request.POST['title']
        try:
            image = request.POST['image_url']
        except KeyError:
            image = "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"
        description = request.POST['description']
        price = request.POST['price']
        category = request.POST['category']
        auction = AuctionListing(owner=request.user, title=title, description=description, image_url=image,
                                 start_bid=price, category=category)
        auction.save()
        return HttpResponseRedirect(reverse("index"))


def listing(request, listing_pk):
    listing = AuctionListing.objects.get(pk=listing_pk)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "is_in_watchlist": not is_in_watchlist(request.user, listing_pk),
        "can_close": listing.owner.username == request.user.username and listing.closed is False,
        "is_win": listing.is_that_user_the_greatest_bit(request.user) and listing.closed is True
    })


def is_in_watchlist(user, listing_pk):
    listing = AuctionListing.objects.get(pk=listing_pk)
    try:
        listing.users_watchlist.get(username=user.username)
        return True
    except auctions.models.User.DoesNotExist:
        return False


def change_watchlist(request, listing_pk):
    auction = AuctionListing.objects.get(pk=listing_pk)
    if is_in_watchlist(request.user, listing_pk):
        auction.users_watchlist.remove(request.user)
        request.user.Watch_list.remove(auction)
    else:
        auction.users_watchlist.add(request.user)
        request.user.Watch_list.add(auction)
    return HttpResponseRedirect(reverse("listing", args=(listing_pk,)))


def bid(request, listing_pk):
    if request.method == "POST":
        price = int(request.POST['bid'])
        listing = AuctionListing.objects.get(pk=listing_pk)
        if price <= listing.max_bid() or listing.closed is True:
            return render(request, "auctions/allert_bid.html", {
                "listing": listing
            })
        bid = Bid(owner=request.user, auction=AuctionListing.objects.get(pk=listing_pk), price=price)
        bid.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_pk,)))


def watch_list(request):
    return render(request, "auctions/watch_list.html", {
        "listings": request.user.Watch_list.all()
    })


def categories_view(request):
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def category_listing(request, name):
    return render(request, "auctions/index.html", {
        "title": f"Category {name}:",
        "listings": AuctionListing.objects.filter(category=name)
    })


def add_comment(request, listing_pk):
    if request.method == "POST":
        content = request.POST['comment']
        comment = Comment(owner=request.user, auction=AuctionListing.objects.get(pk=listing_pk), content=content)
        comment.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_pk,)))


def close(request, listing_pk):
    if request.method == "POST":
        listing = AuctionListing.objects.get(pk=listing_pk)
        listing.closed = True
        return HttpResponseRedirect(reverse("listing", args=(listing_pk,)))
