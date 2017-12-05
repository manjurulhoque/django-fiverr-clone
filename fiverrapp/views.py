from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from fiverrapp.forms import GigForm, UserLoginForm, UserRegistrationForm
from fiverrapp.models import Gig, Purchase, Review, Profile


def home(request):
    gigs = Gig.objects.filter(status=True)
    return render(request, "home.html", {"gigs": gigs})


@login_required(login_url="/login")
def profile(request, username):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        profile.about = request.POST['about']
        profile.slogan = request.POST['slogan']
        profile.save()
    else:
        try:
            profile = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            return redirect('/')

    gigs = Gig.objects.filter(user=profile.user, status=True)
    return render(request, 'profile.html', {"profile": profile, "gigs": gigs})


def gig_detail(request, id):
    if request.method == 'POST' and \
            not request.user.is_anonymous() and \
                    Purchase.objects.filter(gig_id=id, buyer=request.user).count() > 0 and \
                    'content' in request.POST and \
                    request.POST['content'].strip() != '':
        Review.objects.create(content=request.POST['content'], gig_id=id, user=request.user)

    try:
        gig = Gig.objects.get(id=id)
    except Gig.DoesNotExist:
        return redirect('/')

    if request.user.is_anonymous() or \
                    Purchase.objects.filter(gig=gig, buyer=request.user).count() == 0 or \
                    Review.objects.filter(gig=gig, user=request.user).count() > 0:
        show_post_review = False
    else:
        show_post_review = Purchase.objects.filter(gig=gig, buyer=request.user).count() > 0

    reviews = Review.objects.filter(gig=gig)
    return render(request, 'gig_detail.html', {"show_post_review": show_post_review, "reviews": reviews, "gig": gig, })


@login_required(login_url="/login")
def create_gig(request):
    error = ''
    if request.method == 'POST':
        gig_form = GigForm(request.POST, request.FILES)
        if gig_form.is_valid():
            gig = gig_form.save(commit=False)
            gig.user = request.user
            gig.save()
            return redirect('my_gigs')
        else:
            error = "Data is not valid"

    gig_form = GigForm()
    return render(request, 'create_gig.html', {"error": error})


@login_required(login_url="/login")
def edit_gig(request, id):
    try:
        gig = Gig.objects.get(id=id, user=request.user)
        error = ''
        if request.method == 'POST':
            gig_form = GigForm(request.POST, request.FILES, instance=gig)
            if gig_form.is_valid():
                gig.save()
                return redirect('my_gigs')
            else:
                error = "Data is not valid"

        return render(request, 'edit_gig.html', {"gig": gig, "error": error})
    except Gig.DoesNotExist:
        return redirect('/')


@login_required(login_url="/login")
def my_gigs(request):
    gigs = Gig.objects.filter(user=request.user)
    return render(request, 'my_gigs.html', {"gigs": gigs})


def login_view(request):  # users will login with their Email & Password
    if request.user.is_authenticated:
        return redirect("/")
    else:
        title = "Login"
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            # authenticates Email & Password
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect("/")
        context = {"form": form,
                   "title": title
                   }
        return render(request, "accounts/login.html", context)


def register_view(request):  # Creates a New Account & login New users
    if request.user.is_authenticated:
        return redirect("/")
    else:
        title = "Register"
        form = UserRegistrationForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            prof = Profile(user=user)
            prof.save()
            authenticate(email=user.email, password=password)
            login(request, user)
            return redirect("/")

        context = {"title": title, "form": form}

        return render(request, "accounts/form.html", context)


def logout_view(request):  # logs out the logged in users
    if not request.user.is_authenticated():
        return redirect("login")
    else:
        logout(request)
        return redirect("/")
