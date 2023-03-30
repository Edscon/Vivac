from django.shortcuts import render, get_object_or_404, redirect

from .models import Product, Review


def product(request, slug):

    product = get_object_or_404(Product, slug=slug)

    if request.method == 'POST':

        rating = request.POST.get('rating', 3)
        titulo = request.POST.get('titulo', '')
        content = request.POST.get('content', '')

        if content:

            reviews = Review.objects.filter(
                created_by=request.user, product=product)

            if reviews.count() > 0:
                review = reviews.first()
                review.rating = rating
                review.titulo = titulo
                review.content = content

                review.save()

            else:
                review = Review.objects.create(
                    product=product,
                    rating=rating,
                    titulo=titulo,
                    content=content,
                    created_by=request.user,
                )
            return redirect('product', slug=slug)

    return render(request, 'product/product.html', {'product': product})
