from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Cart, CartItem
from products.models import Product
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
user = User.objects.first()  #

@csrf_exempt
def add_to_cart(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        product_id = data.get("product_id")
        quantity = int(data.get("quantity", 1))
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({"error": "Invalid request"}, status=400)

    if not product_id:
        return JsonResponse({"error": "Missing product_id"}, status=400)

    # Assuming the user is authenticated
    # user = request.user
    # if not user.is_authenticated:
    #     return JsonResponse({"error": "User not authenticated"}, status=401)

    # Get or create the user's cart
    cart, created = Cart.objects.get_or_create(user=user)

    # Get the product
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product does not exist"}, status=404)

    # Add or update cart item
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    return JsonResponse({"message": f"{product.name} added to cart", "quantity": cart_item.quantity})
