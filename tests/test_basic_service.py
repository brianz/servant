import pytest

def test_test_client(test_client):
    response = test_client.say_name()
    assert not response.is_error()
    assert response.name == 'Test Service'
    assert response.age >= 0
    assert response.age <= 100

def test_test_client_values(test_client):
    response = test_client.say_name(name='bz', age=41)
    assert not response.is_error()
    assert response.name == 'bz'
    assert response.age == 41


def test_test_client_errors(test_client):
    response = test_client.say_name(age='abc')
    assert response.is_error()
    assert response.field_errors.age[0].error == "Value 'abc' is not int"
    assert not response.errors


def test_client_v2(test_client_v2):
    response = test_client_v2.say_name()
    assert not response.is_error()
    assert response.name == 'Test Service'


def test_client_v2_full_name(test_client_v2):
    response = test_client_v2.say_full_name(first_name='tom', last_name='jones')
    assert not response.is_error()
    assert response.full_name == 'Tom Jones'
