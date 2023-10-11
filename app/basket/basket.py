

class Basket:
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket

    def add(self, product):
        product_id = product.id

        if product_id not in self.basket:
            self.basket[product_id] = {
                "price": product.price,
            }

        self.save()

    def save(self):
        self.session.modified = True
