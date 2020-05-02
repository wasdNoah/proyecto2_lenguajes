# for transicion in automata.transiciones:
#     if pila[-1] == transicion.sacar_pila and pila_cadena[-1] == transicion.insertar_pila[0]:
#         pila.pop()
#         for char in reversed(transicion.insertar_pila):
#             pila.append(char)
            
#     elif pila[-1] == transicion.sacar_pila and transicion.insertar_pila[0] in self.terminales:
#         for transicion_b in automata.transiciones:
#             if transicion.insertar_pila[0] == transicion_b.sacar_pila and pila_cadena[-1] == transicion_b.insertar_pila[0]:
#                 pila.pop() #sacando el no terminal del tope de la pila
#                 for char in reversed(transicion_b.insertar_pila):
#                     pila.append(char)
    
#     elif pila[-1] == transicion.sacar_pila and transicion.insertar_pila[0] in self.no_terminales:
#         for transicion_b in automata.transiciones:
#             if transicion.insertar_pila[0] == transicion_b.sacar_pila and pila_cadena[-1] == transicion_b.insertar_pila[0]:
#                 pila.pop() #sacando el no terminal del tope de la pila
#                 for char in reversed(transicion_b.insertar_pila):
#                     pila.append(char)
            
#     elif pila[-1] == transicion.sacar_pila and 'epsilon' in transicion.insertar_pila:
#         pila.pop()
        
#     else:
#         print('Cadena inválida xcdddd POR FAVOR FUNCIONA')
#         input('')
#         return