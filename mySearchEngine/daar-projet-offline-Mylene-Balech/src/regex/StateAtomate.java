package regex;

import java.util.ArrayList;

public class StateAtomate {
    ArrayList<Integer> ancien;
    int nouveau;
    
    //Associe l'ancien état et le nouveal
    public StateAtomate(ArrayList<Integer> ancien, int nouveau){
        this.ancien = ancien;
        this.nouveau = nouveau;
    }
}
