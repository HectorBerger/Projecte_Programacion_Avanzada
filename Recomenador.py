from dataset import Dataset
import numpy as np
import math

class Recomenador:
    _dataset: Dataset

    def __init__(self, dataset): #-> bool:
        self._dataset = dataset
        #hauriem de tenir un atribut array?
        return None
        
    def __str__(self):
        return #f"Recomanació per a l'usuari {usuari}: {recom._dataset._items[recom._dataset._pos_items[recomanacio[0][1]]]} amb score {round(recomanacio[0][0], 1)} "
    
    def recomanacio_simple(self, user_id, min_vots=3):
        # Comprova si l’usuari existeix al dataset
        if user_id not in self._dataset.get_users():
            print(f"Usuari {user_id} no trobat.")
            return None

        # Obté la fila de la matriu que correspon a aquest usuari i les seves valoracions
        user_row = self._dataset.get_row_user(user_id) #crear getters
        user_ratings = self._dataset._ratings[user_row]

        millor_item = None # Aquí guardarem l’ítem recomanat
        millor_score = -1  # Inicialitzem el millor score
                #!#!Habría que hacerlo al iniciar los datasets?
        avg_global = self.get_avg_global() #Calculem la mitjana global 
        llista_valoracions = [] #On guardarem totes les valoracions

        # Iterem per tots els ítems disponibles
        for item_id, col in self._dataset._pos_items.items():
            # Si l’usuari ja ha valorat aquest ítem, el saltem
            if user_ratings[col] > 0:
                continue  # Ja l'ha valorat

            # Comptem quants vots té aquest ítem i mirem que sigui fiable
            num_vots = self.get_num_vots(item_id)
            if num_vots < min_vots:
                continue  # No prou fiable

            # Calculem la mitjana d’aquest ítem 
            avg_item = self.get_avg(item_id)

            # Calculem el score ponderat segons la fórmula
            score = (num_vots / (num_vots + min_vots)) * avg_item + \
                    (min_vots / (num_vots + min_vots)) * avg_global

            """
            # Si aquest score és millor que l’anterior, l’actualitzem
            if score > millor_score:
                millor_score = score
                millor_item = item_id
            """
            
            #Guardem un tuple a la llista de valoracions el score i el id del item
            llista_valoracions.append((score, item_id)) #!#! No es más lógico del reves?

        llista_valoracions = sorted(llista_valoracions, key=lambda x: x[0], reverse=True) #Ordenem segons el score de més gran a més petit
        
        return llista_valoracions[:5]

    def recomanacio_colaboratiu(self, user_id, k):
        
        array_ratings = self._dataset.get_ratings()
        llista_recomenacions = []
        user_pos = self._dataset.get_row_user(user_id)
        user_row = array_ratings[user_pos]
        llista_similitud = []

        #1
        for i,row in enumerate(array_ratings): #i = numero de fila del veï 
            if user_pos != i:
                mask = (user_row != -1) & (row != -1)
                if np.any(mask):
                    denominator = (
                        math.sqrt(np.sum(np.power(user_row[mask], 2))) *
                        math.sqrt(np.sum(np.power(row[mask], 2)))
                    )
                    if denominator != 0:
                        similitud = np.dot(user_row[mask], row[mask]) / denominator
                    else:
                        similitud = 0
                else:
                    similitud = 0

                llista_similitud.append( (i,similitud) )


        #2
        llista_similitud = sorted(llista_similitud, key=lambda x: x[1], reverse=True)[:k] #Ordenem segons el score de més gran a més petit

        # Step 3: Calculate scores for items not rated by the user
        
        #Pre-càlculs per ser més eficients i l'array dels top-k veins 
        mitja_user = np.mean(user_row[user_row != -1]) #Esto lo podriamos hacer al iniciar en el pickle
        veins_arrays = array_ratings[[sim[0] for sim in llista_similitud], :]
        mitjas_veins = np.column_stack(np.array([np.mean(row[row != -1]) if np.any(row != -1) else 0 for row in veins_arrays]))  # Mean ratings of all neighbors
        columna_similitud = np.column_stack(np.array([sim[1] for sim in llista_similitud])) # Similarities with top-k veins

        for item_id, col in self._dataset._pos_items.items(): #S'ha d'iterar per items no vists per l'user (columnes)
            if user_row[col] == -1:  # Only consider items not rated by the user
                veins_col = np.column_stack(veins_arrays[:, col])  # Ratings of the current item by all neighbors

                # Mask for neighbors who rated the item
                veins_mask = veins_col != -1

                # Calculate the numerator and denominator
                numerator = np.sum( columna_similitud[veins_mask] * (veins_col[veins_mask] - mitjas_veins[veins_mask]) )
                denominator = np.sum(np.abs(columna_similitud[veins_mask]))

                # Calculate the final score
                if denominator != 0:
                    score = mitja_user + numerator / denominator
                else:
                    score = mitja_user  # Default to the user's mean if no neighbors rated the item
                
                llista_recomenacions.append((score, item_id)) # Append the score and item ID #!#! Cómo he puesto antesno es más lógico del reves?

        # Sort the scores and return the top 5 recommendations
        llista_recomenacions = sorted(llista_recomenacions, key=lambda x: x[1], reverse=True )
        return llista_recomenacions[:5]

    #!#!#Mejorar lógica intentar hacerlos más generales i iniciarlos al principio con los datasets
    def get_num_vots(self, item_id): 
        col = self._dataset._pos_items[item_id]  # Obté la columna corresponent
        column_values = self._dataset._ratings[:, col]  # Obté els valors de la columna
        return np.count_nonzero(column_values)  # Retorna quantes valoracions són no-zero (valoracions reals)

    def get_avg(self, item_id):
        col = self._dataset._pos_items[item_id]   # Obté la columna corresponent a l'ítem
        values = self._dataset._ratings[:, col]   # Obté els valors de la columna
        avaluades = values[values != -1] # Filtra només les valoracions que han estat efectuadas
        return np.mean(avaluades) if len(avaluades) > 0 else 0  # Retorna la mitjana si n’hi ha
    
    def get_avg_global(self):
        all_ratings = self._dataset._ratings # Obté tota la matriu de valoracions del dataset
        avaluades = all_ratings[all_ratings != -1]  # Filtra només les valoracions que han estat efectuadas
        return np.mean(avaluades) if len(avaluades) > 0 else 0 # Retorna la mitjana global
    

    #def get_item(self,id):