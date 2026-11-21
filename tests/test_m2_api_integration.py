from fastapi.testclient import TestClient
from app.main import app
from app.api.routes.auth_router import service as auth_service
from app.api.routes.customer_router import service as customer_service
from app.api.routes.cart_router import service as cart_service
from app.api.routes.order_router import service as order_service
from app.repositories.commerce_repository import CommerceRepository


def isolate_commerce_services(tmp_path, monkeypatch):
    repo = CommerceRepository(tmp_path / "commerce.json")
    for service in (auth_service, customer_service, cart_service, order_service):
        monkeypatch.setattr(service, "repo", repo)
    monkeypatch.setattr(auth_service, "sessions", {})


def test_real_menu_to_order_via_api(tmp_path, monkeypatch):
    isolate_commerce_services(tmp_path, monkeypatch)
    client = TestClient(app)
    customer = client.post('/customers/register', json={
        'name': 'Demo', 'email': 'demo@example.com',
        'password': 'correct-horse-battery', 'address': '123 Main Street',
    })
    assert customer.status_code == 201, customer.text
    login = client.post('/customers/login', json={
        'email': 'demo@example.com', 'password': 'correct-horse-battery',
    })
    assert login.status_code == 200, login.text
    auth = {'Authorization': f"Bearer {login.json()['access_token']}"}
    menus = client.get('/restaurants/1/menu')
    assert menus.status_code == 200
    item = menus.json()[0]
    assert client.get('/cart').status_code == 401
    added = client.post('/cart/items', headers=auth, json={'item_id': item['id'], 'quantity': 2})
    assert added.status_code == 200, added.text
    assert added.json()['total_cents'] == 2 * item['price']
    checked = client.post('/checkout', headers=auth)
    assert checked.status_code == 201, checked.text
    order = checked.json()
    assert order['total_cents'] == 2 * item['price']
    assert client.get('/cart', headers=auth).json()['items'] == []
    assert client.get(f"/orders/{order['id']}", headers=auth).json()['id'] == order['id']
    assert CommerceRepository(tmp_path / 'commerce.json').read()['orders'][order['id']]['id'] == order['id']


def test_real_menu_availability_round_trip(tmp_path, monkeypatch):
    import json
    from app.repositories import item_repository
    source = item_repository.DATA_PATH
    temp = tmp_path / 'items.json'
    temp.write_text(source.read_text(encoding='utf-8'), encoding='utf-8')
    monkeypatch.setattr(item_repository, 'DATA_PATH', temp)
    isolate_commerce_services(tmp_path, monkeypatch)
    client = TestClient(app)
    client.post('/customers/register', json={'name':'Demo','email':'other@example.com','password':'secret1234','address':'123 St'})
    token = client.post('/customers/login',json={'email':'other@example.com','password':'secret1234'}).json()['access_token']
    auth = {'Authorization':f'Bearer {token}'}
    item = client.get('/restaurants/1/menu').json()[0]
    assert client.post('/cart/items', headers=auth, json={'item_id':item['id'],'quantity':1}).status_code == 200
    data = json.loads(temp.read_text())
    for row in data:
        if row['id'] == item['id']:
            row['available'] = False
    temp.write_text(json.dumps(data), encoding='utf-8')
    assert client.get('/cart',headers=auth).status_code == 200
    assert client.post('/checkout',headers=auth).status_code == 409
    assert client.delete(f"/cart/items/{item['id']}",headers=auth).status_code == 200

def test_deactivated_customer_cannot_access_cart(tmp_path, monkeypatch):
    isolate_commerce_services(tmp_path, monkeypatch)

    client = TestClient(app)

    customer = {
        'name': 'Test User',
        'email': 'inactive@example.com',
        'password': 'securepass123',
        'address': '123 Main Street'
    }

    assert client.post('/customers/register', json=customer).status_code == 201

    login = client.post('/customers/login', json={
        'email': customer['email'],
        'password': customer['password']
    })
    assert login.status_code == 200

    auth = {
        'Authorization': f"Bearer {login.json()['access_token']}"
    }

    assert client.get('/cart', headers=auth).status_code == 200
    assert client.delete('/customers/me', headers=auth).status_code == 204

    assert client.get('/cart', headers=auth).status_code == 403
    assert client.post('/cart/items', headers=auth, json={
        'item_id': 'a',
        'quantity': 1
    }).status_code == 403
    assert client.delete('/cart', headers=auth).status_code == 403
    assert client.post('/checkout', headers=auth).status_code == 403

def test_restaurant_menu_write_requires_admin():
    client = TestClient(app)

    restaurant = {
        'name': 'Unauthorized Restaurant'
    }

    response = client.post('/restaurants', json=restaurant)

    assert response.status_code == 401, response.text


    response = client.put('/restaurants/1', json=restaurant)

    assert response.status_code == 401, response.text


    item = {
        'name': 'Unauthorized Item',
        'price': 1200
    }

    response = client.post('/restaurants/1/menu', json=item)

    assert response.status_code == 401, response.text


    response = client.put('/restaurants/1/menu/a', json=item)

    assert response.status_code == 401, response.text


def test_customer_cannot_modify_restaurant_or_menu(
    tmp_path, monkeypatch, isolated_restaurants, isolated_items
):

    isolate_commerce_services(tmp_path, monkeypatch)

    client = TestClient(app)

    registered = client.post('/customers/register', json={
        'name': 'Regular Customer',
        'email': 'regular@example.com',
        'password': 'securepass123',
        'address': '123 Main Street'
    })
    assert registered.status_code == 201

    login = client.post('/customers/login', json={
        'email': 'regular@example.com',
        'password': 'securepass123'
    })
    assert login.status_code == 200

    auth = {
        'Authorization': f"Bearer {login.json()['access_token']}"
    }

    from app.repositories import restaurant_repository, item_repository

    restaurant_file = restaurant_repository.DATA_PATH
    item_file = item_repository.DATA_PATH

    restaurants_before = restaurant_file.read_bytes()
    items_before = item_file.read_bytes()

    requests = [
        client.post('/restaurants', headers=auth, json={
            'name': 'Unauthorized Restaurant'
        }),
        client.put('/restaurants/1', headers=auth, json={
            'name': 'Changed Restaurant'
        }),
        client.post('/restaurants/1/menu', headers=auth, json={
            'name': 'Unauthorized Item',
            'price': 1200
        }),
        client.put('/restaurants/1/menu/a', headers=auth, json={
            'name': 'Changed Item',
            'price': 1200
        })
    ]


    for response in requests:
        assert response.status_code == 403, response.text

    assert restaurant_file.read_bytes() == restaurants_before
    assert item_file.read_bytes() == items_before



def test_updated_customer_address_used_at_checkout(tmp_path, monkeypatch):
    isolate_commerce_services(tmp_path, monkeypatch)

    client = TestClient(app)

    registered = client.post('/customers/register', json={
        'name': 'Original Name',
        'email': 'address-test@example.com',
        'password': 'securepass123',
        'address': '123 Old Street'
    })
    assert registered.status_code == 201

    login = client.post('/customers/login', json={
        'email': 'address-test@example.com',
        'password': 'securepass123'
    })
    assert login.status_code == 200

    auth = {
        'Authorization': f"Bearer {login.json()['access_token']}"
    }

    updated = client.patch('/customers/me', headers=auth, json={
        'name': 'Updated Name',
        'address': '456 New Street'
    })

    assert updated.status_code == 200, updated.text
    assert updated.json()['name'] == 'Updated Name'
    assert updated.json()['address'] == '456 New Street'

    profile = client.get('/customers/me', headers=auth)

    assert profile.status_code == 200
    assert profile.json()['address'] == '456 New Street'

    item = client.get('/restaurants/1/menu').json()[0]

    added = client.post('/cart/items', headers=auth, json={
        'item_id': item['id'],
        'quantity': 1
    })
    assert added.status_code == 200, added.text

    checkout = client.post('/checkout', headers=auth)

    assert checkout.status_code == 201, checkout.text
    assert checkout.json()['delivery_address'] == '456 New Street'

    saved = CommerceRepository(
        tmp_path / 'commerce.json'
    ).read()

    order_id = checkout.json()['id']
    assert saved['orders'][order_id]['delivery_address'] == '456 New Street'

def test_order_address_does_not_change_after_profile_update(tmp_path, monkeypatch):
    isolate_commerce_services(tmp_path, monkeypatch)

    client = TestClient(app)

    customer = {
        'name': 'Address Test',
        'email': 'order-address@example.com',
        'password': 'securepass123',
        'address': '123 Original Street'
    }

    registered = client.post('/customers/register', json=customer)
    assert registered.status_code == 201

    login = client.post('/customers/login', json={
        'email': customer['email'],
        'password': customer['password']
    })
    assert login.status_code == 200

    auth = {
        'Authorization': f"Bearer {login.json()['access_token']}"
    }

    menu = client.get('/restaurants/1/menu')
    assert menu.status_code == 200
    item = menu.json()[0]

    added = client.post('/cart/items', headers=auth, json={
        'item_id': item['id'],
        'quantity': 1
    })
    assert added.status_code == 200

    checkout = client.post('/checkout', headers=auth)
    assert checkout.status_code == 201

    order_id = checkout.json()['id']
    assert checkout.json()['delivery_address'] == '123 Original Street'

    updated = client.patch('/customers/me', headers=auth, json={
        'address': '789 Updated Street'
    })
    assert updated.status_code == 200

    profile = client.get('/customers/me', headers=auth)
    assert profile.json()['address'] == '789 Updated Street'

    old_order = client.get(f'/orders/{order_id}', headers=auth)
    assert old_order.status_code == 200
    assert old_order.json()['delivery_address'] == '123 Original Street'

    saved = CommerceRepository(tmp_path / 'commerce.json').read()
    assert saved['orders'][order_id]['delivery_address'] == '123 Original Street'
