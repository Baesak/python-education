"""Allows you to create your own virtual restaurant."""

from time import sleep
from random import randrange


class Person:
    """Allows you to create human beings that can do something and have own name."""

    def __init__(self, name):
        self.name = name

    @staticmethod
    def _do_something(action, repeat):
        """Simulates some action by printing it on screen. Number of printing should be
        chosen as second argument."""
        for _ in range(repeat):
            print(action)
            sleep(1)
        print(action)


class OrderCheckMixin:
    """Adds orders validation method to class. Made for Courier and Waiter"""

    @staticmethod
    def _order_validation(order, person):
        """Return False if food in order is not available, or if costumer is less than 18 years
        old and ordered drink with alcohol. Also raises error if Costumer give delivery order
        to Waiter, or non-delivery order to Courier"""

        if isinstance(person, Waiter) and order.delivery:
            raise TypeError("Delivery order should be taken only by Courier.")
        if isinstance(person, Courier) and not order.delivery:
            raise TypeError("Order without delivery should be taken only by Waiter.")

        for food in order.drinks_list + order.dishes_list:

            if not food.available:
                print(f"{food} is not in menu, choose something else!")
                return False

            if order.costumer.age < 18 and isinstance(food, Drinks):
                if food.alcohol:
                    print(f"You should be at least 18 years old to order {food}!")
                    return False

        return True


class Customer(Person):
    """Can make orders for Waiter and delivery orders for Courier with Order
    class.
    Age attribute is used for ordering alcohol drinks. Adress attribute used for
    delivery orders."""

    class Order:
        """Can create orders and delivery orders. Delivery order is an order whose
        'delivery' attribute = True. Regular order should be given to  Waiter. Delivery order
        should be given to Courier. 'price' attribute is setting by Waiter.
        If this a delivery order - 'price'

        Algorithm of processing orders:
        1.Order created by Customer
        2.Order taken by the Waiter
        3.Waiter gives Order to Chef
        4.Chef creating CookedOrder
        5.Chef gives CookedOrder to Waiter
        6.Waiter gives CookedOrder to Customer

        Algorithm of processing delivery orders:
        1.Order created by Customer
        2.Costumer gives Order to Chef
        3.Chef creating CookedOrder
        4.Chef gives CookedOrder to Courier
        5.Courier gives CookedOrder to Customer"""

        price = None

        def __init__(self, drinks_list, dishes_list, costumer, delivery=False):
            self.dishes_list = dishes_list
            self.drinks_list = drinks_list
            self.costumer = costumer
            self.delivery = delivery

    def __init__(self, age, adress, name):
        super().__init__(name)
        self.age = age
        self.adress = adress

    @staticmethod
    def _food_choice(menu):
        """Makes random dishes and drinks choice for orders."""
        dishes_choice1 = menu.dishes_list[randrange(0, len(menu.dishes_list))]
        dishes_choice2 = menu.dishes_list[randrange(0, len(menu.dishes_list))]
        drinks_choice = menu.drinks_list[randrange(0, len(menu.drinks_list))]

        return {'dishes_choice': [dishes_choice1, dishes_choice2], 'drinks_choice': [drinks_choice]}

    def make_order(self, menu):
        """Makes new order using Order class"""

        food_choice = self._food_choice(menu)
        order = self.Order(food_choice['drinks_choice'], food_choice['dishes_choice'], self)

        return order

    def make_delivery_order(self, menu):
        """Makes delivery order using order class"""
        food_choice = self._food_choice(menu)
        order = self.Order(food_choice['drinks_choice'], food_choice['dishes_choice'], self, True)

        return order

    def eat_and_pay(self, cooked_order):
        """This method is called by Waiter class.
        Makes customer eat every dish and drink, and pay to a Waiter."""

        for dish in cooked_order.dishes_list:
            self._do_something(f"Costumer eating {dish.name}...", 3)

        for drink in cooked_order.drinks_list:
            self._do_something(f"Costumer drinking {drink.name}...", 3)

        self._do_something(f'Costumer give {cooked_order.price}$ to waiter.', 1)

    def pay(self, price):
        """This method is called by Courier class
        Makes Costumer pay to Courier"""
        self._do_something(f'Costumer give {price}$ to courier.', 1)

    def __str__(self):
        return self.name


class Waiter(Person, OrderCheckMixin):
    """Takes Order from a Customer and give it to a Chef, then give CookedOrder
    from Chef to Costumer Doesn't work with delivery orders."""

    _orders_list = []
    _order_on_hands = None

    def take_order(self, order):
        """Takes order from Customer and appends it on _orders_list. Sets 'price'
        attribute in Order."""

        if self._order_validation(order, self):
            order.price = sum(order.dishes_list + order.drinks_list)
            self._orders_list.append(order)
            self._do_something("Waiter taking the order...", 3)

    def give_orders_to_chef(self):
        """Returns '_orders_list' method and replaces it with empty list.
        Used for giving orders to Chef."""
        self._do_something("Waiter delivered orders to chef.", 1)
        orders = self._orders_list
        self._orders_list = []
        return orders

    def take_cooked_order(self, cooked_order):
        """Updates '_order_on_hands' variable. Should be only 'CookedOrder' instance."""
        self._order_on_hands = cooked_order
        self._do_something("The waiter takes the order.", 1)

    def give_order_to_customer(self, costumer_list):
        """Search Costumer in costumer_list. Costumer should have the same name as
        Costumer in order. Then calls 'eat_and_pay' method from Costumer"""
        for costumer in costumer_list:
            if costumer.name == self._order_on_hands.costumer.name:
                costumer.eat_and_pay(self._order_on_hands)
                break


class Chef(Person):
    """Creating CookedOrders and can give it to Waiter or Courier.
    Can add and remove food from menu, and change available food.
    _cooked_order_list is storing CookedOrders for Waiter.
    _cooked_delivery_order_list is storing orders for Courier."""

    _orders_list = []
    _cooked_order_list = []
    _cooked_delivery_order = None

    class CookedOrder:
        """Creates cooked orders from orders. CookedOrders should be given to Customer."""

        def __init__(self, order):
            self.costumer = order.costumer
            self.dishes_list = order.dishes_list
            self.drinks_list = order.drinks_list
            self.price = order.price

    def take_order(self, orders):
        """Can take Orders from Waiter."""

        self._do_something("Chef took order.", 1)
        self._orders_list += orders

    def take_delivery_order(self, delivery_order):
        """Can take Orders from Courier"""

        self._do_something("Chef took delivery order.", 1)
        self._orders_list.append(delivery_order)

    def cook_order(self):
        """Creates CookedOrder from last Order in _orders_list."""

        order = self._orders_list.pop()
        self._do_something(f"Chef cooking order for {order.costumer}...", 6)
        if order.delivery:
            self._cooked_delivery_order = order
        else:
            self._cooked_order_list.append(self.CookedOrder(order))

    def give_order_to_waiter(self):
        """Gives orders for Waiter."""

        return self._cooked_order_list.pop()

    def give_delivery_order_to_courier(self):
        """Gives orders for Courier."""
        return self._cooked_delivery_order

    def add_to_menu(self, menu, food_type, name, price, alcohol=False):
        """Add new food to menu. food_type argument can be only 'dish' or 'drink'"""

        if food_type == "dish":
            menu.dishes_list.append(Dishes(name, price))

        elif food_type == "drink":
            menu.dishes_list.append(Drinks(name, price, alcohol))

        self._do_something(f"Chef added {name} to menu.", 1)

    def remove_from_menu(self, menu, name):
        """Remove food from menu by name"""

        food_list = menu.drinks_list + menu.dishes_list
        for food in food_list:
            if food.name == name:
                food_list.remove(food)
                break
        self._do_something(f"Chef removed {name} from menu.", 1)

    def update_available(self, menu, name, bool_available):
        """Change the 'available' attribute in some food from menu."""

        food_list = menu.drinks_list + menu.dishes_list

        for food in food_list:
            if food.name == name:
                food.available = bool_available
                break

        if bool_available:
            self._do_something(f"{name.capitalize()} is available.", 1)
        else:
            self._do_something(f"{name.capitalize()} is not available", 1)


class Courier(Person, OrderCheckMixin):
    """Takes CookedOrder from Chef and gives it to Customer. Works only with delivery orders"""

    _delivery_order = None
    _order_on_hands = None

    def take_delivery_order(self, delivery_order):
        """Takes CookedOrder from Chef and appends it on _orders_list.
        Sets 'price' attribute in Order."""

        if self._order_validation(delivery_order, self):
            delivery_order.price = sum(delivery_order.dishes_list + delivery_order.drinks_list)
            self._delivery_order = delivery_order

        self._do_something("Courier take delivery order.", 1)

    def give_order_to_chef(self):
        """Gives delivery order to Chef."""

        return self._delivery_order

    def take_cooked_delivery_order(self, cooked_order):
        """Takes CookedOrder from Chef."""

        self._order_on_hands = cooked_order
        self._do_something("Courier takes cooked order.", 1)

    def deliver_the_order(self, customers_list):
        """Search Costumer in costumer_list. Costumer should have the same adress
        as Costumer in order. Then calls 'pay' method from Costumer"""

        self._do_something("Courier delivering order...", 6)
        for costumer in customers_list:
            if costumer.adress == self._order_on_hands.costumer.adress:
                costumer.pay(self._order_on_hands.price)
                break


class Dishes:
    """Creates dishes for Menu. Available attribute could be changed by Chef."""

    available = True

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __add__(self, other):
        if isinstance(other, Dishes):
            return self.price + other.price
        return self.price + other

    def __radd__(self, other):
        return self.price + other

    def __str__(self):
        return self.name


class Drinks(Dishes):
    """Just like Dishes, but with 'alcohol' attribute."""

    def __init__(self, name, price, alcohol):
        super().__init__(name, price)
        self.alcohol = alcohol

    def __add__(self, other):
        if isinstance(other, Drinks):
            return self.price + other.price
        return self.price + other

    def __radd__(self, other):
        return self.price + other

    def __str__(self):
        return self.name


class Menu:
    """Stores Dishes and Drinks instances in 'dishes_list' and 'drinks_list'.
    Could be modified by Chef."""

    dishes_list = [Dishes("Pasta Carbonara", 12), Dishes("Beef steak", 20),
                   Dishes("Chicken salad", 6), Dishes("Fruit salad", 5)]

    drinks_list = [Drinks("Milk Shake", 7, False), Drinks("Tea", 3, False), Drinks("Beer", 5, True)]
