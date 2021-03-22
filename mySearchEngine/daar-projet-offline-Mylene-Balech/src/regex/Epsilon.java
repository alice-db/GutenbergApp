package regex;

//Permet de créer le chemin entre deux états avec le chemin défini, soit un caractère soit un epsilon
public class Epsilon {
    protected int source;
    protected int destination;
    protected int root;
    protected String caractere;
    protected boolean isFinal;
    public Epsilon(int source, int destination, String caractere, boolean isFinal, int root){
        this.source = source;
        this.destination = destination;
        this.caractere = caractere;
        this.isFinal = isFinal;
        this.root = root;
    }

    public String toString() {
        String result = String.valueOf(source)+ " → "+String.valueOf(destination)+" = "+caractere;
        return result;
    }
}
