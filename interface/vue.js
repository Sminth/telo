new Vue({
  el: '#app',
  components: {
    'mon-composant': httpVueLoader('./composants/mon-composant.vue')
  },

  data: function () {

    return {
      mode_deplacement: "false",
      mode_obstacle: "false",
      mode_music: "false",
      avancer: 0,
      gauche: 0,
      droite: 0,
      message_erreur: "",
      message: "",
      msg_prg: "",
      volume : 50,
    }

  },
  methods: {
    setVolume(){
      
    },
    depl_libre(){
      if (this.mode_deplacement) axios.get("http://192.168.252.237:6400/api/command/y").then(function (response) { console.log(response); }).catch(function (error) { console.log(error); });

      else axios.get("http://192.168.252.237:6400/api/command/z").then(function (response) { console.log(response); }).catch(function (error) { console.log(error); });

    },
    depl_obstacle(){
      if (this.mode_obstacle) axios.get("http://192.168.252.237:6400/api/command/o").then(function (response) { console.log(response); }).catch(function (error) { console.log(error); });

      else axios.get("http://192.168.252.237:6400/api/command/s").then(function (response) { console.log(response); }).catch(function (error) { console.log(error); });

    },
    musika() {
      console.log("msk");
      if (this.mode_music) axios.get("http://192.168.252.237:6400/api/song/on").then(function (response) { console.log(response); }).catch(function (error) { console.log(error); });

      else axios.get("http://192.168.252.237:6400/api/song/off").then(function (response) { console.log(response); }).catch(function (error) { console.log(error); });

    },

    send_msg1() {
      axios.get("http://192.168.252.237:6400/api/parler/salut, je suis Telo, un robot conçu par les academiciens de l'orange digital center, grâce à qui j'apprends chaque jour de nouvelles choses .")
        .then(function (response) { console.log(response); }).catch(function (error) { console.log(error); });
    },
    send_message() {
      axios.get('http://192.168.252.237:6400/api/parler/' + this.message)
        .then(function (response) { console.log(response); })
        .catch(function (error) { console.log(error); });
    },

    lol() {
      console.log(this.mode_deplacement)
      this.mode_deplacement = "false",
        this.mode_obstacle = "false",
        this.mode_music = "false";
    },

    arret() {
      axios.get('http://192.168.252.237:6400/api/command/s').then(function (response) { console.log(response); })
        .catch(function (error) { console.log(error); });
    },

    depl_prog() {

      commande = ""

      if (this.avancer === 0 && this.gauche === 0 && this.droite === 0) this.message_erreur = "veuillez entrez des valeurs corrects";
      
      else {
        if (this.avancer != 0) commande + "a:" + this.avancer.toString() + ":"
        if (this.gauche != 0) commande + "g:" + this.gauche.toString() + ":"
        if (this.droite != 0) commande + "d:" + this.droite.toString() + ":"
        if (this.msg_prg) {
          console.log(((parseInt(this.avancer) + parseInt(this.gauche) + parseInt(this.droite)) * 1000) + 500);
          var tm = ((parseInt(this.avancer) + parseInt(this.gauche) + parseInt(this.droite)) * 1000) + 500;
          setTimeout(() => {
            console.log(this.msg_prg);
            axios.get('http://192.168.252.237:6400/api/parler/' + this.msg_prg).then(function (response) { console.log(response); }).catch(function (error) { console.log(error); });
  
          }, tm);
        }
        commande = "a:" + this.avancer.toString() + ":d:" + this.droite.toString() + ":g:" + this.gauche.toString() + ":s"
        console.log(commande);
        axios.get('http://192.168.252.237:6400/api/command/' + commande)
          .then(function (response) { console.log(response); })
          .catch(function (error) { console.log(error); });

      }


    }
  }
});