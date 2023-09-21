from decimal import Decimal
from django.conf import settings
from app_megano.models import Products


class CartAnon(object):
    """Класс корзины неавторизованного пользователя"""
    def __init__(self, request):
        """Инициализация корзины"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, item, quantity=1, update_quantity=False):
        """Добавление товара в корзину или изменение количества"""
        item_id = str(item.id)
        if item_id not in self.cart:
            self.cart[item_id] = {
                'product': str(item.product.id),
                'category': str(item.category.id),
                'quantity': 0,
                'price': str(item.price)}
        if update_quantity:
            self.cart[item_id]['quantity'] = quantity
        else:
            self.cart[item_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Обновление корзины"""
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, item):
        """Удаление товара из корзины"""
        item_id = str(item.id)
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def __iter__(self):
        """Перебор элементов корзины и получение данных из БД"""
        item_ids = self.cart.keys()
        items = Products.objects.filter(id__in=item_ids)
        cart = self.cart.copy()
        for i_item in items:
            cart[str(i_item.id)]['product'] = i_item.product
            cart[str(i_item.id)]['category'] = i_item.category
        for unit in cart.values():
            unit['price'] = Decimal(unit['price'])
            unit['total_price'] = unit['price'] * unit['quantity']
            yield unit

    def __len__(self):
        """Возвращает количество наименований товара в корзине"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Возвращает общую стоимость товаров в корзине"""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Очистка корзины"""
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

