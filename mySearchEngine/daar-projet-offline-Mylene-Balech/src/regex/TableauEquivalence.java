package regex;

import java.util.ArrayList;

//Créer le tableau des equivalence en fonction des chemins, des sources et des destinations
public class TableauEquivalence {
    ArrayList<Integer> depart = new ArrayList<Integer>();
    ArrayList<Integer> arrivee = new ArrayList<Integer>();
    int chemin;
    boolean equivalent;
    
    //Créer les équivalences
    public TableauEquivalence(ArrayList<Integer> depart, ArrayList<Integer> arrivee, int chemin, boolean equivalent){
        this.depart = depart;
        this.chemin = chemin;
        this.arrivee = arrivee;
        this.equivalent = equivalent;
    }
    
    //Permet d'afficher joliment les équivalences
    public String toString(){
        String departure = "(";
        for(int d= 0; d < depart.size(); d++){
            departure+=depart.get(d);
            if(d < depart.size()-1) departure += ",";
        }
        departure += ")";
        String arrive = "(";
        for(int d= 0; d < arrivee.size(); d++){
            arrive+=arrivee.get(d);
            if(d < arrivee.size()-1) arrive += ",";
        }
        arrive += ")";
        return departure+" → "+String.valueOf(chemin)+" → "+arrive;
    }
}
