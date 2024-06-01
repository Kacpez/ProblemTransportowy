from flask import Flask
from flask_cors import CORS, cross_origin
from flask import jsonify,request
 
import osmnx as ox
from optymalizacja import vam_metoda, wypisywanie_macierzy, oblicznie_kosztu,generuj_liste
from genetyczne_v3 import genetic_algorithm
import networkx as nx
import numpy as np
from shapely.geometry import shape

#Początkowe miasto
miejsce = ["Wieliczka, Polska"]
coord=[(50.28,19.56)]

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['DEBUG'] = False

def sprawdz_dostepnosc_miejsca(miejsce):
    try:
        G = ox.graph_from_place(miejsce, network_type="drive")
        return True
    except Exception as e:
        return False
 
@app.route("/", methods=['GET'])
@cross_origin()
def hello():
    # Pobieranie danych z OpenStreetMap
    G = ox.graph_from_place(miejsce[0], network_type="drive")

    # Filtracja wierzchołków na podstawie tagów
    tags3={'amenity': 'cafe'}
    tags4={'shop': 'bakery'}


    cafes = ox.geometries_from_place(miejsce[0], tags=tags3)
    print(cafes)
    first_cafe = cafes.iloc[0]
    bakeries = ox.geometries_from_place(miejsce[0], tags=tags4)
    first_bakery = bakeries.iloc[0]

    N=bakeries.shape[0]
    M=cafes.shape[0]
    macierz_kosztu= np.zeros((N,M))
    for i in range(N):
        for j in range(M):
            orig1 = ox.nearest_nodes(G, bakeries.geometry[i].centroid.x, bakeries.geometry[i].centroid.y)
            dest1 = ox.nearest_nodes(G, cafes.geometry[j].centroid.x, cafes.geometry[j].centroid.y)
            length_of_shortest_path = nx.shortest_path_length(G, orig1, dest1, weight='length')
            macierz_kosztu[i][j]=length_of_shortest_path
    macierz_kosztu=np.round(macierz_kosztu,decimals=1)
    macierz=macierz_kosztu.tolist()
    popyt=[]
    podaz=[]
    for i,fb in enumerate(bakeries.iloc):
        geometry=shape(fb['geometry'])
        area=round(geometry.area*10**10)
        if area!=0:
            print(f"Bakery {i} area:{area}")
            popyt.append(area)
        else:
            non_nan_count = fb.notna().sum()
            print(f"Bakery {i} area:{non_nan_count*10}")
            popyt.append(non_nan_count*10)
    print("==========================")
    for i,fc in enumerate(cafes.iloc):
        geometry=shape(fc['geometry'])
        area=round(geometry.area*10**10)
        if area!=0:
            print(f"Cafe {i} area:{area}")
            podaz.append(area)
        else:
            non_nan_count = fc.notna().sum()
            print(f"Cafe {i} area:{non_nan_count*10}")
            podaz.append(non_nan_count*10)
    print(podaz)
    print(popyt)

    #starndaryzacja
    sum_list1 = sum(popyt)
    sum_list2 = sum(podaz)

    desired_sum = sum_list1
    scaling_factor_list1 = desired_sum / sum_list1
    scaling_factor_list2 = desired_sum / sum_list2

    scaled_popyt = [round(x * scaling_factor_list1) for x in popyt]
    scaled_podaz = [round(x * scaling_factor_list2) for x in podaz]
    rest=sum(scaled_podaz)-sum(scaled_popyt)
    scaled_podaz[-1]-=rest
    print("Scaled popyt:", scaled_popyt)
    print("Scaled podaz:", scaled_podaz)

    popyt_lista=[scaled_popyt]
    podaz_lista=[scaled_podaz]

    return jsonify({"macierz_kosztu": macierz,
                    "popyt":popyt_lista[0],
                    "podaz":podaz_lista[0]
                    })


rr=[]
@app.route("/miasto", methods=['POST','GET'])
@cross_origin()
def miasto():
    try:
        if request.method == 'GET':
            return jsonify({'miejsce': miejsce[0], 'coordinaties': coord[0]})
        elif request.method == 'POST':
            data = request.get_json()
            print('Odebrane dane:', data['selectedCity'])
            miejsce[0] = data['selectedCity']
            coord[0]=ox.geocode(miejsce[0])
            return jsonify({'success': True}), 200
    except Exception as e:
        print('Błąd:', e)
        return jsonify({'success': False, 'error': str(e)}), 500


print(miejsce[0])
# Pobieranie danych z OpenStreetMap
G = ox.graph_from_place(miejsce[0], network_type="drive")

# Filtracja wierzchołków na podstawie tagów
tags3={'amenity': 'cafe'}
tags4={'shop': 'bakery'}


cafes = ox.geometries_from_place(miejsce[0], tags=tags3)
print(cafes)
first_cafe = cafes.iloc[0]
bakeries = ox.geometries_from_place(miejsce[0], tags=tags4)
first_bakery = bakeries.iloc[0]

N=bakeries.shape[0]
M=cafes.shape[0]
macierz_kosztu= np.zeros((N,M))
for i in range(N):
    for j in range(M):
        orig1 = ox.nearest_nodes(G, bakeries.geometry[i].centroid.x, bakeries.geometry[i].centroid.y)
        dest1 = ox.nearest_nodes(G, cafes.geometry[j].centroid.x, cafes.geometry[j].centroid.y)
        length_of_shortest_path = nx.shortest_path_length(G, orig1, dest1, weight='length')
        macierz_kosztu[i][j]=length_of_shortest_path
macierz_kosztu=np.round(macierz_kosztu,decimals=1)
macierz=macierz_kosztu.tolist()

popyt=[]
podaz=[]
for i,fb in enumerate(bakeries.iloc):
    geometry=shape(fb['geometry'])
    area=round(geometry.area*10**10)
    if area!=0:
        print(f"Bakery {i} area:{area}")
        popyt.append(area)
    else:
        non_nan_count = fb.notna().sum()
        print(f"Bakery {i} area:{non_nan_count*10}")
        popyt.append(non_nan_count*10)
print("==========================")
for i,fc in enumerate(cafes.iloc):
    geometry=shape(fc['geometry'])
    area=round(geometry.area*10**10)
    if area!=0:
        print(f"Cafe {i} area:{area}")
        podaz.append(area)
    else:
        non_nan_count = fc.notna().sum()
        print(f"Cafe {i} area:{non_nan_count*10}")
        podaz.append(non_nan_count*10)
print(podaz)
print(popyt)

#starndaryzacja
sum_list1 = sum(popyt)
sum_list2 = sum(podaz)

desired_sum = sum_list1

scaling_factor_list1 = desired_sum / sum_list1
scaling_factor_list2 = desired_sum / sum_list2

scaled_popyt = [round(x * scaling_factor_list1) for x in popyt]
scaled_podaz = [round(x * scaling_factor_list2) for x in podaz]
rest=sum(scaled_podaz)-sum(scaled_popyt)
scaled_podaz[-1]-=rest
print("Scaled popyt:", scaled_popyt)
print("Scaled podaz:", scaled_podaz)

popyt_lista=[scaled_popyt]
podaz_lista=[scaled_podaz]

n = N
m = M

@app.route('/get_n_m', methods=['GET'])
def get_n_m():
    return jsonify({'n': n, 'm': m})

@app.route('/endpoint', methods=['POST','GET'])
def handle_form_data():
    try:
        if request.method == 'GET':
            return jsonify({'popyt':popyt_lista[0],'podaz':podaz_lista[0]})
        elif request.method == 'POST':
            data = request.get_json()
            popyt_lista[0] = data.get('popyty')
            podaz_lista[0] = data.get('podazy')
            print('Odebrane dane:', {'popyty': popyt_lista[0], 'podazy': podaz_lista[0]})
            return jsonify({'success': True}), 200
    except Exception as e:
        print('Błąd:', e)
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route("/cele", methods=['GET'])
@cross_origin()
def cele():
    # Pobieranie danych z OpenStreetMap
    G = ox.graph_from_place(miejsce[0], network_type="drive")

    # Filtracja wierzchołków na podstawie tagów
    tags3={'amenity': 'cafe'}
    tags4={'shop': 'bakery'}


    cafes = ox.geometries_from_place(miejsce[0], tags=tags3)
    print(cafes)
    first_cafe = cafes.iloc[0]
    bakeries = ox.geometries_from_place(miejsce[0], tags=tags4)
    first_bakery = bakeries.iloc[0]

    N=bakeries.shape[0]
    M=cafes.shape[0]
    macierz_kosztu= np.zeros((N,M))
    for i in range(N):
        for j in range(M):
            orig1 = ox.nearest_nodes(G, bakeries.geometry[i].centroid.x, bakeries.geometry[i].centroid.y)
            dest1 = ox.nearest_nodes(G, cafes.geometry[j].centroid.x, cafes.geometry[j].centroid.y)
            length_of_shortest_path = nx.shortest_path_length(G, orig1, dest1, weight='length')
            macierz_kosztu[i][j]=length_of_shortest_path
    macierz_kosztu=np.round(macierz_kosztu,decimals=1)
    macierz=macierz_kosztu.tolist()
    BAKERY=[]
    for i in range(N):
        x=bakeries.geometry[i].centroid.x
        y=bakeries.geometry[i].centroid.y
        BAKERY.append([x,y])

    CAFE=[]
    for i in range(M):
        x=cafes.geometry[i].centroid.x
        y=cafes.geometry[i].centroid.y
        CAFE.append([x,y])

    return jsonify({"bakeries": BAKERY,
                    "cafes": CAFE,
                    "center": "1"
                    })

@app.route("/algorytm_optymalizacyjny", methods=['GET'])
@cross_origin()
def optymalizacja():
    G = ox.graph_from_place(miejsce[0], network_type="drive")
    tags3={'amenity': 'cafe'}
    tags4={'shop': 'bakery'}

    cafes = ox.geometries_from_place(miejsce[0], tags=tags3)
    bakeries = ox.geometries_from_place(miejsce[0], tags=tags4)
    popyt=[]
    podaz=[]
    for i,fb in enumerate(bakeries.iloc):
        geometry=shape(fb['geometry'])
        area=round(geometry.area*10**10)
        if area!=0:
            popyt.append(area)
        else:
            non_nan_count = fb.notna().sum()
            popyt.append(non_nan_count*10)
    for i,fc in enumerate(cafes.iloc):
        geometry=shape(fc['geometry'])
        area=round(geometry.area*10**10)
        if area!=0:
            podaz.append(area)
        else:
            non_nan_count = fc.notna().sum()
            podaz.append(non_nan_count*10)

    sum_list1 = sum(popyt)
    sum_list2 = sum(podaz)
    desired_sum = sum_list1
    scaling_factor_list1 = desired_sum / sum_list1
    scaling_factor_list2 = desired_sum / sum_list2
    scaled_popyt = [round(x * scaling_factor_list1) for x in popyt]
    scaled_podaz = [round(x * scaling_factor_list2) for x in podaz]
    rest=sum(scaled_podaz)-sum(scaled_popyt)
    scaled_podaz[-1]-=rest
    
    popyt_lista=[scaled_popyt]
    podaz_lista=[scaled_podaz]
    N=bakeries.shape[0]
    M=cafes.shape[0]
    macierz_kosztu= np.zeros((N,M))
    for i in range(N):
        for j in range(M):
            orig1 = ox.nearest_nodes(G, bakeries.geometry[i].centroid.x, bakeries.geometry[i].centroid.y)
            dest1 = ox.nearest_nodes(G, cafes.geometry[j].centroid.x, cafes.geometry[j].centroid.y)
            length_of_shortest_path = nx.shortest_path_length(G, orig1, dest1, weight='length')
            macierz_kosztu[i][j]=length_of_shortest_path
    macierz_kosztu=np.round(macierz_kosztu,decimals=1)
    macierz_wynikowa4=vam_metoda(macierz_kosztu,popyt_lista[0],podaz_lista[0])
    macierz_wynikowa4=macierz_wynikowa4.tolist()

    lista_wsporzednych_tras=[]
    for i in range(N):
        trasa_dostawcy=[]
        for j in range(M):
            wsp_sciezki=[]
            if macierz_wynikowa4[i][j]!=0:
                wsp_sciezki.append([bakeries.geometry[i].centroid.y, bakeries.geometry[i].centroid.x])
                orig1 = ox.nearest_nodes(G, bakeries.geometry[i].centroid.x, bakeries.geometry[i].centroid.y)
                dest1 = ox.nearest_nodes(G, cafes.geometry[j].centroid.x, cafes.geometry[j].centroid.y)
                route1 = nx.shortest_path(G, orig1, dest1, weight='length')            
                for r in route1:
                    node_coordinates = G.nodes[r]['y'], G.nodes[r]['x']
                    wsp_sciezki.append(list(node_coordinates))
                wsp_sciezki.append([cafes.geometry[j].centroid.y, cafes.geometry[j].centroid.x])

            trasa_dostawcy.append(wsp_sciezki)
        lista_wsporzednych_tras.append(trasa_dostawcy)
    return jsonify({"lista_wsporzednych_tras": lista_wsporzednych_tras,
                    "najlepszy_koszt": np.round(oblicznie_kosztu(macierz_kosztu,macierz_wynikowa4),decimals=1),
                    "macierz_wynikowa":macierz_wynikowa4
                    })


@app.route("/algorytm_genetyczny", methods=['GET'])
@cross_origin()
def genetyczne():
    # Pobieranie danych z OpenStreetMap
    G = ox.graph_from_place(miejsce[0], network_type="drive")

    # Filtracja wierzchołków na podstawie tagów
    tags3={'amenity': 'cafe'}
    tags4={'shop': 'bakery'}


    cafes = ox.geometries_from_place(miejsce[0], tags=tags3)
    print(cafes)
    first_cafe = cafes.iloc[0]
    bakeries = ox.geometries_from_place(miejsce[0], tags=tags4)
    first_bakery = bakeries.iloc[0]
    popyt=[]
    podaz=[]
    for i,fb in enumerate(bakeries.iloc):
        geometry=shape(fb['geometry'])
        area=round(geometry.area*10**10)
        if area!=0:
            print(f"Bakery {i} area:{area}")
            popyt.append(area)
        else:
            non_nan_count = fb.notna().sum()
            print(f"Bakery {i} area:{non_nan_count*10}")
            popyt.append(non_nan_count*10)
    print("==========================")
    for i,fc in enumerate(cafes.iloc):
        geometry=shape(fc['geometry'])
        area=round(geometry.area*10**10)
        if area!=0:
            print(f"Cafe {i} area:{area}")
            podaz.append(area)
        else:
            non_nan_count = fc.notna().sum()
            print(f"Cafe {i} area:{non_nan_count*10}")
            podaz.append(non_nan_count*10)
    print(podaz)
    print(popyt)

    #starndaryzacja
    sum_list1 = sum(popyt)
    sum_list2 = sum(podaz)

    desired_sum = sum_list1

    scaling_factor_list1 = desired_sum / sum_list1
    scaling_factor_list2 = desired_sum / sum_list2

    scaled_popyt = [round(x * scaling_factor_list1) for x in popyt]
    scaled_podaz = [round(x * scaling_factor_list2) for x in podaz]
    rest=sum(scaled_podaz)-sum(scaled_popyt)
    scaled_podaz[-1]-=rest
    print("Scaled popyt:", scaled_popyt)
    print("Scaled podaz:", scaled_podaz)

    popyt_lista=[scaled_popyt]
    podaz_lista=[scaled_podaz]
    N=bakeries.shape[0]
    M=cafes.shape[0]
    macierz_kosztu= np.zeros((N,M))
    for i in range(N):
        for j in range(M):
            orig1 = ox.nearest_nodes(G, bakeries.geometry[i].centroid.x, bakeries.geometry[i].centroid.y)
            dest1 = ox.nearest_nodes(G, cafes.geometry[j].centroid.x, cafes.geometry[j].centroid.y)
            length_of_shortest_path = nx.shortest_path_length(G, orig1, dest1, weight='length')
            macierz_kosztu[i][j]=length_of_shortest_path
    macierz_kosztu=np.round(macierz_kosztu,decimals=1)
    macierz=macierz_kosztu.tolist()
    population_size = 400
    generations = 150
    mutation_rate = 0.3
    macierz_wynikowa4, best_cost,history = genetic_algorithm(population_size, generations, mutation_rate,macierz_kosztu,popyt_lista[0].copy(),podaz_lista[0].copy())
    macierz_wynikowa4=macierz_wynikowa4.tolist()
    
    lista_wsporzednych_tras=[]
    for i in range(N):
        trasa_dostawcy=[]
        for j in range(M):
            wsp_sciezki=[]
            

            if macierz_wynikowa4[i][j]!=0:
                wsp_sciezki.append([bakeries.geometry[i].centroid.y, bakeries.geometry[i].centroid.x])
                orig1 = ox.nearest_nodes(G, bakeries.geometry[i].centroid.x, bakeries.geometry[i].centroid.y)
                dest1 = ox.nearest_nodes(G, cafes.geometry[j].centroid.x, cafes.geometry[j].centroid.y)
                route1 = nx.shortest_path(G, orig1, dest1, weight='length')
            
                for r in route1:
                    node_coordinates = G.nodes[r]['y'], G.nodes[r]['x']
                    wsp_sciezki.append(list(node_coordinates))
                wsp_sciezki.append([cafes.geometry[j].centroid.y, cafes.geometry[j].centroid.x])

            trasa_dostawcy.append(wsp_sciezki)
        lista_wsporzednych_tras.append(trasa_dostawcy)
    return jsonify({"lista_wsporzednych_tras": lista_wsporzednych_tras,
                    "najlepszy_koszt": np.round(best_cost,decimals=1),
                    "macierz_wynikowa":macierz_wynikowa4
                    })

