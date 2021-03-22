package regex;

import java.util.ArrayList;
//Créer un équivalence entre un état et une liste d'état
public class Equivalence {
    int ancien;
    ArrayList<Integer> nouveau;
    int chemin;

    public Equivalence(int ancien, ArrayList<Integer> nouveau){
        this.ancien = ancien;
        this.nouveau = nouveau;
    }
}
