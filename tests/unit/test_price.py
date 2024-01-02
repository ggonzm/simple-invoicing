from src.simple_invoicing.domain.model import add_category_price

def test_price_assignment_to_products(fruit_category_tree, clients):
    n1, n2, _, n4,*_ = fruit_category_tree
    client1, *_ = clients

    add_category_price(client1, n4, 10.0)

    assert client1._category_prices[n4.path] == 10.0