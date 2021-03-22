package regex;

import java.util.ArrayList;

//Création des états DFA
public class EtatDFA {
    int source;
    ArrayList<Integer> sourceI;
    ArrayList<Integer> destinationI;
    String chemin;
    boolean isFinal;
    ArrayList<Integer> enfants = new ArrayList<Integer>();
    
    //Avant changement
    public EtatDFA(int source,ArrayList<Integer> enfants){
        this.source = source;
        this.enfants = enfants;
    }
    
    public EtatDFA(){
    }
    
    //Après création des listes d'états ayant le même chemin vers les destinations
    public EtatDFA(ArrayList<Integer> source,ArrayList<Integer> destination, String chemin, boolean isFinal ){
        this.sourceI = source;
        this.destinationI = destination;
        this.chemin = chemin;
        this.isFinal = isFinal;
    }
    
    //Retourne la source
    public int getSource() {
        return source;
    }
    
    //Modifie la source
    public void setSource(int source) {
        this.source = source;
    }
    
    //Retourne les enfants
    public ArrayList<Integer> getEnfants() {
        return enfants;
    }
    
    //Modifie les enfants
    public void setEnfants(ArrayList<Integer> enfants) {
        this.enfants = enfants;
    }
    
    //Retourne en chaine de caractère, la source vers ses enfants
    public String toString(){
        String result = String.valueOf(source);
        for( Integer i : enfants){
            result += String.valueOf(","+i);
        }
        return result;
    }
    
    //Retourne joliment les relations
    public String toString2(){
        String result = String.valueOf(sourceI)+" →  "+String.valueOf(destinationI)+ " = "+String.valueOf(chemin);
        return result;
    }
    
    //Création des equivalences entre source et ses enfants
    public ArrayList<Integer> equivalence(){
        ArrayList<Integer> equivalent = new ArrayList<Integer>();
        equivalent.add(source);
        for(Integer i : enfants){
            equivalent.add(i);
        }
        return equivalent;
    }
}
