from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("watchlist", views.watch_list, name="watch_list"),
    path("categories", views.categories_view, name="categories"),
    path("categories/<str:name>", views.category_listing, name="category_listing"),
    path("create/submit", views.create_submit, name="create_submit"),
    path("listing/<int:listing_pk>", views.listing, name="listing"),
    path("listing/<int:listing_pk>/bid", views.bid, name="bid"),
    path("listing/<int:listing_pk>/change_watchlist", views.change_watchlist, name="change_watchlist"),
    path("listing/<int:listing_pk>/add_comment", views.add_comment, name="add_comment"),
    path("listing/<int:listing_pk>/close", views.close, name="close")
]
