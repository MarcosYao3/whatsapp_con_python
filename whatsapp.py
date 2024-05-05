from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, ElementNotInteractableException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
import pyautogui
import time

class Whatsapp:
    def __init__(self):
        self.wa_url = 'https://web.whatsapp.com/'
        self.driver = webdriver.Chrome()
        self.elemento_caja_busca = '//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div[1]/p'
        self.elemento_flecha_retroceder = '//*[@id="side"]/div[1]/div/div[2]/button/div[2]/span'
                                         # //*[@id="side"]/div[1]/div/div[2]/button/div[2]/span
        # self.elemento_menu = '//*[@id="main"]/header/div[3]/div/div[2]/div/div/span'
        self.elemento_menu = '//span[@data-icon="menu" and contains(@class, "xr9ek0c")]'
        # //*[@id="main"]/header/div[3]/div/div[4]/div/div/span
        self.element_cerrar_chat = '//*[@id="app"]/div/span[5]/div/ul/div/div/li[3]/div'
        self.objeto_boton_enviar_mensaje = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span'
        self.elemento_boton_enviar_imagen = '//*[@id="app"]/div/div[2]/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div/span'
        self.elemento_boton_adjuntar = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div/div/div/div/span'
        self.elemento_fotos_y_video = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div/div/span/div/ul/div/div[2]/li/div/span'
        self.chat_area = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p'
                        # //*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p
        self.flecha_regresar = '//*[@id="side"]/div[1]/div/div[2]/button/div[2]/span'
        self.encabezado_contacto_abierto = '//*[@id="main"]/header/div[2]/div[1]'


    def esperar_login(self):
        se_inicio = False
        while not se_inicio:
            try:
                foto_perfil = self.driver.find_element(By.XPATH, "//div[@aria-label='foto del perfil']")
            except NoSuchElementException:
                pass
            else:
                se_inicio = True
        print("Se a inicialisado WhatsApp")
    def iniciar_whatsapp(self):
        print("Esperando hacer Login")
        self.driver = webdriver.Chrome()
        self.driver.get(self.wa_url)
        self.esperar_login()

    def cerrar_whatsapp(self):
        self.driver.quit()

    def enviar_mensaje(self, contacto, mensaje):
        self.buscar_contacto(contacto)
        try:
            chat_area = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, self.chat_area)))
        except NoSuchElementException:
            print("no se pudo encontra rl area de chat")
            raise NoSuchElementException
        except TimeoutException:
            print("se acabo el tiemo excepcion")
            raise TimeoutException
        chat_area.send_keys(mensaje)
        enter_si = False
        while not enter_si:
            try:
                chat_area.send_keys(Keys.ENTER)
                enter_si = True
            except:
                print("fallo en enviar enter")
                chat_area = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.XPATH, self.chat_area)))
        self.cerrrar_chat()

    def enviar_imagen(self, contacto, ruta):
        # Lo ideal
        # 1. buscar y abrir contacto
        # 2. borrar busqueda (dar click en la flecha retroceder)
        # 3. Proceder enviar imagen
        # 4. Cerrar chat

        # Buscar contacto
        try:
            self.buscar_contacto(contacto)
        except:
            print("enviar_imagen, error al ejecutar la funcion buscar contacto")
            return None
        # Enviar imagen
        # Buscamso y damos click en el boton adjuntar, levantamos una excepcion que tendremos que manenar en
        # el siguiente nivel
        try:
            boton_adjuntar = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, self.elemento_boton_adjuntar)))
            self.click(boton_adjuntar)
        except:
            print("Enviar imagen, no se puddo encontrar o hacer click al botona adjuntar")
            raise NoSuchElementException

        # Busar y dar click al elemento "imagenes y video", levantamos una excepción si ocurre un error
        # y lo manejamos en el siguiente nivel
        try:
            imagenes_video = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, self.elemento_fotos_y_video)))
            imagenes_video.click()
        except:
            print("Enviar imagenes, no se pudo enocntrar o hacer click en el elemento imagenes y video")
            raise NoSuchElementException

        time.sleep(2)  # Da tiempo para que se abra el cuadro de diálogo
        pyautogui.write(ruta)  # Escribe la ruta al archivo
        pyautogui.press('enter')  # Presiona 'enter' para subir el archivo

        try:
            boton_enviar = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, self.elemento_boton_enviar_imagen)))
            boton_enviar.click()
        except:
            print("Enviar imagen, no se pudo encontrar o hacer click en el boton 'Enviar imagen'")
            raise NoSuchElementException

        # Cerramos el chat
        self.cerrrar_chat()

    def click(self, boton):
        se_hizo_click = False
        while not se_hizo_click:
            try:
                boton.click()
            except ElementClickInterceptedException:
                print("ElementClickInterceptedException, intentando otra vez")
                time.sleep(0.5)
            else:
                se_hizo_click = True


    def buscar_contacto(self, contacto):
        # Ubicar la caja de texto donde esribimos nuestra busqueda
        try:
            caja_busqueda = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, self.elemento_caja_busca)))
        except:
            # Si no se encuentra el elemento mandamos levantamos una excepcion para despues
            # manejarla en el nivel que sigue
            print("Enviar imagen, error al ubicar la caja de busqueda")
            raise NoSuchElementException

        caja_busqueda.send_keys(contacto)
        caja_busqueda.send_keys(Keys.ENTER)
        try:
            flecha_retroceder = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, self.elemento_flecha_retroceder)))
            flecha_retroceder.click()
        except:
            print("buscar contacto, no se pudo encontrar o hacer click la flehca de retroceder")


    def cerrrar_chat(self):
        try:
            menu = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, self.elemento_menu)))
        except NoSuchElementException:
            print("carrar_chat, no se pudo encontrar el elemento menu")
            raise NoSuchElementException

        menu.click()
        try:
            cerar_chat = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, self.element_cerrar_chat)))
            cerar_chat.click()
        except NoSuchElementException:
            print("cerrar_chat, no se pudo encontrar cerrar chat")
            raise NoSuchElementException
        except ElementNotInteractableException:
            print("Elemento no interactuable al momento")
            raise ElementNotInteractableException

    def leer_mensaje(self, contacto, numero):
        """
        Notas:
        selenium si detecta los saltos de linea de los mensajes
        """

        todos_mensajes = ''
        self.buscar_contacto(contacto)
        # Espera hasta que los mensajes sean visibles
        try:
            messages = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'message-in')]")))
        except:
            print("funcion leer mensaje no se pudieron encontrar los mensajes")
        # Reducir la lista con el numero indicado para solo leer los últimos
        lista_recucida = messages[-numero:]
        for mensaje in lista_recucida:
            separar = mensaje.text.split('\n')
            separar.pop()
            mensaje = " ".join(separar)
            todos_mensajes = todos_mensajes + mensaje + " "
        self.cerrrar_chat()
        return todos_mensajes


    def lista_mensajes_nuevos(self):
        contactos_con_nuevo_mensaje = []
        contactos_con_nuevo_mensaje_2 = []
        try:
            contactos_con_nuevo_mensaje = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@aria-label, 'mensajes no leídos')]")))
        except:
            print("No se pudo obtener lista de contactos con mensajes no leídos")

        try:
            contactos_con_nuevo_mensaje_2 = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@aria-label, 'mensaje no leído')]")))
        except:
            print("No se pudo encontrar lista de contactos con un mensaje no leído")
        contactos_con_nuevo_mensaje += contactos_con_nuevo_mensaje_2
        print(f"Contactos con un nuevo mensaje: {len(contactos_con_nuevo_mensaje)}\n")
        return contactos_con_nuevo_mensaje

    def mensajes_no_leidos(self, lista):
        lista_informacion = []
        for i in lista:
            try:
                elemento_padre = i.find_element(By.XPATH, '../../../../..')
            except:
                print(f"No se pudieron encontra los elementos de {i}")
                continue
            lista_texto = elemento_padre.text.split("\n")
            if len(lista_texto) > 4:
                concatenado = lista_texto[2] + lista_texto[3] + lista_texto[4]
                lista_texto = [lista_texto[0], lista_texto[1], concatenado, lista_texto[5]]
            dic = {"nombre": lista_texto[0], "hora": lista_texto[1], "ultimo": lista_texto[2],
                    "numero": int(lista_texto[3])}
            lista_informacion.append(dic)
        return (lista_informacion)


# Establecer un proceso par responder mensajes

# Obtener lista de contactos con mensaje
# Definir a que mensaje responder solamente

    def responder_mensajes(self, *args):
        # Obtener lista de contactos con mensaje
        # Nota: La funcion "mensajes_no_leidos necesita una lista de elementos web
        # La cual la proporcionamos po medio de la funico "lista_mensajes_nuevos""
        lista_contactos = self.mensajes_no_leidos(self.lista_mensajes_nuevos())
        for el in lista_contactos:
            print("\n")
            print(el)

        # 1. Rescatar nombre de cada lista
        # 2. Comprobar con un





