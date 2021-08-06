# Proyecto 3 BDII

_Proyecto de Face Recognition_

### Objetivos

_Construir una plafaroma en donde busques imágenes similares a una imagen de tu elección._
_La imagen de input puede ser cualquiera que siga el formato._
_La imagen de output va a ser una de las imagenes dentro de la base de datos._

### Estructura: índice RTree

_Primero se leen las imagenes y se obtienen arrays de los vectores característicos de estas._
_Estos arrays lo metemos en un diccionario el cual va estar ordenado por el nombre de las personas para luego poder procesarlo en disco._

<img src="https://cdn.discordapp.com/attachments/841118704547659797/873079711553683477/unknown.png" height="100">

_Las imágenes van a ser guardadas en un RTree._

_Lo que hace un Rtree es ubicar valores de 2 a más dimensiones en su estructura de manera espacial y según las "coordenadas" de sus puntos.
Sin embargo, ahora tenemos vectores con 128 dimensiones, por lo que utilizar un rtree convencional no es una opción._

_Entonces usaremos una colección de rtrees y dividiremos el vector de 128 valores de cada imagen en grupos de 2._

_Cada rtree analizará estas parejas de "coordenadas" y podremos hacer las consultas respectivas, y estos rtrees devolverán la información únicamente tomando en cuenta estas dos coordenadas_

* Contenido de RTrees <br />

<img src="https://cdn.discordapp.com/attachments/841118704547659797/873081201894768640/unknown.png" height="100">

_Luego de hacer las consultas, tendremos k respuestas por cada rtree que tengamos_

_En el backend lo que mapeamos cuántas veces se repite esto y se arma un ránking de los k valores o k imágenes que más se hayan repetido_

<img src = "https://cdn.discordapp.com/attachments/841118704547659797/873083696041824327/unknown.png" height="100">

<img src="https://cdn.discordapp.com/attachments/841118704547659797/873083565460570122/unknown.png" height="200">

_Se utilizó la Librería https://rtree.readthedocs.io/en/latest/ para realizar los rtree_


### Técnicas de busqueda por similitud a utilizar


_Se utilizarán los siguientes algoritmos para la busqueda por similitud:_
* Algoritmo de búsqueda KNN
* Algoritmo de búsqueda por rango

#### Algoritmo KNN
##### KNN RTree
_Llamas a N imágenes más similares utilizando la estructura de los Rtrees_ 

##### KNN Secuencial
_Primero iteramos por cada Vector Carácterístico de cada imágen y le asignamos un Score a cada uno._

_El Score es calculado a partir de La distancia euclediana del vector característico de la imágen de input y el resto de vectores característicos._

_Se ordenan todos los scores de menor a mayor_

_Se obtienen las imagenes de los n primeros Scores_

#### Algoritmo de búsqueda por rango

_Se calcula el Score de cada imágen._

_Se asigna un valor de radio._

_Se obtienen todas las imágenes que tengan un Score menor al Radio_


### Análisis

_Las siguientes pruebas se realizarán con la imagen mateo.jpg_

* Se realizará una busqueda de las 8 imágenes más cercanas.
* Donde N = Número de imágenes en la colección:

| Tiempo(s)     | KNN-RTree     | KNN-Secuencial  |
| ------------- |:-------------:| -----:          |
| N = 100       | 3.9572        | 4.3598          |
| N = 200       | 4.3071        | 4.0087          |
| N = 400       | 3.9692        | 4.0960          |
| N = 800       | 3.9818        | 4.3787          |
| N = 1600      | 4.1173        | 4.3265          |
| N = 3200      | 4.2010        | 4.8141          |
| N = 6400      | 4.0116        | 4.8795          |
| N = 12800     | 4.1451        | 5.0317          |

* Busqueda por rango, datos = 13171

| Radio         | Cantidad de valores| 
| ------------- |:-------------:     | 
| 0.7           | 249                | 
| 0.8           | 2982               | 
| 0.9           | 9931               | 
| 1             | 13002              | 
