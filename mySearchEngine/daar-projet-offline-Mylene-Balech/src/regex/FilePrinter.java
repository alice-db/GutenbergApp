package regex;

import java.awt.Point;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.util.ArrayList;

//Permet de récupérer le texte lu et d'écrire les résultats de la recherche dans un fichier
public class FilePrinter {
	
	public FilePrinter() {};
	
	//Sauvegarde dans le fichier les résultats
	void saveToFile(String filename,ArrayList<String> result){
		int index=0;
		try {
			while(true){
				BufferedReader input = new BufferedReader(new InputStreamReader(new FileInputStream(filename+Integer.toString(index)+".points")));
				try {
					input.close();
				} catch (IOException e) {
					System.err.println("I/O exception: unable to close "+filename+Integer.toString(index)+".txt");
				}
				index++;
			}
		} catch (FileNotFoundException e) {
			printToFile(filename+Integer.toString(index)+".txt",result);
		}
	}
	
	//Ecrit dans le fichier les résultats
	private static void printToFile(String filename,ArrayList<String> resultats){
		try {
			PrintStream output = new PrintStream(new FileOutputStream(filename));
			
			for(String string : resultats) {
				output.println(string);
			}
			
			output.close();
		} catch (FileNotFoundException e) {
			System.err.println("I/O exception: unable to create "+filename);
		}
	}
	
	//FILE LOADER
    ArrayList<String> readFromFile(String filename) throws IOException, FileNotFoundException {
        String line;
        ArrayList<String> texte=new ArrayList<String>();
        BufferedReader input = new BufferedReader(
                new InputStreamReader(new FileInputStream(filename))
        );
        try {
            while ((line=input.readLine())!=null) {
                texte.add(line);
            }
        } catch (IOException e) {
            System.err.println("Exception: interrupted I/O.");
        } finally {
            try {
                input.close();
            } catch (IOException e) {
                System.err.println("I/O exception: unable to close "+filename);
            }
        }

        return texte;
    }
}
