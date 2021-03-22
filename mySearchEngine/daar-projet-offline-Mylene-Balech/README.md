Pour lancer le programme :
	- Dans le build xml :
		- mettre le motif recherché dans le premier argument (Ex: Sargon, S(a|r|g)*on, S(h|e|r)*lock, S(a|r|g)*on|A(s|y)*rian),S(h|ch)erlock, S(c|h)*erlock
		- mettre le nom du fichier dans lequel on souhaite faire la recherche
		- Pour faire une recherche avec des caractères ASCII, il faut mettre le code ASCII entre crochets : Exemple pour Sargon: [83][97][114][103][111][110]
		- Si le motif est une chaîne de caractère, alors c'est KMP qui parse le fichier
	
	- En ligne decommande:
		`ant build` 
		`ant Regex`
		Exemple = pour S(a|r|g)*on|A(s|y)*rian
		<arg value="S(a|r|g)*on|A(s|y)*rian"/>
        <arg value="sargon.txt"/>
        
        Exemple = pour S(c|h)erlock
        <arg value="S(c|h)erlock"/>
        <arg value="sherlock.txt"/>
