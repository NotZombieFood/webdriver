from selenium import webdriver 

class Chrome:
    def __init__(self, headless = False):
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notificactions") # Quita que una pagina entregue notificaciones
        options.add_argument("--disable-geolocation") # Quita que se pueda usar ubicacion
        options.add_argument("--disable-media-stream") # Quita que pueda usarse el mic
        options.add_argument("--disable-extensions") # No extensiones
        # Pass the argument 1 to allow and 2 to block
        options.add_experimental_option("prefs", { 
            "profile.default_content_setting_values.notifications": 1 
        })
        options.add_argument("window-size=1400,600")
        if headless:
            options.add_argument("--headless")
        # Para instalar el webdriver se tiene que ir a esta pagina: https://chromedriver.storage.googleapis.com/index.html?path=92.0.4515.107/
        self.driver = webdriver.Chrome(chrome_options=options, executable_path=r'C:\webdriver\chromedriver.exe') 

    def clean_up(self):
        """
            Limpiar los cookies por si las dudas.
        """
        self.driver.delete_all_cookies()

import time

def download_cute_dogs():
    website = "https://www.reddit.com/r/Awww/" # Este es sincrono, entoncees espera al loading
    browser = Chrome()
    browser.clean_up()
    browser.driver.get(website)
    browser.driver.fullscreen_window()
    top_button = browser.driver.find_element_by_link_text("Top") # Va a buscar cualquier link que tenga la palabra top
    top_button.click()
    browser.driver.implicitly_wait(2) # Agregar un delay para poder esperar a que cargue (es super util para hacer search y que espere un poco m[as si no encuentra nada)
    sort_picker = browser.driver.find_element_by_id("TimeSort--SortPicker") # usandi el id del elemento de html
    sort_picker.click() # lo clickeamos
    menu_items = browser.driver.find_elements_by_css_selector('a[role="menuitem"]') # Vamos a obtener todos los elementos de menu item. Tag es A con attributo role y valor menuitem
    # <a role="menuitem" href="/r/Awww/top/?t=day"><span class="_2-cXnP74241WI7fpcpfPmg">Today</span></a>
    for menu_item in menu_items:
        if menu_item.text.lower() == "all time": # podemos obtener el texto dentro de un tag
            menu_item.click() 

    adds  = browser.driver.find_elements_by_class_name("promotedlink") # podemos agarrar elementos por clase de html
    for add in adds: 
        browser.driver.execute_script("""
            var element = arguments[0];
            element.parentNode.removeChild(element);
            """, add) # y usar una funcion as[i para borrarlos
    browser.driver.execute_script('console.log("cute doggy")') # se puede correr codigo de js para interactuar con el sitio
    cute_dogs_search = browser.driver.find_elements_by_css_selector('img[alt="Post image"]') # <img alt="Post image" src="image.jpeg"> Ese seria lo mismo que las siguientes lineas
    images = browser.driver.find_elements_by_tag_name("img")
    cute_dogs = []
    for image in images:
        if image.get_attribute("alt") == "Post image": # Obtener un attributo de un elemento:
            cute_dogs.append(image.get_attribute("src")) # Podemos hacer lo mismo para obtener la imagen, el truco es siempre sacar src para imagenes y href para links
    for doggy in cute_dogs:
        browser.driver.get(doggy) 
        time.sleep(5) # no se puede usar implicit wait porque ese es solo para esperar a que cargue el DOM 
    import pdb; pdb.set_trace()
    # un pdb solo para que no muera 
    browser.driver.close()

download_cute_dogs()