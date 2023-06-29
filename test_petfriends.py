from api.api import PetFriends
from api.settings import valid_email, valid_password, invalid_password, invalid_email
import os


pf = PetFriends()

#Test1
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем, что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result
    print(result)

#Test 2
def test_create_pet_without_photo_with_valid_data(name='Chewbacca', animal_type='Wookie',
                                                  age='232'):
    """Добавляем нового питомца с корректными данными"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

#Test 3
def test_successful_add_pet_photo(pet_photo='images/chewbacca.jpg'):
    """Добавляем фото карточке питомца"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        assert status == 200

    else:
        raise Exception("There is no my pets")

#Test 4
def test_get_all_pets_with_valid_key(filter=''):
    """ Передаем корректный ключ для получения списка питомцев """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

#Test 5
def test_add_new_pet_with_valid_data(name='Ранкор', animal_type='Rancor', age='80',
                                     pet_photo='image\rancor.jpg'):
    """Добавляем нового питомца с фото"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

#Test 6
def test_successful_delete_self_pet():
    """Удаляем питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Ранкор", "Rancor", "80")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()

#Test 7
def test_successful_update_self_pet_info(name='Chewbacca', animal_type='Вуки', age='233'):
    """Обновляем информацию о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

#Test 8
def test_add_new_pet_without_name(name='', animal_type='Wampa',
                                  age='135'):
    """Добавляем питомца c пустым полем Имя"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 400

#Test 9
def test_get_api_key_with_wrong_password(email=valid_email, password=invalid_password):
    """Проверяем, что запрос api ключа возвращает статус 403 при неправильном пароле"""

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert "key" not in result

#Test 10
def test_get_api_key_with_wrong_email(email=invalid_email, password=valid_password):
    """Проверяем, что запрос api ключа возвращает статус 403 при неправильном email"""

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert "key" not in result