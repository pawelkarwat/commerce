from django.contrib import admin

from .models import AuctionListing, Bid, Comment, User

# Register your models here.

admin.site.register(AuctionListing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(User)
