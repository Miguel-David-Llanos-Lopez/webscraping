from bs4 import BeautifulSoup as bs
import pandas as pd
import lxml
import pymysql

import requests

titulos_libros = []
precios_libros = []
url_libros = []

url = "https://cuspide.com/100-mas-vendidos/"
response = requests.get(url)

libros = bs(response.content, "html.parser")
titulo = libros.find_all(class_="name product-title woocommerce-loop-product__title")
precio = libros.find_all(class_="price")
error_url = []
error_titulo = []

for i, j in zip(titulo,precio):
    try:
        titulo_ = i.find("a").get_text(strip = True)
        url_ = i.find("a").get("href")
        precio_ = j.find("bdi").get_text(strip=True).replace("$","").replace(".","").replace(",",".")
        
        url_libros.append(url_)
        precios_libros.append(float(precio_))
        titulos_libros.append(titulo_)
    except AttributeError:
        error_titulo.append(i.find("a").get_text(strip = True))
        error_url.append(i.find("a").get("href"))


datos = {'titulo':titulos_libros, 'url':url_libros, 'precio':precios_libros}
datos_errores = {'titulo':error_titulo, 'url':error_url}
df_errores = pd.DataFrame(datos_errores)
df = pd.DataFrame(datos)

url2 = "https://www.xe.com/es/currencyconverter/convert/?Amount=1&From=USD&To=ARS"
response2 = requests.get(url2)
dolares = bs(response2.content, "html.parser")
dolar_a_arg = dolares.find(class_="sc-295edd9f-1 jqMUXt").get_text().replace(",",".").split(" ")
dolar_a_arg = float(dolar_a_arg[0])

df["precio en dolares"] = round(df["precio"] / dolar_a_arg, 2)
print(dolar_a_arg)
print(df)
print(df_errores)

conexcion = 'mysql+mysqlconnector://root:root1234@localhost/webscrapping_cuspide'
df.to_sql(name='webscraping', con=conexcion, if_exists="replace", index=False)
df_errores.to_sql(name='errores_webscraping', con=conexcion, if_exists="replace", index=False)