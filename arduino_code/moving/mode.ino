
#include <Scheduler.h>

// Check for SparkFun SAMD21 Breakout
#if defined(ARDUINO_ARCH_SAMD) && (USB_PID == 0x8D21)
#define Serial SerialUSB
#endif

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
int mode_auto = 1;
int mode_obstacle = 0;

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

void setup()
{
  Serial.begin(57600);
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
Serial.println("setup1");
Scheduler.start(setup3, loop3);
  Scheduler.start(setup2, loop2);
  
}

void loop()
{
  Serial.println("loop1");
  // Turn LED off
  Serial.print(millis());
  Serial.println("loop2");
  mode_obstacle =0;
    Mdistance_Avant();
    delay(2);
    Mdistance_Gauche();
    delay(2);
    Mdistance_Droite();
    delay(2);

    //pour avancer 
     if( Distance_Avant>=Distance_max  ){
      Serial.print(Distance_Avant);
      Serial.println("cm Avant");
      Avancer();
      delay(3000);
      Stop();
      delay(300);
    
  }
 ///////////////////////////// 
 else if( Distance_Avant < Distance_max ){
       Distance_maxi =max(Distance_Droite,Distance_Gauche);
       if( Distance_maxi== Distance_Droite ){
          Serial.print(Distance_Droite);
          Serial.println("cm Droite");
          TournerADroite();
          delay(TempTourner);
          Stop();
          delay(300);
       }
      else if( Distance_maxi== Distance_Gauche ){
          Serial.print(Distance_Gauche);
          Serial.println("cm Gauche");
          TournerAGauche();
          delay(TempTourner);
          Stop();
          delay(300);
       } 
       
   }
      
  else if(Distance_Droite<Distance_min && Distance_Gauche<Distance_min && Distance_Avant<Distance_min){
    Mdistance_Arriere();
        Serial.print(Distance_Arriere);
        Serial.println("cm Arriere");
    if(Distance_Arriere>Distance_min){
      if(Distance_Droite>Distance_Gauche){
        Serial.print(Distance_Droite);
        Serial.println("cm Droite");
        TournerADroite();
        delay(TempTourner);
        Stop();
        delay(300);
      }
      else if(Distance_Droite<Distance_Gauche){
        TournerAGauche();
        delay(TempTourner);
        Stop();
        delay(300);
        
      }
    }
 
    
   }
  Serial.println(Scheduler.stack());
}

void setup2()
{
  Serial.print(millis());
  Serial.println(F(":setup2"));

}

void loop2()
{
  /*
  while (!Serial.available());
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
                else if (String(strToken) == "y") {
                  mode_auto =1;
                }
                 else if (String(strToken) == "z") {
                  mode_auto =0;
    mode_obstacle =0;
                }
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

*/
}

void setup3()
{
  Serial.print(millis());
  Serial.println(F(":setup3"));
}

void loop3()
{
  static char* buf = NULL;

  // Check for buffer allocation
  if (buf == NULL) {
    buf = (char*) malloc(64);
    Serial.print(millis());
    Serial.print(F(":loop3:alloc:buf=0x"));
    Serial.println((int) buf, HEX);
    if (buf == NULL) {
      delay(1000);
      return;
    }
  }

  // Read line and yield while waiting for characters
  // Capture wait time and number of yields
  char* bp = buf;
  unsigned long yields = 0;
  unsigned long start = millis();
  int c;
  while ((c = Serial.read()) != '\n') {
    if (c > 0)
      *bp++ = c;
    else {
      yields += 1;
      yield();
    }
  }
  *bp = 0;

  // Print wait time, number of yields and line
  unsigned long stop = millis();
  unsigned long ms = stop - start;
  Serial.print(millis());
  Serial.print(F(":loop3:yields="));
  Serial.print(yields);
  Serial.print(F(",ms="));
  Serial.print(ms);
  Serial.print(F(",buf="));
  Serial.println(buf);

  // Check for buffer free command
  if (!strcmp_P(buf, (const char*) F("free"))) {
    Serial.print(millis());
    Serial.print(F(":loop3:free:buf=0x"));
    Serial.println((int) buf, HEX);
    free(buf);
    delay(500);
    buf = NULL;
  }

  Serial.print(millis());
  Serial.print(F(":loop3::stack="));
  Serial.println(Scheduler.stack());
}