new Vue({
    el: '#app',
    components: {
      'mon-composant': httpVueLoader('./composants/mon-composant.vue')
    },
  
    data :function() {
 
        return {
            mode_deplacement : "false",
            mode_obstacle : "false",
            mode_music : "false",
            avancer:0,
            gauche:0,
            droite:0,
            message_erreur:""
        }
   
    },
    methods :{
        lol(){
            console.log(this.mode_deplacement)
            this.mode_deplacement = "false",
            this.mode_obstacle = "false",
            this.mode_music = "false";
        },
        arret(){
            axios.get('http://192.168.252.237:6400/api/command/s')
      .then(function (response) {
        // handle success
        console.log(response);
      })
      .catch(function (error) {
        // handle error
        console.log(error);
      });
        },
        depl_prog(){
            
            commande =""
          
            if(this.avancer===0 && this.gauche===0 && this.droite===0) this.message_erreur = "veuillez entrez des valeurs corrects";
            else{
                if(this.avancer!=0) commande+"a:"+this.avancer.toString()+":"
                if(this.gauche!=0) commande+"g:"+this.gauche.toString()+":"
                if(this.droite!=0) commande+"d:"+this.droite.toString()+":"
                commande ="a:"+this.avancer.toString()+":d:"+this.droite.toString()+":g:"+this.gauche.toString()+":s"
                console.log(commande);
                axios.get('http://192.168.252.237:6400/api/command/'+commande)
      .then(function (response) {
        // handle success
        console.log(response);
      })
      .catch(function (error) {
        // handle error
        console.log(error);
      });
            }

           
        }
    }
  });