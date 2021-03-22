package regex;

import java.util.ArrayList;

//Class qui permet de créer l'automate fini déterministe
public class DFA {
    private ArrayList<String> dfaMax = new ArrayList<String>();

    public DFA(){}
    
    // Vérifier si la source fait partie des états
    private boolean getEtatDFAVerify(int source, ArrayList<EtatDFA> etats){
        for(EtatDFA etat : etats){
            if (etat.source == source){
                return true;
            }
        }
        return false;
    }
    
    // Récupère toutes les destinations d'une source en fonction des états
    public ArrayList<Integer> getChildrens (int source, ArrayList<Epsilon> etats){
        ArrayList<Integer> childrens= new ArrayList<Integer>();
        for(int i = 0; i < etats.size(); i++){
            Epsilon etat = etats.get(i);
            if(etat.source == source && etat.caractere == "ε"){
                childrens.add(etat.destination);
                if(getChildrens(etat.destination, etats).size() > 0) childrens.addAll(getChildrens(etat.destination, etats));
            }
        }
        return childrens;
    }
    
    //Vérifie si un état existe dans les états 
    private boolean ifExist(EtatDFA atrouver, ArrayList<EtatDFA> etats){
        boolean trouve = false;
        for(EtatDFA etat : etats){
            if(etat.source == atrouver.source){
                trouve = true;
            }
        }

        return trouve;
    }
    
    // Retourne l'index de l'état à chercher grâce à la source
    private int getEtat(EtatDFA atrouver, ArrayList<EtatDFA> etats){
        int trouve = -1;
        for(int i = 0; i < etats.size(); i++){
            if(etats.get(i).source == atrouver.source){
                trouve = i;
            }
        }
        return trouve;
    }
    
    //Vérifie si un enfant existe
    private boolean childExists(int c, ArrayList<Integer> integers){
        for(Integer i : integers){
            if(c == i) return true;
        }
        return false;
    }
    
    // Vérifie si une des destination est finale 
    private boolean monEnfantestFinal(ArrayList<Integer> enfants, ArrayList<Epsilon> etats){
        boolean isFinal = false;
        for(Integer i : enfants) {
            for (Epsilon etat : etats) {
                if(etat.destination == i)
                    if(etat.isFinal == true) isFinal = true;
            }
        }

        return isFinal;
    }
    
    // Création du tableau automate final déterministe
    
    public ArrayList<EtatDFA> lancementDFAMax(ArrayList<Epsilon> etats){
        ArrayList<EtatDFA> etatDFAArraylist = new ArrayList<EtatDFA>();
        
        //Création du tableau des états 
        //Si les chemins sont reliés par un epsilon on les concatène ensemble
        //Une source a donc un tableau de destinations si celle ci a des epsilons
        for(int i = 0; i < etats.size(); i++){
            ArrayList<Integer> childrens = new ArrayList<Integer>();
            Epsilon etat = etats.get(i);
            if(etat.caractere == "ε"){
                childrens.add(etat.destination);
                for(int j = i+1 ; j < etats.size(); j++){
                    Epsilon etat2 = etats.get(j);
                    if(etat2.source == etat.source && etat.caractere == "ε"){
                        childrens.add(etat2.destination);
                    }
                }
            }

            if (childrens.size() > 0 ) {
                EtatDFA nouvel = new EtatDFA(etat.source, childrens);
                if(ifExist(nouvel, etatDFAArraylist)){
                    EtatDFA point = etatDFAArraylist.get(getEtat(nouvel, etatDFAArraylist));
                    etatDFAArraylist.remove(point);
                    point.enfants.addAll(childrens);
                    ArrayList<Integer> childs = new ArrayList<Integer>();
                    for(Integer in : point.enfants){
                        if (!childExists(in, childs)) childs.add(in);
                    }
                    point.setEnfants(childs);
                    etatDFAArraylist.add(point);
                }
                else etatDFAArraylist.add(nouvel);
            }
        }

        ArrayList<EtatDFA> tableauEtat = new ArrayList<EtatDFA>();
        //Trie le tableau en fonction de l'indice de la source
        while (!etatDFAArraylist.isEmpty()){
            EtatDFA point = etatDFAArraylist.get(0);
            for(int i = 0; i < etatDFAArraylist.size(); i++){
                if(point.source > etatDFAArraylist.get(i).source){
                    point = etatDFAArraylist.get(i);
                }
            }
            tableauEtat.add(point);
            etatDFAArraylist.remove(point);
        }
        
        //S'il existe encore des epsilons transitions pour des sources
        //Alors on concatème ses enfants, si la source est aussi une destination avec epsilon, 
        //ses destinations fusionnent avec les destinations de la source avant
        boolean changement = true;
        while(changement) {
            boolean ibreak = false;
            changement = false;
            for(int i = 0; i < tableauEtat.size() && !ibreak; i++){
                EtatDFA etat1 = tableauEtat.get(i);
                for( int c = 0; c < etat1.enfants.size() && !ibreak; c++) {
                    for (int j = i + 1; j < tableauEtat.size(); j++) {
                        EtatDFA etat2 = tableauEtat.get(j);
                        if (etat1.enfants.get(c) == etat2.source){
                            ArrayList<Integer> children = new ArrayList<Integer>();
                            children.addAll(etat1.enfants);
                            children.addAll(etat2.enfants);
                            etat1.setEnfants(children);
                            tableauEtat.remove(etat2);
                            ibreak = true;
                            changement = true;
                        }
                    }
                }
            }
        }
         
        // Création des nouveaux états (liste d'états) si des états sont dans une même racine alors ils sont équivalents
        ArrayList<EtatDFA> mesNouveauxEtats = new ArrayList<EtatDFA>();
        for (Epsilon etat : etats) {
            boolean inRacine = false;
            ArrayList<Integer> equivalence = new ArrayList<Integer>();
            for (EtatDFA etatDFA : tableauEtat) {
                if (etatDFA.source == etat.source) inRacine = true;
                for (Integer c : etatDFA.enfants) {
                    if (c == etat.source) {
                        inRacine = true;
                        equivalence = etatDFA.equivalence();
                    }
                }
            }
            
            //Si l'état n'est pas dans la racine, on crée une nouvelle équivalence 
            if (!inRacine) {
                for (EtatDFA etatDFA : tableauEtat) {
                    if (etatDFA.source == etat.destination) equivalence = etatDFA.equivalence();
                    for (Integer c : etatDFA.enfants) {
                        if (c == etat.destination) {
                            equivalence = etatDFA.equivalence();
                        }
                    }
                }
                ArrayList<Integer> source = new ArrayList<Integer>();
                source.add(etat.source);
                mesNouveauxEtats.add(new EtatDFA(source, equivalence, etat.caractere, etat.isFinal));
            }
        }
        
        // Pour tous les états qui sont liés par un caractère 
        // On récupère les enfants et on les ajoutes dans le tableau DFA
        for (EtatDFA etatd : tableauEtat){
            for (Integer c : etatd.enfants){
                for(Epsilon epsilon : etats){
                    if(c == epsilon.source && epsilon.caractere != "ε"){
                        boolean found = false;
                        boolean isFinal = false;
                        EtatDFA nouvelEtat = new EtatDFA();
                        for (EtatDFA etatd2 : tableauEtat){
                            if(etatd2.source == epsilon.destination){
                                nouvelEtat = etatd2;
                                found = true;
                            }
                        }
                        if(!found) {
                            ArrayList<Integer> child = new ArrayList<Integer>();
                            nouvelEtat = new EtatDFA(epsilon.destination, child);
                        }
                        isFinal = monEnfantestFinal(nouvelEtat.enfants, etats);
                        if(!isFinal){
                            ArrayList<Integer> Nchild = new ArrayList<Integer>();
                            Nchild.add(etatd.source);
                            Nchild.addAll(nouvelEtat.enfants);
                        }
                        if(!isFinal) isFinal = epsilon.isFinal;
                        mesNouveauxEtats.add(new EtatDFA(etatd.equivalence(),nouvelEtat.equivalence(),epsilon.caractere, isFinal));
                    }
                }
            }
        }
        //On vérifie qu'il n'y a pas eu d'oublis
        ArrayList<EtatDFA> mesNouveauxEtat2 = (ArrayList<EtatDFA>) mesNouveauxEtats.clone();
        for(EtatDFA etat : mesNouveauxEtats){
            boolean trouve = false;
            for(EtatDFA etat2 : mesNouveauxEtats){
                if(etat.destinationI.equals(etat2.sourceI)) trouve = true;
            }
            if(!trouve && !etat.isFinal){
            	boolean star = false;
            	for(Integer enf : etat.destinationI) {
	            	for(Epsilon epsilon : etats) {
	            		if (enf == epsilon.destination)
	            			if(epsilon.root == Regex.ETOILE) star = true;
	            		
	            		if (enf == epsilon.source)
	            			if(epsilon.root == Regex.ETOILE) star = true;
	            	}
            	}
            	for(Integer enf : etat.sourceI) {
	            	for(Epsilon epsilon : etats) {
	            		if (enf == epsilon.destination)
	            			if(epsilon.root == Regex.ETOILE) star = true;
	            		
	            		if (enf == epsilon.source)
	            			if(epsilon.root == Regex.ETOILE) star = true;
	            	}
            	}
            	
            	//Si la racine des chemins est une étoile, cela veut dire que tous les chemins vont vers les autres chemins de l'étoile et vers eux mêmes
            	if(star) {
	                for(EtatDFA etat3 : mesNouveauxEtats){
	                    if(etat.sourceI.equals(etat3.sourceI)){
	                        mesNouveauxEtat2.add(new EtatDFA(etat.destinationI,etat3.destinationI,etat3.chemin,etat.isFinal));
	                    }
	                }
            	}
            	
            	//Si ce n'est pas une étoile, on récupère la destination de l'homologue du chemin et on lui affecte
            	if(!star) {
            		for(EtatDFA etat4 : mesNouveauxEtats) {
            			if (etat4.sourceI.equals(etat.sourceI) && !etat4.destinationI.equals(etat.destinationI)) {
            				System.out.println(etat4.destinationI);
            				for(EtatDFA etat5 : mesNouveauxEtats) {
            					if(etat5.sourceI.equals(etat4.destinationI)) {
            						mesNouveauxEtat2.add(new EtatDFA(etat.destinationI,etat5.destinationI,etat5.chemin,etat.isFinal));
            					}
            				}
            			}
            		}
            	}
                
            }
        }
        
        return mesNouveauxEtat2; //Retourne le DFA
    }
}
