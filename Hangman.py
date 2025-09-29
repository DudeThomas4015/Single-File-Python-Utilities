import random

# List of words for the word bank
word_bank = [
    "python", "hangman", "challenge", "programming", "bioengineering", "development", "statistics",
    "algorithm", "analysis", "anatomy", "biology", "botany", "calculus", "chemistry", "climate", "coding",
    "computation", "data", "design", "diagnosis", "ecology", "education", "engineering", "environment",
    "equation", "experiment", "fabrication", "fluid", "genetics", "geology", "geometry", "graph", "hypothesis",
    "immunology", "innovation", "inorganic", "investigation", "kinematics", "laboratory", "machine", "materials",
    "mathematics", "mechanics", "medicine", "microbiology", "modeling", "molecule", "nanotechnology", "neuroscience",
    "nucleus", "nutrition", "optics", "organism", "organic", "particle", "pathology", "pharmacology", "physics",
    "physiology", "plant", "polymer", "probability", "protein", "psychology", "quantum", "radiation", "research",
    "robotics", "simulation", "sociology", "software", "spectroscopy", "synthesis", "technology",
    "thermodynamics", "toxicology", "transmission", "vaccine", "virology", "virus", "voltage", "wave", "xray",
    "yeast", "zoology", "bacteria", "biosphere", "cell", "chromosome", "ecosystem", "enzyme", "evolution",
    "fossil", "gene", "genome", "heredity", "mutation", "nucleotide", "photosynthesis", "reproduction", "respiration",
    "species", "tissue", "variation", "absorption", "acid", "alkali", "base", "buffer", "catalyst", "compound",
    "concentration", "crystal", "dissolution", "emulsion", "equilibrium", "exothermic", "gel", "ionic", "isotope",
    "lipid", "mixture", "osmosis", "pH", "precipitate", "reagent", "reaction", "salt", "solution", "solvent",
    "sublimation", "surface", "valence", "vector", "velocity", "viscosity", "volume", "wavelength", "weight", "work",
    "yield", "acceleration", "amplitude", "atom", "balance", "binary", "boiling", "bond", "calorie", "centrifuge",
    "coefficient", "condensation", "conductor", "convection", "current", "density", "diffusion", "effusion",
    "electricity", "electrolyte", "energy", "enthalpy", "entropy", "evaporation", "force", "friction", "gas",
    "gravity", "heat", "hydrogen", "inertia", "insulator", "ion", "kinetic", "laser", "light", "mass", "matter",
    "melting", "momentum", "neutron", "oscillation", "pendulum", "phase", "photon", "plasma", "pressure", "proton",
    "reactor", "resonance", "rotation", "scalar", "solid", "sound", "spectrometer", "spectrum", "stress", "strain",
    "superconductor", "temperature", "thermometer", "torsion", "vacuum", "vibration", "arithmetic", "calculation",
    "coordinates", "cube", "dimension", "inequality", "integral", "inverse", "logarithm", "matrix", "median", "mode",
    "parameter", "perimeter", "polygon", "quadratic", "radius", "range", "rectangle", "regression", "slope", "symmetry",
    "tangent", "theorem", "trigonometry", "variable", "amplification", "antenna", "bit", "byte", "circuit", "computer",
    "digital", "electronics", "encryption", "hardware", "input", "interface", "microprocessor", "network", "output",
    "processing", "program", "protocol", "semiconductor", "signal", "storage", "transistor", "waveform", "automation",
    "benchmark", "boolean", "bytecode", "cache", "cipher", "compiler", "cryptography", "cybersecurity", "database",
    "debugging", "firewall", "firmware", "function", "heuristic", "iteration", "kernel", "loop", "middleware", "module",
    "multithreading", "packet", "parallel", "pixel", "process", "queue", "recursion", "scalability", "scripting", "syntax",
    "token", "virtual", "voxel", "web", "wireless", "wizard", "xenon", "yaml", "zephyr", "adrenaline", "aerobic", "amino",
    "anabolic", "antibody", "antigen", "aorta", "artery", "beta", "biopsy", "capillary", "cardiac", "cartilage", "collagen",
    "cytoplasm", "dendrite", "dermis", "digestion", "epidermis", "erythrocyte", "excretion", "fermentation", "fibrin",
    "fibrosis", "glucose", "hemoglobin", "hormone", "immunity", "incubation", "infection", "insulin", "interferon",
    "leukocyte", "ligament", "liver", "lymph", "membrane", "metabolism", "mitosis", "muscle", "myelin", "nervous", "neuron",
    "organ", "osteocyte", "pancreas", "pathogen", "peptide", "phagocyte", "plasma", "platelet", "receptor", "ribosome",
    "saliva", "serum", "skeleton", "tendon", "thrombosis", "vitamin", "xylem", "zygote", "alloy", "anion", "aqueous",
    "dissolution", "electrolysis", "element", "freezing", "neutralization", "oxidation", "suspension", "vapour",
    "frequency", "resistance", "light", "charge"
]

def choose_word(word_bank):
    return random.choice(word_bank)

def display_word(word, guessed_letters):
    display = ""
    for letter in word:
        if letter in guessed_letters:
            display += letter
        else:
            display += "_"
    return display

def play_game():
    word = choose_word(word_bank)
    guessed_letters = []
    incorrect_guesses = 0
    max_incorrect_guesses = 6
    
    print("Welcome to Hangman!")
    print("Try to guess the word.")
    
    while incorrect_guesses < max_incorrect_guesses:
        display = display_word(word, guessed_letters)
        print(f"Word: {display}")
        
        if "_" not in display:
            print("Congratulations! You've guessed the word!")
            break
        
        guess = input("Enter a letter: ").lower()
        
        if guess in guessed_letters:
            print("You already guessed that letter. Try again.")
        elif guess in word:
            guessed_letters.append(guess)
            print("Correct!")
        else:
            guessed_letters.append(guess)
            incorrect_guesses += 1
            print(f"Incorrect! You have {max_incorrect_guesses - incorrect_guesses} guesses left.")
        
        print("Guessed letters: ", " ".join(guessed_letters))
    
    if incorrect_guesses == max_incorrect_guesses:
        print(f"Sorry, you've run out of guesses. The word was '{word}'.")
    
    play_again = input("Would you like to play again? (yes/no): ").lower()
    if play_again == "yes":
        play_game()
    else:
        print("Thanks for playing! Goodbye.")

if __name__ == "__main__":
    play_game()
