#STEFANOS PANAGIOTIS GIANNAKOS 3568
#You need to run the main-3568.py file to see the output of this code.

import random
import itertools
import json
import time

# Το dictionary users_scores χρησιμοποιείται για την αποθήκευση του σκορ κάθε παίκτη/ χρήστη
# Μεταφορτώνει τα σκορ από το αρχείο userscores.json εάν υπάρχε
users_scores = {}
with open("userscores.json","r") as loadfile:
    users_scores = json.load(loadfile)

# Η κλάση SakClass αναπαριστά το σακουλάκι με τα γράμματα του παιχνιδιού Scrabble
class SakClass:
    # Το LETTER_DISTR είναι ένα dictionary που περιέχει τον αριθμό των γραμμάτων
    # και τους πόντους τους για κάθε γράμμα της ελληνικής αλφαβήτας. Περισσότερα στο guidelines
    #(Οι πληροφορίες του dicitonary είναι από το wikipedia)
    LETTER_DISTR = {
        'Α': [12, 1], 'Β': [1, 8], 'Γ': [2, 4], 'Δ': [2, 4], 'Ε': [8, 1],
        'Ζ': [1, 10], 'Η': [7, 1], 'Θ': [1, 10], 'Ι': [8, 1], 'Κ': [4, 2],
        'Λ': [3, 3], 'Μ': [3, 3], 'Ν': [6, 1], 'Ξ': [1, 10], 'Ο': [9, 1],
        'Π': [4, 2], 'Ρ': [5, 2], 'Σ': [7, 1], 'Τ': [8, 1], 'Υ': [4, 2],
        'Φ': [1, 8], 'Χ': [1, 8], 'Ψ': [1, 10], 'Ω': [3, 3]
    }

    def __init__(self):
        self.sak = []  # Τα γράμματα στο σακουλάκι
        self.NumLetters = 104  # Ο συνολικός αριθμός των γραμμάτων
        self.generate_sak()  # Δημιουργεί το σακουλάκι με γράμματα

    def randomize_sak(self):
        # Ανακατεύει τα γράμματα στο σακουλάκι
        random.shuffle(self.sak)

    def generate_sak(self):
        # Δημιουργεί το σακουλάκι με γράμματα βάσει του LETTER_DISTR
        for letter, values in self.LETTER_DISTR.items():
            self.sak.extend([letter] * values[0])
        self.randomize_sak()

    def putbackletters(self, player_letters):
        # Επιστρέφει γράμματα στο σακουλάκι
        self.NumLetters += len(player_letters)
        self.generate_sak()

    def getletters(self, NumLetters):
        # Επιστρέφει γράμματα για τον παίκτη
        if self.NumLetters < NumLetters:
            NumLetters = self.NumLetters
        letters = [self.sak.pop() for _ in range(NumLetters)]
        self.NumLetters -= NumLetters
        return letters

# Η κλάση Player αναπαριστά έναν παίκτη του παιχνιδιού Scrabble
class Player:
    def __init__(self, name, score):
        self.name = name  # Το όνομα του παίκτη
        self.score = score  # Οι πόντοι του παίκτη
        self.letters = []  # Τα γράμματα που κρατάει ο παίκτης

    def measure_time(func):
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs) #τα ορίσματα για τη func είναι τα args και τα kwargs
            end_time = time.perf_counter()
            print(f"Ο χρόνος εκτέλεσης της μεθόδου {func.__name__}: {end_time - start_time} δευτερόλεπτα")
            return result
        return wrapper

    @measure_time
    def play_word(self, word, sak):
        # Ο παίκτης παίζει μια λέξη, υπολογίζει τους πόντους και ενημερώνει τα γράμματά του
        self.score += Game.game_score(word)
        for letter in word:
            self.letters.remove(letter)
        available_letters = sak.getletters(len(word))
        self.letters.extend(available_letters)

# Η κλάση Computer αποτελεί έναν παίκτη υπολογιστή
class Computer(Player):
    def __init__(self):
        super().__init__("H/Y", 0)  # Το όνομα του υπολογιστή και οι πόντοι του

    def play_word(self, word, sak):
        # Ο υπολογιστής παίζει μια λέξη και εμφανίζει το αποτέλεσμα
        print("Παίκτης: Computer \nΓράμματα", self.letters)
        super().play_word(word, sak)
        print("\nΛΕΞΗ:", word, "\nΠόντοι λέξης:", Game.game_score(word), "\nΣκορ H/Y: ", self.score, "\n")

    def play(self, dictionary):
        return self.SMART_FAIL(dictionary)

    #Υλοποίηση της μεθόδου SMART_FAIL
    def SMART_FAIL(self, dictionary):
        valid_words = []
        # Εδώ ελέγχουμε όλες τις δυνατές λέξεις από τα γράμματα του υπολογιστή.
        # Αν η λέξη είναι έγκυρη και υπάρχει στο λεξικό, την προσθέτουμε στη λίστα των δυνατών λέξεων
        for length in range(8, 2, -1):
            for word in itertools.permutations(self.letters, length):
                word_str = ''.join(word)
                if word_str in dictionary:
                    valid_words.append(word_str)
        # Επιστρέφουμε μία τυχαία έγκυρη λέξη από τη λίστα δυνατών λέξεων. Υλοποίθηκε έτσι για να μην είναι πάντα προβλέψιμος ο υπολογιστής...
        # Δεν υπάρχει κίνδυνος να επναληφθεί η ίδια λέξη, γιατί οι πιθανές λέξεις είναι πολλές και διαφορετικές σε κάθε περίπτωση
        # Αν δεν υπάρχει καμία έγκυρη λέξη, επιστρέφουμε "e" ως ένδειξη ότι ο υπολογιστής δεν μπορεί να παίξει
        return random.choice(valid_words) if valid_words else "e"

# Η κλάση Human αναπαριστά έναν ανθρώπινο παίκτη
class Human(Player):
    def __init__(self, name, score):
        super().__init__(name, score)

    def play_word(self, dictionary, word, sak):
        super().play_word(word, sak)

    def play(self, dictionary, sak):
        # Ο παίκτης εισάγει τη λέξη που θέλει να παίξει
        print("Παίκτης:", self.name, "\nΓράμματα", self.letters, "\nΤο Σκορ σου: ", self.score, "\n")
        while True:
            print("\nΔώσε μία λέξη ή 'p' για να περάσει η σειρά σου. (Αν θέλεις να τερματίσεις το παιχνίδι πάτα 'q')")
            word = input("ΛΕΞΗ: ")
            if word == "q": # Πίσω στο μενού
                print("\nΤο παιχνίδι διακόπηκε από τον χρήστη...\n")
                return "q"
            elif word == "p":
                return "p"
            elif word in dictionary:
                if all(letter in self.letters for letter in word):
                    super().play_word(word, sak)
                    print("\nΠόντοι λέξης: ", Game.game_score(word), "\nσκορ: ", self.score)
                    return word
                else:
                    print("Δεν έχεις αυτά τα γράμματα...")
            else:
                print("Δεν υπάρχει αυτή η λέξη στο λεξικό...")

# Η κλάση Game χειρίζεται την ροή του παιχνιδιού
class Game:
    @staticmethod
    def game_score(word):
        # Υπολογίζει τους πόντους μιας λέξης
        score = 0
        for letter in word:
            score += SakClass.LETTER_DISTR.get(letter, [0, 1])[1]
        return score

    def __init__(self, name):
        # Αρχικοποιεί το παιχνίδι
        self.user = Human(name, 0)
        self.pc = Computer()
        self.sack = SakClass()
        self.sack.generate_sak()
        self.dict = {}

    def setup(self):
        # Φορτώνει το λεξικό από ένα αρχείο και υπολογίζει τους πόντους κάθε λέξης
        with open("greek7.txt", "r", encoding='utf-8') as dict_file:
            for line in dict_file:
                word = line.strip()
                score = self.game_score(word)
                self.dict[word] = score

    def run(self):
        # Ξεκινάει το παιχνίδι
        self.user.letters = self.sack.getletters(7)
        self.pc.letters = self.sack.getletters(7)
        while True:
            print("************************************")
            computer_word = self.pc.play(self.dict)
            if computer_word == "e":
                if self.sack.NumLetters >= 7:
                    self.pc.letters = self.sack.getletters(7)
                else:
                    self.end()
                    return
            else:
                self.pc.play_word(computer_word, self.sack)
                if len(computer_word) > self.sack.NumLetters:
                    self.end()
                    return
            print("Υπολειπόμενα γράμματα", self.sack.NumLetters)
            print("************************************")

            word = self.user.play(self.dict, self.sack)
            if word in ("e", "q"):
                break
            if word == "p":
                if self.sack.NumLetters < 7:
                    self.end()
                    return
                self.sack.putbackletters(self.user.letters)
                self.user.letters = self.sack.getletters(7)
            print("Υπολειπόμενα γράμματα", self.sack.NumLetters)
            if self.sack.NumLetters < len(word):
                self.end()
                return

        if word == "q":
            return "q"

    def end(self):
        # Ολοκληρώνει το παιχνίδι και εμφανίζει το τελικό σκορ
        print("\n************************************")
        print("ΤΕΛΟΣ ΠΑΙΧΝΙΔΙΟΥ")
        print("************************************\n")

        final_score = self.user.score
        print("ΣΚΟΡ ΠΑΙΧΝΙΔΙΟΥ:")
        print("H/Y: ", self.pc.score)
        print(self.user.name,": ", self.user.score)
        if self.user.score > self.pc.score:
            print("\nΜπράβο είσαι ο μεγάλος ΝΙΚΗΤΗΣ!!!\n")
        elif self.user.score < self.pc.score:
            print("\nΟ υπολογιστής νίκησε... \n")
        else:
            print("\nIt's a Draw\n")

        try:
            if users_scores[self.user.name] < final_score:
                users_scores[self.user.name] = final_score
        except KeyError:
            users_scores[self.user.name] = final_score

        with open("userscores.json", "w") as save:
            json.dump(users_scores, save)

        return

    def replay(self):
        # Ξεκινάει ένα νέο παιχνίδι
        self.sack.generate_sak()
        self.user.score = 0
        self.pc.score = 0
        self.user.name = ""
