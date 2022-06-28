from requests_html import HTMLSession
from bs4 import BeautifulSoup
from sympy import print_maple_code

from destinos.farmacias.Ahumada import *
from destinos.farmacias.Salcobrand import *
from destinos.farmacias.RedFarma import *

from csvOriented.Escritor import Escritor
from csvOriented.Medicamento import *
from destinos.BancoUF import *
from csvOriented.Escritor import *
import csv

url_ahumada = "https://www.farmaciasahumada.cl/catalogsearch/result/index/?p=1&q="
url_salcobrand = "https://salcobrand.cl/search_result?query="

with open('principios_activos.txt',encoding='utf8') as f:
    lines = f.readlines()
    

with open('out.csv', 'a', newline='',encoding='utf8') as f_object:  
            # Pass the CSV  file object to the writer() function
    writer_object = csv.writer(f_object)
    writer_object.writerow(["busqueda","farmacia","descripcion","precio_clp","precio_uf"])

abuscar = []
for line in lines:
    line = line.replace("\n","")
    line = line.replace(" ","+")
    abuscar.append(line)

print(abuscar)

uf = int(Banco().get_uf())

print("El valor actual del UF es: " + str(uf))




for busqueda in abuscar:


    print("busqueda de ahora = ", busqueda)
    paginas_ahumada = []
    paginas_salcobrand = []
    paginas_red = []

    url_ahumada = 'https://www.farmaciasahumada.cl/catalogsearch/result/index/?p='+str(1)+'&q=' + busqueda

    while True:
        f_ahumada = Ahumada(busqueda,url_ahumada) #crea un objeto de la clase Ahumada
        next_page = f_ahumada.getnextpage() #obtiene el url de la siguiente pagina
        if  next_page == False: #si no hay siguiente pagina, termina el ciclo
            break
        else:
            url_ahumada = next_page #si hay siguiente pagina, cambia el query
        paginas_ahumada.append(f_ahumada) #agrega el objeto a la lista de paginas de ahumada

    escritor_ahumada = Escritor(busqueda = busqueda,uf=uf,paginas = paginas_ahumada)
    
    escritor_ahumada.to_csv_ahumada()

    url_salcobrand = "https://salcobrand.cl/search_result?query=" + busqueda
    f_salcobrand= Salcobrand(busqueda=busqueda, url=url_salcobrand)
    paginas_salcobrand.append(f_salcobrand) 

    escritor_salcobrand= Escritor(busqueda=busqueda,uf=uf,paginas=paginas_salcobrand)
    escritor_salcobrand.to_csv_salcobrand()


    url_red = "https://www.redfarma.cl/productos/?nombre=" + busqueda + "&pagina=1"
    f_red = RedFarma(busqueda,url_red)
    paginas_red.append(f_red) 
    escritor_red= Escritor(busqueda=busqueda,uf=uf,paginas=paginas_red)

    numero  = 1

    while True:
        url_red = "https://www.redfarma.cl/productos/?nombre=" + busqueda + "&pagina="+str(numero)
        f_red = RedFarma(busqueda,url_red)
        this_page = f_red.is_valid_page() #oRevisa asi la pagina tiene items
        if  this_page: #si no hay siguiente pagina, termina el ciclo
            paginas_red.append(f_red)
            numero = numero + 1
        else:
            
            break

    escritor_red = Escritor(busqueda = busqueda,uf=uf,paginas = paginas_red)
    escritor_red.to_csv_red()
    print("TERMINE RED")











# ######
#     print("TERMINE AHUMADA")



print("TERMINE")