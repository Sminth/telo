# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

# This is a simple example for a custom action which utters "Hello World!"

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import requests
import json

from typing import Dict, Text, Any, List, Union, Optional

from rasa.shared.core.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.forms import FormValidationAction
from re import search
import time, locale
from datetime import datetime

locale.setlocale(locale.LC_TIME, 'fr_FR')

class ActionHelloWorld(Action):
    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Bonjour à tous, ceci est ma première action.")
        return []


               
class ActionAvecNom(Action):
    def name(self) -> Text:
        return "avec_nom"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        entities = tracker.latest_message['entities']

        name=""
        message=""
        print(entities)

        for e in entities:
            if e['entity'] == 'nom':
                name=e['value']
                name = name.lower()
                print(name)
        print("name : "+name)
        
        heure = time.strftime("%H")
        print(heure)
        if(int(heure)>13):
            
            S1 ="Bonsoir"
            S2 ="Ce soir"
        else:
            S1 ="Bonjour"
            S2 ="Ce matin"
        
        if(name=="roxane" or name=="djigo"):
            
            message  = S1 + " roxane ! , vous êtes ravissante " + S2 + "!"
        
        elif(name=="emmanuel" or name=="malan"):
            
            message  = S1 + " emmanuel  ! , vous êtes beau !" + S2 + "!"
            
        elif(name=="latifate" or name=="kabore"):
                    
                    message  = S1 + " latifate, vous êtes belle "+ S2 + "!"
        elif(name=="marc" or name=="aurel"):
            
            message  = S1 + " marc aurel, vous êtes beau  ! "+ S2 + "!"
        
        elif(name=="mohamed" or name=="ali"):
            
            message  = S1 + " Ali, vous êtes holistique  ! "+ S2 + "!"
            
        elif(name=="sande" or name=="franck" or name=="oscar"):
            
            message  = S1 + " Oscar, vous êtes beau  " + S2 + "!"
        else:
            dispatcher.utter_message(template="utter_bjr_avec_nom") 
        dispatcher.utter_message(text=message)          
class ActionBonjour(Action):
    def name(self) -> Text:
        return "action_bonjour"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Bonjour à tous, ceci est ma première action.")
        return []



class ActionSection(Action):
    def name(self) -> Text:
        return "section"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        entities = tracker.latest_message['entities']
        name=""
        # declarer la variable  actions avant l'affactation d'une valeur
        message = ""

        for e in entities:
            print("-------------------------------") 
            print(e['value'])
            print("-------------------------------") 
            if e['entity'] == 'nom_section':
                name=e['value']
            # Trouver le bon message en fonction de la secrtion que l'utiliateur à rentrer
            if name.lower() == "fab":
                message="Orange Fab est un accélérateur de start-up qui accompagne les jeunes pousses et leur permet de développer des partenariats commerciaux nationaux et internationaux avec une ou plusieurs entités du groupe."

            elif name.lower() == "fablab" or "lab" in name :
                message="le FabLab Solidaire, atelier de fabrication numérique qui permet de prototyper les projets et d'apprendre en pratiquant."

            elif name.lower() == "ventures":
                message="Orange Ventures est un fonds d'investissement pour financer les start-up innovantes."

            elif "Academy".lower() in name.lower() or "digital" in name.lower() or name.lower() == "digital academy" or name.lower()=="orange digital academy" or name.lower()=="oda":
                message="L'orange digital academy (oda) est un  centre à vocation technologique qui propose des formations et des animations."
            else:
                name = ""
        
        # Je verifi, si aucun élément n'a été saisi par l'utilusateur je lui propose les differentes sections, sinon je 
        if name != "" or message != "":
            dispatcher.utter_message(text=message)
        # else:
        #     data= [ { "title":"fablab", "payload":"parle nous de orange fablab" }, { "title":"ODA", "payload":"parle nous de orange digital Academy" }, { "title":"ventures", "payload":"parle nous de ventures" } , { "title":"fab", "payload":"parle nous du fab" }]
        #     message={"payload":"quickReplies","data":data}
        #     dispatcher.utter_message(text="Pouvez-vous m'indiquez la section s'il vous plait ? ",json_message=message)
        
        message = "" #je vide le message après l'envoi
        try:
            url = 'http://192.168.252.237:6400/api/section/' + name.lower
            response = requests.get(url).text
            print("ok")   
        except Exception as e:
            print(e)
        return[]
    

               
class ActionRespoOdc(Action):
    def name(self) -> Text:
        return "respo_odc"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        entities = tracker.latest_message['entities']
        print("debut €€€€€€€€€€€€€€€€€€")   

        name=""
        message=""
        print(entities)

        habib = ["habib", "abib", "abibe", "habibe", "bamba"]
        leonce = ["leonce", "léonce", "leonse", "léonse", "kone", "koné"]
        franck = ["franc", "franck", "frank", "wodie", "wodié", "vodié", "vodie"]
        didier = ["didier", "any", "ani", "didier", "any"]
        for e in entities:
            if e['entity'] == 'name_responsable':
                name=e['value']
                name = name.lower()
                print(name)
            print("name "+name)
                
            if any(x in name for x in leonce):
                message="Léonce Koné est le manager du digital academy."
                
            if any(x in name for x in franck):
                message="Franck Wodié est le manager senior de l'orange digital center."    

            if any(x in name for x in habib):
                message="Habib Bamba est le directeur de la transformation du digital, des médias et directeur de la fondation orange côte d'ivoire."
            
            if any(x in name for x in didier):
                    message="Didier Any est le manager  de l'orange fab."    
            
                
            print("debut giutyuio€€€€€€€€€€€€€€"+message)  
         
        try:
            url = 'http://192.168.252.237:6400/api/personnel'
            response = requests.get(url).text
            print("ok")   
        except Exception as e:
            print(e)
        message = ""
        dispatcher.utter_message(text=message)

        return[]



class ActionResponsables(Action):
    def name(self) -> Text:
        return "action_presentation_responsable"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        entities = tracker.latest_message['entities']
        name=""
        message=""
        print(entities)   
         
        for e in entities:
            if e['entity'] == 'nom_section':
                name=e['value']
                if name == "fab":
                    message="Le responsable du fab est didier any."

                if name == "fablab":
                    message="Le fablab n'a pas encore de manager."
                        

                if name == "ventures":
                    message="L'orange venture n'a pas encore de manager."


                if name == "digital academy" or name=="orange digital academy" or name=="oda":
                    message="Léonce koné est le manager du digital academy."
                    name = "oda"

        try:
            url = 'http://192.168.252.237:6400/api/section/manager/' + name
            response = requests.get(url).text
            print("ok")   
        except Exception as e:
            print(e)

        dispatcher.utter_message(text=message)
          
            
        return[]



class ActionVisite(Action):
    def name(self) -> Text:
        return "action_visite_resp"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
  
        entities = tracker.latest_message['entities']
        message ="desolé, j'ai pas bien saisi le lieu indiqué."
        name=""
        url = 'manager'

        # print(entities)   
         
        for e in entities:
            
            print(e)   
            
            if e['entity'] == 'name_responsable':
                name=e['value']
                url = 'manager'

                if len(name) > 0 :
                    message="suivez moi, je vous conduit chez "+name
                
                # if name == "Léonce Koné":
                #     message="suivez moi, je vous indique chez "+name
                    

                # if name == "Franck Wodié":
                #     message="suivez moi, je vous conduit chez "+name
                    
                
            if e['entity'] == 'nom_section':
                name=e['value']
                url = 'section'
 
                if len(name) > 0 : 
                    if name == "digital academy":
                        message="suivez moi, je vous conduit à l'academy."
                    else:
                        message="suivez moi, je vous conduit au "+name
                    try:
                        url = "http://192.168.252.237:6400/api/guide/run/" + name
                        response = requests.get(url).text
                        print("ok")   
                    except Exception as e:
                            print(e)
                        
                # if name == "fab":
                #     message="suivez moi, je vous conduit au "+name
                    

                # if name == "fablab":
                #     message="suivez moi, je vous conduit au "+name
                    
                # if name == "digital academy":
                #     message="suivez moi, je vous conduit a l'orange "+name
                    

        dispatcher.utter_message(text=message)   
          
        # try:
        #     url = "http://192.168.252.237:6400/api/visite/" + url
        #     response = requests.get(url).text
        #     print("ok")   
        # except Exception as e:
        #         print(e)
        return[]
    
    

class ActionServiceOdc(Action):
    def name(self) -> Text:
        return "service_oda"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
             
        last_message=tracker.latest_message['text']
        # print(last_message)
        
        if "fablab" in last_message:
            dispatcher.utter_message(template="utter_info_fablab")

        elif "fab" in last_message:
            dispatcher.utter_message(template="utter_info_fab")
        
        elif "ventures" in last_message:
            dispatcher.utter_message(template="utter_info_ventures")
               
        elif ("oda" in last_message) or ("digital academy" in last_message):
            dispatcher.utter_message(template="utter_info_oda")
                
 

# class Bonjour(Action):
#     """Example of a form validation action."""

#     def name(self) -> Text:
#         return "get_nom"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
             
#         last_message=tracker.latest_message['text']
#         print("t:"+last_message)
        
     
#         jesuis = "je suis "
#         jemappelle = "je m'appelle "
#         jemenomme = "je me nomme "
#         information =""
#         if(search(jesuis, last_message.lower())):
#             #spliter l information entre par utilisateur
#             information = last_message.lower().split(jesuis)
            
#         elif(search(jemappelle, last_message.lower())):
#             #spliter l information entre par utilisateur
#             information = last_message.lower().split(jemappelle)

#         elif(search(jemenomme, last_message.lower())):
#             #spliter l information entre par utilisateur
#             information = last_message.lower().split(jemenomme) 
        
          
#         nom = information[1]
#         print(nom)
        
            
#         dispatcher.utter_message(text="bonjour "+nom)
        
#         return []
    
    
    
                 
       
class ActionGetNewst(Action):
    def name(self):
        return 'action_get_news'

    def run(self, dispatcher, tracker, domain):
        category = tracker.get_slot('category')
        if category == None:
            category = 'monde'
        print('category ', category)
        try:
            url = 'https://newsapi.org/v2/everything?q={category}&apiKey=5f839c4b07a44b5d9bf69baf9b1bc611'.format(
                category=category)
            response = requests.get(url).text
            # print('response',response)
            json_data = json.loads(response)['articles']
            i = 0
            # print('response articles ' ,response)
            for results in json_data:
                i = i + 1
                message = "<i>" + str(i) + "." + results['title'] + "</i>"
                print(i)
                dispatcher.utter_message(message)
                if i > 4:
                    return
        except Exception as e:
            print(e)
            dispatcher.utter_message(
                text=f"<br><b>custom action message</b><br>")
        return [SlotSet('category', category)]

# class ActionTestRecognition(Action):
#     def name(self):
#         return 'action_get_recogniton'

#     def run(self, dispatcher, tracker, domain):
#         category = tracker.get_slot('category')
#         if category == None:
#             category = 'monde'
#         print('category ', category)
#         try:
#             url = 'http://192.168.252.228:5005/webhooks/rest/webhook'
            
#             dataToSend = {'message':'message' , 'sender':'Me'}
            
#             response = requests.post(url, data=dataToSend)
#             # print('response',response)
#             json_data = json.loads(response)['text']
#             i = 0
#             # print('response articles ' ,response)
#             for results in json_data:
#                 i = i + 1
#                 message = "<i>" + str(i) + "." + results['title'] + "</i>"
#                 print(i)
#                 dispatcher.utter_message(message)
#                 if i > 4:
#                     return
#         except Exception as e:
#             print(e)
#             dispatcher.utter_message(
#                 text=f"<br><b>custom action message</b><br>")
#         return [SlotSet('category', category)]


class ValidateRecuperationDuForm(FormValidationAction):
    """Example of a form validation action."""

    def name(self) -> Text:
        return "validate_recuperation_du_form"

    @staticmethod
    def is_int(string: Text) -> bool:
        """Check if a string is an integer."""

        try:
            int(string)
            return True
        except ValueError:
            return False

    def validate_nom_complet(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validation du nom saisi par l'utilisateur"""

        jesuis = "je suis "
        jemappelle = "je m'appelle "
        jemenomme = "je me nomme "
        monnomcest="mon nom c'est "
        information =""
        nomaucasou=""
        if(search(jesuis, value.lower())):
            #spliter l information entre par utilisateur
            information = value.lower().split(jesuis)

        elif(search(jemappelle, value.lower())):
            #spliter l information entre par utilisateur
            information = value.lower().split(jemappelle)

        elif(search(jemenomme, value.lower())):
            #spliter l information entre par utilisateur
            information = value.lower().split(jemenomme) 
        
        elif(search(monnomcest, value.lower())):
            #spliter l information entre par utilisateur
            information = value.lower().split(monnomcest)
        elif(search(nomaucasou, value.lower())):
            #spliter l information entre par utilisateur
            information = value.lower().split(monnomcest)
            information.insert(0,"")
              
        res = information

        myintent = tracker.latest_message['intent'].get('name')
        
        if(myintent == "bonjour" or myintent == "salutations" ):
            return {"nom_complet": None}
        
        #print(res[1])
        return {"nom_complet": res[1]}
    
       
       
        #else:
            #sinon affichage du message d'erreur que l'age n'est pas valide
            #dispatcher.utter_message(template="utter_mauvais_nom")
            # attribution de valeur null au slot
            #return {"nom_complet": None}
            #return {"nom_complet": value}
   
# class ValidateResponsableDuForm(FormValidationAction):
#     """Example of a form validation action."""

#     def name(self) -> Text:
#         return "validate_responsable_du_form"

#     @staticmethod
#     def is_int(string: Text) -> bool:
#         """Check if a string is an integer."""

#         try:
#             int(string)
#             return True
#         except ValueError:
#             return False

#     def validate_nom_respo(
#             self,
#             value: Text,
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any],
#     ) ->  Dict[Text, Any]:
#         """Validation du nom saisi par l'utilisateur"""
       
#         try:
#             b1 = "je veux aller au bureau de "
#             b2 = "montre moi le chemin pour aller au bureau de "
#             b3 = "où se trouve le bureau de "
#             b4 = "conduitt moi au bureau de "
#             b5 = "fais moi visiter "
#             b6 = "je veux visiter "
           
#             myintent = tracker.latest_message['intent'].get('name')
            
#             if(myintent == "oscar" or myintent == "telo_form"):
#                 return {"nom_respo": None}

#             information =""
#             print(value)
#             if(search(b1, value.lower())):
#                 #spliter l information entre par utilisateur
#                 information = value.lower().split(b1) 
#             elif(search(b2, value.lower())):
#                 #spliter l information entre par utilisateur
#                 information = value.lower().split(b2) 
#             elif(search(b3, value.lower())):
#                 #spliter l information entre par utilisateur
#                 information = value.lower().split(b3) 
#             elif(search(b4, value.lower())):
#                     #spliter l information entre par utilisateur
#                 information = value.lower().split(b4) 
#             elif(search(b5, value.lower())):
#                     #spliter l information entre par utilisateur
#                 information = value.lower().split(b5) 
#             elif(search(b6, value.lower())):
#                     #spliter l information entre par utilisateur
#                 information = value.lower().split(b6) 
#             else:
#             #     #spliter l information entre par utilisateur
#                 dispatcher.utter_message(template="utter_mauvais_nom")
#                 return {"nom_respo": None}

          
#             nom_res = information[1]
#             print("b:"+nom_res)
        
#             if len(nom_res) > 0:
#                 #print("b:"+nom_res)
                
#                 return {"nom_respo": nom_res}
          
#             else:
#                 dispatcher.utter_message(template="utter_mauvais_nom")
#                  # attribution de valeur null au slot
#                 return {"nom_respo": None}
#         except Exception as e:
#             print("error")
#             print(e)
#             # dispatcher.utter_message(template="utter_mauvais_nom")
#             return {"nom_respo": None}

class ActionLien(Action):
    def name(self) -> Text:
        return "action_lien"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        Link = "https://laboutique.orange.ci/mobiles/smartphones-petits-prix"

        print("LINK ==== ", Link)
        dispatcher.utter_template("utter_lien", tracker, link=Link)
        return []


# class AppelApi(Action):
    
#     def name(self) -> Text:
#         return "action_appel_api"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
#         lieu=""
#         # je recupere la valeur qui se trouve dans le slot de nom_respo 
#         nom_responsable = tracker.get_slot("nom_respo")
#         #print(nom_responsable)

#         try:
#             #url = 'https://newsapi.org/v2/everything?q=techcrunch&apiKey=5f839c4b07a44b5d9bf69baf9b1bc611'
        
#             url = 'http://192.168.252.228:5000/users/odc'
#             #url = 'http://192.168.252.228:5000/users/'+nom_responsable
            
#             response = requests.get(url).text
#             if(len(response) != 0):
                
           
              
#                 json_data = json.loads(response)
#                 i = 0
#                 print("merde1")
#                 print(json_data)
#                 #lieu = json_data["location"] 
#                 #print(lieu)
#                 #print("merde3")
#                 dispatcher.utter_template("utter_suivre", tracker)
#                 print("merde4")
#                 dispatcher.utter_template("utter_suivre_lieu", tracker, lieu_indique=lieu)
#             else :
#                 print("merde5")
#                 dispatcher.utter_template("utter_lieu_non_trouver",tracker, nom_respo=nom_responsable)
                
#                 # print("desolé je ne sais pas ou se trouve le bureau de "+nom_responsable)
#         except Exception as e:
            
#             print(e)
#             # dispatcher.utter_message(text=f"<br><b>custom action message</b><br>")
#             #print("pret a afficher le dispatcher")
        
#         #print("dispatcher ok, return")
#         #return {"lieu_indique": lieu}
#         return []
    
    
    class ActionApi(Action):
        def name(self) -> Text:
            return "action_programme"

        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                
            # last_message=tracker.latest_message['text']
            # last_message1=last_message.lower()
            try:
                
                # url = 'http://192.168.252.214/top'
                url = 'https://newsapi.org/v2/everything?q=techcrunch&apiKey=5f839c4b07a44b5d9bf69baf9b1bc611'
                print("merde4")
                response = requests.get(url).text
                json_data = json.loads(response)['articles']
                
                desc = json_data[0]['description']
                imgs = json_data[0]['urlToImage']
                    
                dispatcher.utter_template("utter_test_api", tracker, descript = desc, monimg = imgs)
                return []
                #dispatcher.utter_template(text="suivez moi, je vous conduis !")
           
                                      # print("desolé je ne sais pas ou se trouve le bureau de "+nom_responsable)
            except Exception as e:
                print(e)
                
    class ActionDate(Action):
        def name(self) -> Text:
            return "action_date"
        def run(self, dispatcher: CollectingDispatcher,
                    tracker: Tracker,
                    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
            h = datetime.now()
            
            date = h.strftime("Aujourd'hui est le %d %B %Y")
            
            heure = h.strftime("il est %H heure %M minute")
        
 
    # class ActionApiSocket(Action):
    #     def name(self) -> Text:
    #         return "apisocket"

    #     def run(self, dispatcher: CollectingDispatcher,
    #             tracker: Tracker,
    #             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                
    #         last_message=tracker.latest_message['text']
    #         last_message1=last_message.lower()
    #         try:
                
    #             url = 'http://192.168.252.214/top'

              
    #             response = requests.get(url).text
    #          #   json_data = json.loads(response)
    #             print(response)
    #             dispatcher.utter_message(text="suivez moi, je vous conduis !")
    #             #dispatcher.utter_template(text="suivez moi, je vous conduis !")
           
    #                               # print("desolé je ne sais pas ou se trouve le bureau de "+nom_responsable)
    #         except Exception as e:
                
    #             print(e)
