#! /usr/bin/python3
# Encoding: UTF-8

# Generador de RUTs chilenos. Genera la cantidad especificada de RUTs chilenos válidos (1 por defecto).
# Opcionalmente se puede especificar un rango numérico entre el cual generar RUTs, por defecto
# genera entre 5000000 y 25000000.
# (c) Junio 2013 por Jaime de los Hoyos M. Liberado bajo la licencia MIT: http://www.opensource.org/licenses/mit-license.php

# v1.0: Versión inicial, con generador y validador
# v1.1: Agrega generador de nombres y fechas de nacimiento

import sys
import random
import datetime
import argparse

separador="\t"  # Separador de campos en caso de usar la opción de generación de nombres

def formatoFechaHora(fecha):
    # Regresa la fecha pasada como parámetro (p. ej., datetime.datetime.today()) sin microsegundos
    return fecha.strftime("%Y-%m-%d %H:%M:%S")
    
def formatoFecha(fecha):
    # Regresa la fecha pasada como parámetro (p. ej., datetime.datetime.today()), sin hora (formato dd-mm-aaaa)
    return fecha.strftime("%d-%m-%Y")
    
def calculaDV(rut):
    # Calcula el dígito verificador válido para un RUT
    rut_str=str(rut)[::-1]  # Invierte el string! Ver http://stackoverflow.com/questions/931092/reverse-a-string-in-python
    
    # Variables para el cálculo
    multiplicador=2
    suma=0
    
    for c in rut_str:
        # Iteramos sobre todos los caracteres del RUT ya invertido, sumando los dígitos * el multiplicador
        suma+=int(c)*multiplicador
        multiplicador+=1
        if multiplicador>7:
            multiplicador=2
        
    dv=str(11-(suma%11))  # 11 - Módulo
    
    # Excepciones
    if dv=='11':
        dv='0'
    if dv=='10':
        dv='K'
        
    return dv
    
def generaRut(rango_inf, rango_sup):
    # Genera un rut válido entre los rangos especificados
    # random.seed()     # No hace falta. Al importar el módulo, se hace esto automáticamente.
    rut=random.randint(rango_inf, rango_sup)
    dv=calculaDV(rut)
    res=str(rut)+'-'+dv
    
    return res
    
def calculaEdad(rut):
    # Cálculo de fecha de nacimiento. Se tomará como fecha de hoy el límite superior de RUT, para que no queden
    # fechas de nacimiento a futuro al momento de ser generadas.
    
    rut=int(rut[0:-2])   # Quitamos los dos últimos caracteres (guión y separador) y lo pasamos a un entero
    
    hoy=datetime.datetime.today()
    nacs_por_dia=900    # Cantidad arbitraria, para estimar cuántos RUTs se generan a diario.
    
    fecha_nac=(hoy-datetime.timedelta(days=(args.sup-rut)/nacs_por_dia))
    
    return formatoFecha(fecha_nac)+separador
    
def generaNombre():
    # Genera un nombre a partir de las listas cargadas
    # Determinación de sexo
    sexo=random.randint(0, 1)
    if sexo==0:
        nombre="M"+separador
        lista_nombres=nombres_masc
    else:
        nombre="F"+separador
        lista_nombres=nombres_fem
    
    # Elegimos dos nombres, de acuerdo al sexo. No pueden coincidir.
    recuento=len(lista_nombres)
    idx_primer_nombre=random.randint(0, recuento-1)
    while True:
        idx_segundo_nombre=random.randint(0, recuento-1)
        if idx_segundo_nombre!=idx_primer_nombre:
            break
    nombre+=lista_nombres[idx_primer_nombre]+separador+lista_nombres[idx_segundo_nombre]+separador
    
    # Ahora dos apellidos. Estos sí pueden coincidir.
    recuento=len(apellidos)
    idx_primer_apellido=random.randint(0, recuento-1)
    idx_segundo_apellido=random.randint(0, recuento-1)
    nombre+=apellidos[idx_primer_apellido]+separador+apellidos[idx_segundo_apellido]+separador
    
    return nombre
    
# Manejo de opciones de línea de comando
parser=argparse.ArgumentParser(description="""\
Genera un listado de RUTs chilenos validos, con digito verificador.

Uso: genrut.py [opciones]

""")
    
parser.add_argument('-i', '--inf',
    type=int, action='store', dest="inf", metavar='lim_inf', default=5000000,
    help="Opcional. Especifica el limite inferior de numero de RUT generado (5000000 por omision).")
parser.add_argument('-s', '--sup',
    type=int, action='store', dest="sup", metavar='lim_sup', default=25000000,
    help="Opcional. Especifica el limite superior de numero de RUT generado (25000000 por omision).")
parser.add_argument('-c', '--cantidad',
    type=int, action='store', dest="cantidad", metavar='numero_ruts', default=1,
    help="Opcional. Especifica la cantidad de RUTs a generar (1 por omision).")
parser.add_argument('-v', '--validar',
    type=int, action='store', dest="validar", metavar='rut_a_validar', default=0,
    help="Opcional. Especifica un RUT (sin DV) y devuelve el mismo, incluyendo su DV.")
parser.add_argument('-n', '--nombres', action='store_true',
    dest='nombres', default=False,
    help="Opcional. Genera sexo, edad y nombres ademas de los RUTs, separados por tabs.")

args = parser.parse_args()

# Si se pasó un RUT para validar, se hace de inmediato y se termina.
if args.validar>0:
    dv=calculaDV(args.validar)
    print (args.validar, "-", dv, sep="")
    sys.exit(0)
    
# Validaciones de parámetros
if args.inf<1000000 or args.sup<1000000:
    # Falta algún parámetro obligatorio
    print ('ERROR: Tanto el limite inferior como el superior deben ser igual o mayor a 1000000.')
    sys.exit(1)
    
if args.inf>=args.sup:
    print ('ERROR: El limite superior debe ser mayor al inferior.')
    sys.exit(1)
    
if args.cantidad<1:
    print ('ERROR: La cantidad de RUTs a generar debe ser mayor o igual a 1.')
    sys.exit(1)
    
# Si se especificó generación de nombres, cargamos los listados de nombres en memoria.
if args.nombres:
    try:
        with open("genrut_nombres_masc.txt") as f:
            nombres_masc = [line.rstrip() for line in f]
            
        with open("genrut_nombres_fem.txt") as f:
            nombres_fem = [line.rstrip() for line in f]
            
        with open("genrut_apellidos.txt") as f:
            apellidos = [line.rstrip() for line in f]
            
    except:
        print ("ERROR: Fallo al intentar leer archivos de nombres/apellidos.")
        sys.exit(1)
        
# Ciclo principal
for i in range(args.cantidad):
    rut=generaRut(args.inf, args.sup)
    if args.nombres:
        rut=generaNombre()+calculaEdad(rut)+rut
    print (rut)
