import random
import datetime

class Player :
    keyboard_key = {'z':(-1,0),
                    'q':(0,-1),
                    's':(1,0),
                    'd':(0,1)}
    
    #methode
    def __init__(self, points = 0, start = (0,0)):
        self._name = ""
        self._points = points
        self._position = start
        self._life = 100
        self._symbol = 0
          
    def move (self,board_size) :
        move = Player.keyboard_key[Game.key.lower()]
        self._position = (self._position[0] + move[0], self._position[1] + move[1])
        
        if self._position == (-1,self._position[1]):
            self._position = (board_size -1, self._position[1])
        elif self._position == (self._position[0], -1 ):
            self._position = (self._position[0], board_size - 1)
        elif self._position == (board_size, self._position[1]):
            self._position = (0, self._position[1])
        elif self._position == (self._position[0],board_size):
            self._position = (self._position[0], 0)

        
    # getters et setters
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,new_name):
        self._name = new_name
    @property
    def points(self):
        return self._points
    @points.setter
    def points(self, new_points):
        self._points = new_points
    @property 
    def position(self):
        return self._position
    @position.setter
    def position(self, new_position):
        self._position = new_position
    @property
    def life(self):
        return self._life
    @life.setter
    def life(self,new_life):
        self._life = new_life
    @property
    def symbol(self):
        return self._symbol
    @symbol.setter
    def symbole(self, new_symbol):
        self._symbol = new_symbol




            
# Class mére de Candy et Trap
class Item:
    def __init__(self,symbol):
        self.symbol = symbol
        self.position = []

     # Fait apparaitre un item
    def pop_item(self,board_size):
        new_item = (random.choice(range(board_size)),random.choice(range(board_size)))
        if new_item not in self.position :
            self.position.append(new_item)
            
# Class fille de Items
class Candy(Item):
    def __init__(self, symbol, value):
        Item.__init__(self,symbol)
        self.value = value
        
    # Regarde s'il y a un bonbon à prendre (et le prend)
    def check_candy(self, player_position, player_points):
        if player_position in self.position:
            player_points += self.value
            self.position.remove(player_position)
        return player_points

# Class fille de Items
class Trap(Item):
    def __init__(self, symbol, dammage):
        Item.__init__(self,symbol)
        self.dammage = dammage
            

        # Regarde s'il y a un piége (et enleve des points de vie)
    def check_trap(self ,player_position, player_life):
        if player_position in self.position:
            player_life -= self.dammage
            self.position.remove(player_position)
        return player_life





class Game :
    # Utiliser pour demander au joueur de rentrer une touche
    key = ""
    def __init__(self, player, size=10):
        self._player = player
        self._board_size = size
        self._candies = []
        self._traps = []
        
        
    # getters et setters
    @property
    def player(self):
        return self._player
    @player.setter
    def player(self,new_player):
        self._player = new_player
    @property
    def board_size(self):
        return self._board_size
    @board_size.setter
    def board_size(self, new_board_size):
        new_board_size = self._board_size
    @property
    def candies(self):
        return self._candies
    @candies.setter
    def candies(self,new_candies):
        self._candies = new_candies

    # Dessine le plateau
    def draw(self):
        for line in range(self._board_size):
            for col in range(self._board_size):
                if (line,col) in self._candies[0].position:
                    print(self._candies[0].symbol, end=" ")
                elif (line,col) in self._candies[1].position:
                    print(self._candies[1].symbol, end=" ")
                elif (line,col) in self._candies[2].position:
                    print(self._candies[2].symbol, end=" ")
                elif (line,col) in self._traps[0].position:
                    print(self._traps[0].symbol, end=" ")
                elif (line,col) in self._traps[1].position:
                    print(self._traps[1].symbol, end=" ")
                elif (line,col) in self._traps[2].position:
                    print(self._traps[2].symbol, end=" ")
                    
                elif (line,col) == self.player._position :
                    print(self._player._symbol,end=" ")
                else : 
                    print(".",end=" ")
            print()

    
    # Choisir une option et la renvoie
    @classmethod
    def choice(cls):
        cls.key = input(" mouvement : Z,Q,S,D | pause : P | quitter : X => ")
        while cls.key.upper() not in "Z,Q,S,D,P,X" :
            cls.key = input(" mouvement : Z,Q,S,D | pause : P | quitter : X => ")
        return cls.key

    # Modifier les paramtres du joueur
    def settings(self):
        while len(self._player._name) not in range(1,10):
            self._player._name = input("Entrer votre nom : ")
        while self._player._symbol not in ["$", "%", "+", "ù", "€"]:
            self._player._symbol = input("Choisissez un de ces symboles => $ % + ù € : ")

    # Permet de modifier la difficulté de la partie
    def choose_difficulty(self):
        self._player._life = 500
        self._board_size = 500
        while self._player._life not in range(1,201):
            try: 
                self._player._life = int(input("Choisissez le nombre de vos points de vie : "))
                if self._player._life not in range(1,201):
                    print("Vous devez avoir un nombre de points entre 0 (non compris) et 200 (compris)")
            except ValueError:
                print("Vous devez entrer un nombre entier")
        while self._board_size not in range(10,16):
            try:
                self._board_size = int(input("Choisissez la taille du tableau : "))
                if self._board_size not in range(10,16):
                    print("La taille du tableau doit etre entre 10 (compris) et 15 (compris)")
            except ValueError:
                print("Vous devez entrer un nombre entier")

    # Sauvegarde l'historique des parties dans un fichier
    def history_game(self):
        with open("history.txt", "a") as scores :
            scores.write("\nPseudo : " + self._player._name + " | Points : "\
            + str(self._player._points)+" | Points de vie restant  : "+str(self._player._life) + "\nFait le " +str(datetime.datetime.today())+"\n")
        
    
    # Demande une confirmation et la renvoie
    @staticmethod
    def quit_confirm():
        confirmation = "a"
        while confirmation.upper() not in "O,N":
            confirmation = input("Etes-vous sûr de vouloir quitter (O/N) ?")
            if confirmation.upper() == 'N':
                print("----- La partie reprend -----")
        return confirmation
                

    # Affiche l'index et renvoie le temps de pause
    @classmethod
    def delta_pause(cls):
        start_pause = datetime.datetime.today()
        cls.index()
        resume = ''
        while resume.upper() != "R":
            resume = input("Appuyer sur R pour revenir au jeu : ")    
        print("----- La partie reprend -----")
        end_pause = datetime.datetime.today()
        delta_pause = end_pause - start_pause
        return delta_pause
    
    # retourne le moment où le jeu est censé être fini
    @staticmethod
    def end_time(delta_minute, delta_second):
        delta = datetime.timedelta(minutes=delta_minute, seconds=delta_second)
        end = datetime.datetime.today() + delta
        return end

    @staticmethod
    def index():
        print("--------------------INDEX--------------------")
        print("Pour vous deplacez utilisez les touches :")
        print(" Z ==> HAUT")
        print(" S ==> BAT")
        print(" Q ==> GAUCHE")
        print(" D ==> DROITE")
        print("---------------------------------------------")
        print("Les piéges sont representé par :")
        print(" # ==> BOMBE : les bombes font 50 de dégât")
        print(" O ==> TROU  : si vous tombez dans un trou vous mourez direct")
        print(" * ==> MUR   : si vous rentrer dans un mur vous perdez 40 points de vie")
        print("---------------------------------------------")
        print("Les bonbons sont representé par :")
        print(" S ==> Petit Bonbon : mangez le pour avoir 1 points")
        print(" M ==> Moyen Bonbon : mangez le pour avoir 2 points")
        print(" G ==> Gros Bonbon  : mangez le pour avoir 3 points")
        print("---------------------------------------------")
        print("Voici quelque option que vous pouvez utilisez :")
        print(" P ==>  Pause  : vous permez de revoir l'index")
        print(" X ==> Quitter : vous permez quitté le jeu")
        print("---------------------------------------------")

    # Mets en place la partie
    def setup_game(self):
        print("______ BIENVENUE SUR MON PREMIER JEU ______")
        print("Le but est de manger un max de bonbon pour")
        print("gagnez des points mais faites attention aux piéges !")
        Game.index()
        self.settings()
        self.choose_difficulty()
        input("Appuyez sur Enter quand vous serez prêt à commencer : ")
        print("Bon jeu", self._player._name)
        print("--- Début de la partie ---")
        
        # Joue une partie complète
    def play(self):
        self.setup_game()
        
        end = Game.end_time(1,0)
        now = datetime.datetime.today()
        
        while now < end :
            self.draw()
            print("---------------------------------------------------")
            Game.key = Game.choice()
            print("---------------------------------------------------")
            if Game.key.lower() in Player.keyboard_key:
                self.player.move(self._board_size)
                for i in range(0,3):
                    self._player._points = self._candies[i].check_candy(self._player._position, self._player._points) #check_candy
                for i in range(0,3):
                    self._player._life = self._traps[i].check_trap(self._player._position, self._player._life)        #check_trap
                    
                #vie <= 0 alors fin partie
                if self._player._life <= 0:
                    self._player._life = 0 
                    print("______Tu es mort _____")
                    end = now
                    
            #Faire pause
            elif Game.key.upper() == "P":
                delta_pause = Game.delta_pause()
                end += delta_pause
                
            #Quitter le jeu
            elif Game.key.upper() == "X":
                start_quit_time = datetime.datetime.today()
                confirmation = Game.quit_confirm()
                if confirmation.upper() == "O":
                    end = now
                elif confirmation.upper() == "N":
                    end_quit_time = datetime.datetime.today()
                    delta_quit = end_quit_time - start_quit_time
                    end += delta_quit
            
            if random.randint(1,5) == 1 :
                    self._candies[0].pop_item(self._board_size)
                    self._traps[0].pop_item(self._board_size)
            if random.randint(1,10) == 1 :
                    self._candies[1].pop_item(self._board_size)
                    self._traps[1].pop_item(self._board_size)
            if random.randint(1,15) == 1 :
                    self._candies[2].pop_item(self._board_size)
                    self._traps[2].pop_item(self._board_size)
        
                

            now = datetime.datetime.today()
        
        
        print("")
        print("Vous avez", self._player._points, "points" )
        print("Vous avez", self._player._life, "points de vie")
        print("A la prochaine",self._player._name)
        self.history_game()
        
if __name__ == "__main__" :
    p = Player()
    g = Game(p)
    
    small_candy = Candy("S", 1)
    medium_candy = Candy("M", 2)
    big_candy = Candy("B", 3)
    bomb = Trap("@", 50)
    hole = Trap("O", 100)
    wall = Trap("*", 40)
    g._candies = [small_candy,medium_candy,big_candy]
    g._traps = [bomb, hole, wall]
    g.play()
