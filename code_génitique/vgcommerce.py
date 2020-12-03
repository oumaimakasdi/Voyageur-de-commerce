
import time
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

# Debut du decompte du temps
start_time = time.time()


import math
import random

class Ville:
   def __init__(self, lon, lat, nom):
      self.lon = lon
      self.lat = lat
      self.nom = nom


   def distance(self, ville):
      distanceX = (ville.lon-self.lon)*40000*math.cos((self.lat+ville.lat)*math.pi/360)/360
      distanceY = (self.lat-ville.lat)*40000/360
      distance = math.sqrt( (distanceX*distanceX) + (distanceY*distanceY) )
      return distance
class GestionnaireCircuit:
   villesDestinations = []

   def ajouterVille(self, ville):
      self.villesDestinations.append(ville)

   def getVille(self, index):
      return self.villesDestinations[index]

   def nombreVilles(self):
      return len(self.villesDestinations)

class Circuit:
   def __init__(self, gestionnaireCircuit, circuit=None):
      self.gestionnaireCircuit = gestionnaireCircuit
      self.circuit = []
      self.fitness = 0.0
      self.distance = 0
      if circuit is not None:
         self.circuit = circuit
      else:
         for i in range(0, self.gestionnaireCircuit.nombreVilles()):
            self.circuit.append(None)

   def __len__(self):
      return len(self.circuit)

   def __getitem__(self, index):
     return self.circuit[index]

   def __setitem__(self, key, value):
     self.circuit[key] = value

   def genererIndividu(self):
     for indiceVille in range(0, self.gestionnaireCircuit.nombreVilles()):
        self.setVille(indiceVille, self.gestionnaireCircuit.getVille(indiceVille))
     random.shuffle(self.circuit)

   def getVille(self, circuitPosition):
     return self.circuit[circuitPosition]

   def setVille(self, circuitPosition, ville):
     self.circuit[circuitPosition] = ville
     self.fitness = 0.0
     self.distance = 0

   def getFitness(self):
     if self.fitness == 0:
        self.fitness = 1/float(self.getDistance())
     return self.fitness

   def getDistance(self):
     if self.distance == 0:
        circuitDistance = 0
        for indiceVille in range(0, self.tailleCircuit()):
           villeOrigine = self.getVille(indiceVille)
           villeArrivee = None
           if indiceVille+1 < self.tailleCircuit():
              villeArrivee = self.getVille(indiceVille+1)
           else:
              villeArrivee = self.getVille(0)
           circuitDistance += villeOrigine.distance(villeArrivee)
        self.distance = circuitDistance
     return self.distance

   def tailleCircuit(self):
     return len(self.circuit)

   def contientVille(self, ville):
     return ville in self.circuit


class Population:
   def __init__(self, gestionnaireCircuit, taillePopulation, init):
      self.circuits = []
      for i in range(0, taillePopulation):
         self.circuits.append(None)

      if init:
         for i in range(0, taillePopulation):
            nouveauCircuit = Circuit(gestionnaireCircuit)
            nouveauCircuit.genererIndividu()
            self.sauvegarderCircuit(i, nouveauCircuit)

   def __setitem__(self, key, value):
      self.circuits[key] = value

   def __getitem__(self, index):
      return self.circuits[index]

   def sauvegarderCircuit(self, index, circuit):
      self.circuits[index] = circuit

   def getCircuit(self, index):
      return self.circuits[index]

   def getFittest(self):
      fittest = self.circuits[0]
      for i in range(0, self.taillePopulation()):
         if fittest.getFitness() <= self.getCircuit(i).getFitness():
            fittest = self.getCircuit(i)
      return fittest

   def taillePopulation(self):
      return len(self.circuits)
class GA:
   def __init__(self, gestionnaireCircuit):
      self.gestionnaireCircuit = gestionnaireCircuit
      self.tauxMutation = 0.015
      self.tailleTournoi =5
      self.elitisme = True

   def evoluerPopulation(self, pop):
      nouvellePopulation = Population(self.gestionnaireCircuit, pop.taillePopulation(), False)
      elitismeOffset = 0
      if self.elitisme:
         nouvellePopulation.sauvegarderCircuit(0, pop.getFittest())
         elitismeOffset = 1

      for i in range(elitismeOffset, nouvellePopulation.taillePopulation()):
         parent1 = self.selectionTournoi(pop)
         parent2 = self.selectionTournoi(pop)
         enfant = self.crossover(parent1, parent2)
         nouvellePopulation.sauvegarderCircuit(i, enfant)

      for i in range(elitismeOffset, nouvellePopulation.taillePopulation()):
         self.muter(nouvellePopulation.getCircuit(i))

      return nouvellePopulation


   def crossover(self, parent1, parent2):
      enfant = Circuit(self.gestionnaireCircuit)

      startPos = int(random.random() * parent1.tailleCircuit())
      endPos = int(random.random() * parent1.tailleCircuit())

      for i in range(0, enfant.tailleCircuit()):
         if startPos < endPos and i > startPos and i < endPos:
            enfant.setVille(i, parent1.getVille(i))
         elif startPos > endPos:
            if not (i < startPos and i > endPos):
               enfant.setVille(i, parent1.getVille(i))

      for i in range(0, parent2.tailleCircuit()):
         if not enfant.contientVille(parent2.getVille(i)):
            for ii in range(0, enfant.tailleCircuit()):
               if enfant.getVille(ii) == None:
                  enfant.setVille(ii, parent2.getVille(i))
                  break

      return enfant

   def muter(self, circuit):
     for circuitPos1 in range(0, circuit.tailleCircuit()):
        if random.random() < self.tauxMutation:
           circuitPos2 = int(circuit.tailleCircuit() * random.random())

           ville1 = circuit.getVille(circuitPos1)
           ville2 = circuit.getVille(circuitPos2)

           circuit.setVille(circuitPos2, ville1)
           circuit.setVille(circuitPos1, ville2)

   def selectionTournoi(self, pop):
     tournoi = Population(self.gestionnaireCircuit, self.tailleTournoi, False)
     for i in range(0, self.tailleTournoi):
        randomId = int(random.random() * pop.taillePopulation())
        tournoi.sauvegarderCircuit(i, pop.getCircuit(randomId))
     fittest = tournoi.getFittest()
     return fittest

if __name__ == '__main__':

   gc = GestionnaireCircuit()

   #on cree nos villes

   ville1 = Ville( -8.976985099999979, 29.7182191, 'Tafraoute')
   gc.ajouterVille(ville1)
   ville2 = Ville( -12.926285099999973, 27.9375382, 'Tarfaya')
   gc.ajouterVille(ville2)
   ville3 = Ville( -8.874876500000028, 30.4727126, 'Taroudante')
   gc.ajouterVille(ville3)
   ville4 = Ville(-7.975634300000024, 29.750877, 'Tata')
   gc.ajouterVille(ville4)
   ville5 = Ville( -6.927396899999962, 33.9203274, 'Temara')
   gc.ajouterVille(ville5)
   ville6 = Ville( -2.8935027999999647,34.3983716, 'Taourirte')
   gc.ajouterVille(ville6)

   ville7 = Ville(-6.3207151000000295,33.8954803, 'Tifelt')
   gc.ajouterVille(ville7)
   ville8 = Ville(-7.484122200000002,33.5507563, 'Tit melil')
   gc.ajouterVille(ville8)
   ville9 = Ville(-4.727752799999962, 31.9051275, 'Tafilate')
   gc.ajouterVille(ville9)
   ville10 = Ville( -9.73215700000003, 29.693392, 'Tiznit')
   gc.ajouterVille(ville10)

   ville11 = Ville(-4.639869299999987, 34.536917, 'Taounate')
   gc.ajouterVille(ville11)
   ville12 = Ville(-8.52267059999997, 32.2438426, 'Youssoufia')
   gc.ajouterVille(ville12)
   ville13 = Ville(-5.840658699999949, 30.34589979999999, 'Zagoura')
   gc.ajouterVille(ville13)
   ville14 = Ville(-8.709578899999997, 32.6243878, 'Zemamra')
   gc.ajouterVille(ville14)
   ville15 = Ville( -7.5898434, 33.5731104, 'Casablanca')
   gc.ajouterVille(ville15)
   ville16 = Ville( -5.0002800,34.0331300, 'Fes')
   gc.ajouterVille(ville16)
   ville17 = Ville(-9.2371800, 32.2993900, 'Safi')
   gc.ajouterVille(ville17)
   ville18 = Ville(-5.7077500, 34.2214900 , 'Sidi Kacem ')
   gc.ajouterVille(ville18)
   ville19 = Ville(-5.7997500, 35.7672700, 'Tanger')
   gc.ajouterVille(ville19)
   ville20 = Ville(-6.7984600,34.0531000, 'Salé ')
   gc.ajouterVille(ville20)
   
   ville21 = Ville(-7.9999400, 31.6341600, 'Marrakech ')
   gc.ajouterVille(ville21)
   ville22 = Ville(-5.5472700, 33.8935200, 'Meknès')
   gc.ajouterVille(ville22)
   ville23 = Ville(-6.8325500, 34.0132500, 'Rabat')
   gc.ajouterVille(ville23)
   ville24 = Ville(-1.9085800,34.6813900, 'Oujda')
   gc.ajouterVille(ville24)
   ville25 = Ville(-6.5802000, 34.2610100, 'Kénitra  ')
   gc.ajouterVille(ville25)
   ville26 = Ville(-9.5981500, 30.4201800, 'Agadir')
   gc.ajouterVille(ville26)
   ville27 = Ville(-5.3683700, 35.5784500, 'Tétouan')
   gc.ajouterVille(ville27)
   ville28 = Ville(-7.3829800, 33.6860700, 'Mohammédia')
   gc.ajouterVille(ville28)
   ville29 = Ville(-6.9063000,32.8810800, 'Khouribga')
   gc.ajouterVille(ville29)
   ville30 = Ville(-8.5060200,33.2549200, 'El Jadida ')
   gc.ajouterVille(ville30)
   ville31 = Ville(-6.3498300, 32.3372500, 'Béni Mellal ')
   gc.ajouterVille(ville31)
   ville32 = Ville(-4.0100000, 34.2100000, 'Taza')
   gc.ajouterVille(ville32)
   ville33 = Ville(-5.6616700,32.9349200, 'Khénifra')
   gc.ajouterVille(ville33)
   ville34 = Ville(-9.7700000,31.5125000, 'Essaouira')
   gc.ajouterVille(ville34)
   ville35 = Ville(-3.9372300, 35.2516500, 'Al Hoceima ')
   gc.ajouterVille(ville35)
   ville36 = Ville(-2.3200000,34.9200000, ' Berkane')
   gc.ajouterVille(ville36)
   ville37 = Ville( -1.9620900, 32.5337900, 'Bouafra ')
   gc.ajouterVille(ville37)
   ville38 = Ville( -5.2636000, 35.1687800, 'Chechaouèn ')
   gc.ajouterVille(ville38)
   ville39 = Ville(-10.0573800, 28.9869600, 'Guelmim ')
   gc.ajouterVille(ville39)
   ville40 = Ville(-2.9335200, 35.1681300, 'Nador')
   gc.ajouterVille(ville40)
   ville41 = Ville(-6.7746400, 32.9004600, ' Boujniba ')
   gc.ajouterVille(ville41)
   ville42 = Ville(-6.573000, 31.964910, 'Azilal')
   gc.ajouterVille(ville42)
   ville43 = Ville(-5.231887, 33.4347305, 'Azrou')
   gc.ajouterVille(ville43)
   ville44 = Ville(-7.4503829,33.6353103, 'Ain Harrouda')
   gc.ajouterVille(ville44)
   ville45 = Ville(-7.13055359,33.6189698, 'Ben Slimane')
   gc.ajouterVille(ville45)
   ville46 = Ville(-7.011459000000059,31.7320849, 'Demnate')
   gc.ajouterVille(ville46)
   ville47 = Ville(-7.5843171,33.268687, 'Berrechide')
   gc.ajouterVille(ville47)
   ville48 = Ville(-7.63311299999998,33.4497542, 'Bouskoura')
   gc.ajouterVille(ville48)
   ville49 = Ville(-7.159941900000035,33.7734338, 'Bouznika')
   gc.ajouterVille(ville49)
   ville50 = Ville(-4.730339700000059,33.3625159, 'Boulmane')
   gc.ajouterVille(ville50)
   ville51 = Ville(-6.393222000000037,32.7691969, 'Bejaad')
   gc.ajouterVille(ville51)
   ville52 = Ville(-4.428498499999932,31.927236, 'Errachidia')
   gc.ajouterVille(ville52)
   ville53 = Ville(-11.67836710000006,26.741856, 'Essmara')
   gc.ajouterVille(ville53)
   ville54 = Ville(-7.227533600000015,33.2787909, 'El gara')
   gc.ajouterVille(ville54)
   ville55 = Ville(-5.367784400000005,33.685735, 'El hajeb')
   gc.ajouterVille(ville55)
   ville56 = Ville(-9.029470800000013,32.7361897, 'Loualidia')
   gc.ajouterVille(ville56)
   ville57 = Ville(-8.00016329999994,33.3736523, 'Lbir jdid')
   gc.ajouterVille(ville57)
   ville58 = Ville(-13.199075799999946,27.1500384, 'Laayoun')
   gc.ajouterVille(ville58)
   ville59 = Ville(-7.573253700000009,33.3670393, 'Nouaceur')
   gc.ajouterVille(ville59)
   ville60 = Ville(-6.937015999999971,30.9335436, 'Ourzazate')
   gc.ajouterVille(ville60)
   ville61 = Ville(-5.093710099999953,35.4449242, 'Ouad laou')
   gc.ajouterVille(ville61)
   ville62 = Ville(-6.5775187000000415,32.8501501, 'Ouad zem')
   gc.ajouterVille(ville62)
   ville63 = Ville(-5.567557999999963,34.7953732, 'Ouazane')
   gc.ajouterVille(ville63)
   ville64 = Ville(-6.0017674000000625,33.425066, 'Oulmess')
   gc.ajouterVille(ville64)
   ville65 = Ville(-6.6023665000000165,33.5229186, 'Romani')
   gc.ajouterVille(ville65)
   ville66 = Ville(-5.284117700000024,35.6196262, 'Martil')
   gc.ajouterVille(ville66)
   ville67 = Ville(-9.636919000000034,30.0040871, 'Massa')
   gc.ajouterVille(ville67)
   ville68 = Ville(-8.764638800000057,31.5383581, 'Chichawa')
   gc.ajouterVille(ville68)
   ville69 = Ville(-5.323321299999975,35.6805832, 'Mediq')
   gc.ajouterVille(ville69)
   ville70 = Ville(-7.516602000000034,33.4540939, 'Mediouna')
   gc.ajouterVille(ville70)
   ville71 = Ville(-4.732926799999973,32.6799423, 'Midelt')
   gc.ajouterVille(ville71)
   ville72 = Ville(-6.67584080000006,34.2562684, 'Mehdia')
   gc.ajouterVille(ville72)
   ville73 = Ville(-4.451013800000055,31.9370967, 'Moulay ali cherif')
   gc.ajouterVille(ville73)
   ville74 = Ville(-5.521051100000022,34.055902, 'Moulay driss zerhoun')
   gc.ajouterVille(ville74)
   ville75 = Ville(-6.274773399999958,34.8826391, 'Moulay bousselham')
   gc.ajouterVille(ville75)
   ville76 = Ville(-6.197785100000033,33.2253439, 'Moulay bouazza')
   gc.ajouterVille(ville76)
   ville77 = Ville(-6.030865, 35.464612, 'Assilah')
   gc.ajouterVille(ville77)
   ville78 = Ville(-4.234382999, 31.43663339, 'Arfoud')
   gc.ajouterVille(ville78)
   ville79 = Ville(-7.67108889,31.5634338, 'Ait ourir')
   gc.ajouterVille(ville79)
   ville80 = Ville(-9.1525340,30.0688758, 'Ait baha')
   gc.ajouterVille(ville80)
   ville81 = Ville(-8.3471781,33.286667, 'Azemour')
   gc.ajouterVille(ville81)
   ville82 = Ville(-1.9734743,32.5275178, 'Bouarfa')
   gc.ajouterVille(ville82)
   ville83 = Ville(-14.48473469999999,26.1252493, 'Boujdour')
   gc.ajouterVille(ville83)
   ville84 = Ville(-15.934738400000015,23.7221111, 'Dakhla')
   gc.ajouterVille(ville84)
   ville85 = Ville(-4.957494699999984,31.6891751, 'Goulmima')
   gc.ajouterVille(ville85)
   ville86 = Ville(-3.3489670999999817,34.2299391, 'Guercif')
   gc.ajouterVille(ville86)
   ville87 = Ville(-7.505773699999963,32.7668648, 'Guisser')
   gc.ajouterVille(ville87)
   ville88 = Ville(-2.2876645000000053,35.0998833, 'Saidia')
   gc.ajouterVille(ville88)
   ville89 = Ville(-9.081991399999993,32.1062572, 'Sebt gzoula')
   gc.ajouterVille(ville89)
   ville90 = Ville(-4.835315400000013,33.8305244, 'Sefro')
   gc.ajouterVille(ville90)
   ville91 = Ville(-7.622266500000023,32.99242419999999, 'Ssettat')
   gc.ajouterVille(ville91)
   ville92 = Ville(-8.511690300000055,32.8285457, 'Sidi smail ')
   gc.ajouterVille(ville92)
   ville93 = Ville(-10.175928500000055,29.3701124, 'Sidi ifni')
   gc.ajouterVille(ville93)
   ville94 = Ville(-7.060599799999977,33.8509477, 'Skhirate')
   gc.ajouterVille(ville94)
   ville95 = Ville(-7.9456658999999945,33.4774313, 'Sidi rahal')
   gc.ajouterVille(ville95)
   ville96 = Ville(-8.54738210000005,33.2312144, 'Sidi bouzid')
   gc.ajouterVille(ville96)
   ville97 = Ville(-5.110955200000035,33.5228062, 'Ifran')
   gc.ajouterVille(ville97)
   ville98 = Ville(-9.551496499999985,30.3523115, 'Inzegan')
   gc.ajouterVille(ville98)
   ville99 = Ville(-8.845797700000048,31.1719751, 'Imintanoute')
   gc.ajouterVille(ville99)
   ville100 = Ville(-5.015645599999971,33.7311674, 'Imouzzer')
   gc.ajouterVille(ville100)
  """
   ville101 = Ville(-2.1794135999999753,34.3061791, 'Jrada')
   gc.ajouterVille(ville101)
   ville102 = Ville(-6.0017674000000625,32.3576301, 'Jamaat shaim')
   gc.ajouterVille(ville102)
   ville103 = Ville(-6.269460799999933,32.5958283, 'Kasbat tadla ')
   gc.ajouterVille(ville103)
   ville104 = Ville(-6.057330200000024,33.8153704, 'khemissate')
   gc.ajouterVille(ville104)
   ville105 = Ville(-6.126192500000002,31.2370612, 'kalaat megouna')
   gc.ajouterVille(ville105)
   ville106= Ville(-5.915536900000006,35.0035307, 'kasr kbir')
   gc.ajouterVille(ville106)
   ville107= Ville(-5.723400699999950065,29.8257743, 'Mhamid Ghizlane')
   gc.ajouterVille(ville107)
   ville108 = Ville(-4.013361000000032,31.0801676, 'Marzouga')
   gc.ajouterVille(ville108)
   ville109 = Ville(-7.91979409999999,31.1377449, 'imlil')
   gc.ajouterVille(ville109)
   ville110 = Ville(-7.1318995999999976,31.047043, 'Ait benhadou')
   gc.ajouterVille(ville110)
   ville111 = Ville(-6.467660900000055,31.6456567, 'Ait Bouguemez')
   gc.ajouterVille(ville111)
   ville112 = Ville(-6.71975599999961,32.0152979, 'Ouzoud')
   gc.ajouterVille(ville112)
   ville113 = Ville(-4.0133610000000,32.1085649, 'Ben el widane')
   gc.ajouterVille(ville113)
   ville114 = Ville(-6.099025799999936,31.8286379, 'Oued Ahanesal')
   gc.ajouterVille(ville114)
   ville115= Ville(-3.152869199999941,34.9815148, 'Tiztoutine')
   gc.ajouterVille(ville115)
   ville116= Ville(-4.013361000000032,34.0613642, 'Oualili')
   gc.ajouterVille(ville116)
   ville117 = Ville(-5.335087599999952,33.395397, 'Sidi Addi ')
   gc.ajouterVille(ville117)
   ville118 = Ville(-8.21648099999993,32.9547248, 'Oulad Frej ')
   gc.ajouterVille(ville118)
   ville119 = Ville(-8.478758999999968,30.6362398, 'Oulad Berhil ')
   gc.ajouterVille(ville119)
   ville120 = Ville(-6.797592000000009,32.2018894, 'Oulad ayad')
   gc.ajouterVille(ville120)
   ville121 = Ville(-7.855108599999994,31.19477729999999, 'Oukaimeden')
   gc.ajouterVille(ville121)
   ville122 = Ville(-8.519925400000034,32.3931336, 'Oulad Amrane')
   gc.ajouterVille(ville122)
   ville123 = Ville( -8.240439700000024,31.2185473, 'Amizmiz ')
   gc.ajouterVille(ville123)
   ville124 = Ville(-2.514842000000044,34.8861599, 'Aklim ')
   gc.ajouterVille(ville124)
   ville125 = Ville(-2.032217199999991,34.0084384, 'Ain Bni Mathar ')
   gc.ajouterVille(ville125)
   ville126 = Ville( -5.041655100000071,33.8860615, 'Ain Cheggag ')
   gc.ajouterVille(ville126)
   ville127 = Ville(-5.549915599999963,34.5997921, 'Ain Defali')
   gc.ajouterVille(ville127)
   ville128 = Ville(-2.103301699999967,34.9518203, 'ahfir')
   gc.ajouterVille(ville128)
   ville129 = Ville( -9.436711599999967,28.6089376, 'ASsa ')
   gc.ajouterVille(ville129)
   ville130 = Ville(-8.608509000000026,33.1760943, 'Ouled Ghadbane')
   gc.ajouterVille(ville130)
   ville131 = Ville(-4.890968100000009,34.0084384, 'Bab Berred ')
   gc.ajouterVille(ville131)
   ville132 = Ville(-8.797693699999968,30.5122316, 'Ait Iaaza ')
   gc.ajouterVille(ville132)
   ville133 = Ville(-5.3390101999999615,33.2875171, 'Ainleuh ')
   gc.ajouterVille(ville133)
   ville134 = Ville(-7.238317800000004, 33.0656876, 'Ben Ahmed  ')
   gc.ajouterVille(ville134)
   ville135 = Ville(-7.348955100000012,33.6812829, 'Ben Yakhlef  ')
   gc.ajouterVille(ville135)
   ville136 = Ville(-5.485645999999974, 33.7557952, 'Boufakrane  ')
   gc.ajouterVille(ville136)
   ville137 = Ville(-5.566322200000059,34.9645166, 'Brikcha ')
   gc.ajouterVille(ville137)
   ville138 = Ville( -6.091751700000032,34.4207757, 'Dar Gueddari ')
   gc.ajouterVille(ville138)
   ville139 = Ville(-3.3313365000000204,35.1225129, 'Figuig  ')
   gc.ajouterVille(ville139)
   ville140 = Ville(-1.2298060000000532, 32.1092613, 'Douar Bel Aguide ')
   gc.ajouterVille(ville140)
   ville141 = Ville(-5.736564199999975, 34.6159961, 'Had Kourt  ')
   gc.ajouterVille(ville141)
   ville142 = Ville(-9.464489299999968,30.2969233, 'Lqliâa  ')
   gc.ajouterVille(ville142)
   ville143 = Ville( -6.065271899999971,34.8465381, 'Lalla Mimouna ')
   gc.ajouterVille(ville143)
   ville144 = Ville(-9.217598800000019,30.3917567, 'Oulad Teïma ')
   gc.ajouterVille(ville144)

   """



   #on initialise la population avec 50 circuits
   pop = Population(gc,50, True)
   print("_______________________________________________________________________________________")
   print ("Distance initiale : " + str(pop.getFittest().getDistance()))

   # On fait evoluer notre population sur 100 generations
   ga = GA(gc)
   pop = ga.evoluerPopulation(pop)
   for i in range(0,100):
      pop = ga.evoluerPopulation(pop)

   print("_______________________________________________________________________________________")

   print ("Distance finale : " + str(pop.getFittest().getDistance()))
   meilleurePopulation = pop.getFittest()


   #on genere une carte représentant notre solution
   lons = []
   lats = []
   noms = []
   print("_______________________________________________________________________________________")
   print("*** les villes en ordre de visite : ***")

   l=[]
   for ville in meilleurePopulation.circuit:

      l.append(ville.nom)


      lons.append(ville.lon)
      lats.append(ville.lat)
      noms.append(ville.nom)
   print(l)


   lons.append(lons[0])
   lats.append(lats[0])
   noms.append(noms[0])

   plt.figure(figsize=(10, 10))
   plt.legend(prop={'size':20})
   map = Basemap(projection='merc',llcrnrlat=20,urcrnrlat=37,llcrnrlon=-18,urcrnrlon=0,resolution='c')

   map.drawmapboundary(fill_color='#90D1F0')
   map.fillcontinents(color='#F7F956',lake_color='#56C3F9')
   map.drawcoastlines()
   map.drawcountries()
   x,y = map(lons,lats)
   map.plot(x,y,'bo', markersize=1)
   for nom,xpt,ypt in zip(noms,x,y):
       plt.text(xpt+5000,ypt+25000,nom)

   map.plot(x, y, 'D-', markersize=8, linewidth=1, color='k', markerfacecolor='b')
   plt.show()
# Mettez votre code ici…
a=time.time() - start_time

# Affichage du temps d execution
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


print("_______________________________________________________________________________________")
