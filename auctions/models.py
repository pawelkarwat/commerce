from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max, Count


class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Auctions")
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    start_bid = models.DecimalField(max_digits=20, decimal_places=2)
    image_url = models.CharField(max_length=350)
    category = models.CharField(max_length=350, blank=True)
    closed = models.BooleanField(default=False)
    users_watchlist = models.ManyToManyField(User, blank=True, related_name="Watch_list")

    def max_bid(self):
        if self.bids.aggregate(price=Max('price'))['price'] is None:
            return self.start_bid
        else:
            return self.bids.aggregate(price=Max('price'))['price']

    def bids_count(self):
        return self.bids.aggregate(Count('pk'))['pk__count']

    def is_that_user_the_greatest_bit(self, user):
        max_value = 0
        max_bid = None
        for bid in self.bids.all():
            if bid.price > max_value:
                max_value = bid.price
                max_bid = bid
        if max_bid is None:
            return False
        if max_bid.owner.username == user.username:
            return True
        return False


class Bid(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    price = models.DecimalField(max_digits=20, decimal_places=2)


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=2000)
