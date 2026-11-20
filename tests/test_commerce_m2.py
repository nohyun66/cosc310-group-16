from types import SimpleNamespace
import pytest
from fastapi import HTTPException
from app.repositories.commerce_repository import CommerceRepository
from app.services.commerce_service import CommerceService
from app.schemas.commerce import RegisterInput

class Items:
    def __init__(self):
        self.values = {
            'a': SimpleNamespace(id='a', name='Pie', price=1200, restaurant_id=1, available=True),
            'b': SimpleNamespace(id='b', name='Soup', price=700, restaurant_id=1, available=True),
            'c': SimpleNamespace(id='c', name='Pizza', price=1500, restaurant_id=2, available=True),
        }
    def get_by_item_id(self, item_id):
        return self.values.get(item_id)

class Restaurants:
    def get_by_id(self, rid):
        return SimpleNamespace(id=rid, is_open=True) if rid in ('1','2') else None

@pytest.fixture
def setup(tmp_path):
    repo = CommerceRepository(tmp_path / 'commerce.json')
    items = Items()
    service = CommerceService(repo=repo, items=items, restaurants=Restaurants())
    user = service.register(RegisterInput(name='Test', email='test@example.com', password='securepass', address='123 St'))
    return service, repo, items, user['id']

def expect_status(status, f):
    with pytest.raises(HTTPException) as caught:
        f()
    assert caught.value.status_code == status


def test_integrated_customer_to_order_and_restart(setup):
    svc, repo, items, uid = setup
    token = svc.login('test@example.com', 'securepass')['access_token']
    assert svc.authenticated(token)['id'] == uid
    svc.add(uid, 'a', 2)
    svc.add(uid, 'b', 1)
    assert svc.cart(uid)['total_cents'] == 3100
    items.values['a'].price = 1300
    order = svc.checkout(uid)
    assert order['total_cents'] == 3300
    assert order['items'][0]['unit_price_cents'] == 1300
    assert svc.cart(uid)['items'] == []
    after_restart = CommerceService(repo=CommerceRepository(repo.path), items=items, restaurants=Restaurants())
    assert after_restart.get_order(uid, order['id'])['id'] == order['id']
    assert len(after_restart.list_orders(uid)) == 1


def test_mixed_restaurants_rejected_without_mutation(setup):
    svc, repo, items, uid = setup
    svc.add(uid, 'a', 1)
    expect_status(409, lambda: svc.add(uid, 'c', 1))
    assert len(svc.cart(uid)['items']) == 1


def test_unavailable_and_invalid_quantity_rejected(setup):
    svc, repo, items, uid = setup
    items.values['a'].available = False
    expect_status(409, lambda: svc.add(uid, 'a', 1))
    expect_status(422, lambda: svc.add(uid, 'b', 0))
    assert svc.cart(uid)['items'] == []


def test_empty_checkout_and_deactivated_customer(setup):
    svc, repo, items, uid = setup
    expect_status(409, lambda: svc.checkout(uid))
    token = svc.login('test@example.com', 'securepass')['access_token']
    svc.deactivate(uid)
    expect_status(403, lambda: svc.authenticated(token))
    expect_status(401, lambda: svc.login('test@example.com', 'securepass'))


def test_failed_save_keeps_cart(setup, monkeypatch):
    svc, repo, items, uid = setup
    svc.add(uid, 'a', 1)
    original = repo.save
    def broken(_):
        raise OSError('simulated disk error')
    monkeypatch.setattr(repo, 'save', broken)
    with pytest.raises(OSError):
        svc.checkout(uid)
    monkeypatch.setattr(repo, 'save', original)
    assert svc.cart(uid)['items'][0]['item_id'] == 'a'
    assert svc.list_orders(uid) == []


def test_order_isolation(setup):
    svc, repo, items, uid = setup
    other = svc.register(RegisterInput(name='Other', email='other@example.com', password='securepass', address='456 St'))['id']
    svc.add(uid, 'a', 1)
    order = svc.checkout(uid)
    expect_status(403, lambda: svc.get_order(other, order['id']))



def test_unavailable_item_remains_visible_and_removable(setup):
    svc, repo, items, uid = setup

    svc.add(uid, 'a', 1)
    items.values['a'].available = False

    expect_status(409, lambda: svc.checkout(uid))

    saved = repo.read()

    assert saved['carts'][uid]['items']['a'] == 1
    assert saved['orders'] == {}

    assert svc.cart(uid)['items'][0]['item_id'] == 'a'
    assert svc.remove(uid, 'a')['items'] == []



def test_unavailable_item_cannot_be_added_to_new_cart(setup):
    svc, repo, items, uid = setup
    items.values['a'].available = False
    expect_status(409, lambda: svc.add(uid, 'a', 1))

def test_unavailable_item_quantity_change_rejected(setup):
    svc, repo, items, uid = setup

    svc.add(uid, 'a', 2)
    items.values['a'].available = False

    expect_status(409, lambda: svc.change(uid, 'a', 5))

    cart = svc.cart(uid)
    assert cart['items'][0]['item_id'] == 'a'
    assert cart['items'][0]['quantity'] == 2

    saved_cart = repo.read()['carts'][uid]
    assert saved_cart['items']['a'] == 2


def test_closed_restaurant_checkout_keeps_cart(setup):
    svc, repo, items, uid = setup

    svc.add(uid, 'a', 2)

    original_restaurants = svc.restaurants

    class ClosedRestaurants:
        def get_by_id(self, rid):
            return SimpleNamespace(id=rid, is_open=False)

    svc.restaurants = ClosedRestaurants()

    try:
        expect_status(409, lambda: svc.checkout(uid))

        cart = svc.cart(uid)
        assert len(cart['items']) == 1
        assert cart['items'][0]['item_id'] == 'a'
        assert cart['items'][0]['quantity'] == 2

        assert svc.list_orders(uid) == []
    finally:
        svc.restaurants = original_restaurants

def test_order_keeps_original_price_after_menu_change(setup):
    svc, repo, items, uid = setup

    svc.add(uid, 'a', 2)

    order = svc.checkout(uid)

    assert order['total_cents'] == 2400
    assert order['items'][0]['unit_price_cents'] == 1200

    items.values['a'].price = 1500

    saved_order = svc.get_order(uid, order['id'])

    assert saved_order['total_cents'] == 2400
    assert saved_order['items'][0]['unit_price_cents'] == 1200
    assert saved_order['items'][0]['line_total_cents'] == 2400

    restarted = CommerceService(
        repo=CommerceRepository(repo.path),
        items=items,
        restaurants=Restaurants()
    )

    restored_order = restarted.get_order(uid, order['id'])

    assert restored_order['total_cents'] == 2400
    assert restored_order['items'][0]['unit_price_cents'] == 1200

def test_cart_can_switch_restaurants_after_removing_last_item(setup):
    svc, repo, items, uid = setup

    first_cart = svc.add(uid, 'a', 2)

    assert first_cart['restaurant_id'] == '1'
    assert len(first_cart['items']) == 1

    empty_cart = svc.remove(uid, 'a')

    assert empty_cart['restaurant_id'] is None
    assert empty_cart['items'] == []
    assert empty_cart['total_cents'] == 0

    second_cart = svc.add(uid, 'c', 1)

    assert second_cart['restaurant_id'] == '2'
    assert len(second_cart['items']) == 1
    assert second_cart['items'][0]['item_id'] == 'c'
    assert second_cart['total_cents'] == 1500

    order = svc.checkout(uid)

    assert order['restaurant_id'] == '2'
    assert order['total_cents'] == 1500
    assert svc.cart(uid)['items'] == []

def test_cart_quantity_update_and_persistence(setup):
    svc, repo, items, uid = setup

    svc.add(uid, 'a', 1)
    svc.add(uid, 'b', 2)

    assert svc.cart(uid)['total_cents'] == 2600

    updated = svc.change(uid, 'a', 3)

    assert updated['total_cents'] == 5000
    assert updated['subtotal_cents'] == 5000

    quantities = {
        item['item_id']: item['quantity']
        for item in updated['items']
    }

    assert quantities == {'a': 3, 'b': 2}

    expect_status(422, lambda: svc.change(uid, 'a', 0))
    expect_status(422, lambda: svc.change(uid, 'a', -1))

    assert svc.cart(uid)['total_cents'] == 5000

    restarted = CommerceService(
        repo=CommerceRepository(repo.path),
        items=items,
        restaurants=Restaurants()
    )

    restored = restarted.cart(uid)

    assert restored['total_cents'] == 5000
    assert {
        item['item_id']: item['quantity']
        for item in restored['items']
    } == {'a': 3, 'b': 2}

def test_customer_carts_are_isolated(setup):
    svc, repo, items, uid = setup

    other = svc.register(RegisterInput(
        name='Other',
        email='other@example.com',
        password='securepass',
        address='456 St'
    ))['id']

    svc.add(uid, 'a', 2)
    svc.add(other, 'b', 3)

    assert svc.cart(uid)['total_cents'] == 2400
    assert svc.cart(other)['total_cents'] == 2100

    svc.change(uid, 'a', 1)

    assert svc.cart(uid)['total_cents'] == 1200
    assert svc.cart(other)['total_cents'] == 2100

    svc.clear(uid)

    assert svc.cart(uid)['items'] == []
    assert svc.cart(other)['items'][0]['item_id'] == 'b'
    assert svc.cart(other)['items'][0]['quantity'] == 3

    order = svc.checkout(other)

    assert order['customer_id'] == other
    assert order['total_cents'] == 2100
    assert svc.list_orders(uid) == []
    assert len(svc.list_orders(other)) == 1

def test_duplicate_email_rejected(setup):
    svc, repo, items, uid = setup

    duplicate = RegisterInput(
        name='Another User',
        email='test@example.com',
        password='anotherpass',
        address='456 St'
    )

    expect_status(409, lambda: svc.register(duplicate))

    customers = repo.read()['customers']
    assert len(customers) == 1
    assert uid in customers

def test_wrong_password_rejected(setup):
    svc, repo, items, uid = setup

    sessions_before = dict(svc.sessions)

    expect_status(
        401,
        lambda: svc.login('test@example.com', 'wrongpassword')
    )

    assert svc.sessions == sessions_before
    assert uid in repo.read()['customers']

def test_missing_items_and_orders_rejected(setup):
    svc, repo, items, uid = setup

    expect_status(404, lambda: svc.add(uid, 'missing-item', 1))
    expect_status(404, lambda: svc.change(uid, 'missing-item', 2))
    expect_status(404, lambda: svc.get_order(uid, 'missing-order'))

    assert svc.cart(uid)['items'] == []
    assert svc.list_orders(uid) == []

def test_checkout_rejects_invalid_saved_quantity(setup):
    svc, repo, items, uid = setup

    svc.add(uid, 'a', 2)

    db = repo.read()
    db['carts'][uid]['items']['a'] = 0
    repo.save(db)

    expect_status(409, lambda: svc.checkout(uid))

    saved = repo.read()
    assert saved['carts'][uid]['items']['a'] == 0
    assert saved['orders'] == {}

def test_checkout_rejects_item_restaurant_mismatch(setup):
    svc, repo, items, uid = setup

    svc.add(uid, 'a', 2)

    items.values['a'].restaurant_id = 2

    expect_status(409, lambda: svc.checkout(uid))

    saved = repo.read()
    assert saved['carts'][uid]['restaurant_id'] == '1'
    assert saved['carts'][uid]['items']['a'] == 2
    assert saved['orders'] == {}

def test_checkout_rejects_missing_delivery_address(setup):
    svc, repo, items, uid = setup

    svc.add(uid, 'a', 2)

    db = repo.read()
    db['customers'][uid]['address'] = ''
    repo.save(db)

    expect_status(409, lambda: svc.checkout(uid))

    saved = repo.read()
    assert saved['carts'][uid]['items']['a'] == 2
    assert saved['orders'] == {}
