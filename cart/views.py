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


@csrf_exempt
def remove_from_cart(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        product_id = data.get("product_id")
        quantity = int(data.get("quantity", 0))  # optional: reduce by this amount
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({"error": "Invalid request"}, status=400)

    if not product_id:
        return JsonResponse({"error": "Missing product_id"}, status=400)

    # Temporary user for testing
    user = User.objects.first()  # replace with request.user in production

    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        return JsonResponse({"error": "Cart not found"}, status=404)

    try:
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
    except CartItem.DoesNotExist:
        return JsonResponse({"error": "Product not in cart"}, status=404)

    if quantity <= 0 or quantity >= cart_item.quantity:
        # Remove the item completely
        cart_item.delete()
        return JsonResponse({"message": "Product removed from cart"})
    else:
        # Reduce quantity
        cart_item.quantity -= quantity
        cart_item.save()
        return JsonResponse({"message": "Product quantity reduced", "quantity": cart_item.quantity})

def view_cart(request):
    # Get user_id from query params: /api/cart/view/?user_id=1
    user_id = request.GET.get("user_id")

    if not user_id:
        return JsonResponse({"error": "Missing user_id"}, status=400)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User does not exist"}, status=404)

    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        return JsonResponse({"cart_items": []})  # empty cart

    items = cart.items.all()
    data = []
    for item in items:
        data.append({
            "product_id": item.product.id,
            "name": item.product.name,
            "quantity": item.quantity,
            "price": str(item.product.price),
        })

    return JsonResponse({"cart_items": data})