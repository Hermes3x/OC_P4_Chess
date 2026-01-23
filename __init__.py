joueurs = ["A", "B", "C", "D", "E","F"]



def create_paires(joueurs):
    pairs = []
    if len(joueurs)%2 != 0:
        print("la liste ne contient pas assez de joueur. ajouter un joueur pour coninuer")
        print("joueur supplémentaire : ")
        joueur_supplémentaire = input()
        joueurs.append(joueur_supplémentaire)
        for i in range(0, len(joueurs), 2):
            pair = (joueurs[i], joueurs[i+1])
            pairs.append(pair)
    else: 
        for i in range(0, len(joueurs), 2):
            pair = (joueurs[i], joueurs[i+1])
            pairs.append(pair)

    return "\n".join([f"Match {i+1}: {p[0]} vs {p[1]}" for i,p in enumerate(pairs)])

x = create_paires(joueurs)
print(x)
