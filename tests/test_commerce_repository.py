
from app.repositories.commerce_repository import CommerceRepository


def test_repository_initializes_empty_data(tmp_path):
    repo = CommerceRepository(tmp_path / 'commerce.json')

    assert repo.read() == {
        'customers': {},
        'carts': {},
        'orders': {}
    }


def test_repository_save_and_reload(tmp_path):
    path = tmp_path / 'commerce.json'
    repo = CommerceRepository(path)

    data = {
        'customers': {
            'customer-1': {
                'id': 'customer-1',
                'name': 'Test Customer'
            }
        },
        'carts': {
            'customer-1': {
                'restaurant_id': '1',
                'items': {'item-1': 2}
            }
        },
        'orders': {
            'order-1': {
                'id': 'order-1',
                'customer_id': 'customer-1'
            }
        }
    }

    repo.save(data)

    reloaded = CommerceRepository(path).read()

    assert reloaded == data
    assert reloaded['customers']['customer-1']['id'] == 'customer-1'
    assert reloaded['orders']['order-1']['id'] == 'order-1'
    assert reloaded['orders']['order-1']['customer_id'] == 'customer-1'


def test_repository_save_replaces_existing_data(tmp_path):
    repo = CommerceRepository(tmp_path / 'commerce.json')

    first = {
        'customers': {},
        'carts': {},
        'orders': {}
    }

    repo.save(first)

    updated = repo.read()
    updated['customers']['customer-1'] = {
        'id': 'customer-1',
        'name': 'Updated Customer'
    }

    repo.save(updated)

    reloaded = CommerceRepository(repo.path).read()

    assert reloaded['customers']['customer-1']['name'] == 'Updated Customer'
    assert len(reloaded['customers']) == 1
