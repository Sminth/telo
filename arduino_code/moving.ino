#define Roue_DroitBleu   25
#define Roue_DroitJaune  23
#define Roue_DroitVert   27

#define Roue_GaucheBleu  24
#define Roue_GaucheJaune 22
#define Roue_GaucheVert  26

#define AccelerationDroit  10    // Broche de commande de la vitesse droit 
#define AccelerationGauche  11    // Broche de commande de la vitesse Gauche
//Capteur Droit
#define TRIGGER_R_DROIT 2
#define ECHO_R_DROIT 3
//Capteur gauche
#define TRIGGER_R_GAUCHE 4
#define ECHO_R_GAUCHE 5
//capteur Arriere 
#define TRIGGER_R_ARRIERE 6
#define ECHO_R_ARRIERE 7
//capteur Avant
#define TRIGGER_R_AVANT 8
#define ECHO_R_AVANT 9


const char * separators = ":";


//VITESSE MAX A INJECTE 130
int Vitesse0 = 0;
int VitesseTourner = 60; 
int VitesseNormale = 110;


float Distance_Droite = 0;
float Distance_Gauche = 0;
float Distance_Arriere = 0; 
float Distance_Avant = 0; 
float Distance_direction; 
float Distance_max = 200;
float Distance_maxi ;
float Distance_min = 30;
float Distance_Tourner ;
int TempStop = 1000;
int TempTourner = 1000;

//Communication Port Série
String incomingByte ;
String data; 


//Fonction Avancé 
void Avancer(){
  analogWrite(AccelerationDroit,VitesseNormale);
  digitalWrite(Roue_GaucheBleu,HIGH);
  digitalWrite(Roue_GaucheJaune,HIGH);
  digitalWrite(Roue_GaucheVert,HIGH);
  digitalWrite(Roue_DroitBleu,HIGH);
  digitalWrite(Roue_DroitJaune,HIGH);
  digitalWrite(Roue_DroitVert,HIGH);
  
}

void Stop(){
  Serial.print("Je m'arrete");
  analogWrite(AccelerationDroit,Vitesse0);
  digitalWrite(Roue_GaucheBleu,HIGH);
  digitalWrite(Roue_GaucheJaune,HIGH);
  digitalWrite(Roue_GaucheVert,HIGH);
  digitalWrite(Roue_DroitBleu,HIGH);
  digitalWrite(Roue_DroitJaune,HIGH);
  digitalWrite(Roue_DroitVert,HIGH);
  
}

void TournerADroite(){
  Serial.print("Je tourne à droite");
  analogWrite(AccelerationDroit,VitesseNormale);
  digitalWrite(Roue_DroitBleu,LOW);
  digitalWrite(Roue_DroitJaune,LOW);
  digitalWrite(Roue_DroitVert,LOW);
//  
  digitalWrite(Roue_GaucheBleu,HIGH);
  digitalWrite(Roue_GaucheJaune,HIGH);
  digitalWrite(Roue_GaucheVert,HIGH);
  
}
void TournerAGauche(){
  Serial.print("Je tourne à gauche");
  analogWrite(AccelerationDroit,VitesseNormale);
  digitalWrite(Roue_DroitBleu,HIGH);
  digitalWrite(Roue_DroitJaune,HIGH);
  digitalWrite(Roue_DroitVert,HIGH);
//  
  digitalWrite(Roue_GaucheBleu,LOW);
  digitalWrite(Roue_GaucheJaune,LOW);
  digitalWrite(Roue_GaucheVert,LOW);
}


float Mdistance_Droite(){
    float Mdistance1;
    float T1=0;
    digitalWrite(TRIGGER_R_DROIT, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIGGER_R_DROIT, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIGGER_R_DROIT, LOW);
    Mdistance1= pulseIn(ECHO_R_DROIT, HIGH);
    T1 = (Mdistance1/2)/29.1;
    if (T1>400){
      T1=399;
    }
    Distance_Droite=T1;
    return(Distance_Droite);   
}
float Mdistance_Gauche(){
    float Mdistance2;
    float T2=0;
    digitalWrite(TRIGGER_R_GAUCHE, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIGGER_R_GAUCHE, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIGGER_R_GAUCHE, LOW);
    Mdistance2= pulseIn(ECHO_R_GAUCHE, HIGH);
    T2 = (Mdistance2/2)/29.1;
    if (T2>400){
      T2=399;
    }
    Distance_Gauche=T2;
    return(Distance_Gauche);
}
float Mdistance_Arriere(){
    float Mdistance3;
    float T3=0;
    digitalWrite(TRIGGER_R_ARRIERE, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIGGER_R_ARRIERE, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIGGER_R_ARRIERE, LOW);
    Mdistance3= pulseIn(ECHO_R_ARRIERE, HIGH);
    T3 = (Mdistance3/2)/29.1;
    if (T3>400){
      T3=399;
    }
    Distance_Arriere=T3;
    return(Distance_Arriere);
}
float Mdistance_Avant(){
    float Mdistance4;
    float T4=0;
    digitalWrite(TRIGGER_R_AVANT, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIGGER_R_AVANT, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIGGER_R_AVANT, LOW);
    Mdistance4= pulseIn(ECHO_R_AVANT, HIGH);
    T4 = (Mdistance4/2)/29.1;
    if (T4>400){
      T4=400;
    }
    Distance_Avant=T4;
    return(Distance_Avant);
} 

 
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
    //-----------------
    pinMode(LED_BUILTIN, OUTPUT);
    //Relais pour commander les directions du robot
   pinMode(Roue_DroitBleu, OUTPUT);
   pinMode(Roue_DroitJaune, OUTPUT);
   pinMode(Roue_DroitVert, OUTPUT);
   pinMode(Roue_GaucheBleu, OUTPUT);
   pinMode(Roue_GaucheJaune, OUTPUT);
   pinMode(Roue_GaucheVert, OUTPUT);


  pinMode(AccelerationDroit, OUTPUT);
  pinMode(AccelerationGauche, OUTPUT);
  
  pinMode(TRIGGER_R_DROIT, OUTPUT);
  pinMode(ECHO_R_DROIT, INPUT);
  pinMode(TRIGGER_R_GAUCHE, OUTPUT);
  pinMode(ECHO_R_GAUCHE, INPUT);
  pinMode(TRIGGER_R_ARRIERE, OUTPUT);
  pinMode(ECHO_R_ARRIERE, INPUT);
  pinMode(TRIGGER_R_AVANT, OUTPUT);
  pinMode(ECHO_R_AVANT, INPUT);

//  analogWrite(AccelerationDroit,Vitesse0);
//  analogWrite(AccelerationGauche,Vitesse0);
//  delay(5000);
//    Stop();
//    delay(3000);
}

int stopCount = 0;
char scan()
{
    // ping times in microseconds
    unsigned int left_scan, centre_scan, right_scan;
    char choice;
 
    // scan left
    Mdistance_Gauche();
 
    // scan right
    Mdistance_Droite();
    
    // scan straight ahead
    Mdistance_Avant();
 
    if (Distance_Gauche>Distance_Droite && Distance_Gauche>Distance_Avant)
    {
        choice = 'L';
    }
    else if (Distance_Droite>Distance_Gauche && Distance_Droite>Distance_Avant)
    {
        choice = 'R';
    }
    else {
      choice = 'C';
    }
 
    return choice;
}



void loop() {

  
  if (Serial.available() > 0) {

    data = Serial.readStringUntil('\n');
  
    int data_len = data.length() + 1;
    char data_array[data_len];
    data.toCharArray(data_array, data_len);
  
    //Serial.println(data);
    Serial.println(data_array);
    char * strToken = strtok ( data_array, separators );
    if(data){
        int i =0;
        while ( strToken != NULL ) {
  
            if(i%2==0){
            
                if (String(strToken) == "a") Avancer();
                else if (String(strToken) == "g") TournerAGauche();
                
                else if (String(strToken) == "d") TournerADroite();
                
                else if (String(strToken) == "s") Stop();
                else{
                 Stop();
                 delay(TempStop);
                }
                
            }else{
                Serial.println("ok");
                delay(atof(strToken)*1000);
            }
            // On demande le token suivant.
            strToken = strtok ( NULL, separators );
            
            i=i+1;
        }
    }

  }

 
}
