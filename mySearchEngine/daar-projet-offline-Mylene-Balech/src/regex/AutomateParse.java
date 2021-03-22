package regex;

import java.io.*;
import java.util.ArrayList;

//Lis le fichier et renvoie les résultats de la recherche 
public class AutomateParse {
    public AutomateParse(){}
    
    //Récupère le fichier et récupère les résultats
    public ArrayList<String> readFile(ArrayList<Automate> automate, String filename, String regex) throws IOException {
    	FilePrinter fileprinter= new FilePrinter();
        ArrayList<String> texte = fileprinter.readFromFile(filename);

        ArrayList<String> resultats = getResultat(texte, automate);
        
        fileprinter.saveToFile("resultats/resultats_Regex_"+regex, resultats);

        return resultats;
    }
    
    //Vérifie si l état est final
    private boolean isFinal(ArrayList<Automate> automate, int nouvelEtat, int ancienEtat, int chemin){
        for(Automate auto :automate){
            if(auto.sourceFinal == ancienEtat && auto.destinationFinal == nouvelEtat){
                if(auto.cheminFinal == chemin || auto.cheminFinal == Regex.DOT)
                    return auto.isFinalFinal;
            }
        }
        return false;
    }
    
    //Récupère les états suivants en fonction de l'état source et du chemin
    private boolean futurState(ArrayList<Automate> automate, int chemin, int ancienState){
        boolean isFinal = false;
        for(Automate auto :automate){
            if(auto.sourceFinal == ancienState){
                if(auto.cheminFinal == chemin || auto.cheminFinal == Regex.DOT){
                    isFinal = true;
                }
            }
        }
        return isFinal;
    }
    
    //Récupère les destinations
    private ArrayList<Integer> getDestinations(ArrayList<Automate> automate, int chemin, int ancienState){
        ArrayList<Integer> destinations = new ArrayList<Integer>();
        for(Automate auto :automate){
            if(auto.sourceFinal == ancienState){
                if(auto.cheminFinal == chemin || auto.cheminFinal == Regex.DOT){
                    destinations.add(auto.destinationFinal);
                }
            }
        }
        return destinations;
    }
    
    //Récupère un état 
    private int getState(ArrayList<Automate> automate, int chemin, int source){
        for(Automate auto : automate) {
            if (auto.sourceFinal == source) {
                if (auto.cheminFinal == chemin || auto.cheminFinal == Regex.DOT)
                    return auto.destinationFinal;
            }
        }
        return 0;
    }
    
    //On parse toute la ligne pour trouver le motif
    private boolean parseLine(ArrayList<Automate> automate, String line){
        int state = 0;
        int ancienState = state;
        boolean isFinal = false;
        for(int i = 0; i<line.length(); i++){
            int chemin = (int)line.charAt(i);
            int prochainChemin = 0;
            if(i < line.length()-1) {
                prochainChemin = (int)line.charAt(i+1);
            }
            // Mon state = state
            if(futurState(automate, chemin, state)) {
                ancienState = state;
                // Récupération des destinations pour l'état
                ArrayList<Integer> destinations = getDestinations(automate, chemin, state);
                if(destinations.size() > 1) {
                    for (int d = 0; d < destinations.size(); d++) {
                        int destination = destinations.get(d);
                        if (futurState(automate, prochainChemin, destination)) {
                            state = destination;
                        }
                    }
                }else{
                    state = getState(automate, chemin, ancienState);
                }
                if(isFinal(automate, state, ancienState, chemin)) {
                    isFinal = true;
                }
            }
            else {
                state = 0;
            }
        }

        return isFinal;
    }
    
    //Permet de récupérer les résultats en fonction de chaque ligne
    private ArrayList<String> getResultat(ArrayList<String> texte, ArrayList<Automate> automate){
        ArrayList<String> resultats = new ArrayList<String>();
        for(int i = 0; i < texte.size() ; i++){
            if(parseLine(automate, texte.get(i))) resultats.add(texte.get(i));
        }
        return resultats;
    }
}
