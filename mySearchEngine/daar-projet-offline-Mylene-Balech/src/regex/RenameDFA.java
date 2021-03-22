package regex;

import java.util.ArrayList;

public class RenameDFA {
    int nouveau;
    ArrayList<Integer> ancien;
    boolean isFinal;
    
    //Renomme l'état 
    public RenameDFA(int nouveau, ArrayList<Integer> ancien, boolean isFinal){
        this.nouveau = nouveau;
        this.ancien = ancien;
        this.isFinal = isFinal;
    }
}
