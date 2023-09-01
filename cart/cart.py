from django.conf import settings
from product.models import Product, Variant, Color


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        for p in self.cart.keys():
            self.cart[str(p)]['variant'] = Variant.objects.get(pk=p)

        for item in self.cart.values():
            item['total_price'] = float(item['variant'].precio * item['quantity'])

            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def add(self, product_id, color, size , quantity=1, update_quantity=False):
        product_id = str(product_id)
        variant_id = Variant.objects.filter(product=Product.objects.get(pk=product_id), color=Color.objects.get(code=color), size=size).values('id')[0]['id']
        
        variant_id = str(variant_id)
        
        if variant_id not in self.cart:
            size = size.replace('/','|')
            self.cart[variant_id] = {'quantity': 1, 'id': variant_id, 'color': color, 'size': size}
    
        if update_quantity:

            self.cart[variant_id]['quantity'] += int(quantity)

            if self.cart[variant_id]['quantity'] == 0:
                self.remove(variant_id)

        self.save()

    def remove(self, variant_id):
        
        if variant_id in self.cart:
            del self.cart[variant_id]
        self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_total_cost(self):
        for p in self.cart.keys():
            self.cart[str(p)]['variant'] = Variant.objects.get(pk=p)

        return sum(float(item['variant'].precio * item['quantity']) for item in self.cart.values())

    def get_item(self, variant_id):

        if str(variant_id) in self.cart:
            return self.cart[str(variant_id)]
        else:
            return None
