#include <ESP8266WiFi.h>
 
const char* ssid = "WIFI ODC";
const char* password = "Digital1";
 
int ledPin = 16; 
int ledPin2 = 5; 
int ledPin3 = 14; 
int ledPin4 = 12; 
WiFiServer server(80);
 
void setup() 
{
  // initialisation de la communication série
  Serial.begin(115200);
  
  delay(100);

  // initialisation de la sortie pour la led 
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
  pinMode(ledPin2, OUTPUT);
  digitalWrite(ledPin2, LOW);

 pinMode(ledPin3, OUTPUT);
  digitalWrite(ledPin3, LOW);
  pinMode(ledPin4, OUTPUT);
  digitalWrite(ledPin4, LOW);
  
  // Connexion wifi
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
 
  WiFi.begin(ssid, password);

  // connection  en cours ...
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  // Wifi connecter
  Serial.println("WiFi connecter");
 
  // Démmarrage du serveur.
  server.begin();
  Serial.println("Serveur demarrer !");
 
  // Affichage de l'adresse IP
  Serial.print("Utiliser cette adresse URL pour la connexion :");
  Serial.print("http://");
  Serial.print(WiFi.localIP());
  Serial.println("/");
 
}
 
void loop() 
{
WiFiClient client;

  
  // Vérification si le client est connecter.
  client = server.available();
  if (!client)
  {
    return;
  }
 
  // Attendre si le client envoie des données ...
  Serial.println("nouveau client");
  while(!client.available()){
    delay(1);
  }
 
  String request = client.readStringUntil('\r');
  Serial.println(request);
  client.flush();

  int value = LOW;
  if (request.indexOf("/vert") != -1)  {
    digitalWrite(ledPin, HIGH); // allumer la led
    digitalWrite(ledPin3, LOW);
    digitalWrite(ledPin4, HIGH);
    digitalWrite(ledPin2, LOW);
    value = HIGH;
  }
  if (request.indexOf("/rouge") != -1)  {
    digitalWrite(ledPin2, HIGH);
    digitalWrite(ledPin, LOW); // éteindre la led
    digitalWrite(ledPin3, HIGH);
    digitalWrite(ledPin4, LOW);
    value = LOW;
  }
 
  // Réponse
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/html");
  client.println(""); 
  client.println("<!DOCTYPE HTML>");
  client.println("<html>");
 
  client.print("Etat de la led : ");
 
  if(value == HIGH) {
    client.print("On");
  } else {
    client.print("Off");
  }
  client.println("<br><br>");
  client.println("<a href=\"/vert\"\"><button>Allumer vert </button></a>");
  client.println("<a href=\"/rouge\"\"><button>Eteindre vert </button></a><br />");  
  client.println("</html>");
 
  delay(1);
  Serial.println("Client deconnecter");
  Serial.println("");
 
}