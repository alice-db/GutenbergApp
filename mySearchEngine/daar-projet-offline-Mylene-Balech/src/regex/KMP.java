package regex;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;

public class KMP {
	
	public KMP() {}
	
	//Lit le fichier et renvoie le résultat
	public ArrayList<String> readFile(String p, String filename) throws IOException {
		FilePrinter fileprinter= new FilePrinter();
        ArrayList<String> texte = fileprinter.readFromFile(filename);

        ArrayList<String> resultats = kmp(texte, p);
        
        fileprinter.saveToFile("resultats/resultats_kmp_"+p, resultats);
        
        return resultats;
    }
	
	// Fonction qui fait KMP et ressort les résultats obtenus 
	private ArrayList<String> kmp(ArrayList<String> texte, String prefixe){
        ArrayList<String> resultats = new ArrayList<String>();
        
		for(int c = 0; c < texte.size(); c++) {
			boolean trouve = false;
			String line = texte.get(c);
			int PT = prefixe.length(); 
	        int LT = line.length(); 
	        
	        int pi[] = new int[PT]; 
	        int j = 0; 
	        
	        pi = calculPrefixe(prefixe, PT, pi); 
	        
	        int i = 0; 
	        while (i < LT) { 
	            if (prefixe.charAt(j) == line.charAt(i)) { 
	                j++; 
	                i++; 
	            } 
	            if (j == PT) { 
	                trouve = true;
	                j = pi[j - 1];
	            } 
	            else if (i < LT && prefixe.charAt(j) != line.charAt(i)) { 
	                if (j != 0) {
	                    j = pi[j - 1]; 
	                } else
	                    i = i + 1; 
	            } 
	        } 
	        
	        if(trouve) resultats.add(line);
		}
		        
        return resultats;
    }
	
	//Renvoie le tableau des états du préfixe
	private int[] calculPrefixe(String prefixe, int PT, int pi[]) 
    { 

        int len = 0; 
        int i = 1; 
        pi[0] = 0; 
  
        while (i < PT) { 
            if (prefixe.charAt(i) == prefixe.charAt(len)) { //S'il y a une répétition d'un motif
                len++; 
                pi[i] = len; 
                i++; 
            } 
            else 
            { 
                if (len != 0) { 
                    len = pi[len - 1]; 
                } 
                else 
                { 
                    pi[i] = len; 
                    i++; 
                } 
            } 
        }
        
        return pi;
    } 
}
