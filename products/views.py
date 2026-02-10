from django.http import JsonResponse
from django.db.models import Q
from .models import Product
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        products = list(Product.objects.values())
        return JsonResponse(products, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # Assuming 'name' is unique for products. Change to your unique field(s)
        product_name = data.get('name')
        if not product_name:
            return JsonResponse({'error': 'Missing product name'}, status=400)

        # Try to get the product first
        product, created = Product.objects.update_or_create(
            name=product_name,  # field to check uniqueness
            defaults=data       # fields to update or create
        )

        if created:
            return JsonResponse({'message': 'Product created', 'id': product.id})
        else:
            return JsonResponse({'message': 'Product updated', 'id': product.id})
        


def search_products(request):
    if request.method == "GET":
        q = request.GET.get("q", "").strip()

        if not q:
            return JsonResponse({"error": "Missing search query (?q=...)"}, status=400)

        products = Product.objects.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q)   # remove if you don't have description
        ).values()

        if not products:  # if no matching products
            return JsonResponse({"message": "There is no product matching your search."})

        return JsonResponse(list(products), safe=False)

    return JsonResponse({"error": "Method not allowed"}, status=405)
