from afd_er import limpiar_terminal
from afd_er import menu_principal
import graphviz

#lista que contiene los automatas de pila (AP)
lista_gramaticas = []

# g = graphviz.Digraph('G', filename='hello.gv', format='png')

# g.edge('Hello', 'World')

# g.view()

class Gramatica():
    def __init__(self, nombre_gramatica): #valores por defecto para luego irlos reemplazando
        self.nombre_gramatica = nombre_gramatica
        self.terminales = []
        self.no_terminales = []
        self.producciones = []
        self.nt_inicial = ''
    
    def ingresar_no_terminales(self):
        while True:
            nuevo_noTerminal = input('Ingresa un nuevo no terminal, representado por una letra del abecedario. Ingresa 0 para terminar: >> ').upper()
            if len(nuevo_noTerminal) > 1:
                print('No se permiten más de dos caracteres en un no terminal.')
            elif nuevo_noTerminal == '0':
                limpiar_terminal()
                break
            elif nuevo_noTerminal.isdigit():
                print('No se permiten números como no terminales.')
                input('')
                limpiar_terminal()
            elif nuevo_noTerminal == '':
                print('ERROR. Espacio vacío')
                input('')
                limpiar_terminal()
            elif nuevo_noTerminal in self.no_terminales:
                print('ERROR. Ya existe un no terminal con esa etiqueta.')
                input('')
                limpiar_terminal()
            else:
                self.no_terminales.append(nuevo_noTerminal)
                limpiar_terminal()
            
    def ingresar_terminales(self):
        while True:  # se sale del ciclo cuando se ingresa el @
            nuevo_terminal = input('''Ingresa un nuevo terminal, representado por una letra del abecedario, número o símbolo. Ingresa @ para terminar: >> ''').lower()

            if len(nuevo_terminal) > 1:
                print('No se permiten más de dos caracteres en un terminal.')
                input('')
                limpiar_terminal()
            elif nuevo_terminal == '@':
                limpiar_terminal()
                break
            elif nuevo_terminal == '':
                print('ERROR. Espacio vacío')
                input('')
                limpiar_terminal()
            elif nuevo_terminal in self.terminales:
                print('ERROR. Ya existe un terminal con esa etiqueta.')
                input('')
                limpiar_terminal()
            else:
                self.terminales.append(nuevo_terminal)
                limpiar_terminal()
    
    def ingresar_producciones(self):
        if len(self.no_terminales) == 0:
            print('Aún no se han creado no terminales')
            input('')
            limpiar_terminal()
        elif len(self.terminales) == 0:
            print('Aún no se han creado terminales')
            input('')
            limpiar_terminal()
        else:
            while True:
                print('No terminales disponibles --> ', self.no_terminales)
                print('Terminales disponibles --> ', self.terminales)
                
                nueva_produccion = input('Introducir nueva producción: >> ')
                
                if nueva_produccion == '@':
                    break
                elif nueva_produccion == '' or nueva_produccion is None or nueva_produccion == ' ':
                    print('ERROR. Entrada vacía')
                    input('')
                    limpiar_terminal()
                else:       
                    produccion_analizada = self.analizar_produccion(nueva_produccion, self.no_terminales, self.terminales)
                    
                    if produccion_analizada == 0:
                        print('ERROR. El lado izquierdo de la producción no es válido.')
                        input('')
                        limpiar_terminal()
                    elif produccion_analizada == 1:
                        print('ERROR. El lado derecho de la producción contiene elementos no válidos.')
                        input('')
                        limpiar_terminal()
                    elif produccion_analizada in self.producciones:
                        print('ERROR. Producción ya existe.')
                        input('')
                        limpiar_terminal()
                    else:
                        self.producciones.append(produccion_analizada)
                        limpiar_terminal()
    
    def analizar_produccion(self, produccion, no_terminales, terminales):
        produccion_original = produccion
        
        aux = produccion.split('>')
        aux_izquierda = aux[0].replace(' ', '')
        
        aux_derecha = []
        if 'epsilon' in aux[1]: #si de lado derecho viene "epsilon" no pasa nada
            aux_derecha = aux[1].replace(' ', '')
        else:
            for char in aux[1]:
                if char == ' ':
                    continue
                else:
                    aux_derecha.append(char)
        
        #validando que todos los elementos en la produccion existen
        if aux_izquierda not in no_terminales:
            return 0
        
        if aux_derecha != 'epsilon':
            for elemento in aux_derecha:
                if elemento not in no_terminales and elemento not in terminales:
                    return 1
        
        #si pasa las validaciones se ingresa todo 
        produccion = Produccion(aux_izquierda, aux_derecha, produccion_original)
        return produccion
    
    def eliminar_produccion(self, produccion):
        produccion_sinEspacios = produccion.replace(' ', '')
        
        for produccion in self.producciones:
            original_sinEspacios = produccion.original.replace(' ', '')
            print(original_sinEspacios)
            input('')
            if produccion_sinEspacios == original_sinEspacios:
                index_produc = self.producciones.index(produccion)
                self.producciones.pop(index_produc)
            else:
                print('La producción no existe.')
                input('')
        # print('Producciones actualizadas --> ', self.producciones)
        # input('')
    
    def ingresar_nt_inicial(self):
        if self.no_terminales == []:
            print('Primero se debe crear no terminales')
            input('')
        else:
            print('No terminales disponibles --> ', *self.no_terminales)
            nuevo_nt_inicial = input('Ingresa el nuevo no terminal incial: >> ')
            
            if nuevo_nt_inicial not in self.no_terminales:
                print('El no terminal ingresado no existe.')
                input('')
            elif nuevo_nt_inicial == '' or nuevo_nt_inicial is None:
                print('Debes ingresar un no terminal')
                input('')
            else:
                self.nt_inicial = nuevo_nt_inicial
    
    #quitando recursividad por la izquierda 
    def quitar_recursividad_izq(self):
        nuevas_producciones = []
        producc_noRI = []
        producc_RI = []
        
        for produccion in self.producciones:
            if produccion.lado_izq != produccion.lado_der[0]:
                #produccion sin recursivad por la izquierda
                producc_noRI.append(produccion)
            else:
                producc_RI.append(produccion)
                
        if producc_RI == []:
            return 0
        else:
            print('Gramática presenta recursividad por la izquierda.')
            input('')
        
        #comenzando a quitar la recursividad por la izquierda
        
        #buscando las producciones que no tienen recursividad y tampoco tienen relación con las produccines recursivas    
        lado_izquierdo_R = []
        for produccion_r in producc_RI:
            lado_izquierdo_R.append(produccion_r.lado_izq)
        
        for produccion in producc_noRI:
            if produccion.lado_izq not in lado_izquierdo_R:
                lado_derecho = ''
                for char in produccion.lado_der:
                    if char == ' ' or char is None or char == '':
                        pass
                    else:
                        lado_derecho = lado_derecho + char + ' '
                
                lado_derecho = lado_derecho[:-1]
                
                elementos = []
                for char in produccion.lado_der:
                    elementos.append(char)
                
                produccion_normal = '{} > {}'.format(produccion.lado_izq, lado_derecho)
                produccion_normal_ = Produccion(produccion.lado_izq, elementos, produccion_normal)
                nuevas_producciones.append(produccion_normal_)
                
        
        for produccion in producc_RI:
            nt_prima = produccion.lado_izq+'P'
            self.no_terminales.append(nt_prima) #agregando prima a la lista de no terminales
            
            produccion_ep = '{} > {}'.format(nt_prima, 'epsilon')
            produccion_epsilon = Produccion(nt_prima, 'epsilon', produccion_ep)
            nuevas_producciones.append(produccion_epsilon)
            
            lado_derecho = '' #lado derecho que se imprime
            for char in produccion.lado_der[1:]:
                if char == ' ' or char is None or char == '':
                    pass
                else:
                    lado_derecho = lado_derecho + char + ' '
            lado_derecho = lado_derecho + nt_prima
            #lado_derecho = lado_derecho[:-1]
            
            elementos = []
            for char in produccion.lado_der[1:]:
                elementos.append(char)
            elementos.append(nt_prima)
                
            produccion_prim = '{} > {}'.format(nt_prima, lado_derecho)
            produccion_prima = Produccion(nt_prima, elementos, produccion_prim)
            nuevas_producciones.append(produccion_prima)
        
        for produccion_a in producc_noRI:
            for produccion_b in producc_RI:
                if produccion_a.lado_izq == produccion_b.lado_izq:
                    nt_prima_ = produccion_a.lado_izq+'P'
                    
                    lado_derecho = ''
                    for char in produccion_a.lado_der:
                        if char == ' ' or char is None or char == '':
                            pass
                        else:
                            lado_derecho = lado_derecho + char + ' '
                            
                    lado_derecho = lado_derecho + nt_prima_
                    #lado_derecho = lado_derecho[:-1]
                    
                    elementos_derecha = []
                    for elemento in produccion_a.lado_der:
                        elementos_derecha.append(elemento)
                    elementos_derecha.append(nt_prima_)
                    
                    produccion_ingresar = '{} > {}'.format(produccion_a.lado_izq, lado_derecho)
                    nueva_produccion = Produccion(produccion_a.lado_izq, elementos_derecha, produccion_ingresar)
                    nuevas_producciones.append(nueva_produccion)
        
        print('Lista de terminales hasta ahora --> ', self.no_terminales)
        input('')
        return nuevas_producciones
    
    def eliminar_repetidos(self):
        lista_sin_repetidos = []
        for produccion in self.producciones:
            if produccion.original not in lista_sin_repetidos:
                lista_sin_repetidos.append(produccion)
        
        self.producciones = lista_sin_repetidos
    
    def crear_automata_pila(self):
        alfabeto = self.terminales
        simbolos_pila = self.terminales + self.no_terminales #simbolos de pila
        simbolos_pila.append('#')
        
        automata_pila = Automata_Pila(alfabeto, simbolos_pila)
        
        automata_pila.transicion_inicial()
        automata_pila.transicion_simbolo_inicial(self.nt_inicial)
        
        for produccion in self.producciones:
            automata_pila.transicion_no_terminal(produccion.lado_izq, produccion.lado_der)
        
        for terminal in self.terminales:
            automata_pila.transicion_terminal(terminal)
        
        automata_pila.transicion_final()
        
        return automata_pila
    
    def generar_grafo(self):
        transiciones_label = ''
        automata_graficar = self.crear_automata_pila()
        
        dot = graphviz.Digraph(comment='wenas tardes', format='png')
        dot.node('A', 'i', shape= 'circle')
        dot.node('B', 'p', shape='circle')
        dot.edge('A', 'B', constraint='false', label='λ,λ;#')
        dot.node('C', 'q', shape='circle')
        dot.edge('B', 'C', constraint='false', label='λ,λ;'+self.nt_inicial)
        
        for transicion in automata_graficar.transiciones:
            if str(transicion.sacar_pila) != 'λ' and str(transicion.lectura_cadena) == 'λ':
                transiciones_label = transiciones_label + '{}, {}; {}'.format('λ', transicion.sacar_pila, ', '.join(transicion.insertar_pila).replace(', ', '')) + '\n'
            elif str(transicion.lectura_cadena) == str(transicion.sacar_pila) and str(transicion.insertar_pila) == 'λ':
                transiciones_label = transiciones_label + '{}, {}; {}'.format(str(transicion.lectura_cadena), str(transicion.sacar_pila), 'λ') + '\n'
        dot.edge('C', 'C', label=transiciones_label)
        dot.node('D', 'f', shape='doublecircle')
        dot.edge('C', 'D', constraint='True', label='λ, #; λ')
        
        dot.render(filename='Grafo_test', view=True)
    
    def validar_cadena(self):
        
        contenido_movimientos = ''
        
        while True:
            
            print('1. Ingresar cadena')
            print('2. Resultado')
            print('3. Reporte')
            print('4. Regresar')
            print('')
            
            eleccion = input('Elige una opción: >> ')
            
            if eleccion == '1':
                cadena_a_validar = input('Ingresa la cadena que deseas evaluar: >> ')
                
                contenido_movimientos = self.validacion(cadena_a_validar)
                
                # print('Contenido para el archivo')
                # print(contenido_movimientos)
                # input('')
                
                print('Terminó de validar la cadena')
                input('')
            elif eleccion == '2':
                self.generar_arbol()
            elif eleccion == '3':
                self.generar_archivo_movimientos(contenido_movimientos)
                print('Se generó el archivo')
            elif eleccion == '4':
                print('Regresando al Menú Autómata de Pila')
                input('')
                break
    
    def validacion(self, cadena):
        
        movimientos = ''
        
        condicion = True
        hubo_movimiento = False
        automata = self.crear_automata_pila() #automata que se utlizará
        aux_cadena = cadena.split(' ')
        
        pila_cadena = []
        for char in reversed(aux_cadena):
            pila_cadena.append(char)
            
        pila = [] #pila del automata
        
        #primeros dos movimientos
        pila.append('#')
        pila.append(str(self.nt_inicial))
        
        movimientos = movimientos + 'PILA $ ENTRADA $ TRANSICION' + '\n'
        movimientos = self.agregar_movimiento(movimientos, pila, cadena, '(i, λ, λ; p, #)')
        
        try:
            while condicion == True:
                
                hubo_movimiento = False
                
                if pila[-1] == self.nt_inicial:
                    pila.pop()
                    for transicion in automata.transiciones:
                        if self.nt_inicial == transicion.sacar_pila:
                            for char in reversed(transicion.insertar_pila):
                                pila.append(char)
                            
                            movimientos = self.agregar_movimiento(movimientos, pila, pila_cadena, transicion.imprimir())
                    
                elif pila[-1] in self.no_terminales:
                    coincidencias = []
                    primeros_char_insertar_pila = []
                    
                    for transicion in automata.transiciones:
                        if transicion.sacar_pila == pila[-1]:
                            coincidencias.append(transicion)
                    
                    for coincidencia in coincidencias:
                        if coincidencia.insertar_pila == 'epsilon':
                            primeros_char_insertar_pila.append('epsilon')
                        else:
                            primeros_char_insertar_pila.append(coincidencia.insertar_pila[0])
                    
                    print('Coincidencias:')
                    for coincidencia in coincidencias:
                        print(coincidencia.insertar_pila)
                    
                    print('Primeros char:')
                    print(primeros_char_insertar_pila)
                    input('')
                    
                    for char in primeros_char_insertar_pila:
                        if char.isupper() and pila_cadena[-1] not in primeros_char_insertar_pila:
                            coincidencias2 = []
                            primeros_char = []
                            print('No terminal encontrado --> ', char)
                            input('')
                            
                            for transicion in automata.transiciones:
                                if transicion.sacar_pila == char:
                                    coincidencias2.append(transicion)
                            
                            for match in coincidencias2:
                                if match.insertar_pila == 'epsilon':
                                    primeros_char.append('epsilon')
                                else:
                                    primeros_char.append(match.insertar_pila[0])
                            
                            if 'epsilon' in primeros_char and pila_cadena[-1] not in primeros_char:
                                pila.pop()
                                
                                transicion_movimiento = '(q, λ, {}; q, epsilon)'.format(char) #transicion que se insertará en achivo
                                movimientos = self.agregar_movimiento(movimientos, pila, pila_cadena, transicion_movimiento)
                                
                                hubo_movimiento = True
                            else:
                                if pila_cadena[-1] not in primeros_char:
                                    print('CADENA INVALIDAAAAAfdafdsafs4555')
                                    input('')
                                    
                                    movimientos = movimientos + '¡¡¡ENTRADA INVÁLIDA!!!' + '\n'
                                    condicion = False
                                else:
                                    for match in coincidencias2:
                                        if match.insertar_pila[0] == pila_cadena[-1]:
                                            pila.pop()
                                            for char in reversed(match.insertar_pila):
                                                pila.append(char)
                                            
                                            movimientos = self.agregar_movimiento(movimientos, pila, pila_cadena, match.imprimir())
                                            hubo_movimiento = True
                    
                    if hubo_movimiento == True:
                        pass
                    else:
                        if 'epsilon' in primeros_char_insertar_pila and len(pila_cadena) == 0:
                            pila.pop()
                            transicion_movimiento = '(q, λ, {}; q, epsilon)'.format(pila[-1]) #transicion que se insertará en achivo
                            movimientos = self.agregar_movimiento(movimientos, pila, pila_cadena, transicion_movimiento)
                        else:
                            if 'epsilon' in primeros_char_insertar_pila and pila_cadena[-1] not in primeros_char_insertar_pila:
                                pila.pop()
                                transicion_movimiento = '(q, λ, {}; q, epsilon)'.format(pila[-1]) #transicion que se insertará en achivo
                                movimientos = self.agregar_movimiento(movimientos, pila, pila_cadena, transicion_movimiento)
                            else:
                                if pila_cadena[-1] not in primeros_char_insertar_pila:
                                    print('Cadena inválidaaaadfn')
                                    input('')
                                    
                                    movimientos = movimientos + '¡¡¡ENTRADA INVÁLIDA!!!' + '\n'
                                    
                                    condicion = False
                                else:
                                    for coincidencia in coincidencias:
                                        if coincidencia.insertar_pila[0] == pila_cadena[-1]:
                                            pila.pop()
                                            for char in reversed(coincidencia.insertar_pila):
                                                pila.append(char)
                                            
                                            movimientos = self.agregar_movimiento(movimientos, pila, pila_cadena, coincidencia.imprimir())
                                            
                elif pila[-1] in self.terminales:
                    if (pila[-1] == pila_cadena[-1]):
                        transicion_agregar = '(q, {}, {}; q, λ)'.format(pila[-1], pila_cadena[-1])
                        movimientos = self.agregar_movimiento(movimientos, pila, pila_cadena, transicion_agregar)
                        
                        pila_cadena.pop()
                        pila.pop()
                        
                    elif pila[-1] != pila_cadena[-1]:
                        print('Cadena inválida')
                        input('')
                        movimientos = movimientos + '¡¡¡ENRTADA INVÁLIDA!!!' + '\n'
                        condicion = False
                
                #cadena aceptada
                elif len(pila_cadena) == 0 and len(pila) == 1 and pila[0] == '#':
                    pila.pop()
                    print('Cadena válida :D')
                    input('')
                    
                    movimientos = movimientos + '¡¡¡ENTRADA VÁLIDA!!!' + '\n'
                    condicion = False
                
                print('Pila --> ', pila)
                print('Cadena --> ', pila_cadena)
                input('')
            
            print('Salió del ciclo')
            input('')
        except:
            print('Cadena no válida try catch')
            input('')
        
        print(movimientos)
        input('')
        
        return movimientos
    
    #método que va agregando los movimientos a la cadena principal
    def agregar_movimiento(self, texto, pila, cadena, transicion):
        texto = texto + '{}${}${}'.format(pila, cadena, transicion) + '\n'
        return texto
    
    #generando archivo CSV
    def generar_archivo_movimientos(self, contenido):
        ruta = 'D:\Repos-Github\proyecto2_lenguajes\proyecto2_lenguajes\Reporte.csv'
        archivo = open(ruta, 'a', encoding='utf-8')
        
        archivo.write(contenido)
        archivo.close()
    
    def generar_arbol(self):
        nodo_internos_noActivos = []
        
        id = 1
        
        nuevo_arbol = Arbol() #instanciando el árbol que se utilizará
        dot = graphviz.Graph(comment='The Round Table', format='png')
        
        for produccion in self.producciones:
            nuevo_arbol.crear_nodo_interno(id, produccion.lado_izq)
            nuevo_arbol.crear_hoja(id, produccion.lado_izq)
            nodo_internos_noActivos.append(produccion.lado_izq)
            id += 1
        #hojas
        for produccion in self.producciones:
            for char in produccion.lado_der:
                if char not in nodo_internos_noActivos:
                    nuevo_arbol.crear_hoja(id, char)
                    id += 1
        
        for produccion in self.producciones:
            nuevo_arbol.buscar_coincidencia(produccion.lado_izq, produccion.lado_der)
        
        #graficar nodos
        for nodo_interno in reversed(nuevo_arbol.nodos_internos):
            dot.node(str(nodo_interno.id), str(nodo_interno.simbolo), shape = 'circle')
            for hoja in nuevo_arbol.hojas:
                dot.node(str(hoja.id), str(hoja.simbolo), shape = 'circle')
        
        #contenctando los nodos creados
        for nodo_interno in nuevo_arbol.nodos_internos:
            for hoja in nodo_interno.hojas:
                dot.edge(str(nodo_interno.id), str(hoja.id), constraint = 'true')
        
        dot.render(filename='Arbol_sintactico', view=True)
        
    
    def imprimir_automata(self):
        automata = self.crear_automata_pila()
        automata.imprimir()
        input('')
    
    def imprimir_no_terminales(self):
        print('')
        print('No terminales creados --> ', *self.no_terminales)
        input('')
    
    def imprimir_terminales(self):
        print('')
        print('Terminales creados --> ', *self.terminales)
        input('')
        
    def imprimir_producciones(self):
        if len(self.producciones) == 0:
            pass
        else:
            for produccion in self.producciones:
                print(produccion.original)
            input('')

class Produccion():
    def __init__(self, lado_izq = '', lado_der = [], original = ''):
        self.lado_izq = lado_izq
        self.lado_der = lado_der
        self.original = original

class Automata_Pila():
    def __init__(self, alfabeto, simbolos_pila):
        self.alfabeto = alfabeto
        self.simbolos_pila = simbolos_pila
        self.transiciones = []
    
    def transicion_inicial(self):
        nueva_transicion = Transicion('i', 'λ', 'λ', 'p', '#')
        self.transiciones.append(nueva_transicion)
    
    def transicion_simbolo_inicial(self, nt_inicial):
        nueva_transicion = Transicion('p', 'λ', 'λ', 'q', nt_inicial)
        self.transiciones.append(nueva_transicion)
    
    def transicion_no_terminal(self, lado_izq, lado_der):
        nueva_transicion = Transicion('q', 'λ', lado_izq, 'q', lado_der)
        self.transiciones.append(nueva_transicion)
    
    def transicion_terminal(self, terminal):
        nueva_transicion = Transicion('q', terminal, terminal, 'q', 'λ')
        self.transiciones.append(nueva_transicion)
    
    def transicion_final(self):
        nueva_transicion = Transicion('q', 'λ', '#', 'f', 'λ')
        self.transiciones.append(nueva_transicion)
    
    def imprimir(self):
        print('S: [i, p, q f]')
        print('Σ: [{}]'.format(', '.join(self.alfabeto)))
        print('Γ: [{}]'.format(', '.join(self.simbolos_pila)))
        print('L: i')
        print('F: f')
        print('T:')
        for transicion in self.transiciones:
            transicion.imprimir()
        
class Transicion():
    def __init__(self, estado_actual, lectura_cadena, sacar_pila, estado_destino, insertar_pila):
        self.estado_actual = estado_actual
        self.lectura_cadena = lectura_cadena
        self.sacar_pila = sacar_pila
        self.estado_destino = estado_destino
        self.insertar_pila = insertar_pila
    
    def imprimir(self):
        return '({}, {}, {}; {}, {})'.format(self.estado_actual, self.lectura_cadena, self.sacar_pila, self.estado_destino, ', '.join(self.insertar_pila).replace(', ', ''))

#-------------------------------------CLASES PARA EL ÁRBOL SINCTÁTICO-------------------------------------
    
class Arbol():
    def __init__(self):
        self.nodos_internos = []
        self.hojas = []
    
    def crear_nodo_interno(self, id, simbolo):
        nuevo_nodo_interno = NodoInterno(id, simbolo)
        self.nodos_internos.append(nuevo_nodo_interno)
    
    def crear_hoja(self, id, simbolo):
        nueva_hoja = Hoja(id, simbolo)
        self.hojas.append(nueva_hoja)
        
    def buscar_coincidencia(self, lado_izquierdo, lado_derecho): #recibe lado izquierdo y derecho de una produccion
        for nodo_interno in self.nodos_internos:
            if nodo_interno.simbolo == lado_izquierdo and nodo_interno.activo == True:
                for simbolo in lado_derecho:
                    for hoja in self.hojas:
                        if hoja.simbolo == simbolo and hoja.activo == True:
                            nodo_interno.hojas.append(hoja)
                            hoja.activo = False
                            break
                nodo_interno.activo = False
                return
    
class NodoInterno():
    def __init__(self, id, simbolo):
        self.id = id
        self.simbolo = simbolo
        self.activo = True
        self.hojas = []

class Hoja():
    def __init__(self, id, simbolo):
        self.id = id
        self.simbolo = simbolo
        self.activo = True

def menu_automataPila():
    limpiar_terminal()
    condicion = True
    
    while condicion == True:
        #print('Lista de gramáticas --> ', lista_gramaticas)
        
        limpiar_terminal()
        
        print('+-----------------------------------+')
        print('|        Autómatas de Pila          |')
        print('+-----------------------------------+')
        print('')
        print('1. Crear/Modificar gramática')
        print('2. Generar Autómata de Pila')
        print('3. Visualizar autómata')
        print('4. Validar cadena')
        print('5. Regresar al menú principal')
        print('')
        
        eleccion = input('Elige una opción: >> ')
        
        if eleccion == '1':
            nombre_gramatica = input('Ingresa un nombre para la gramática: >> ')
            
            if nombre_gramatica == '' or nombre_gramatica == ' ':
                print('Debes ingresar el nombre de una gramática')
                input('')
            else:
                if len(lista_gramaticas) == 0:
                    nueva_gramatica = Gramatica(nombre_gramatica)
                    menu_gramatica(nueva_gramatica)
                else:
                    for gramatica in lista_gramaticas:
                        if nombre_gramatica == gramatica.nombre_gramatica:
                            limpiar_terminal()
                            modificar_gramatica(nombre_gramatica)
                        else:
                            limpiar_terminal()
                            nueva_gramatica = Gramatica(nombre_gramatica)
                            menu_gramatica(nueva_gramatica)
                
        elif eleccion == '2':
            gramatica_buscar = input('Nombre de la gramática: >> ')
            
            for gramatica in lista_gramaticas:
                if gramatica.nombre_gramatica == gramatica_buscar:
                    gramatica.imprimir_automata()
                    gramatica.generar_grafo()
                    limpiar_terminal()
                else:
                    print('No se encontró la gramática')
                    input('')
                    limpiar_terminal()
            
        elif eleccion == '3':
            gramatica_buscar = input('Nombre de la gramática: >> ')
            
            for gramatica in lista_gramaticas:
                if gramatica.nombre_gramatica == gramatica_buscar:
                    gramatica.imprimir_automata()
                    gramatica.generar_grafo()
                    limpiar_terminal()
                else:
                    print('No se encontró la gramática.')
                    input('')
                    limpiar_terminal()
        
        elif eleccion == '4':
            gramatica_buscar = input('Nombre de la gramática para la validacion: >> ')
            
            for gramatica in lista_gramaticas:
                if gramatica.nombre_gramatica == gramatica_buscar:
                    limpiar_terminal()
                    gramatica.validar_cadena()
                else:
                    print('No se encontró una gramática con ese nombre.')
                    input('')
                    limpiar_terminal()
        elif eleccion == '5':
            print('Regresando al mneú prinicipal...')
            input('')
            break
    
def menu_gramatica(gramatica):
    limpiar_terminal()
    
    while True:
        limpiar_terminal()
        print('')
        print('1. Ingresar no terminales')
        print('2. Ingresar terminales')
        print('3. Ingresar producciones')
        print('4. Borrar producciones')
        print('5. No terminal incial')
        print('6. Regresar')
        print('')
        
        eleccion = input('Elige una opción: >> ')
        
        if eleccion == '1':
            limpiar_terminal()
            gramatica.ingresar_no_terminales()
            gramatica.imprimir_no_terminales()
            
        elif eleccion == '2':
            limpiar_terminal()
            gramatica.ingresar_terminales()
            gramatica.imprimir_terminales()
            
        elif eleccion == '3':
            limpiar_terminal()
            gramatica.ingresar_producciones()
            gramatica.imprimir_producciones()
                
        elif eleccion == '4': # opcion que permite eliminar producciones
            if gramatica.producciones == []:
                print('Primero se deben crear producciones')
                input('')
                limpiar_terminal()
            else:
                print('Producciones disponibles:')
                for produccion in gramatica.producciones:
                    print(produccion.original)
                
                produccion_a_eliminar = input('Ingrese la produccion que desea eliminar: >> ')
                gramatica.eliminar_produccion(produccion_a_eliminar)
                    
        elif eleccion == '5': # opción para elegir el no terminal inicial
            gramatica.ingresar_nt_inicial()
            print('No terminal inicial --> ', gramatica.nt_inicial)
            input('')
            limpiar_terminal()
                    
        elif eleccion == '6':
            
            if gramatica.no_terminales == [] or gramatica.terminales == [] or gramatica.producciones == [] or gramatica.nt_inicial == '':
                print('Imposible regresar si no se han ingresado todos los elementos de la gramática')
                input('')
            else:
                producciones_corregidas = gramatica.quitar_recursividad_izq()
                
                if producciones_corregidas == 0:
                    print('Gramática sin recursividad por la izquierda.')
                    for produccion in gramatica.producciones:
                        print(produccion.original)
                    input('')
                    lista_gramaticas.append(gramatica)
                    limpiar_terminal()
                    break
                else:
                    gramatica.producciones = producciones_corregidas
                    gramatica.eliminar_repetidos()
                    print('Gramatica sin recursividad: ')
                    for produccion in gramatica.producciones:
                        print(produccion.original)
                    input('')
                
        else:
            print('Entrada inválida')
            input('')
            limpiar_terminal()
    
def modificar_gramatica(nombre_gramatica):
    pass