package regex;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Scanner;

public class Regex {
	//MACROS
	static final int CONCAT = 0xC04CA7;
	static final int ETOILE = 0xE7011E;
	static final int ALTERN = 0xA17E54;
	static final int PROTECTION = 0xBADDAD;

	static final int PARENTHESEOUVRANT = 0x16641664;
	static final int PARENTHESEFERMANT = 0x51515151;
	static final int DOT = 0xD07;

	//REGEX
	private static String regEx;
	private static String fileName;

	//MAIN
	public static void main(String arg[]) {
		System.out.println("Welcome to the clone of the egrep UNIX command");
		long debutTime = System.currentTimeMillis();
		if (arg.length!=0) {
			regEx = arg[0];
			fileName = arg[1];
		} else {
			Scanner scanner = new Scanner(System.in);
			System.out.print("  >> Please enter a regEx: ");
			regEx = scanner.next();
		}
		System.out.println("  >> Parsing regEx \""+regEx+"\".");
		System.out.println("  >> ...");

		if (regEx.length()<1) {
			System.err.println("  >> ERROR: empty regEx.");
		} else {
			//Vérifie si c'est un facteur
			boolean isString = true;
			for (int i=0;i<regEx.length();i++) {
				int carac = (int)regEx.charAt(i);
				if (carac < 65 || carac > 90 && carac < 97 || carac > 122) {
					isString = false;
				}
			}
			//Si c'est un facteur on fait KMP sinon REgEx
			if(isString) {
				KMP kmp = new KMP();
				try {
					//Récupère résultats fournis par KMP
					ArrayList<String> resultats = kmp.readFile(regEx, fileName);
					
					System.out.println("  >> Results in the texte : "+resultats.size());
					
					for(int i = 0; i< resultats.size(); i++){
						System.out.println(resultats.get(i));
					}
					
					System.out.println("  >> End of results : "+resultats.size());
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}else {
				//Vérifie si ce sont des codes ascii
				boolean isCodeAscii = false;
				String code = new String();
				String ascii = new String();
				int compteur = 0;
				for (int i=0;i<regEx.length();i++) {
					int carac = (int)regEx.charAt(i);
					String debut = "[";
					String fin = "]";
					if(carac == (int)debut.charAt(0)){
						isCodeAscii = true;
					}
					if(carac == (int)fin.charAt(0)) {
						isCodeAscii = false;
					}
					if(isCodeAscii && carac != (int)debut.charAt(0)) {
						code += regEx.charAt(i);
					}
					if(!isCodeAscii) {
						if(code.length() > 0) {
							int newCode = Integer.parseInt(code);
							if(newCode >= 65 && newCode <= 90 || newCode >= 97 && newCode <= 122) {
								ascii += String.valueOf(newCode);
								code = new String();
								compteur++;
							}
						}
						else {
							ascii += String.valueOf(carac);
							compteur++;
						}

						if(compteur < regEx.length()){
							ascii += ",";
						}
					}
				}
				System.out.println("  >> ASCII codes: ["+ascii+"]");

				try {
					RegExTree ret = parse(); //Création de l'arbre syntaxique
					
					System.out.println("  >> Tree result: "+ret.toString()+".");
					
					NDFA ndfa = new NDFA();
					ArrayList<Epsilon> tableauNDFA = ndfa.lancementNDFA(ret); //Création de l'automate avec epsilons transitions
					System.out.println("  >> NDFA: "+String.valueOf(tableauNDFA));
					
					DFA dfa = new DFA();
					ArrayList<EtatDFA> etatsDfa = dfa.lancementDFAMax(tableauNDFA); //Création de l'automate déterministe 
					String etatd = "";
					int cpt = 1;
					for(EtatDFA etat : etatsDfa){
						etatd += etat.toString2();
						if(cpt < etatsDfa.size()) etatd += ", ";
						cpt++;
					}
					System.out.println("  >> DFA: "+etatd);

					DFAMinimal dfaMinimal = new DFAMinimal();
					
					ArrayList<Automate> automatesc = dfaMinimal.getDFAMinimal(etatsDfa);// Création de l'automate fini déterministe avec un nombre d'état minimale
				
					ArrayList<Automate >automate = dfaMinimal.createAutomate(automatesc);
					String s_automate = "[";
					cpt = 1;
					for(Automate at : automate){
						String cheminFinal = Character.toString((char) at.cheminFinal);
						if(at.cheminFinal == DOT) cheminFinal = ".";
						s_automate+= at.sourceFinal+" → "+at.destinationFinal+" = "+cheminFinal;
						if(cpt < automate.size()) s_automate+=", ";
						cpt++;
					}
					s_automate+="]";
					System.out.println("  >> DFA with minimum states : "+s_automate) ; //Création de l'automate fini déterministe avec un nombre d'état minimale en ayant renommé les états

					AutomateParse file = new AutomateParse();
					ArrayList<String> resultats = file.readFile(automate, fileName, regEx);
					System.out.println("  >> Results in the texte : "+resultats.size());
					for(int i = 0; i< resultats.size(); i++){
						System.out.println(resultats.get(i));
					}
					System.out.println("  >> End of results : "+resultats.size());
				} catch (Exception e) {
					System.err.println("  >> ERROR: syntax error for regEx \""+regEx+"\".");
				}
			}
		}
		long fin = System.currentTimeMillis();
		
		long duration = fin-debutTime;
		System.out.println("Execution time: "+duration+" ms");

	}

	//FROM REGEX TO SYNTAX TREE
	private static RegExTree parse() throws Exception {
		//BEGIN DEBUG: set conditionnal to true for debug example
		if (false) throw new Exception();
		RegExTree example = exampleAhoUllman();
		if (false) return example;
		//END DEBUG

		ArrayList<RegExTree> result = new ArrayList<RegExTree>();
		String code = new String();
		boolean isCodeAscii = false;
		for (int i=0;i<regEx.length();i++) {
			int carac = charToRoot(regEx.charAt(i));
			String debut = "[";
			String fin = "]";
			if((int) regEx.charAt(i) == (int)debut.charAt(0)){
				isCodeAscii = true;
			}
			if((int) regEx.charAt(i) == (int)fin.charAt(0)) {
				isCodeAscii = false;
			}
			if(isCodeAscii && (int)regEx.charAt(i) != (int)debut.charAt(0)) {
				code += regEx.charAt(i);
			}
			if(!isCodeAscii) {
				if(code.length() > 0) {
					int newCode = Integer.parseInt(code);
					if(newCode >= 65 && newCode <= 90 || newCode >= 97 && newCode <= 122) {
						result.add(new RegExTree(newCode, new ArrayList<RegExTree>()));
						code = new String();
					}
					else throw new Exception();
				}
				else {
					result.add(new RegExTree(carac,new ArrayList<RegExTree>()));
				}
			}
		}

		return parse(result);
	}
	private static int charToRoot(char c) {
		if (c=='.') return DOT;
		if (c=='*') return ETOILE;
		if (c=='|') return ALTERN;
		if (c=='(') return PARENTHESEOUVRANT;
		if (c==')') return PARENTHESEFERMANT;
		return (int)c;
	}
	private static RegExTree parse(ArrayList<RegExTree> result) throws Exception {
		while (containParenthese(result)) result=processParenthese(result);
		while (containEtoile(result)) result=processEtoile(result);
		while (containConcat(result)) result=processConcat(result);
		while (containAltern(result)) result=processAltern(result);

		if (result.size()>1) throw new Exception();
		return removeProtection(result.get(0));
	}
	private static boolean containParenthese(ArrayList<RegExTree> trees) {
		for (RegExTree t: trees) if (t.root==PARENTHESEFERMANT || t.root==PARENTHESEOUVRANT) return true;
		return false;
	}
	private static ArrayList<RegExTree> processParenthese(ArrayList<RegExTree> trees) throws Exception {
		ArrayList<RegExTree> result = new ArrayList<RegExTree>();
		boolean found = false;
		for (RegExTree t: trees) {
			if (!found && t.root==PARENTHESEFERMANT) {
				boolean done = false;
				ArrayList<RegExTree> content = new ArrayList<RegExTree>();
				while (!done && !result.isEmpty())
					if (result.get(result.size()-1).root==PARENTHESEOUVRANT) { done = true; result.remove(result.size()-1); }
					else content.add(0,result.remove(result.size()-1));
				if (!done) throw new Exception();
				found = true;
				ArrayList<RegExTree> subTrees = new ArrayList<RegExTree>();
				subTrees.add(parse(content));
				result.add(new RegExTree(PROTECTION, subTrees));
			} else {
				result.add(t);
			}
		}
		if (!found) throw new Exception();
		return result;
	}
	private static boolean containEtoile(ArrayList<RegExTree> trees) {
		for (RegExTree t: trees) if (t.root==ETOILE && t.subTrees.isEmpty()) return true;
		return false;
	}
	private static ArrayList<RegExTree> processEtoile(ArrayList<RegExTree> trees) throws Exception {
		ArrayList<RegExTree> result = new ArrayList<RegExTree>();
		boolean found = false;
		for (RegExTree t: trees) {
			if (!found && t.root==ETOILE && t.subTrees.isEmpty()) {
				if (result.isEmpty()) throw new Exception();
				found = true;
				RegExTree last = result.remove(result.size()-1);
				ArrayList<RegExTree> subTrees = new ArrayList<RegExTree>();
				subTrees.add(last);
				result.add(new RegExTree(ETOILE, subTrees));
			} else {
				result.add(t);
			}
		}
		return result;
	}
	private static boolean containConcat(ArrayList<RegExTree> trees) {
		boolean firstFound = false;
		for (RegExTree t: trees) {
			if (!firstFound && t.root!=ALTERN) { firstFound = true; continue; }
			if (firstFound) if (t.root!=ALTERN) return true; else firstFound = false;
		}
		return false;
	}
	private static ArrayList<RegExTree> processConcat(ArrayList<RegExTree> trees) throws Exception {
		ArrayList<RegExTree> result = new ArrayList<RegExTree>();
		boolean found = false;
		boolean firstFound = false;
		for (RegExTree t: trees) {
			if (!found && !firstFound && t.root!=ALTERN) {
				firstFound = true;
				result.add(t);
				continue;
			}
			if (!found && firstFound && t.root==ALTERN) {
				firstFound = false;
				result.add(t);
				continue;
			}
			if (!found && firstFound && t.root!=ALTERN) {
				found = true;
				RegExTree last = result.remove(result.size()-1);
				ArrayList<RegExTree> subTrees = new ArrayList<RegExTree>();
				subTrees.add(last);
				subTrees.add(t);
				result.add(new RegExTree(CONCAT, subTrees));
			} else {
				result.add(t);
			}
		}
		return result;
	}
	private static boolean containAltern(ArrayList<RegExTree> trees) {
		for (RegExTree t: trees) if (t.root==ALTERN && t.subTrees.isEmpty()) return true;
		return false;
	}
	private static ArrayList<RegExTree> processAltern(ArrayList<RegExTree> trees) throws Exception {
		ArrayList<RegExTree> result = new ArrayList<RegExTree>();
		boolean found = false;
		RegExTree gauche = null;
		boolean done = false;
		for (RegExTree t: trees) {
			if (!found && t.root==ALTERN && t.subTrees.isEmpty()) {
				if (result.isEmpty()) throw new Exception();
				found = true;
				gauche = result.remove(result.size()-1);
				continue;
			}
			if (found && !done) {
				if (gauche==null) throw new Exception();
				done=true;
				ArrayList<RegExTree> subTrees = new ArrayList<RegExTree>();
				subTrees.add(gauche);
				subTrees.add(t);
				result.add(new RegExTree(ALTERN, subTrees));
			} else {
				result.add(t);
			}
		}
		return result;
	}
	private static RegExTree removeProtection(RegExTree tree) throws Exception {
		if (tree.root==PROTECTION && tree.subTrees.size()!=1) throw new Exception();
		if (tree.subTrees.isEmpty()) return tree;
		if (tree.root==PROTECTION) return removeProtection(tree.subTrees.get(0));

		ArrayList<RegExTree> subTrees = new ArrayList<RegExTree>();
		for (RegExTree t: tree.subTrees) subTrees.add(removeProtection(t));
		return new RegExTree(tree.root, subTrees);
	}

	//EXAMPLE
	// --> RegEx from Aho-Ullman book Chap.10 Example 10.25
	private static RegExTree exampleAhoUllman() {
		RegExTree a = new RegExTree((int)'a', new ArrayList<RegExTree>());
		RegExTree b = new RegExTree((int)'b', new ArrayList<RegExTree>());
		RegExTree c = new RegExTree((int)'c', new ArrayList<RegExTree>());
		ArrayList<RegExTree> subTrees = new ArrayList<RegExTree>();
		subTrees.add(c);
		RegExTree cEtoile = new RegExTree(ETOILE, subTrees);
		subTrees = new ArrayList<RegExTree>();
		subTrees.add(b);
		subTrees.add(cEtoile);
		RegExTree dotBCEtoile = new RegExTree(CONCAT, subTrees);
		subTrees = new ArrayList<RegExTree>();
		subTrees.add(a);
		subTrees.add(dotBCEtoile);
		return new RegExTree(ALTERN, subTrees);
	}
}
