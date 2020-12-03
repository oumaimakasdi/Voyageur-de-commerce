# -*- coding: utf-8 -*-
import math
import matplotlib.pyplot as plt
import mpl_toolkits.basemap
import time

# Debut du decompte du temps
start_time = time.time()

from aco import ACO, Graph

def distance(city1: dict, city2: dict):

      distanceX = (city1['x']-city2['x'])*40000*math.cos((city1['y'] - city2['y'])*math.pi/360)/360
      distanceY = (city1['y'] - city2['y'])*40000/360
      distance = math.sqrt( (distanceX*distanceX) + (distanceY*distanceY) )
      return distance



def main():
    cities = []
    points = []
    with open('D:\les cours\Master\S2\AlgoBigData\PVC\pvc-grp3\Code_Fourmis\Villes100.txt') as f:
        for line in f.readlines():
            city = line.strip().split(' ')
            cities.append(dict(index=int(city[0]), x=float(city[1]), y=float(city[2]),z=str(city[3])))
            points.append((float(city[1]), float(city[2])))
    cost_matrix = []
    rank = len(cities)
    for i in range(rank):
        row = []
        for j in range(rank):
            row.append(distance(cities[i], cities[j]))
        cost_matrix.append(row)
    """aco = ACO(100, 100, 1, 10.0, 0.5, 10, 2)"""
    aco = ACO(10,100, 1, 10.0, 0.5, 10, 2)
    graph = Graph(cost_matrix, rank)
    path, cost = aco.solve(graph)
    p=[]
    d=dict()
    for j in range(len(cities)):
        d[cities[j]["index"]]=cities[j]["z"]

    p=[]
    for i in path:
        if i in d.keys():
            p.append(d[i])

    print('cost: {}, path: {}'.format(cost, p))
    a=time.time() - start_time

# Affichage du temps d'execution
    print("_______________________________________________________________________________________")
    if(a<60):
        b=a
        print("Temps de calcul : %s secondes" % (b))
    elif(a>=60*60*24):
        b=a/(60*60*24)
        print("Temps de calcul : %s jours" % (b))
    elif(a>60*60):
        b=a/(60*60)
        print("Temps de calcul : %s heures" % (b))
    elif(a>60):
        b=a/60
        print("Temps de calcul : %s minutes" % (b))
    lons = []
    lats = []
    noms = []

    for i in path:
      for j in range(len(cities)):
          if cities[j]["index"]==i:
              lons.append(cities[j]["x"])
              lats.append(cities[j]["y"])
              noms.append(cities[j]["z"])

    plt.figure(figsize=(20,20))

    map = mpl_toolkits.basemap.Basemap(projection='merc',llcrnrlat=10,urcrnrlat=40,llcrnrlon=-20,
             urcrnrlon=0, resolution='c')
    map.drawmapboundary(fill_color='#AADAFF')
    map.fillcontinents(color='#F8F3DA',lake_color='#AADAFF')
    map.drawcoastlines()
    map.drawcountries()
    x,y = map(lons,lats)
    map.plot(x,y,'bo', markersize=12)
    for nom,xpt,ypt in zip(noms,x,y):
       plt.text(xpt+5000,ypt+25000,nom)

    map.plot(x, y, 'D-', markersize=10, linewidth=2, color='gold', markerfacecolor='b')
    plt.show()

if __name__ == '__main__':
    main()
