from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class Registration:
    def fill_form(self, name, last_name, emai_address, password):
        # Ждём загрузки страницы
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"page-right\"]/div/div[1]/div/form/button")))
        # Вводим имя
        self.driver.find_element(By.NAME, "firstName").send_keys(name)
        # Вводим валидную фамилию
        self.driver.find_element(By.NAME, "lastName").send_keys(last_name)
        # Вводим email
        self.driver.find_element(By.ID, "address").send_keys(emai_address)
        # Вводим пароль
        self.driver.find_element(By.NAME, "password").send_keys(password)
        # Подтверждаем пароль
        self.driver.find_element(By.NAME, "password-confirm").send_keys(password)
        # Нажимаем кнопку "Зарегистрироваться"
        self.driver.find_element(By.XPATH, "//*[@id=\"page-right\"]/div/div[1]/div/form/button").click()
