package regex;

import java.util.ArrayList;

public class RegExTree{
    protected int root;
    protected ArrayList<RegExTree> subTrees;
    public RegExTree(int root, ArrayList<RegExTree> subTrees) {
        this.root = root;
        this.subTrees = subTrees;
    }
    //FROM TREE TO PARENTHESIS
    public String toString() {
        if (subTrees.isEmpty()) return rootToString();
        String result = rootToString()+"("+subTrees.get(0).toString();
        for (int i=1;i<subTrees.size();i++) result+=","+subTrees.get(i).toString();
        return result+")";
    }
    private String rootToString() {
        Regex regex = new Regex();
        if (root==regex.CONCAT) return ".";
        if (root==regex.ETOILE) return "*";
        if (root==regex.ALTERN) return "|";
        if (root==regex.DOT) return ".";
        return Character.toString((char)root);
    }
}
