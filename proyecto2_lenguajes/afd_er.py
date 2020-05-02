import os
import tkinter as tk
from tkinter import filedialog

import ntpath
ntpath.basename("a/b/c")

# cosas globales
# ------------------------------carga de archivos-------------------------------------
# crear la gui
root = tk.Tk()
# especifica que no se abra toda
root.withdraw()

# Abre el explorador de archivos y retorna la ruta del archivo seleccionado
def cargarArchivo():
    file = filedialog.askopenfilename(initialdir="/Desktop", title="Selecciona un archivo",
                                      filetypes=(("Gramaticas", "*.grm"),
                                                 ("Automata Finito Determinista", "*.afd"), ("all files", "*.*")))
    return file

# obtiene el contenido del archivo
def obtenerTexto(ruta):
    file_contenido = ""
    with open(ruta, 'r') as file:
        file_contenido = file.read()
        
    return file_contenido

# metodo que retorna el nombre del archivo

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

# AFD
coleccion_afds = {}

# ER
coleccion_grs = {}

def limpiar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def info_est():
    print('''
          ------------------------------------------------
          Lenguajes Formales y de Programación
          Sección B-
          201801043
          ------------------------------------------------
          ''')

def menu_principal():
    limpiar_terminal()

    #print(coleccion_afds)
    print(coleccion_grs)
    print('+-----------------------------------+')
    print('|           MENÚ PRINCIPAL          |')
    print('+-----------------------------------+')
    print('')
    print('1. Crear AFD')
    print('2. Crear Gramática')
    print('3. Evaluar cadena')
    print('4. Reportes')
    print('5. Cargar archivo de entrada (AFD Y GRAMÁTICAS)')
    print('6. Crear Autómata de pila')
    print('7. Salir')
    print('')

    eleccion = input('Por favor, elige una opción: >> ')

    if eleccion == '1':
        nombreAFD = input('Por favor, ingresa un nombre para el AFD: ')
        
        for key, contenido in coleccion_afds.items():
            if key == nombreAFD:
                limpiar_terminal()
                menu_AFD(nombreAFD, contenido[0], contenido[1], contenido[2], contenido[3], contenido[4])
            else:
                limpiar_terminal()
                menu_AFD(nombreAFD)

    elif eleccion == '2':
        nombreGR = input('Por favor, ingresa un nombre para la GR: ')
        
        for key, contenido in coleccion_grs.items():
            if key == nombreGR:
                limpiar_terminal()
                menu_GR(nombreGR, contenido[0], contenido[1], contenido[2], contenido[3], contenido[4])
            else:
                limpiar_terminal()
                menu_GR(nombreGR)

    elif eleccion == '3':
        pass
    elif eleccion == '4':
        menu_reportes()
    elif eleccion == '5':
        menu_cargarArchivo()
        # print(coleccion_afds)
        menu_principal()
    elif eleccion == '6':
        from proyecto2 import menu_automataPila
        menu_automataPila()
        menu_principal()
    elif eleccion == '7':
        exit()
    else:
        limpiar_terminal()
        print('Entrada inválida.')
        menu_principal()

def menu_AFD(nombre_afd, estados=[], alfabeto=[], estado_inicial='', aceptacion=[], transiciones=[]):

    limpiar_terminal()

    aux_estados = estados
    aux_alfabeto = alfabeto
    aux_inicial = estado_inicial
    aux_aceptacion = aceptacion
    aux_transiciones = transiciones
    
    #print('Estados en menu AFD --> ', aux_estados)
    # print(aux_estados)

    # print(lista_estados)

    print('+-----------------------------------+')
    print('|              MENÚ AFD             |')
    print('+-----------------------------------+')
    print('')
    print('1. Ingresar estados')
    print('2. Ingresar alfabeto')
    print('3. Estado inicial')
    print('4. Estados de aceptación')
    print('5. Transiciones')
    print('6. Ayuda')
    print('7. Regresar al menú principal')
    print('')

    eleccion = input('Por favor, escoge una opción: >> ')

    if eleccion == '1':  # estados
        aux_estados = estados_afd()
        menu_AFD(nombre_afd, aux_estados, aux_alfabeto,
                 aux_inicial, aux_aceptacion)

    elif eleccion == '2':  # alfabeto
        aux_alfabeto = alfabeto_afd()
        menu_AFD(nombre_afd, aux_estados, aux_alfabeto,
                 aux_inicial, aux_aceptacion)

    elif eleccion == '3':  # estado iniclal
        limpiar_terminal()

        aux_inicial = inicial(aux_estados)

        if aux_inicial == 1:
            print('Aún no se han creado estados.')
            # limpiar_terminal()
            menu_AFD(nombre_afd, aux_estados, aux_alfabeto)
        elif aux_inicial == 2:
            print('El estado ingresado no existe.')
            menu_AFD(nombre_afd, aux_estados, aux_alfabeto)
        else:
            limpiar_terminal()
            menu_AFD(nombre_afd, aux_estados, aux_alfabeto,
                     aux_inicial, aux_transiciones)

        """ if len(aux_estados) == 0:
            print('Aún no se han creado estados.')
            menu_AFD(nombre_afd, aux_estados, aux_alfabeto, aux_inicial, aux_aceptacion)
        else:
            print('Estados disponibles --> ', aux_estados)
            estado_inicial = input('Por favor, escoge uno de los estados previamente establecidos: ').upper()
            
            if estado_inicial not in estados:
                print('El estado ingresado no existe')
                menu_AFD(nombre_afd, aux_estados, aux_alfabeto, aux_inicial, aux_aceptacion)
            else:
                aux_inicial = estado_inicial
                menu_AFD(nombre_afd, estados, alfabeto, aux_inicial, aux_aceptacion)"""

    elif eleccion == '4':  # estados de aceptación
        limpiar_terminal()

        if len(aux_estados) == 0:
            print('Aún no se han creado estados')
            menu_AFD(nombre_afd, aux_estados, aux_alfabeto,
                     aux_inicial, aux_aceptacion)
        else:
            print('Estados disponibles --> ', aux_estados)

            aux_aceptacion = evaluar_aceptacion(aux_estados)

            limpiar_terminal()
            menu_AFD(nombre_afd, aux_estados, aux_alfabeto,
                     aux_inicial, aux_aceptacion)

    elif eleccion == '5':  # transiciones, AY MI MADREEE
        limpiar_terminal()

        if len(aux_estados) == 0:
            print('Aún no se han creado estados.')
            menu_AFD(nombre_afd, estados, alfabeto,
                     aux_inicial, aux_aceptacion)
        elif len(aux_alfabeto) == 0:
            print('Aún no se han creado terminales')
            menu_AFD(nombre_afd, estados, alfabeto,
                     aux_inicial, aux_aceptacion)
        else:
            print('Estados --> ', aux_estados)
            print('Alfabeto -->', aux_alfabeto)

            aux_transiciones = transiciones_afd(aux_estados, aux_alfabeto)

            limpiar_terminal()
            menu_AFD(nombre_afd, aux_estados, aux_alfabeto,
                     aux_inicial, aux_aceptacion, aux_transiciones)

    elif eleccion == '6':
        ayuda()
        menu_AFD(nombre_afd, estados, alfabeto, aux_inicial,
                 aux_aceptacion, aux_transiciones)

    elif eleccion == '7':

        afd_props = []  # lista que contiene las propiedades/elementos del afd

        # hasta este punto se tienen todos los datos
        afd_props.append(aux_estados)
        afd_props.append(aux_alfabeto)
        afd_props.append(aux_inicial)
        afd_props.append(aux_aceptacion)
        afd_props.append(aux_transiciones)

        # verificando que vayan todos los elementos del AFD
        if len(aux_estados) == 0 or len(aux_alfabeto) == 0 or aux_inicial == '' or len(aux_aceptacion) == 0 or len(aux_transiciones) == 0:
            print('ERROR. No se puede guardar el AFD si hacen falta partes.')
            menu_AFD(nombre_afd, estados, alfabeto, aux_inicial,
                     aux_aceptacion, aux_transiciones)
        else:
            coleccion_afds[nombre_afd] = afd_props
            menu_principal()

    else:
        limpiar_terminal()
        print('Entrada inválida')
        menu_AFD(nombre_afd, estados, alfabeto, aux_inicial,
                 aux_aceptacion, aux_transiciones)


def estados_afd():
    nuevo_estado = ''

    estados = []

    while nuevo_estado != '0':  # se sale del ciclo cuando se ingresa el 0

        nuevo_estado = input(
            '''Ingresa un nuevo estado, representado por una letra del abecedario. Ingresa 0 para terminar... ''').upper()

        if len(nuevo_estado) > 1:
            print('No se permiten más de dos caracteres en un estado.')
        elif nuevo_estado == '0':
            limpiar_terminal()
            continue
        elif nuevo_estado.isdigit():
            print('No se permiten números como estados.')
        elif nuevo_estado == '':
            print('ERROR. Espacio vacío')
        elif nuevo_estado in estados:
            print('ERROR. Ya existe un estado con esa etiqueta.')
        else:
            estados.append(nuevo_estado)

    return estados

def alfabeto_afd():
    nuevo_terminal = ''
    alfabeto = []

    while nuevo_terminal != '@':  # se sale del ciclo cuando se ingresa el 0

        nuevo_terminal = input(
            '''Ingresa un nuevo terminal, representado por una letra del alfabeto o número. Ingresa @ para terminar... ''').lower()

        if len(nuevo_terminal) > 1:
            print('No se permiten más de dos caracteres en un terminal.')
        elif nuevo_terminal == '@':
            limpiar_terminal()
            continue
        elif nuevo_terminal == '':
            print('ERROR. Espacio vacío')
        elif nuevo_terminal in alfabeto:
            print('ERROR. Ya existe un terminal con esa etiqueta.')
        else:
            alfabeto.append(nuevo_terminal)

    return alfabeto

def inicial(arreglo):

    if len(arreglo) == 0:
        return 1
    else:
        print('Disponibles --> ', arreglo)

        inicial = input('Seleccione uno de los disponibles... ').upper()

        if inicial not in arreglo:
            return 2
        else:
            return inicial

def evaluar_aceptacion(estados):
    nuevo_aceptacion = ''
    estados_aceptados = []  # lista que almacena los estados que se irán agregando

    while nuevo_aceptacion != '0':
        nuevo_aceptacion = input(
            'Ingrese uno de los estados previamente establecidos. Ingrese 0 para terminar... ').upper()

        if nuevo_aceptacion not in estados:
            print('ERROR. El estado no existe.')
        elif nuevo_aceptacion == '0':
            limpiar_terminal()
            continue
        else:
            estados_aceptados.append(nuevo_aceptacion)

    return estados_aceptados

def transiciones_afd(estados, alfabeto):

    transicion = ''
    # transicion_aceptada = [] # ['A', 'B', 'a']
    aceptadas = []  # [['A', 'B', 'a'], ['C', 'B', 'b']]

    while transicion != '@':
        transicion = input(
            'Ingresa una transición con los estados y terminales disponibles. Ingresa @ para terminar... ')

        if transicion == '@':  # si es @ sale del while
            break

        resultado = analizar_transicion(
            transicion, estados, alfabeto, aceptadas)

        if resultado == 0:
            print('AFD no acepta transiciones con epsilon')
        elif resultado == 1:
            print('El terminal no es válido')
        elif resultado == 2:
            print('Uno o ambos estados no existen')
        elif resultado == 3:
            print(
                'No se permiten dos o más transiciones con el mismo terminal desde un mismo estado.')
        else:
            aceptadas.append(resultado)
            # print(aceptadas)

    return aceptadas  # retornando el arreglo lleno

# analizando si la transcion es válida.
def analizar_transicion(cadena, estados, alfabeto, transiciones):

    #print(cadena, estados, alfabeto, inicial, aceptacion)
    transicion = []

    aux = cadena.split(';')
    trans = aux[0].split(',')

    if aux[1] == 'epsilon':
        return 0
    if aux[1] not in alfabeto:
        return 1
    for estado in trans:
        if estado not in estados:
            return 2

    trans.append(aux[1])  # ingresando el terminal/simbolo
    transicion = trans  # estados

    if len(transiciones) == 0:
        #print('Holi 1')
        return transicion
    else:
        for tr in transiciones:  # tr = ['A', 'B', 'a']
            # print(tr)
            if transicion[0] == tr[0] and transicion[2] == tr[2]:
                return 3

        return transicion

# ------------------ Gramáticas Regulares -------------------------------

def menu_GR(nombre_ER, no_Terminales=[], terminales=[], nt_inicial='', producciones=[], gramatica_fin=[]):

    # auxiliares que permiten cambiar el valor de los elementos
    aux_no_terminales = no_Terminales
    aux_terminales = terminales
    aux_nt_inicial = nt_inicial
    aux_producciones = producciones

    aux_gramatica_fin = gramatica_fin  # ['', []]

    # print(aux_no_terminales)
    # print(aux_terminales)
    # print(aux_nt_inicial)

    print('+-----------------------------------+')
    print('|           MENÚ GRAMÁTICA          |')
    print('+-----------------------------------+')
    print('')
    print('1. No terminales')
    print('2. Terminales')
    print('3. No terminal inicial')
    print('4. Producciones')
    print('5. Mostrar gramática corregida')
    print('6. Ayuda')
    print('7. Volver al menú principal')
    print('')

    eleccion = input('Por favor, elige una opcion: >> ')

    if eleccion == '1':
        aux_no_terminales = no_terminales_ER()
        menu_GR(nombre_ER, aux_no_terminales, aux_terminales,
                aux_nt_inicial, aux_producciones)
    elif eleccion == '2':
        aux_terminales = terminales_er()
        menu_GR(nombre_ER, aux_no_terminales, aux_terminales,
                aux_nt_inicial, aux_producciones)
    elif eleccion == '3':
        limpiar_terminal()
        aux_nt_inicial = inicial(aux_no_terminales)

        if aux_nt_inicial == 1:
            print('Aún no se han creado No Terminales. Por favor, ingrésalos.')
            menu_GR(nombre_ER, aux_no_terminales, aux_terminales)
        elif aux_nt_inicial == 2:
            print('El no terminal ingresado no existe.')
            menu_GR(nombre_ER, aux_no_terminales, aux_terminales)
        else:
            limpiar_terminal()
            menu_GR(nombre_ER, aux_no_terminales,
                    aux_terminales, aux_nt_inicial)
    elif eleccion == '4':
        limpiar_terminal()

        if len(aux_no_terminales) == 0:
            limpiar_terminal()
            print('No se han creado no terminales.')
            menu_GR(nombre_ER, aux_no_terminales,
                    aux_terminales, aux_nt_inicial)
        elif len(aux_terminales) == 0:
            limpiar_terminal()
            print('No se han creado terminales.')
            menu_GR(nombre_ER, aux_no_terminales,
                    aux_terminales, aux_nt_inicial)
        else:
            print('No terminales disponibles --> ', aux_no_terminales)
            print('Terminales disponibles -->', aux_terminales)

            aux_producciones = producciones_er(aux_no_terminales, aux_terminales, aux_nt_inicial)

            # ELIMINACION DE RECURSION POR LA IZQUIERDA
            producciones_final = quitar_recurs_izq(aux_producciones, aux_no_terminales, aux_terminales, aux_nt_inicial)

            # print(producciones_final)

            if producciones_final == 0:
                print('----------------------------------------------------------------------')
                print('La gramática no presenta problemas o recursividad por la izquierda.')
                print('La gramatica no ha sufrido cambios')
                print('---------------------------------------------------------------------')

                aux_gramatica_fin.append(
                    'GRAMATICA NO TIENE RECURSIVIDAD POR LA IZQUIERDA')
                aux_gramatica_fin.append(aux_producciones)
                menu_GR(nombre_ER, aux_no_terminales, aux_terminales,
                        aux_nt_inicial, aux_producciones, aux_gramatica_fin)
            else:
                aux_gramatica_fin.append(aux_producciones)
                aux_gramatica_fin.append(producciones_final)

                menu_GR(nombre_ER, aux_no_terminales, aux_terminales,
                        aux_nt_inicial, aux_producciones, aux_gramatica_fin)
    elif eleccion == '5':
        limpiar_terminal()

        if aux_gramatica_fin[0] == 'GRAMATICA NO TIENE RECURSIVIDAD POR LA IZQUIERDA':
            print('GRAMATICA NO TIENE RECURSIVIDAD POR LA IZQUIERDA')
            print('-----------------------------------------------')
            imprimir_gramatica(aux_producciones)
        else:
            print('Gramática Original:')
            imprimir_gramatica(aux_gramatica_fin[0])
            print('-----------------------------------------------')
            print('Gramática corregida')
            imprimir_gramatica(aux_gramatica_fin[1])

        menu_GR(nombre_ER, aux_no_terminales, aux_terminales,
                aux_nt_inicial, aux_producciones, aux_gramatica_fin)
    elif eleccion == '6':
        limpiar_terminal()
        ayuda()
        menu_GR(nombre_ER, aux_no_terminales, aux_terminales,
                aux_nt_inicial, aux_producciones, aux_gramatica_fin)
    elif eleccion == '7':
        er_props = []
        er_props.append(nombre_ER)
        er_props.append(aux_no_terminales)
        er_props.append(aux_terminales)
        er_props.append(aux_nt_inicial)
        er_props.append(aux_gramatica_fin)

        if len(aux_no_terminales) == 0 or len(aux_terminales) == 0 or len(aux_nt_inicial) == '' or len(aux_gramatica_fin) == 0:
            print('ERROR. Hacen falta elementos.')
            menu_GR(nombre_ER, aux_no_terminales, aux_terminales,
                    aux_nt_inicial, aux_producciones, aux_gramatica_fin)
        else:
            coleccion_grs[nombre_ER] = er_props
            menu_principal()
    else:
        print('ENTRADA INVÁLIDA')
        menu_GR(nombre_ER, aux_no_terminales, aux_terminales,
                aux_nt_inicial, aux_producciones, aux_gramatica_fin)

def no_terminales_ER():
    nuevo_noTerminal = ''
    no_terminales = []

    while nuevo_noTerminal != '0':
        nuevo_noTerminal = input(
            '''Ingresa un nuevo no terminal, representado por una letra del abecedario. Ingresa 0 para terminar... ''').upper()

        if len(nuevo_noTerminal) > 1:
            print('No se permiten más de dos caracteres en un no terminal.')
        elif nuevo_noTerminal == '0':
            limpiar_terminal()
            continue
        elif nuevo_noTerminal.isdigit():
            print('No se permiten números como no terminales.')
        elif nuevo_noTerminal == '':
            print('ERROR. Espacio vacío')
        elif nuevo_noTerminal in no_terminales:
            print('ERROR. Ya existe un no terminal con esa etiqueta.')
        else:
            no_terminales.append(nuevo_noTerminal)

    return no_terminales

def terminales_er():
    nuevo_terminal = ''
    terminales_aceptados = []

    while nuevo_terminal != '@':  # se sale del ciclo cuando se ingresa el 0

        nuevo_terminal = input('''Ingresa un nuevo terminal, representado por una letra del abecedario o un número.\
        Ingresa @ para terminar... ''').lower()

        if len(nuevo_terminal) > 1:
            print('No se permiten más de dos caracteres en un terminal.')
        elif nuevo_terminal == '@':
            limpiar_terminal()
            continue
        elif nuevo_terminal == '':
            print('ERROR. Espacio vacío')
        elif nuevo_terminal in terminales_aceptados:
            print('ERROR. Ya existe un terminal con esa etiqueta.')
        else:
            terminales_aceptados.append(nuevo_terminal)

    return terminales_aceptados

def producciones_er(no_terminales, terminales, inicial):

    produccion = ''  # A > a B - A > Ab | A > a | B > epsilon | B > B s
    producciones_aceptadas = []  # [[A, a, B], [A, b, A], [A, epsilon], [B, epsilon]]
    # con recursividad por la izquierda [[A > B a], [A > b]]

    while produccion != '@':
        produccion = input('Ingresa una produccion. Ingresa @ para terminar... ')  # A > a B

        if produccion == '@':
            break

        for produccion_aceptada in producciones_aceptadas:
            if (produccion[4] == produccion_aceptada[1]) and (produccion[0] == produccion_aceptada[0]) and produccion[4] not in no_terminales:
                print('ERROR. No es posible ir con el mismo terminal desde un no terminal hacia dos o mas no terminales.')

        resultado = analizar_produccion(
            produccion, no_terminales, terminales, inicial)

        producciones_aceptadas.append(resultado)

    return producciones_aceptadas

def analizar_produccion(produccion, no_terminales, terminales, inicial):

    produccion_valida = []

    aux = produccion.split('>')
    izquierda = aux[0].replace(' ', '')
    derecha = aux[1].replace(' ', '')

    # print(izquierda)
    # print(derecha)

    if izquierda not in no_terminales:
        return 0
    else:
        produccion_valida.append(izquierda)

    if derecha == 'epsilon':
        produccion_valida.append(derecha)
    else:
        for a in derecha:
            produccion_valida.append(a)

    return produccion_valida

def quitar_recurs_izq(producciones, no_terminales, terminales, nt_inicial):

    no_terminal = ''
    #alpha = ''
    beta = ''

    no_terminales_ = []
    betas = []

    aux_transiciones = []  # ['a', 'b', 'c', 'A']

    arreglo_izq_rec = []  # producciones que deben ser corregidas
    arreglo_normal = []  # producciones que no presentan recursividad por la izquierda

    # producciones sin recursividad por la izquierda (SRI)
    producciones_sinRI = []

    for produccion in producciones: # ['A', 'A', 'b'], ['A', 'a']
        if produccion[1] in no_terminales:
            arreglo_izq_rec.append(produccion)
            aux_transiciones.append(produccion[1])
        elif len(produccion) == 2 and ('epsilon' not in produccion): ### PENDIENTE REVISAR PRODUCCIONES CON MISMO SIMBOLO
            arreglo_izq_rec.append(produccion)
            aux_transiciones.append(produccion[1])
        else:
            arreglo_normal.append(produccion)

    if len(arreglo_izq_rec) == 0:
        return 0
    else:
        print('Gramática con recursividad por la izquierda.')

    # print(arreglo_izq_rec)
    # print(arreglo_normal)
    # input('')

    for produccion in arreglo_normal:
        if produccion[1] == 'epsilon':
            aux_produ = []
            aux_produ.append(produccion[0])
            aux_produ.append(produccion[1])
        else:
            aux_produ = []
            # '{} > {} {}'.format(produccion[0], produccion[1], produccion[2]) #produccion normal
            aux_produ.append(produccion[0])
            aux_produ.append(produccion[1])
            aux_produ.append(produccion[2])

        producciones_sinRI.append(aux_produ)

    for produccion in arreglo_izq_rec:
        if len(produccion) == 2:
            beta = produccion[1]
            betas.append(beta)

            no_terminal = produccion[0]
            no_terminales_.append(no_terminal)

            aux_produ = []
            # '{} > {} {}P'.format(produccion[0], produccion[1], produccion[0])
            aux_produ.append(produccion[0])
            aux_produ.append(produccion[1])
            aux_produ.append(produccion[0]+'P')
            producciones_sinRI.append(aux_produ)

    #print('betas hallados --> ', betas)
    #print('no terminales --> ', no_terminales_)

    for produccion in arreglo_izq_rec:
        for nt in no_terminales:
            if len(produccion) > 2:
                if produccion[0] == nt:
                    aux_produ1 = []
                    aux_produ_epsilon = []
                    # '{}P > {} {}P'.format(nt, produccion[2], nt)
                    aux_produ1.append(nt+'P')
                    aux_produ1.append(produccion[2])
                    aux_produ1.append(nt+'P')

                    # '{}P > epsilon'.format(nt)
                    aux_produ_epsilon.append(nt+'P')
                    aux_produ_epsilon.append('epsilon')

                    producciones_sinRI.append(aux_produ1)
                    producciones_sinRI.append(aux_produ_epsilon)

    return producciones_sinRI
    #print('Gramatica corregida --> ', producciones_sinRI)

def imprimir_gramatica(gramatica):
    for produccion in gramatica:
        if len(produccion) == 2:
            print('{} > {}'.format(produccion[0], produccion[1]))
        else:
            print('{} > {} {}'.format(
                produccion[0], produccion[1], produccion[2]))

def ayuda():
    limpiar_terminal()
    print('''
    Lenguajes Formales y de Programación, Sección B-
    Aux: Luis Yela
    Último dígito: 3
    ''')
    input('')

    ayuda()

#------------------------------------
def menu_reportes():
    
    limpiar_terminal()
    
    print('+-----------------------------------+')
    print('|              REPORTES             |')
    print('+-----------------------------------+')
    print('')
    print('1. Ver detalle (Gramatica o AFD)')
    print('2. Generar reporte (PDF)')
    print('3. Ayuda')
    print('4. Regresar al menú principal')
    print('')
    
    eleccion = input('Elige una opcion: >> ')
    
    if eleccion == '1':
        
        nombre_objecto = input('Ingresar nombre de Gramática o AFD: >> ')
        limpiar_terminal()
        for key_afd, contenido_afd in coleccion_afds.items():
            if nombre_objecto == key_afd:
                print('Estados >> ', *contenido_afd[0])
                print('Alfabeto >> ', *contenido_afd[1])
                print('Estado inicial >> ', *contenido_afd[2])
                print('Estados de aceptacion >> ', *contenido_afd[3])
                print('Transiciones:')
                for transicion in contenido_afd[4]:
                    print('{},{};{}'.format(transicion[0], transicion[1], transicion[2]))
                
                input('') #pausa para ver todos los detalles
                
                menu_reportes()
        
        for key_grm, contenido_grm in coleccion_grs.items():
            if nombre_objecto == key_grm:
                if contenido_grm[4][0] == 'GRAMATICA NO TIENE RECURSIVIDAD POR LA IZQUIERDA':
                    print('No terminales >> ', *contenido_grm[0])
                    print('Terminales >> ', *contenido_grm[1])
                    print('No terminal inicial >> ', contenido_grm[2])
                    print('Producciones')
                    for produccion in contenido_grm[3]:
                        if len(produccion) > 2:
                            print('{} > {} {}'.format(produccion[0], produccion[1], produccion[2]))
                        else:
                            print('{} > {}'.format(produccion[0], produccion[1]))
                    
                    input('')
                    menu_reportes()
                else:
                    print('No terminales >> ', *contenido_grm[0])
                    print('Terminales >> ', *contenido_grm[1])
                    print('No terminal inicial >> ', contenido_grm[2])
                    print('Gramática original:')
                    for produccion in contenido_grm[4][0]:
                        if len(produccion) > 2:
                            print('{} > {} {}'.format(produccion[0], produccion[1], produccion[2]))
                        else:
                            print('{} > {}'.format(produccion[0], produccion[1]))
                    print('---------------------------------')
                    print('Gramática corregida:')
                    for produccion in contenido_grm[4][1]:
                        if len(produccion) > 2:
                            print('{} > {} {}'.format(produccion[0], produccion[1], produccion[2]))
                        else:
                            print('{} > {}'.format(produccion[0], produccion[1]))
                    
                    input('')
                    menu_reportes()
        
    elif eleccion == '2':
        pass
    elif eleccion == '3':
        ayuda()
        menu_reportes()
    elif eleccion == '4':
        menu_principal()
    else:
        print('Entrada inválida')
        input('')
        menu_reportes()
    
# -----------------------------------------------------------------------
def menu_cargarArchivo():
    limpiar_terminal()

    print('+-----------------------------------+')
    print('|           CARGAR ARCHIVOS         |')
    print('+-----------------------------------+')
    print('')
    print('1. Cargar archivo AFD (.afd)')
    print('2. Cargar archhvo Gramática (.grm)')
    print('3. Regresar al menú principal')
    print('')

    eleccion = input('Por favor, elige una opción: >> ')

    if eleccion == '1':
        limpiar_terminal()

        ruta_archivo = cargarArchivo()

        # obteniendo el nombre del archiv y eliminando la extension .afd
        nombreAFD = path_leaf(ruta_archivo).split('.')[0]
        # print(nombre_archivo)

        if ruta_archivo:
            data = obtenerTexto(ruta_archivo)
            print(data)

            transiciones = data.splitlines()

            estados = []
            alfabeto = []
            aceptacion = []
            afd_transiciones = []
            estado_inicial = ''

            # Estado inicial es siempre el primer estado que se lee del archivo
            aux_inicial = transiciones[0].split(';')
            estado_inicial = aux_inicial[0].replace(' ', '').split(',')[0]

            for transicion in transiciones:
                aux = transicion.split(';')
                aux_izquierda = aux[0].replace(' ', '').split(',')

                # Ingresando las transiciones
                aux_transicion = []
                aux_transicion.append(aux_izquierda[0])
                aux_transicion.append(aux_izquierda[1])
                aux_transicion.append(aux_izquierda[2])
                afd_transiciones.append(aux_transicion)

                # Ingresando estados
                if aux_izquierda[0] in estados:
                    pass
                else:
                    estados.append(aux_izquierda[0])

                if aux_izquierda[1] in estados:
                    pass
                else:
                    estados.append(aux_izquierda[1])

                # ingresando alfabeto/simbolos
                if aux_izquierda[2] in alfabeto:
                    pass
                else:
                    alfabeto.append(aux_izquierda[2])

                # ingresando estados de aceptacion
                aux_derecha = aux[1].replace(' ', '').split(',')

                if aux_derecha[0] == 'true' and aux_izquierda[0] not in aceptacion:
                    aceptacion.append(aux_izquierda[0])
                elif aux_derecha[0] == 'false' and aux_izquierda[0] in aceptacion:
                    index = aceptacion.index(aux_izquierda[0])
                    aceptacion.pop(index)

                if aux_derecha[1] == 'true' and aux_izquierda[1] not in aceptacion:
                    aceptacion.append(aux_izquierda[1])
                elif aux_derecha[1] == 'false' and aux_izquierda[1] in aceptacion:
                    index = aceptacion.index(aux_izquierda[1])
                    aceptacion.pop(index)

            print('Transiciones --> ', afd_transiciones)
            print('Estados --> ', estados)
            print('Alfabeto -->', alfabeto)
            print('Aceptacion --> ', aceptacion)
            print('Inicial --> ', estado_inicial)

            # propiedades del afd
            afd_props = []
            afd_props.append(estados)
            afd_props.append(alfabeto)
            afd_props.append(estado_inicial)
            afd_props.append(aceptacion)
            afd_props.append(afd_transiciones)

            coleccion_afds[nombreAFD] = afd_props

        else:
            limpiar_terminal()
            print('No se seleccionó ningún archivo.')
            menu_cargarArchivo()

    elif eleccion == '2':
        limpiar_terminal()

        ruta_archivo = cargarArchivo()
        nombre_GR = path_leaf(ruta_archivo).split('.')[0]
        #print(nombre_GR)
        # input('')

        if ruta_archivo:
            data = obtenerTexto(ruta_archivo)

            producciones = data.splitlines()
            no_terminales = []
            terminales = []
            nt_inicial = ''
            gr_producciones = []

            # obteniendo el no terminal inicial
            nt_inicial = producciones[0].replace(' ', '').split('>')[0]
            #print(nt_inicial)
            # input('')
            
            # Ingresando no terminales
            for produccion in producciones:
                aux = produccion.split('>')
                izquierda = aux[0].replace(' ', '')
                
                if izquierda not in no_terminales:
                    no_terminales.append(izquierda)
                else:
                    pass

            for produccion in producciones:
                aux = produccion.split('>')
                izquierda = aux[0].replace(' ', '')
                derecha = aux[1].replace(' ', '')

                # ingresando produccion
                aux_produccion = []
                aux_produccion.append(izquierda)
                if derecha == 'epsilon':
                    aux_produccion.append(derecha)
                else:
                    for letra in derecha:
                        aux_produccion.append(letra)

                gr_producciones.append(aux_produccion)
                
                # Ingresando terminales
                if derecha != 'epsilon':
                    for letra in derecha:
                        if letra not in no_terminales and (letra not in terminales):
                            terminales.append(letra)
            
            print('Nombre de gramatica --> ', nombre_GR)
            print('No terminales --> ', no_terminales)
            print('Terminales --> ', terminales)
            print('No terminal inicial --> ', nt_inicial)
            print('Producciones --> ', gr_producciones)
            input('')
            
            producciones_final = quitar_recurs_izq(gr_producciones, no_terminales, terminales, nt_inicial)
            
            gramatica_final = [] #[]
            
            if producciones_final == 0:
                producciones_final = gr_producciones
                # print('Gramatica sin recursividad por la izquierda')
                # print(producciones_final)
                
                gramatica_final.append('GRAMATICA NO TIENE RECURSIVIDAD POR LA IZQUIERDA')
                gramatica_final.append(producciones_final)
            else:
                #print('Gramatica corregida --> ', producciones_final)
                gramatica_final.append(gr_producciones)
                gramatica_final.append(producciones_final)
            
            #input('')
            
            #propiedades gramatica
            gr_props = []
            gr_props.append(no_terminales)
            gr_props.append(terminales)
            gr_props.append(nt_inicial)
            gr_props.append(gr_producciones)
            gr_props.append(gramatica_final)
            
            coleccion_grs[nombre_GR] = gr_props

        else:
            limpiar_terminal()
            print('No se seleccinó ningún archivo')
            menu_cargarArchivo()

    elif eleccion == '3':
        menu_principal()

info_est()
input('')
menu_principal()