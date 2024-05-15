from app.config import VALID_NAME, VALID_LAST_NAME, VALID_EMAIL, VALID_PASSWORD
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from app.registration import Registration


@pytest.fixture(scope="function", params=[
    ("", "Необходимо заполнить поле кириллицей. От 2 до 30 символов."),
    ("а", "Необходимо заполнить поле кириллицей. От 2 до 30 символов."),
    ("аа", None),
    ("а" * 30, None),
    ("а" * 31, "Необходимо заполнить поле кириллицей. От 2 до 30 символов."),
    ("а" * 255, "Необходимо заполнить поле кириллицей. От 2 до 30 символов."),
    ("а" * 1001, "Необходимо заполнить поле кириллицей. От 2 до 30 символов."),
    ("12345", "Необходимо заполнить поле кириллицей. От 2 до 30 символов."),
    ("Vasya", "Необходимо заполнить поле кириллицей. От 2 до 30 символов."),
    ("意志自由", "Необходимо заполнить поле кириллицей. От 2 до 30 символов."),
    (r"!@#$%^&*()_-+=\/", "Необходимо заполнить поле кириллицей. От 2 до 30 символов."),
    (VALID_NAME, None),
])
def param_name(request):
    return request.param


@pytest.fixture(scope="function", params=[
    ("", "Необходимо заполнить поле кириллицей. От 2 до 30 символов."),
    ("а", "Необходимо заполнить поле кириллицей. От 2 до 30 символов."),
    ("аа", None),
    ("а" * 30, None),
    ("а" * 31, "Необходимо заполнить поле кириллицей. От 2 до 30 символов."),
    ("а" * 255, "Необходимо заполнить поле кириллицей. От 2 до 30 символов."),
    ("а" * 1001, "Необходимо заполнить поле кириллицей. От 2 до 30 символов."),
    ("12345", "Необходимо заполнить поле кириллицей. От 2 до 30 символов."),
    ("Vasya", "Необходимо заполнить поле кириллицей. От 2 до 30 символов."),
    ("意志自由", "Необходимо заполнить поле кириллицей. От 2 до 30 символов."),
    (r"!@#$%^&*()_-+=\/", "Необходимо заполнить поле кириллицей. От 2 до 30 символов."),
    (VALID_LAST_NAME, None),
])
def param_last_name(request):
    return request.param


def go_to_registration_page(driver, wait):
    # Переходим на страницу авторизации
    driver.get("https://b2c.passport.rt.ru/")
    # Ждём пока страница загрузится
    wait.until(EC.presence_of_element_located((By.ID, "kc-register")))
    # Нажимаем "Зарегистрироваться"
    driver.find_element(By.ID, "kc-register").click()


class TestRegistration:
    def setup_class(self):
        # Создаём объект webdriver
        self.driver = webdriver.Chrome()
        # Разворачиваем окно на весь экран для корректного отображения элементов
        self.driver.maximize_window()
        # Создаём объект WebDriverWait
        self.wait = WebDriverWait(self.driver, 10)
        # Переходим на страницу регистрации
        go_to_registration_page(self.driver, self.wait)
        # Создаём объект регистрации
        self.registration = Registration

    def test_name(self, param_name):
        # Берём имя и ошибку, которая должна появиться при вводе невалидного имени
        # при expected_error = None - имя валидное, ошибки не ожидается
        (name, expected_error) = param_name

        # Вводим данные в форму
        self.registration.fill_form(self, name, VALID_LAST_NAME, VALID_EMAIL, VALID_PASSWORD)

        # Если регистрация должна пройти успешно
        if expected_error is None:
            try:
                assert self.driver.find_element(By.ID, "card-title").text == "Подтверждение email"
            except NoSuchElementException:
                # Ожидали заголовок "Подтверждение email", но элемента не оказалось на странице, тест не пройден
                assert False
            finally:
                # Возвращаемся к странице регистрации
                go_to_registration_page(self.driver, self.wait)
            # Если поля содержат некорректные данные, которые должны вызывать ошибку
        else:
            try:
                assert self.driver.find_element(By.XPATH, "//*[@id=\"page-right\"]/div/div[1]/div/form/div[1]/div[1]/span").text == expected_error
            except NoSuchElementException:
                # Ожидали ошибку, но её элемента не оказалось на странице, тест не пройден
                assert False
            finally:
                # Перезагружаем страницу, чтобы очистить поля
                self.driver.refresh()

    def test_last_name(self, param_last_name):
        # Берём фамилию и ошибку, которая должна появиться при вводе невалидной фамилии
        # при expected_error = None - фамилия валидная, ошибки не ожидается
        (last_name, expected_error) = param_last_name

        # Вводим данные в форму
        self.registration.fill_form(self, VALID_NAME, last_name, VALID_EMAIL, VALID_PASSWORD)

        # Если регистрация должна пройти успешно
        if expected_error is None:
            try:
                assert self.driver.find_element(By.ID, "card-title").text == "Подтверждение email"
            except NoSuchElementException:
                # Ожидали заголовок "Подтверждение email", но элемента не оказалось на странице, тест не пройден
                assert False
            finally:
                # Возвращаемся к странице регистрации
                go_to_registration_page(self.driver, self.wait)
        # Если поля содержат некорректные данные, которые должны вызывать ошибку
        else:
            try:
                assert self.driver.find_element(By.XPATH, "//*[@id=\"page-right\"]/div/div[1]/div/form/div[1]/div[2]/span").text == expected_error
            except NoSuchElementException:
                # Ожидали ошибку, но её элемента не оказалось на странице, тест не пройден
                assert False
            finally:
                # Перезагружаем страницу, чтобы очистить поля
                self.driver.refresh()

    def teardown_class(self):
        # После прохождения всех тестов закрываем webdriver
        self.driver.quit()
