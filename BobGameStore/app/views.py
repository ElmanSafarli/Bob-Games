from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, ListView, DetailView
from .models import Category, Subcategory, Product, Cart
from django.db.models import Q
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from django.conf import settings


class HomePage(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['subcategories'] = Subcategory.objects.all()

        # Get the four most recently added products
        recent_products = Product.objects.order_by('-id')[:4]
        context['recent_products'] = recent_products

        return context

class ProductListView(ListView):
    model = Product
    template_name = 'pages/product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch distinct genres and years from the database
        context['genres'] = Product.objects.values_list('genre', flat=True).distinct().order_by('genre')
        context['years'] = Product.objects.values_list('year', flat=True).distinct().order_by('year')
        context['categories'] = Category.objects.all()
        context['subcategories'] = Subcategory.objects.all()

        return context

    def get_queryset(self):
        queryset = Product.objects.all()

        # Handle filters for genre
        genres = self.request.GET.getlist('genres')
        if genres:
            queryset = queryset.filter(genre__in=genres)

        # Handle filters for year
        years = self.request.GET.getlist('years')
        if years:
            queryset = queryset.filter(year__in=years)

        # Handle filters for price
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price and max_price:
            # Use Q objects to filter products within the price range
            queryset = queryset.filter(Q(price__gte=min_price) & Q(price__lte=max_price))

        return queryset

class CategoryProductListView(ListView):
    model = Product
    template_name = 'pages/category_product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')
        context['category'] = get_object_or_404(Category, slug=category_slug)
        context['categories'] = Category.objects.all()
        context['subcategories'] = Subcategory.objects.all()
        return context

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        category = get_object_or_404(Category, slug=category_slug)
        return Product.objects.filter(subcategory__category=category)

class SubcategoryProductListView(ListView):
    model = Product
    template_name = 'pages/subcategory_product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subcategory_slug = self.kwargs.get('subcategory_slug')
        context['subcategory'] = get_object_or_404(Subcategory, slug=subcategory_slug)
        context['categories'] = Category.objects.all()
        context['subcategories'] = Subcategory.objects.all()
        return context

    def get_queryset(self):
        subcategory_slug = self.kwargs.get('subcategory_slug')
        subcategory = get_object_or_404(Subcategory, slug=subcategory_slug)
        return Product.objects.filter(subcategory=subcategory)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'pages/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['categories'] = Category.objects.all()
        context['subcategories'] = Subcategory.objects.all()

        # Get the four most recently added products (excluding the current product)
        recent_products = Product.objects.exclude(id=self.object.id).order_by('-id')[:4]
        context['recent_products'] = recent_products

        return context


def cart_view(request):
    if request.user.is_authenticated:
        # If the user is authenticated, fetch cart items for the user
        cart_items = Cart.objects.filter(user=request.user)
    else:
        # If the user is anonymous, fetch cart items using the session ID
        session = Session.objects.get(session_key=request.session.session_key)
        session_id = session.session_key if session else None
        cart_items = Cart.objects.filter(session_id=session_id)

    context = {'cart_items': cart_items}
    context['categories'] = Category.objects.all()
    context['subcategories'] = Subcategory.objects.all()
    return render(request, 'pages/view_cart.html', context)

@require_POST
def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    quantity = int(request.GET.get('quantity', 1))

    if request.user.is_authenticated:
        user = request.user
        session_id = None
    else:
        # For anonymous users, use session_key to identify the cart
        session_id = request.session.session_key
        user = None

    cart_item, created = Cart.objects.get_or_create(user=user, session_id=session_id, product=product)

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return JsonResponse({'status': 'success'})

@require_POST
def remove_from_cart(request, product_id):
    try:
        if request.user.is_authenticated:
            # If the user is authenticated, remove the product from the cart for the user
            cart_item = Cart.objects.get(user=request.user, product__id=product_id)
        else:
            # If the user is anonymous, remove the product from the cart using the session ID
            session_id = request.session.session_key
            cart_item = Cart.objects.get(session_id=session_id, product__id=product_id)

        # Remove the cart item
        cart_item.delete()

        return JsonResponse({'status': 'success'})
    except Cart.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Product not found in the cart'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})



def checkout(request):
    # Get products from the user's cart
    cart_items = get_cart_items(request)

    if cart_items:
        # Calculate the total price
        total_price = sum(item.product.price * item.quantity for item in cart_items)
    else:
        total_price = 0

    context = {'cart_items': cart_items, 'total_price': total_price}
    return render(request, 'pages/checkout.html', context)


def get_cart_items(request):
    if request.user.is_authenticated:
        # If the user is authenticated, fetch cart items for the user
        return Cart.objects.filter(user=request.user)
    else:
        # If the user is anonymous, fetch cart items using the session ID
        session_id = request.session.session_key
        return Cart.objects.filter(session_id=session_id)


@csrf_exempt
def send_to_telegram_view(request):
    if request.method == 'POST':
        try:
            received_data = json.loads(request.body)
            contact_details = received_data.get('contact', {})
            cart_items = get_cart_items(request)

            # Prepare the message for Telegram
            message = f"New Order Details:\n\nContact Information:\nName: {contact_details.get('name')}\nSurname: {contact_details.get('surname')}\nNumber: {contact_details.get('number')}\nAddress: {contact_details.get('address')}\n\nOrdered Items:\n"

            # Include details about the selected products
            for item in cart_items:
                message += f"Product: {item.product.title}\nPrice: ${item.product.price}\nQuantity: {item.quantity}\n\n"

            # Send message to Telegram
            send_to_telegram(message)

            return JsonResponse({'status': 'success'})
        except Exception as e:
            print(f'Error processing the order: {str(e)}')  # Debug print
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



def send_to_telegram(message):
    bot_token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHANNEL_ID

    telegram_api_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': message,
    }

    response = requests.post(telegram_api_url, params=params)

    if response.status_code != 200:
        print(f"Failed to send message to Telegram. Status code: {response.status_code}")

