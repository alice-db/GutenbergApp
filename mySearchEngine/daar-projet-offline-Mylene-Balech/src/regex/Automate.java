package regex;

import java.util.ArrayList;

public class Automate {
    ArrayList<Integer> source;
    ArrayList<Integer> destination;
    int chemin;
    int sourceFinal;
    int destinationFinal;
    int cheminFinal;
    boolean isFinalFinal;
    boolean isFinal;
    
    //Création de l'automate
    public Automate(ArrayList<Integer> source, ArrayList<Integer> destination, int chemin, boolean isFinal){
        this.source = source;
        this.destination = destination;
        this.chemin = chemin;
        this.isFinal = isFinal;
    }
    
    //Création de l'automate final utilisé pour la recherche de motif
    public Automate(int source, int destination, int chemin, boolean isFinal){
        this.sourceFinal = source;
        this.destinationFinal = destination;
        this.cheminFinal = chemin;
        this.isFinalFinal = isFinal;
    }
    
    // Création de la chaine de caractère pour une ligne d'automate
    public String toString(){
        String depart = "(";
        int cpt = 0;
        for(Integer d : source){
            depart+= d;
            if(cpt < source.size()-1) depart+=",";
            cpt++;
        }
        depart += ")";
        String arrive = "(";
        cpt = 0;
        for(Integer d : destination){
            arrive+= d;
            if(cpt < destination.size()-1) arrive+=",";
            cpt++;
        }
        arrive += ")";
        return depart+" → "+chemin+" → "+arrive;
    }
}
