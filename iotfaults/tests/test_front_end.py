# -*- coding: utf-8 -*-
import random
from unittest import TestCase
import time
import sys
from selenium import webdriver
import os

class FunctionalTest(TestCase):

    # def setUp(self):
    #     self.browser= webdriver.Chrome('/opt/google/chrome/chromedriver')
    #     self.baseUrl = 'https://' + os.environ["C9_HOSTNAME"]
        # self.nombreUsuario = 'usuarioprueba' + str(random.randint(1, 9999999))
        # self.nombre = 'Usuario Prueba'
        # self.password = 'agiles123'

    def test_index(self):
        pass
        # Crear el usuario
        # self.browser.get(self.baseUrl)
        # self.browser.implicitly_wait(10)
        # self.assertIn('Laboratorio Uniandes', self.browser.title)
        # link = self.browser.find_element_by_id('link_registrar_usuario')
        # link.click()

        # element = self.browser.find_element_by_id('username')
        # element.send_keys(self.nombreUsuario)

        # element = self.browser.find_element_by_id('first_name')
        # element.send_keys(self.nombre)

        # element = self.browser.find_element_by_id('last_name')
        # element.send_keys('Prueba')

        # element = self.browser.find_element_by_id('email')
        # element.send_keys('jd.patino1@uniandes.edu.co')

        # element = self.browser.find_element_by_id('password')
        # element.send_keys(self.password)

        # element = self.browser.find_element_by_id('password2')
        # element.send_keys(self.password)

        # botonGuardar = self.browser.find_element_by_id('btn_guardar')
        # botonGuardar.click()
        # self.browser.implicitly_wait(3)
        # time.sleep(2)

        # # Regresar a la pagina principal
        # linkRegresar = self.browser.find_element_by_id('link_regresar')
        # linkRegresar.click()
        # self.browser.implicitly_wait(10)
        # self.assertIn('Laboratorio Uniandes', self.browser.title)

        # # Iniciar Sesion
        # time.sleep(2)
        # link = self.browser.find_element_by_id('link_iniciar_sesion')
        # link.click()
        # self.browser.implicitly_wait(3)

        # element = self.browser.find_element_by_id('username')
        # element.send_keys(self.nombreUsuario)

        # clave = self.browser.find_element_by_id('password')
        # clave.send_keys(self.password)

        # btn = self.browser.find_element_by_id('btn_iniciar_sesion')
        # btn.click()
        # self.browser.implicitly_wait(10)
        # self.assertIn('Laboratorio Uniandes', self.browser.title)

        # time.sleep(2)
        # element = self.browser.find_element_by_id('nombre_usuario')
        # self.assertIn(self.nombre, element.text)
        