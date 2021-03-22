package regex;

//Permet de renommer les états
public class EtatRenamed {
    int source;
    int destination;
    int chemin;
    boolean isFinal;
    
    public EtatRenamed(int source, int destination, int chemin, boolean isFinal){
        this.source = source;
        this.destination = destination;
        this.chemin = chemin;
        this.isFinal = isFinal;
    }
    public EtatRenamed(){}
    
    //Retourne joliment le chemin
    public String toString() {
        return source +" → " + destination +"=" + String.valueOf(chemin)+" -> "+isFinal;
    }
}
