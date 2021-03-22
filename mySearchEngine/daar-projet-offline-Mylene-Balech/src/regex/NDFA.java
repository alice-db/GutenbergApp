package regex;

import java.util.ArrayList;

public class NDFA {
    static final int CONCAT = 0xC04CA7;
    static final int ETOILE = 0xE7011E;
    static final int ALTERN = 0xA17E54;
    static final int PROTECTION = 0xBADDAD;
    private int compteurState = 0;
    private int CommunAltern = -1;
    private ArrayList<Epsilon> tableauEpsilon = new ArrayList<Epsilon>();

    public NDFA(){}
    
    //Création des espilons transitions
    public ArrayList<Epsilon> lancementNDFA(RegExTree tree){
        int compteur = 0;
        boolean isFinal = false;
        if(tree.root == ALTERN ) isFinal= true;
        createTableau(tree, true, tree);
        return tableauEpsilon;
    }
    
    //Affecte la valeur final en fonction de la racine
    public boolean isFinal(RegExTree tree, boolean isFinalParent){
        boolean isFinal = false;
        if (isFinalParent == true){
            if (tree.root == ALTERN || tree.root == CONCAT) isFinal = true;
        }
        return isFinal;
    }
    
    //Création des epsilons transitions
    public ArrayList<Epsilon> createTableau(RegExTree tree, boolean isFinalParent, RegExTree parent){
        int Etat_compteur = compteurState;
        int alternEtat = -1;
        if (tree.root == ALTERN){
            alternEtat = Etat_compteur;
        }
        
        int cptConcat = 0;
        boolean isFinal = false;
        if(!tree.subTrees.isEmpty()) {
            if (tree.root == ALTERN){
                // Enfant numéro 2
                compteurState = Etat_compteur + 1;
                tableauEpsilon.add(new Epsilon(alternEtat, compteurState, "ε", isFinalParent, tree.root)); //Permet de créer la relation avec le parent
                createTableau(tree.subTrees.get(1), isFinalParent, tree); //Création des transitions pour les enfants
                int communEtat = compteurState + 1;
                if(tree.subTrees.get(0).root == ALTERN)  CommunAltern = communEtat; // Permet de rejoindre un état dans un alterne 
                tableauEpsilon.add(new Epsilon(compteurState, communEtat, "ε", isFinalParent, tree.root)); 

                if(CommunAltern > 0 && CommunAltern != communEtat)
                    tableauEpsilon.add(new Epsilon(communEtat,CommunAltern, "ε", isFinalParent, tree.root)); //Permet de rejoindre l'enfant commun 

                // Enfant numéro 1
                compteurState = communEtat + 1;
                tableauEpsilon.add(new Epsilon(alternEtat, compteurState, "ε", isFinalParent, tree.root)); //Permet de créer la relation avec le parent
                createTableau(tree.subTrees.get(0), isFinalParent, tree); //Création des transitions pour les enfants
                Etat_compteur = compteurState;
                if (communEtat != CommunAltern) tableauEpsilon.add(new Epsilon(Etat_compteur, communEtat, "ε", isFinalParent, tree.root)); //Permet de rejoindre l'enfant commun 
            }
            if (tree.root == CONCAT){
                for  (RegExTree s : tree.subTrees) {
                    isFinal = isFinalParent;
                    //le premier élément n'est jamais final sauf si son successeur est une étoile
                    if(cptConcat == 0 && tree.subTrees.get(1).root != ETOILE){
                        isFinal = false; 
                    }
                    createTableau(s, isFinal, tree); //Création des epsilons transitions pour le caractère
                    if (cptConcat == 0) {
                        int nouveauEtat = compteurState + 1;
                        tableauEpsilon.add(new Epsilon(compteurState, nouveauEtat, "ε", isFinal, tree.root));//Rajout d'une transition entre les deux parties
                        compteurState = nouveauEtat;
                    }
                    cptConcat++;
                }
            }

            if (tree.root == ETOILE){
                isFinal = isFinalParent;
                int debutEtoile = compteurState;
                compteurState+=1;
                tableauEpsilon.add(new Epsilon(debutEtoile,compteurState, "ε", isFinal, tree.root)); //Transitions du début de l'étoile

                int debutCarc = compteurState;
                createTableau(tree.subTrees.get(0), isFinal, tree); //Création des transitions de l'intérieur de l'étoile
                int finCarac = compteurState;
                
                int finEtoile = compteurState;
                Epsilon last = tableauEpsilon.get(tableauEpsilon.size()-1); //Récupère le dernier état ajouté
            	int final_dest = last.destination;
            	
                if (tree.subTrees.get(0).root == ALTERN) {
                    if (CommunAltern > -1 ) finCarac = CommunAltern; // Si c'est un alterne on récupère l'enfant commun
                    else finCarac = final_dest; // Sinon c'est le dernier état
                }
                tableauEpsilon.add(new Epsilon(finCarac,debutCarc, "ε", isFinal, tree.root)); // Transition de retour en arrière
                int ancienetat = compteurState;
                if (tree.subTrees.get(0).root == ALTERN && CommunAltern == -1) {
                	ancienetat = final_dest; //Necessaire pour faire la transition entre l'ancien état et le prochain
                }
                if (tree.subTrees.get(0).root == ALTERN && CommunAltern > -1) ancienetat = finCarac;
                compteurState+=1;
                tableauEpsilon.add(new Epsilon(ancienetat,compteurState, "ε", isFinal, tree.root)); //Permet de faire le lien entre l'ancient état de l'étoile et le prochain
                finEtoile = compteurState;
                tableauEpsilon.add(new Epsilon(debutEtoile,finEtoile, "ε", isFinal, tree.root)); // Ajout d'une transition de la fin vers le début (ex: 5 -> 8)
            }
        } else {
            int ancienCompteur = Etat_compteur;
            compteurState = Etat_compteur + 1;
            tableauEpsilon.add(new Epsilon(ancienCompteur,compteurState, String.valueOf(tree.root), isFinalParent, -1)); //Ajout de la transition avec le caractère en chemin
        }
        return tableauEpsilon;
    }
}
