import restaurant


class Restaurant:

    menu = restaurant.Menu()
    costumer_list = []
    waiter = restaurant.Waiter("Josh")
    courier = restaurant.Courier("Bob")
    chef = restaurant.Chef("Allen")

    def main(self):
        self.costumer_list.append(restaurant.Customer(10, "Pavlova Street 4", "Bogdan"))
        self.new_order()
        self.give_orders_to_chef()
        self.give_order_to_costumer()

    def new_order(self):
        order = self.costumer_list[0].make_order(self.menu)
        self.waiter.take_order(order)

    def give_orders_to_chef(self):
        self.chef.take_order(self.waiter.give_orders_to_chef())

    def give_order_to_costumer(self):
        self.chef.cook_order()
        self.waiter.take_cooked_order(self.chef.give_order_to_waiter())
        self.waiter.give_order_to_customer(self.costumer_list)


my_restaurant = Restaurant()
my_restaurant.main()
