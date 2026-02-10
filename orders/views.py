from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from products.models import Product
import json

@csrf_exempt
@login_required
def create_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order = Order.objects.create(user=request.user)

        for item in data['items']:
            product = Product.objects.get(id=item['product_id'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity']
            )

        return JsonResponse({'message': 'Order created'})
