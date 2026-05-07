def my_hash(name):
    # 1. Normalisation et Salage discret
    # On utilise un nombre premier de Mersenne pour la complexité
    prime_mersenne = (2**31) - 1
    state = 0xABCDEF12  # Registre d'état initial
    
    # 2. Pré-traitement : Conversion en liste d'entiers avec pondération positionnelle
    # On traite le nom par blocs de caractères
    data = [ord(c) * (i + 1) for i, c in enumerate(name)]
    
    # 3. Boucle de Complexification (Diffusion & Confusion)
    for i, val in enumerate(data):
        # Opération de mélange (Mixer)
        # On utilise une rotation dépendante de la valeur du caractère
        rotation = (val % 24) + 5
        state ^= val
        state = ((state << rotation) | (state >> (32 - rotation))) & 0xFFFFFFFF
        
        # Multiplication modulaire (Transformation non-linéaire)
        # On utilise 0x517CC1B7 (une constante issue de la partie fractionnaire de racine de 3)
        state = (state * 0x517CC1B7) % prime_mersenne
        
        # Injection de l'index pour casser les répétitions (ex: "aaaa")
        state ^= (i * 0x12345678)
    
    # 4. Post-traitement (Finalisation)
    # On applique une dernière couche de XOR pour "lisser" la distribution
    state ^= (state >> 16)
    state = (state * 0x85ebca6b) & 0xFFFFFFFF
    state ^= (state >> 13)
    state = (state * 0xc2b2ae35) & 0xFFFFFFFF
    state ^= (state >> 16)
    
    return f"{state:08x}".upper()

# --- Test de l'algorithme ---
nom_test = "MANDUDI BOYO FANY"
hash_result = my_hash(nom_test)

print(f"Structure de hachage pour : {nom_test}")
print(f"Empreinte Unique : {hash_result}")

# Démonstration de la sensibilité au changement (Effet Avalanche)
print(f"Empreinte avec une variante : {my_hash(nom_test + ' ')}")