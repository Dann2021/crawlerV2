import argparse
import json
import re
from urllib.parse import urljoin, urlparse

import requests as rq
from bs4 import BeautifulSoup

# Creation d'une fonction principale

def robot(url, proxy=None):
  
  # Creation des listes pour resultat final et sans doublons
  resultats = []
  sans_doublons = []

  # Creation des listes pour parser les differents elements
  balises = ['a','img','link','form','iframe', 'area','embed','object']
  attributs = ['href','src', 'action','download','target', 'data-src']
  
  # creation d'un pattern pour les regex des urls
  pattern = r"^https?://[^\s]+"

  # Execution d'une requete
  url = "http://" + url
  requete = rq.get(url, proxies=proxy)
 
  
  # Analyse du code de la requete
  if requete.status_code == 200:
    # Si vrai c'est que tout se deroule bien

    # Extraction du texte de la requete
    texte = requete.text

    # Creation des outils beautifulsoup
    soup = BeautifulSoup(texte, "html.parser")

    # Parcourt des listes de balises et attributs

    # liste balise 
    for balise in balises:

      # creation d'une variable datas pour contenir les valeurs que l'on cherche
      # datas sera une liste qui contiendra la balise recherchee
      datas = soup.find_all(balise)

      # Parcourt de la liste datas pour extraire les attributs specifiques
      for data in datas:

        # Parcourt de la liste des attributs
        for attribut in attributs:

          # Creation d'une variable donnees qui contiendra ce que l'on souhaite
          donnees = data.get(attribut)

          # Verification de la donnees si elle n'est pas vide
          if donnees:

            # Verification si la donnnees est un chemin
            if urlparse(donnees).path:

              # Creation d'une variable hote qui sera l'url complet 
              hote = urljoin(url, donnees)
             

              # Ajout de hote dans la liste resultat
              resultats.append(hote)
            
            else:
              
              # Verification du pattern
              if re.match(pattern, donnees):

                # Ajout de hote dans la liste resultat
                resultats.append(donnees)

    # Creation d'une variable i pour initialiser un compteur
    i = 0 

    # Elimination des doublons
    sans_doublons = list(set(resultats))

    # Parcourt de la liste sans doublons
    for lien in sans_doublons:
      print(vert(f"[{i}] : {lien}"))
      i += 1

  else:
    # Affichage du message avec son code 
    print(f'Erreur : code [{requete.status_code}]')
  return sans_doublons

if __name__ == "__main__":

  # Définir le proxy Tor
  proxy = { 'http':'socks5h://localhost:9050','https':'socks5h://localhost:9050'}


  # Creation de couleur 
  def vert(texte):
      return f"\033[32m{texte}\033[0m"
  def rouge(texte):
      return f"\033[31m{texte}\033[0m"
  

  # Logo
  print(rouge("""

  ██████  ▄████▄   ██▀███   ▄▄▄       ██▓███  
▒██    ▒ ▒██▀ ▀█  ▓██ ▒ ██▒▒████▄    ▓██░  ██▒
░ ▓██▄   ▒▓█    ▄ ▓██ ░▄█ ▒▒██  ▀█▄  ▓██░ ██▓▒
  ▒   ██▒▒▓▓▄ ▄██▒▒██▀▀█▄  ░██▄▄▄▄██ ▒██▄█▓▒ ▒
▒██████▒▒▒ ▓███▀ ░░██▓ ▒██▒ ▓█   ▓██▒▒██▒ ░  ░
▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░░ ▒▓ ░▒▓░ ▒▒   ▓▒█░▒▓▒░ ░  ░
░ ░▒  ░ ░  ░  ▒     ░▒ ░ ▒░  ▒   ▒▒ ░░▒ ░     
░  ░  ░  ░          ░░   ░   ░   ▒   ░░       
      ░  ░ ░         ░           ░  ░         
         ░                                    


"""))


  parser = argparse.ArgumentParser(
  prog=rouge("Mon crawler"),
  description="Ceci est un crawler de site web en python",
   epilog=rouge("Usage dans un cadre strictement légale"))




  # Ajout des arguments

  parser.add_argument('-u',"--url", metavar="", type=str, help="Entrez l'url de site (ex : exemple.com)")
  parser.add_argument("-s","--sortie", metavar="", type=str, help="Fichier de sortie")
  parser.add_argument("-p", "--proxies", help="Activation du proxy Tor", action='store_true')


  # creation d'un arg
  args = parser.parse_args()
  dico = {}
  if args.url:

    liens = robot(args.url, proxy if args.proxies else None)

    
  if args.sortie:
    dico["Liens"] = liens
   
    
    with open(f'{args.sortie}.json', 'w', encoding="utf-8") as f:
      json.dump(dico, f, ensure_ascii=False, indent=4)
      print(f"Fichier {args.sortie}  enregistré")

  else:
    print("Commande invalide")



