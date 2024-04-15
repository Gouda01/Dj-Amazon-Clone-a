from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.db.models.aggregates import Count
from django.http import JsonResponse
from django.template.loader import render_to_string


from .models import Product, Brand, Review, ProductImages


# Create your views here.
class ProductList (ListView):
    model = Product
    paginate_by = 52


class ProductDetail (DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = Review.objects.filter(product=self.get_object())
        context["images"] = ProductImages.objects.filter(product=self.get_object())
        context["related"] = Product.objects.filter(brand=self.get_object().brand)[:10]
        return context
    

class BrandList (ListView) :
    model = Brand
    paginate_by = 20

    queryset = Brand.objects.annotate(product_count=Count('product_brand'))



class BrandDetail (ListView) :
    model = Product
    template_name = 'products/brand_detail.html'
    paginate_by = 20

    def get_queryset(self):
        brand = Brand.objects.get(slug=self.kwargs['slug'])
        queryset = super().get_queryset().filter(brand=brand)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["brand"] = Brand.objects.filter(slug=self.kwargs['slug']).annotate(product_count=Count('product_brand'))[0]
        return context
    
    
# Add Reviews Before use ajax :

# def add_review (request,slug):
#     product = Product.objects.get(slug=slug)
#     review = request.POST.get('review')
#     rate = request.POST.get('rating')

#     Review.objects.create (
#         user = request.user,
#         product = product,
#         review = review,
#         rate = rate,
#     )


#     return redirect(f'/products/{slug}/')



def add_review (request,slug):
    product = Product.objects.get(slug=slug)
    review = request.POST.get('review')
    rate = request.POST.get('rating')

    Review.objects.create (
        user = request.user,
        product = product,
        review = review,
        rate = rate,
    )

    
    #Get all reviews for this product :
    reviews = Review.objects.filter(product=product)
    page = render_to_string('includes/reviews.html', {'reviews':reviews})
    return JsonResponse({'result':page})





def get_brand_products(request) :
    brands = Brand.objects.all()

    context = {
        'brands': brands,
        }
    return render(request, 'products/test/get_brand_products.html', context)


def get_product_list (request):
    brand_id = request.GET.get('brand_id')
    products = Product.objects.filter(brand_id=brand_id)
    page = render_to_string('products/test/includes/products-list.html', {'products':products})
    return JsonResponse({'result':page})
