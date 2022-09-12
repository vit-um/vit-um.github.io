from ast import In
from decimal import Decimal
from lib2to3.pgen2.token import NAME
from operator import truediv
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required

from .models import Lots, User, Category, Bids, Comments


def index(request):
    categories = Category.objects.all().order_by('name')
    lots = Lots.objects.all().order_by('-status')
    lotsMaxBidsList = lotsMaxBids(lots)
    return render(request, "auctions/index.html", {
            "categories": categories,
            "lots": lots,
            "lotsMaxBids": lotsMaxBidsList,
            "titleH": "All listings",
        })

def active(request):
    categories = Category.objects.all().order_by('name')
    lots = Lots.objects.filter(status = True)
    lotsMaxBidsList = lotsMaxBids(lots)
    return render(request, "auctions/index.html", {
            "categories": categories,
            "lots": lots,
            "lotsMaxBids": lotsMaxBidsList,
            "titleH": "Only active listings"
        })

@login_required(redirect_field_name=None,login_url='login')

def mylots(request):
    user = request.user
    categories = Category.objects.all().order_by('name')
    lots = Lots.objects.filter(author = user).order_by('-status')
    lotsMaxBidsList = lotsMaxBids(lots)
    return render(request, "auctions/index.html", {
            "categories": categories,
            "lots": lots,
            "lotsMaxBids": lotsMaxBidsList,
            "titleH": "Only my listings"
        })

@login_required(redirect_field_name=None,login_url='login')

def wishlist(request):
    user = request.user
    lots = Lots.objects.filter(wishlist = user).order_by('-status', 'id')
    categories = Category.objects.all().order_by('name')
    lotsMaxBidsList = lotsMaxBids(lots)
    return render(request, "auctions/index.html", {
            "titleH": "My Wishlist",
            "categories": categories,
            "lotsMaxBids": lotsMaxBidsList,
            "lots": lots
        })

def catview(request, cat):
    catid = Category.objects.get(name = cat)
    lots = Lots.objects.filter(category = catid.id).order_by('-status')
    lotsMaxBidsList = lotsMaxBids(lots)
    categories = Category.objects.all().order_by('name')
    return render(request, "auctions/index.html", {
            "titleH": cat,
            "categories": categories,
            "lots": lots,
            "lotsMaxBids": lotsMaxBidsList
        })

@login_required(redirect_field_name=None,login_url='login')

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


def lotpage(request, lotID):
    categories = Category.objects.all().order_by('name')
    lot = Lots.objects.get(id = lotID)
    messageBad = ""
    messageGood = ""
    UserMaxBid = ""
    user = request.user
    statusWatch = listingInWatchlist(lot, user)
    statusOwner = ownerIndaHouse(lot, user)

    # for comment
    if request.method == "POST" and "Make comment" in request.POST:
        
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))

        form = YourComment(request.POST)
        if form.is_valid():
            objSave(form, lot, user) 

    # for bid
    if request.method == "POST" and "Make bid" in request.POST:
        
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))

        if statusOwner:
            messageBad = "Owner is not allowed to make bid"
        else:     
            form = YourBid(request.POST)
            if form.is_valid():
                price = form.cleaned_data.get("userBid")
                UserBids = getMaxBid(lotID)
                if UserBids:
                    if price > UserBids.userBid:
                        objSave(form, lot, user)
                        messageGood = "Your bid has been accepted"
                    else:
                        messageBad = "Your bid must be higher than the current bid"
                else:
                    if price > lot.bid:
                        objSave(form, lot, user)
                        lot.sold = True
                        lot.save(update_fields=['sold']) # if at least one bid was bidded, switch, for 'unsold' message
                        messageGood = "Your bid has been accepted"
                    else:
                        messageBad = "Your bid must be higher than the starting bid"
            if statusWatch == False and messageGood:
                lot.wishlist.add(user)
                lot.save()
                messageGood = messageGood + ". Lot has been added to your watchlist"
                statusWatch = True
    
    # for adding to watchlist
    if request.method == "POST" and "watchlistSwitch" in request.POST:
        
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))

        if statusWatch == False:
            lot.wishlist.add(user)
            lot.save()
            messageGood = "Lot has been added to your watchlist"
            statusWatch = True
        else:
            lot.wishlist.remove(user)
            lot.save()
            messageBad = "Lot has been deleted from your watchlist"
            statusWatch = False

    UserBid = getMaxBid(lotID)

    # for closing the lot
    if request.method == "POST" and "closelot" in request.POST:
        lot.status = False
        lot.save(update_fields=['status'])
        messageGood = "Lot has been closed"

    Commentses = Comments.objects.filter(lot = lotID)
    if request.user.is_authenticated:
        UserMaxBid = getUserMaxBid(lotID, user)

    return render(request, "auctions/lotpage.html", {
            "lot": lot,
            "bidform": YourBid(),
            "commentform": YourComment(),
            "Comments": Commentses,
            "UserBid": UserBid,
            "messageBad": messageBad,
            "messageGood": messageGood,
            "UserMaxBid": UserMaxBid,
            "statusWatch": statusWatch,
            "statusOwner": statusOwner,
            "categories": categories,
            "user": user
        })


def search(request):
    q = request.GET.get("q")
    lots = Lots.objects.filter(name__icontains = q).order_by('-status')
# https://django.fun/docs/django/ru/4.0/ref/models/querysets/#id4
    categories = Category.objects.all().order_by('name')
    lotsMaxBidsList = lotsMaxBids(lots)
    return render(request, "auctions/index.html", {
            "categories": categories,
            "lots": lots,
            "lotsMaxBids": lotsMaxBidsList,
            "titleH": "Searching results",
        })

###########   Functions   ###########

def objSave(form, lot, user):
    preform = form.save(commit = False)
    preform.lot = lot
    preform.author = user
    preform.save()

def getMaxBid(lotID):
    UserBid = Bids.objects.filter(lot = lotID)
    if UserBid:
        UserBid = UserBid.order_by('-id')[0]
    return UserBid   

def getUserMaxBid(lotID, user):
    UserBid = Bids.objects.filter(lot = lotID, author = user)
    if UserBid:
        UserBid = UserBid.order_by('-id')[0]
    return UserBid

def lotsMaxBids(lots):
    lotsMaxBids = []
    for lot in lots:
        UserBid = getMaxBid(lot.id)
        lotsMaxBids.append(UserBid)
    return lotsMaxBids

def listingInWatchlist(lot, user):
    userlist = User.objects.filter(wishUsers = lot)
    if user in userlist:
        return True
    else:
        return False

def ownerIndaHouse(lot, user):
    authorOfListing = User.objects.filter(authorUser = lot)
    if user in authorOfListing:
        return True
    else:
        return False

###########   Classes   ###########

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
            'urlimage': forms.URLInput(attrs={'class': 'lotURL formElemInlineHeight'}),
            'image': forms.ClearableFileInput(attrs={'class': 'lotUp formElemInlineHeight'}),
            'category': forms.CheckboxSelectMultiple(attrs={'class': 'lotCateg'}),
        }
        labels = {
            'name': "Title",
            'description': "Description",
            'urlimage': "URL or image",
            'image': '',
            'category': "Category",
        }
  
class YourBid(ModelForm):
    userBid = forms.DecimalField(
        min_value = Decimal('0.01'),
        max_value = Decimal('99999'),
        decimal_places = 2,
        required = True,
        label = 'Place your bet',         
        widget = forms.NumberInput(attrs={'class': 'lotBid formElemInlineHeight', 'placeholder': '0.00'})
    )
    class Meta:       
        model = Bids
        fields = ['userBid']

class YourComment(ModelForm):
    class Meta:       
        model = Comments
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'lotAddComment formElemWidth', "placeholder": 'Your comment'}),
        }
        labels = {
            'comment': '',
        }
