package regex;

import java.util.ArrayList;
import java.util.Collections;

//Retourne le DFA avec un nombre minimal d'états
public class DFAMinimal {
    int numberEtat=0;
    public DFAMinimal(){}
    String Spuit = "puit";
    int monPuit = (int)Spuit.charAt(0)+(int)Spuit.charAt(1)+(int)Spuit.charAt(2)+(int)Spuit.charAt(3);
    
    //Vérifie si un état a déjà été renommé
    private boolean ifExists(ArrayList<Integer> etat, ArrayList<RenameDFA> rename){
        boolean trouve = false;
        for(int i = 0; i < rename.size(); i++){
            RenameDFA re = rename.get(i);
            if(re.ancien.equals(etat)){
                trouve = true;
            }
        }

        return trouve;
    }
    
    //Retourne l'état renommé 
    private int getEtatRename(ArrayList<Integer> etat, ArrayList<RenameDFA> rename){
        int etatRetour = -1;
        for(int i = 0; i < rename.size(); i++){
            RenameDFA re = rename.get(i);
            if(re.ancien.equals(etat)){
                etatRetour = re.nouveau;
            }
        }

        return etatRetour;
    }
    
    //Création du DFA avec le nombre minimal d'état (il n'existe plus de liste d'états)
    private ArrayList<EtatRenamed> getDfaMin (ArrayList<EtatDFA> etats, ArrayList<RenameDFA> rename){
        ArrayList<EtatRenamed> nouveau = new ArrayList<EtatRenamed>();
        int cptNouveau = 0;
        //Pour chaque état de la destination et de la source on le renomme, où l'on récupère son identifiant
        for(int i = 0; i < etats.size(); i++){
            EtatDFA etat = etats.get(i);
            int source = -1;
            int destination = -1;
            if(ifExists(etat.sourceI, rename)){
                source = getEtatRename(etat.sourceI, rename);
            }else {
                rename.add(new RenameDFA(cptNouveau, etat.sourceI, etat.isFinal));
                source = getEtatRename(etat.sourceI, rename);
                cptNouveau++;
            }
            if(ifExists(etat.destinationI, rename)){
                destination = getEtatRename(etat.destinationI, rename);
            }else {
                rename.add(new RenameDFA(cptNouveau, etat.destinationI, etat.isFinal));
                destination = getEtatRename(etat.destinationI, rename);
                cptNouveau++;
            }

            nouveau.add(new EtatRenamed(source, destination, Integer.parseInt(etat.chemin), etat.isFinal));
        }

        return nouveau; //Retourne le tableau avec le minimum d'états
    }
    
    //Créer le tableau contenant les différents renommage 
    public ArrayList<RenameDFA> getRename(ArrayList<EtatDFA> etats){
        ArrayList<RenameDFA> rename = new ArrayList<RenameDFA>();
        int cptNouveau = 0;
        for(int i = 0; i < etats.size(); i++){
            EtatDFA etat = etats.get(i);
            if(!ifExists(etat.sourceI, rename)){
                rename.add(new RenameDFA(cptNouveau, etat.sourceI, etat.isFinal));
                cptNouveau++;
            }
            if(!ifExists(etat.destinationI, rename)){
                rename.add(new RenameDFA(cptNouveau, etat.destinationI, etat.isFinal));
                cptNouveau++;
            }
        }
        return rename;
    }
    
    //Vérifie si un etat existe dans les etats destinations
    private boolean existChemin(int etat, ArrayList<Integer> etats){
        for(Integer e : etats){
            if (e == etat) return true;
        }
        return false;
    }
    
    //Récupère toutes les destinations
    private ArrayList<Integer> getChemins(ArrayList<EtatRenamed> etats){
        ArrayList<Integer> chemins = new ArrayList<Integer>();
        for(EtatRenamed etat : etats){
            if(!existChemin(etat.chemin, chemins)) chemins.add(etat.chemin);
        }
        Collections.sort(chemins);
        return chemins;
    }
    
    //Vérifie si la source existe dans les états
    private boolean existArret(int etat, ArrayList<Integer> etats){
        for(Integer e : etats){
            if (e == etat) return true;
        }
        return false;
    }
    
    //Récupère les sources 
    private ArrayList<Integer> getSources(ArrayList<EtatRenamed> etats){
        ArrayList<Integer> sources = new ArrayList<Integer>();
        for(EtatRenamed etat : etats){
            if(!existArret(etat.source, sources)) sources.add(etat.source);
            if(!existArret(etat.destination, sources)) sources.add(etat.destination);
        }
        Collections.sort(sources);
        return sources;
    }
    
    //Création du tableau avec le puit
    private ArrayList<EtatRenamed> createPuit(ArrayList<EtatRenamed> etats, ArrayList<Integer> chemins, ArrayList<Integer> sources){
        ArrayList<EtatRenamed> leschemins = new ArrayList<EtatRenamed>();
        for(Integer c : chemins){
            for(Integer s : sources){
                EtatRenamed puit = new EtatRenamed(s,monPuit, c,false);
                for(EtatRenamed etat : etats){
                    if(etat.chemin == c && etat.source == s){
                        puit = new EtatRenamed(s,etat.destination, c,etat.isFinal);
                    }
                }
                leschemins.add(puit);
            }
        }
        return leschemins;
    }
    
    //Retourne un etat en fonction de sa source et sa destination
    private EtatRenamed getEtatR(Integer source, Integer chemin, ArrayList<EtatRenamed> lesPuits){
        EtatRenamed trouve = new EtatRenamed();
        for(EtatRenamed etat : lesPuits){
            if(etat.source == source && etat.chemin == chemin) trouve = etat;
        }
        return trouve;
    }
    
    //Vérifie si un chemin entre une source et une destination existe dans le tableau
    private boolean existsInMatrice(ArrayList<Integer> sources, int chemin, ArrayList<TableauEquivalence> matrice){
        for(TableauEquivalence t : matrice){
            if(t.depart.equals(sources) && chemin == t.chemin) {
                return true;
            }
        }
        return false;
    }
    
    //Création de la matrice d'équivalence avec les puits 
    private ArrayList<TableauEquivalence> createMatrice(ArrayList<Integer> sources, ArrayList<Integer> chemins,ArrayList<EtatRenamed> lesPuits){
        ArrayList<TableauEquivalence> equivalent = new ArrayList<TableauEquivalence>();
        for(Integer s1 : sources){
            for(Integer s2 : sources){
                if(s2 > s1) {
                    for (Integer c : chemins) {
                        EtatRenamed etat1 = getEtatR(s1, c, lesPuits);
                        EtatRenamed etat2 = getEtatR(s2, c, lesPuits);
                        boolean egal = false;
                        if (etat1.destination != monPuit && etat2.destination != monPuit) {
                            if (etat1.destination == etat2.destination) egal = true;
                        }

                        ArrayList<Integer> depart = new ArrayList<Integer>();
                        depart.add(etat1.source);
                        depart.add(etat2.source);
                        ArrayList<Integer> sortie = new ArrayList<Integer>();
                        sortie.add(etat1.destination);
                        sortie.add(etat2.destination);
                        if (!existsInMatrice(depart, c, equivalent)) {
                            equivalent.add(new TableauEquivalence(depart, sortie, c, egal));
                        }
                    }
                }
            }
        }
        return equivalent;
    }
    
    //Supprime toutes les duplications dans les états 
    private ArrayList<Integer> removeDuplicates(ArrayList<Integer> nouveau){
        ArrayList<Integer> nouvel = new ArrayList<Integer>();
        for(Integer c : nouveau){
            boolean trouve = false;
            for(Integer n : nouvel){
                if(n == c){
                    trouve = true;
                }
            }
            if(!trouve) nouvel.add(c);
        }
        Collections.sort(nouvel);
        return nouvel;
    }
    
    //On change les états s'ils sont équivalents
    private ArrayList<Equivalence> changeState(ArrayList<TableauEquivalence> tableau,  ArrayList<Integer> sources){
        ArrayList<Equivalence> newState = new ArrayList<Equivalence>();
        for(Integer s : sources){
            ArrayList<Integer> nouvelEtat = new ArrayList<Integer>();
            for(TableauEquivalence t : tableau){
                for(Integer i : t.depart){
                    if(i == s) nouvelEtat.addAll(t.depart);
                }
            }
            if(nouvelEtat.isEmpty()){
                ArrayList<Integer> ancien = new ArrayList<Integer>();
                ancien.add(s);
                newState.add(new Equivalence(s, ancien));
            }
            else {
                nouvelEtat = removeDuplicates(nouvelEtat);
                newState.add(new Equivalence(s, nouvelEtat));
            }
        }
        return newState;
    }
    
    //Récupère l'état dans les équivalences
    private ArrayList<Integer> getState(int source, ArrayList<Equivalence> tableau){
        for(Equivalence e : tableau){
            if(e.ancien == source) return e.nouveau;
        }
        return new ArrayList<Integer>();
    }
    
    //On vérifie si un chemin existe déjà dans l'automate
    private boolean existsAutomate(Automate auto, ArrayList<Automate> automate){
        for(Automate a : automate){
            if(a.chemin == auto.chemin && a.destination.equals(auto.destination) && a.source.equals(auto.source) && a.isFinal == auto.isFinal){
                return true;
            }
        }
        return false;
    }
    
    //Création du tableau des automates
    private ArrayList<Automate> createAutomate(ArrayList<Equivalence> tableau, ArrayList<EtatRenamed> rename){
        ArrayList<Automate> automate = new ArrayList<Automate>();
        for(EtatRenamed etat : rename){
            ArrayList source = getState(etat.source, tableau);
            ArrayList destination = getState(etat.destination, tableau);
            Automate newAuto = new Automate(source,destination, etat.chemin, etat.isFinal);
            if(!existsAutomate(newAuto , automate))
                automate.add(newAuto);
        }

        return automate;
    }
    
    //Retourne les tableau des états minimals
    public ArrayList<Automate> getDFAMinimal(ArrayList<EtatDFA> etats){
        ArrayList<EtatRenamed> nouveauTab = new ArrayList<EtatRenamed>();
        ArrayList<RenameDFA> rename = getRename(etats);
        nouveauTab = getDfaMin(etats, rename);
        ArrayList<Integer> chemins = getChemins(nouveauTab);
        ArrayList<Integer> sources = getSources(nouveauTab);
        ArrayList<EtatRenamed> lesPuits = createPuit(nouveauTab, chemins, sources);
        ArrayList<TableauEquivalence> lesEquivalents = createMatrice(sources, chemins, lesPuits); //Création des equivalences

        ArrayList<TableauEquivalence> isEquivalent = new ArrayList<TableauEquivalence>();
        for(TableauEquivalence ev : lesEquivalents){ 
            if(ev.equivalent) isEquivalent.add(ev); //Si deux sources ont le même chemin et la même destination (différente du puit), on les ajoute 
        }
        
        ArrayList<Automate> automate = new ArrayList<Automate>();
        ArrayList<Equivalence> nouvelleEquivalence = changeState(isEquivalent, sources); // change les états en fonction des equivalences

        automate = createAutomate(nouvelleEquivalence, nouveauTab); // Création de l'automate

        return automate;
    }
    
    //Création des états des automates
    private ArrayList<StateAtomate> createStateAuto(ArrayList<Automate> automate){
        ArrayList<StateAtomate> state = new ArrayList<StateAtomate>();
        int cptNouveau = 0;
        for(Automate auto : automate){
            boolean isTrouve = false;
            for(StateAtomate st : state){
                if(st.ancien.equals(auto.source)) isTrouve = true;
            }
            if(!isTrouve) {
                state.add(new StateAtomate(auto.source, cptNouveau));
                cptNouveau++;
            }
            isTrouve = false;
            for(StateAtomate st : state){
                if(st.ancien.equals(auto.destination)) isTrouve = true;
            }
            if(!isTrouve) {
                state.add(new StateAtomate(auto.destination, cptNouveau));
                cptNouveau++;
            }
        }

        return state;
    }
    
    //retourne l'état d'un automate
    private int getStateAu(ArrayList<Integer> achercher, ArrayList<StateAtomate> states){
        int etat = -1;
        for(StateAtomate st : states){
            if(st.ancien.equals(achercher)) etat = st.nouveau;
        }
        return etat;
    }
    
    //Création de l'automate FINAL
    public ArrayList<Automate> createAutomate(ArrayList<Automate> automate){
        ArrayList<Automate> automateFinal = new ArrayList<Automate>();
        ArrayList<StateAtomate> state = createStateAuto(automate);

        for(Automate auto : automate){
            int source = getStateAu(auto.source, state);
            int destination = getStateAu(auto.destination, state);
            automateFinal.add(new Automate(source, destination, auto.chemin, auto.isFinal));
        }
        return automateFinal;
    }
}
