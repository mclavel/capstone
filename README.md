# Capstone
**ICS2122 - Grupo 5**
2018-01
# Indicaciones
El código fue realizado y utilizado en Python 2.7 y 3.6.(Recomendamos correrlo en 3.6)
 Las Librerías utilizadas fueron:
````
-gurobi
-copy
-csv
-numpy
-matplotlib
-time
-os
````
Para clonar el repositorio:
````
-git clone https://github.com/nlvargas/capstone.git
````
Para instalar una librería:
````
-pip install #libreria
````
Para ejecutar una instancia de simulación, en la linea de comando:
````
-py algorithm.py
````
Al correr el comando se escribirán los archivos ````calendario.csv```` y ````tabla_final.csv```` en la carpeta donde está ubicado el código, los documentos son excel,s en donde
estan todos los partidos calendarizados con sus resultados y la tabla final. Para analizarlos recomendamos altamente usar el filtro  de datos de Excel

Finalmente los outputs de gurobi están desabilitados para activarlos se deben comentar la linea 17 de ````min_var.py```` y la linea  61 de ````schedueling.py````. 
````
m.setParam('OutputFlag', 0)
````
# Módulos
- Algorithm: Contiene el algortimo de calendarización de trabajo.
- Data_scrapper: Código utilizado para extraer informacion de AS.com
- Equipos: Esta definido la clase Equipo y los datos de geografía y presupuesto de cada institución
- Schedueling: Contiene todo lo relacionado con calendarizacion, tal como las Fechas y Partidos. Aquí se encuentra el modelo de optimización para obtener las primeras 15 fechas.
- Simulation: Contiene la clase Simulación, aqui se puede ver en detalle como se simula y como se calculan los eventos.
- Montecarlo: Contiene la clase que crea simulaciones montecarlo, utilizamos este código para analizar parámetros y tendencias
- Min_var: Modelo de optimización que calendariza fechas minimizando la amplitud de la tabla pero que se castiga segun la probabilidad de ocurrencia del calendario.