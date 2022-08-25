from decimal import Decimal
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.forms import ModelForm

from .models import Lots, User, Category, Bids, Comments


def index(request):
    categories = Category.objects.all().order_by('name')
    lots = Lots.objects.all()
    return render(request, "auctions/index.html", {
            "categories": categories,
            "lots": lots
        })

def active(request):
    categories = Category.objects.all().order_by('name')
    return render(request, "auctions/active.html", {
            "categories": categories
        })

def mylots(request):
    categories = Category.objects.all().order_by('name')
    return render(request, "auctions/mylots.html", {
            "categories": categories
        })

def wishlist(request):
    user = request.user
    lots = Lots.objects.filter(usersWhoAddToWatchlist = user).order_by('-statusActive', 'id')


    return render(request, "auctions/index.html", {
            "titleH": "My watchlist",
            "lots": lots
        })

def newlot(request):
    if request.method == "POST":
        form = NewLotForm(request.POST, request.FILES)
        if form.is_valid():
            forauthor = form.save(commit = False)
            forauthor.author = request.user
            forauthor.name = forauthor.name.capitalize()
            forauthor.description = forauthor.description.capitalize()
            forauthor.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/createnewlot.html", {
            "form": NewLotForm()
        })

class NewLotForm(ModelForm):
    # checkbox required attr is not valid 
    # for positive numbers 
    bid = forms.DecimalField(
        min_value = Decimal('0.01'),
        max_value = Decimal('99999'),
        decimal_places = 2,
        required = True, 
        label = "Starting bid",
        widget = forms.NumberInput(attrs={'class': 'lotBid formElemInlineHeight'})
    )
    class Meta:       
        model = Lots
        fields = ['name', 'description', 'bid', 'urlimage', 'image', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'lotTitle formElemWidth formElemInlineHeight'}),
            'description': forms.Textarea(attrs={'class': 'lotDescription formElemWidth'}),
            'bid': forms.NumberInput(attrs={'class': 'lotBid formElemInlineHeight'}),
            'urlimage': forms.URLInput(attrs={'class': 'lotURL formElemInlineHeight'}),
            'image': forms.ClearableFileInput(attrs={'class': 'lotUp formElemInlineHeight'}),
            'category': forms.CheckboxSelectMultiple(attrs={'class': 'lotCateg', 'required': 'True'}),
        }
        labels = {
            'name': "Title",
            'description': "Description",
            'bid': ("Starting bid"),
            'urlimage': "URL or image",
            'image': "",
            'category': "Category",
        }
  

# def categories(request):
#     categories = Category.objects.all().order_by('name')
#     return render(request, "auctions/layout.html", {
#             "categories": categories
#         })


def catview(request, title):
    catid = Category.objects.get(name = title)
    lots = Lots.objects.filter(category = catid.id).order_by('-statusActive')
    # lotsMaxBidsList = lotsMaxBids(lots)

    return render(request, "auctions/index.html", {
            "title": title,
            "lots": lots
#            "lotsMaxBids": lotsMaxBidsList
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

def search(request):
    q = request.GET.get("q")
    entry_text = util.get_entry(q)
    if entry_text == None:
        entries = util.list_entries()
        search_entries = []
        for i in entries:
            if i.lower().find(q.lower()) != -1:
                search_entries.append(i)
        if len(search_entries) == 0:
            page_header = "Нічого не знайдено"
        else:
            page_header = "Результати пошуку"
        return render(request, "encyclopedia/index.html", {
            "entries": search_entries,
            "header": page_header
            })
    else:
        return render(request, "wiki/page.html", {
            "entry_text": markdown(entry_text),
            "entry_name": q,
            "edit": True
            })
