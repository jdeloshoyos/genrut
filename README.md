# genrut
Script en Python 3, es capaz de validar un RUT chileno, o generar uno o múltiples RUTs válidos, opcionalmente con "identidades" ficticias asociadas

Se acompaña el script con tres archivos, que contienen nombres (masculinos y femeninos) y apellidos para la generación de "identidades" ficticias. Se puede sustituir estos archivos por otros que contengan otros ejemplos, en el mismo formato.

Usar 'genrut.py --help' para ver las posibles opciones del programa:

Uso: genrut.py [-h] [-i lim_inf] [-s lim_sup] [-c numero_ruts]
                 [-v rut_a_validar] [-n]

Genera un listado de RUTs chilenos validos, con digito verificador. Uso:
genrut.py [opciones]

Argumentos opcionales:
  -h, --help            Muestra la ayuda del programa
  -i lim_inf, --inf lim_inf
                        Opcional. Especifica el limite inferior de numero de
                        RUT generado (5000000 por omision).
  -s lim_sup, --sup lim_sup
                        Opcional. Especifica el limite superior de numero de
                        RUT generado (25000000 por omision).
  -c numero_ruts, --cantidad numero_ruts
                        Opcional. Especifica la cantidad de RUTs a generar (1
                        por omision).
  -v rut_a_validar, --validar rut_a_validar
                        Opcional. Especifica un RUT (sin DV) y devuelve el
                        mismo, incluyendo su DV.
  -n, --nombres         Opcional. Genera sexo, edad y nombres ademas de los
                        RUTs, separados por tabs.
                        
Ejemplos:

Validar el RUT 12345678:
> genrut.py -v 12345678
Resultado: Devuelve 12345678-5

Generar 10 RUTs válidos, entre 5000000 y 25000000 (valores por defecto):
> genrut.py -c 10

Generar 100 RUTs válidos, entre 6000000 y 10000000, con una "identidad" ficticia asociada, en formato .CSV:
> genrut.py -i 6000000 -s 10000000 -c 100 -n

El output de este script es direccionable a un archivo de texto de manera estándar; para capturar los resultados del último ejemplo a un archivo identidades.txt, por ejemplo:
> genrut.py -i 6000000 -s 10000000 -c 100 -n > identidades.txt
