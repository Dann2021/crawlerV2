#!/usr/bin/python

import argparse
import json
import re

#import pandas as pd
import requests as rq
from bs4 import BeautifulSoup


# Creation de couleur 
def vert(texte):
    return f"\033[32m{texte}\033[0m"
def rouge(texte):
    return f"\033[31m{texte}\033[0m"



# Définir le proxy Tor

proxy = { 'http':'socks5h://localhost:9050','https':'socks5h://localhost:9050'}

def crawler(url):
  # transformation url en str
  url = str(url)

  # creation d'un pattern pour les liens 
  pattern = r"^https?://[^\s]+"
  pattern2 = r"^\/[a-zA-Z0-9_\-\/]*$"

  # liste qui contiendra les liens
  liens = []

  # requete http
  requete = rq.get(f"https://{url}")

  # robot
  soup = BeautifulSoup(requete.text, 'html.parser')

  # recherche de liens
  links = soup.find_all('a')
  for link in links:
    link = link.get('href')
    if link is not None:
      if re.match(pattern, link):
      
        liens.append(link)
      if re.match(pattern2,link):
        link = str(link)
        lien = f"https://{url+link}"
        liens.append(lien)
      #else:
      #  print(f'[nv] : {link}')
    #else:
    #   print(f"erreur : {link}")
      
  i = 0   
  for lien in liens:
    print(vert(f"[{i}] : {lien}"))
    #crawler(lien)
    i += 1
  return liens



# Deuxieme fonction
"""def verification(url):
    dico = {}
    r = rq.get(f"https://{url}")
    if r.status_code == 200:
      print("[ok] code 200")
    
      dico['encodage'] = [r.encoding]
      #dico['text'] = [r.text]
      
      dico['content'] = [r.content]
      dico['cookies'] = [r.cookies]

      dico['history'] =  [r.history]
      dico['headers'] = [r.headers]
      dico['url'] = [r.url]
      lien = r.links 
      if lien is not None:
        #print(f"[ok] lien : \n {lien}")
        dico['lien'] =  [lien]
     
      #else:
      #  print(f"lien vide : {lien}")
    

     
    else:
    
      print(f"erreur code : [{r.status_code}]")

    return dico
"""





parser = argparse.ArgumentParser(
  prog=rouge("Mon crawler"),
  description="Ceci est un crawler de site web en python",
   epilog=rouge("Usage dans un cadre strictement légale"))




# Ajout des arguments

parser.add_argument('-u',"--url", metavar="", type=str, help="Entrez l'url de site (ex : exemple.com)")
parser.add_argument("-s","--sortie", metavar="", type=str, help="Fichier de sortie")


# creation d'un arg
args = parser.parse_args()
dico = {}
if args.url:

  liens = crawler(args.url)
  #dat = verification(args.url)
  #print(dat)
  

  
if args.sortie:
  dico["Liens"] = liens
  #df = pd.DataFrame(dico)
  #js = df.to_json(f"{args.url}.json")

  #data = pd.DataFrame(dat)
  #dj = data.to_json(f"{args.url}-lien.json")
  
  with open(f'{args.sortie}.json', 'w', encoding="utf-8") as f:
    json.dump(dico, f, ensure_ascii=False, indent=4)
    print(f"Fichier {args.sortie}  enregistré")
  
  #with open(f'{args.sortie}-info.json', 'w', encoding="utf-8") as fichier:
  #  json.dump(dat, fichier, ensure_ascii=False, indent=4)
  #  print(f"Fichier {args.sortie}-info  enregistré")
     

    

  #else:
  #  print(f"Erreur (code : {r.status_code})")


else:
  print("Commande invalide")