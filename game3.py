import sys
import tkinter as tk
from PIL import Image, ImageTk, ImageOps
import random
import threading
import time             
import subprocess

# Récupération des arguments
pseudo1 = sys.argv[1] if len(sys.argv) > 1 else "Joueur 1"
pseudo2 = sys.argv[2] if len(sys.argv) > 2 else "Joueur 2"
image_perso1 = sys.argv[3] if len(sys.argv) > 3 else "assets/blue.png"
image_perso2 = sys.argv[4] if len(sys.argv) > 4 else "assets/red.png"
image_arme1 = sys.argv[5] if len(sys.argv) > 5 else "assets/pistolet.png"
image_arme2 = sys.argv[6] if len(sys.argv) > 6 else "assets/revolver.png"

class Joueur:
    def __init__(self, canvas, x, y, couleur, image_path, arme_path, pseudo):
        self.canvas = canvas
        self.vie = 100
        self.score = 0
        self.manches = 0
        self.direction = 1
        self.en_air = True
        self.peut_tirer = True
        self.image = ImageTk.PhotoImage(Image.open(image_path).resize((40, 40)))
        self.arme_image_base = Image.open(arme_path).resize((20, 20))
        self.arme_image_gauche = ImageTk.PhotoImage(self.arme_image_base)
        self.arme_image_droite = ImageTk.PhotoImage(ImageOps.mirror(self.arme_image_base))
        self.objet = self.canvas.create_image(x, y, image=self.image, anchor="nw")
        self.arme = self.canvas.create_image(x + 40, y + 10, image=self.arme_image_droite, anchor="nw")
        self.barre_vie = self.canvas.create_rectangle(x, y - 10, x + 40, y - 5, fill="green")
        self.text = self.canvas.create_text(x + 20, y - 20, text=pseudo, fill="#00ffe1", font=("Arial", 12))
        self.dx = 0
        self.dy = 0
        self.traverser = False
        self.traverser_timer = 0
        self.pseudo = pseudo
        self.image_path = image_path
        self.arme_path = arme_path

    def deplacer(self):
        self.canvas.move(self.objet, self.dx, self.dy)
        x, y = self.canvas.coords(self.objet)
        self.canvas.coords(self.barre_vie, x, y - 10, x + self.vie * 0.4, y - 5)
        self.canvas.coords(self.text, x + 20, y - 20)
        if self.direction == 1:
            self.canvas.itemconfig(self.arme, image=self.arme_image_droite)
            self.canvas.coords(self.arme, x + 40, y + 10)
        else:
            self.canvas.itemconfig(self.arme, image=self.arme_image_gauche)
            self.canvas.coords(self.arme, x - 20, y + 10)

    def tirer(self, adversaire):
        if not self.peut_tirer:
            return
        x, y = self.canvas.coords(self.objet)
        start_x = x + 40 if self.direction == 1 else x   
        balle = self.canvas.create_oval(start_x, y + 20, start_x + 10, y + 30, fill="red")
        direction_tir = self.direction

        def deplacer_balle():
            for _ in range(40):
                self.canvas.move(balle, 10 * direction_tir, 0)
                self.canvas.update()
                time.sleep(0.01)
                bx1, by1, bx2, by2 = self.canvas.coords(balle)
                ax, ay = self.canvas.coords(adversaire.objet)
                if bx2 > ax and bx1 < ax + 40 and by2 > ay and by1 < ay + 40:
                    adversaire.vie -= 25
                    self.canvas.delete(balle)
                    return
            self.canvas.delete(balle)

        threading.Thread(target=deplacer_balle).start()
        self.peut_tirer = False
        self.canvas.after(500, lambda: setattr(self, 'peut_tirer', True))


    def respawn(self):
        x, y = random.randint(100, 700), 50
        self.canvas.coords(self.objet, x, y)
        self.canvas.coords(self.arme, x + 40, y + 10)
        self.canvas.coords(self.barre_vie, x, y - 10, x + 40, y - 5)
        self.canvas.coords(self.text, x + 20, y - 20)
        self.vie = 100

class Jeu:
    def __init__(self, root):
        self.root = root    
        self.frame = tk.Frame(root)
        self.frame.pack()

        self.canvas = tk.Canvas(self.frame, width=1920, height=1080, bg="#0d0d1a")
        self.canvas.pack()

        self.platforms = []
        self.creer_plateformes()
        self.joueur1 = Joueur(self.canvas, 100, 100, "blue", image_perso1, image_arme1, pseudo1)
        self.joueur2 = Joueur(self.canvas, 600, 100, "red", image_perso2, image_arme2, pseudo2)
        self.label_score = self.canvas.create_text(400, 30, text="", font=("Arial", 16), fill="#00ffe1")

        self.bouton_retour = None
        self.bouton_rejouer = None
        self.partie_en_cours = True

        self.root.bind("<KeyPress>", self.touche_appuyee)
        self.root.bind("<KeyRelease>", self.touche_relachee)
        self.gravity()
        self.update()

    def creer_plateformes(self, largeur_ecran=1920, hauteur_ecran=1080, nb_plateformes=12):
        self.platforms.clear()
        hauteur_plateforme = 15
        espacement_vertical = hauteur_ecran // (nb_plateformes + 2)
        marge_gauche = 50
        marge_droite = 300
    
        for i in range(nb_plateformes):
            largeur_plateforme = random.randint(150, 300)
            x1 = random.randint(marge_gauche, largeur_ecran - largeur_plateforme - marge_droite)
            x2 = x1 + largeur_plateforme
            y = hauteur_ecran - (i + 2) * espacement_vertical  # on commence vers le bas et on remonte
    
            plat = self.canvas.create_rectangle(
                x1, y, x2, y + hauteur_plateforme,
                fill="#6610f2", outline="#00ffe1"
            )
            self.platforms.append(plat)
    def gravity(self):
        for joueur in [self.joueur1, self.joueur2]:
            if joueur.en_air:
                joueur.dy += 0.8
            else:
                joueur.dy = 0
        self.root.after(30, self.gravity)

    def touche_appuyee(self, event):
        touche = event.keysym
        if touche == "q":
            self.joueur1.dx = -8
            self.joueur1.direction = -1
        elif touche == "d":
            self.joueur1.dx = 8
            self.joueur1.direction = 1
        elif touche == "z" and not self.joueur1.en_air:
            self.joueur1.dy = -25
            self.joueur1.en_air = True
        elif touche == "s":
            self.joueur1.traverser = True
            self.joueur1.traverser_timer = 7
        elif touche == "e":
            self.joueur1.tirer(self.joueur2)

        if touche == "Left":
            self.joueur2.dx = -8
            self.joueur2.direction = -1
        elif touche == "Right":
            self.joueur2.dx = 8
            self.joueur2.direction = 1
        elif touche == "Up" and not self.joueur2.en_air:
            self.joueur2.dy = -25
            self.joueur2.en_air = True
        elif touche == "Down":
            self.joueur2.traverser = True
            self.joueur2.traverser_timer = 7
        elif touche == "Return":
            self.joueur2.tirer(self.joueur1)

    def touche_relachee(self, event):
        touche = event.keysym
        if touche in ["q", "d"]:
            self.joueur1.dx = 0
        if touche in ["Left", "Right"]:
            self.joueur2.dx = 0

    def update(self):
        if self.partie_en_cours:
            for joueur in [self.joueur1, self.joueur2]:
                joueur.deplacer()
                self.verifier_collision(joueur)
                self.verifier_chute(joueur)
                if joueur.traverser:
                    joueur.traverser_timer -= 1
                    if joueur.traverser_timer <= 0:
                        joueur.traverser = False
            self.verifier_mort()
            self.canvas.itemconfig(self.label_score,
                text=f"{self.joueur1.pseudo} : {self.joueur1.manches}  |  {self.joueur2.pseudo} : {self.joueur2.manches}")
        self.root.after(30, self.update)

    def verifier_collision(self, joueur):
        joueur.en_air = True
        x, y = self.canvas.coords(joueur.objet)
        for p in self.platforms:
            px1, py1, px2, py2 = self.canvas.coords(p)
            if px1 < x + 40 < px2 and py1 <= y + 40 <= py2 and joueur.dy >= 0 and not joueur.traverser:
                self.canvas.move(joueur.objet, 0, py1 - (y + 40))
                joueur.en_air = False

   
    def verifier_chute(self, joueur):
    
        _, y = self.canvas.coords(joueur.objet)
    
        if y > 1080:
    
            # L'autre joueur gagne une manche
    
            autre = self.joueur1 if joueur == self.joueur2 else self.joueur2
    
            autre.manches += 1
    
            joueur.respawn()
    
            joueur.vie = 100



    def verifier_mort(self):
        for joueur, autre in [(self.joueur1, self.joueur2), (self.joueur2, self.joueur1)]:
            if joueur.vie <= 0:
                autre.manches += 1
                joueur.respawn()
                joueur.vie = 100 

        if self.joueur1.manches == 6 or self.joueur2.manches == 6:
            gagnant = self.joueur1.pseudo if self.joueur1.manches == 6 else self.joueur2.pseudo
            self.canvas.create_text(950, 350, text=f"{gagnant} a gagné !", font=("Arial", 28), fill="green")
            self.partie_en_cours = False
        
            # Écriture du score complet dans scores.txt
            try:
                with open("scores.txt", "a", encoding="utf-8") as fichier:
                    fichier.write(f"{self.joueur1.pseudo}: {self.joueur1.manches} | {self.joueur2.pseudo}: {self.joueur2.manches} => Vainqueur: {gagnant}\n")
            except Exception as e:
                print(f"Erreur lors de l'écriture du score : {e}")
        
            self.ajouter_boutons_fin()

    def ajouter_boutons_fin(self):
        if not self.bouton_retour:
            self.bouton_retour = tk.Button(self.canvas, text="Retour au menu", command=self.retour_menu)
            self.bouton_retour.place(relx=0.5, rely=0.8, anchor="center")
        if not self.bouton_rejouer:
            self.bouton_rejouer = tk.Button(self.canvas, text="Rejouer", command=self.rejouer)
            self.bouton_rejouer.place(relx=0.5, rely=0.9, anchor="center")

    def retour_menu(self):
        self.root.destroy()
        subprocess.Popen(["python", "main.py"])

    def rejouer(self):
        self.root.destroy()
        subprocess.Popen(["python", "game3.py", pseudo1, pseudo2, image_perso1, image_perso2, image_arme1, image_arme2])

root = tk.Tk()
root.title("Cyberpunk Fight")
jeu = Jeu(root)
root.mainloop()

