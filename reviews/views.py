from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import ReviewForm
from .models import Review
from products.models import Product


@login_required
def add_review(request, product_id):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)

    product = get_object_or_404(Product, id=product_id)

    # Check if the user already reviewed this product
    if Review.objects.filter(product=product, user=request.user).exists():
        return JsonResponse({"error": "You already reviewed this product"}, status=400)

    form = ReviewForm(request.POST)

    if form.is_valid():
        review = form.save(commit=False)
        review.product = product
        review.user = request.user
        review.save()

        return JsonResponse({
            "message": "Review added successfully",
            "rating": review.rating,
            "comment": review.comment,
            "user": review.user.username
        })

    return JsonResponse({"errors": form.errors}, status=400)