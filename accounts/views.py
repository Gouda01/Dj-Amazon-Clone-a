from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.db.models.aggregates import Count
from django.contrib.auth.models import User

from .forms import SignupForm, UserActivateForm
from .models import Profile
from products.models import Product, Brand, Review
from orders.models import Order



# Create your views here.

def signup(request) :
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            user = form.save(commit=False)
            user.is_active = False
            form.save()

            profile = Profile.objects.get(user__username=username)

            # Send Email
            send_mail(
                "Activate your Account",
                f"Welcome {username} \nUse this code {profile.code} to activate your account.",
                "goda61@gmail.com",
                [email],
                fail_silently=False,
            )
            return redirect(f'/accounts/{username}/activate')
    
    else :
        form = SignupForm()
    
    return render(request, 'accounts/signup.html', {'form':form})



def user_active (request,username) :
    
    profile = Profile.objects.get(user__username=username)

    if request.method == 'POST':
        form = UserActivateForm(request.POST)
        if form.is_valid() :
            code = form.cleaned_data['code']

            if code == profile.code :
                profile.code =''
                user = User.objects.get(username=username)
                user.is_active = True

                user.save()
                profile.save()

                return redirect('/accounts/login')

    
    else :
        form = UserActivateForm()
    
    return render(request, 'accounts/activate.html', {'form':form})



def dashboard (request):
    
    new = Product.objects.filter(flag='New')
    sale = Product.objects.filter(flag='Sale').count()
    feature = Product.objects.filter(flag='Feature').count()


    brand_name = []
    brand_products = []
    brands = Brand.objects.all().annotate(product_count=Count('product_brand')).order_by('-product_count')[:10]
    for brand in brands:
        brand_name.append(brand.name)
        brand_products.append(brand.product_count)

    return render (request,'accounts/dashboard.html',{
        'new' :new,
        'sale' :sale,
        'feature' :feature,

        'brand_name' :brand_name,
        'brand_products' :brand_products,
    })