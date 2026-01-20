import customtkinter as tk
from PIL import Image
from tkinter import messagebox
import subprocess
import sys
import os

tk.set_appearance_mode("light")

class SmashGunApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smash Gun Duo")
        self.width = 1920
        self.height = 1080 
        self.root.geometry(f"{self.width}x{self.height}")

        self.ready1 = False
        self.ready2 = False

        self.color_var1 = tk.StringVar(value="blue")
        self.color_var2 = tk.StringVar(value="blue")
        self.weapon_var1 = tk.StringVar(value="./assets/pistolet.png")
        self.weapon_var2 = tk.StringVar(value="./assets/pistolet.png")

        self.pseudo1 = "Joueur 1"
        self.pseudo2 = "Joueur 2"

        self.selected_map_script = "game.py"

        self.init_images()
        self.init_frames()
        self.show_frame(self.frame_intro)

    def init_images(self):
        self.bg_image = tk.CTkImage(Image.open('./assets/bg.jpg'), size=(self.width, self.height))
        self.bg_image_choix = tk.CTkImage(Image.open('./assets/violet.jpg'), size=(self.width, self.height))
        self.fleche_d = tk.CTkImage(Image.open('./assets/fleche_d.png'), size=(50, 50))
        self.fleche_g = tk.CTkImage(Image.open('./assets/fleche_g.png'), size=(50, 50))
        self.home_img = tk.CTkImage(Image.open('./assets/home-page-icon.png'), size=(60, 60))
        self.images_persos = {
            "green": tk.CTkImage(Image.open('./assets/green.png'), size=(200, 200)),
            "blue": tk.CTkImage(Image.open('./assets/blue.png'), size=(200, 200)),
            "red": tk.CTkImage(Image.open('./assets/red.png'), size=(200, 200)),
            "yellow": tk.CTkImage(Image.open('./assets/yellow.png'), size=(200, 200)),
        }
        self.gun1_img = tk.CTkImage(Image.open('./assets/pistolet.png'), size=(80, 80))
        self.gun2_img = tk.CTkImage(Image.open('./assets/revolver.png'), size=(80, 80))
        self.map_1 = tk.CTkImage(Image.open('./assets/map-1.png'), size=(400, 300))
        self.map_2 = tk.CTkImage(Image.open('./assets/map-2.png'), size=(400, 300))
        self.map_3 = tk.CTkImage(Image.open('./assets/map-3.png'), size=(400, 300))

    def show_frame(self, frame):
        frame.pack(fill='both', expand=True)
        for child in self.root.winfo_children():
            if child != frame:
                child.pack_forget()

    def init_frames(self):
        self.init_frame_intro()
        self.init_frame_personnage()
        self.init_frame_map()

    def init_frame_intro(self):
        self.frame_intro = tk.CTkFrame(self.root, width=self.width, height=self.height, fg_color= "white")
        image_label = tk.CTkLabel(self.frame_intro, image=self.bg_image,text="", font=("courier", 50))
        image_label.pack()
        titre = tk.CTkLabel(self.frame_intro, text="Smash Gun Duo", font=("courier", 50), text_color="black", fg_color="transparent", bg_color="transparent")
        titre.place(relx=0.5, rely=0.3, anchor="center")
        btn1 = tk.CTkButton(self.frame_intro, text="Lancer jeu", command=lambda: self.show_frame(self.frame_personnage),
                            fg_color="white", border_color="black", border_width=3.5, text_color="black", hover_color="lightgrey")
        btn1.place(relx=0.5, rely=0.6, anchor="center")
        btn2 = tk.CTkButton(self.frame_intro, text="Afficher stats",border_color="black", border_width=3.5, command=self.afficher_scores)
        btn2.place(relx=0.5, rely=0.7, anchor="center"),
        btn3 = tk.CTkButton(self.frame_intro, text="Réinitialiser les scores",border_color="black", border_width=3.5, command=self.reinitialiser_scores)
        btn3.place(relx=0.5, rely=0.78, anchor="center")

    def afficher_scores(self):
        try:
            if not os.path.exists("scores.txt"):
                messagebox.showinfo("Scores", "Aucun score enregistré.")
                return
    
            with open("scores.txt", "r") as f:
                lignes = f.readlines()
    
            if not lignes:
                messagebox.showinfo("Scores", "Aucun score enregistré.")
                return
    
            historique = "Historique des parties :\n\n"
            classement = {}
    
            for ligne in lignes:
                ligne = ligne.strip()
                if not ligne:
                    continue
                historique += ligne + "\n"
                # Extraction du gagnant
                if "Gagnant:" in ligne:
                    parts = ligne.split("Gagnant:")
                    gagnant = parts[1].strip()
                    classement[gagnant] = classement.get(gagnant, 0) + 1
    
            historique += "\n\nClassement (victoires) :\n"
            for joueur, score in sorted(classement.items(), key=lambda x: -x[1]):
                historique += f"{joueur} : {score} victoires\n"
    
            # Créer une nouvelle fenêtre
            top = tk.CTkToplevel(self.root)
            top.title("Statistiques des parties")
            top.geometry("600x500")
            top.lift()
            top.focus_force()
    
            text_widget = tk.CTkTextbox(top, width=580, height=450)
            text_widget.pack(padx=10, pady=10)
            text_widget.insert("0.0", historique)
            text_widget.configure(state="disabled")
    
            btn_fermer = tk.CTkButton(top, text="Fermer", command=top.destroy)
            btn_fermer.pack(pady=5)
    
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lecture des scores : {e}")
           
    def reinitialiser_scores(self):
        if messagebox.askyesno("Confirmation", "Voulez-vous supprimer tous les scores ?"):
            try:
                if os.path.exists("scores.txt"):
                    os.remove("scores.txt")
                messagebox.showinfo("Succès", "Scores réinitialisés.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur suppression scores : {e}")

    def select_color(self, joueur, color):
        if joueur == 1:
            if color == self.color_var2.get():
                messagebox.showerror("Erreur", "Couleur déjà prise par Joueur 2 !")
                return
            self.color_var1.set(color)
            self.label_image_debut1.configure(image=self.images_persos[color])
        else:
            if color == self.color_var1.get():
                messagebox.showerror("Erreur", "Couleur déjà prise par Joueur 1 !")
                return
            self.color_var2.set(color)
            self.label_image_debut2.configure(image=self.images_persos[color])

    def check_ready(self):
        if self.ready1 and self.ready2:
            self.pseudo1 = self.entry_pseudo1.get().strip() or "Joueur 1"
            self.pseudo2 = self.entry_pseudo2.get().strip() or "Joueur 2"
            self.show_frame(self.frame_map)

    def joueur_ready(self, joueur):
        if joueur == 1:
            self.ready1 = True
        else:
            self.ready2 = True
        self.check_ready()

    def init_frame_personnage(self):
        self.frame_personnage = tk.CTkFrame(self.root, width=self.width, height=self.height)
        image_label11 = tk.CTkLabel(self.frame_personnage, image=self.bg_image_choix,text="")
        image_label11.pack()
        titre = tk.CTkLabel(self.frame_personnage, text="Choix du personnage et de l'arme", font=("Arial", 50))
        titre.place(relx=0.5, rely=0.05, anchor="center")
        couleurs = ["green", "blue", "red", "yellow"]

        self.label_image_debut1 = tk.CTkLabel(self.frame_personnage, image=self.images_persos["red"], text="", fg_color="transparent")
        self.label_image_debut1.place(relx=0.25, rely=0.35, anchor="center")
        self.label_gun_debut1 = tk.CTkLabel(self.frame_personnage, image=self.gun1_img, text="", fg_color="transparent")
        self.label_gun_debut1.place(relx=0.25, rely=0.6, anchor="center")
        self.entry_pseudo1 = tk.CTkEntry(self.frame_personnage, placeholder_text="Pseudo joueur 1", width=300)
        self.entry_pseudo1.place(relx=0.25, rely=0.75, anchor="center")
        for i, color in enumerate(couleurs):
            tk.CTkButton(self.frame_personnage, text='', fg_color=color, width=40, height=40,
                         command=lambda c=color: self.select_color(1, c)).place(relx=0.1 + i * 0.07, rely=0.85, anchor="center")
        tk.CTkButton(self.frame_personnage, image=self.fleche_g, text="", fg_color="transparent",
                     command=lambda: self.set_weapon(1, "./assets/pistolet.png")).place(relx=0.15, rely=0.65, anchor="center")
        tk.CTkButton(self.frame_personnage, image=self.fleche_d, text="", fg_color="transparent",
                     command=lambda: self.set_weapon(1, "./assets/revolver.png")).place(relx=0.35, rely=0.65, anchor="center")
        tk.CTkButton(self.frame_personnage, text='Prêt', fg_color="red", command=lambda: self.joueur_ready(1)).place(relx=0.25, rely=0.95, anchor="center")

        self.label_image_debut2 = tk.CTkLabel(self.frame_personnage, image=self.images_persos["blue"], text="", fg_color="transparent")
        self.label_image_debut2.place(relx=0.75, rely=0.35, anchor="center")
        self.label_gun_debut2 = tk.CTkLabel(self.frame_personnage, image=self.gun1_img, text="", fg_color="transparent")
        self.label_gun_debut2.place(relx=0.75, rely=0.6, anchor="center")
        self.entry_pseudo2 = tk.CTkEntry(self.frame_personnage, placeholder_text="Pseudo joueur 2", width=300)
        self.entry_pseudo2.place(relx=0.75, rely=0.75, anchor="center")
        for i, color in enumerate(couleurs):
            tk.CTkButton(self.frame_personnage, text='', fg_color=color, width=40, height=40,
                         command=lambda c=color: self.select_color(2, c)).place(relx=0.6 + i * 0.07, rely=0.85, anchor="center")
        tk.CTkButton(self.frame_personnage, image=self.fleche_g, text="", fg_color="transparent",
                     command=lambda: self.set_weapon(2, "./assets/pistolet.png")).place(relx=0.65, rely=0.65, anchor="center")
        tk.CTkButton(self.frame_personnage, image=self.fleche_d, text="", fg_color="transparent",
                     command=lambda: self.set_weapon(2, "./assets/revolver.png")).place(relx=0.85, rely=0.65, anchor="center")
        tk.CTkButton(self.frame_personnage, text='Prêt', fg_color="red", command=lambda: self.joueur_ready(2)).place(relx=0.75, rely=0.95, anchor="center")

    def set_weapon(self, joueur, weapon_file):
        if joueur == 1:
            self.weapon_var1.set(weapon_file)
            new_img = self.gun1_img if weapon_file == "./assets/pistolet.png" else self.gun2_img
            self.label_gun_debut1.configure(image=new_img)
        else:
            self.weapon_var2.set(weapon_file)
            new_img = self.gun1_img if weapon_file == "./assets/pistolet.png" else self.gun2_img
            self.label_gun_debut2.configure(image=new_img)

    def init_frame_map(self):
        self.frame_map = tk.CTkFrame(self.root, width=self.width, height=self.height)
        image_label12 = tk.CTkLabel(self.frame_map, image=self.bg_image_choix, text="", )
        image_label12.pack()
        tk.CTkButton(self.frame_map, image=self.map_1, text="", fg_color="transparent",
                     command=lambda: self.set_map_and_launch("game1.py")).place(relx=0.15, rely=0.4, anchor="center")
        tk.CTkButton(self.frame_map, image=self.map_3, text="", fg_color="transparent",
                     command=lambda: self.set_map_and_launch("game3.py")).place(relx=0.5, rely=0.4, anchor="center")
        tk.CTkButton(self.frame_map, image=self.map_2, text="", fg_color="transparent",
                     command=lambda: self.set_map_and_launch("game2.py")).place(relx=0.85, rely=0.4, anchor="center")
        tk.CTkButton(self.frame_map, text="Accueil", image=self.home_img, command=lambda: self.show_frame(self.frame_intro)).place(relx=0.5, rely=0.9, anchor="center")

    def set_map_and_launch(self, script_name):
        self.selected_map_script = script_name
        self.lancer_jeu()

    def lire_et_sauvegarder_gagnant(self):
        if os.path.exists("winner.txt"):
            try:
                with open("winner.txt", "r") as f:
                    gagnant = f.read().strip()
                if gagnant:
                    with open("scores.txt", "a") as f:
                        f.write(f"Gagnant : {gagnant}\n")
                os.remove("winner.txt")
                self.afficher_fin_partie(gagnant)
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de sauvegarder le score : {e}")

    def afficher_fin_partie(self, gagnant):
        self.frame_fin = tk.CTkFrame(self.root, width=self.width, height=self.height)
        texte = f"Victoire de {gagnant} !"
        label_victoire = tk.CTkLabel(self.frame_fin, text=texte, font=("Arial", 50))
        label_victoire.place(relx=0.5, rely=0.4, anchor="center")

        btn_retour = tk.CTkButton(self.frame_fin, text="Retour au menu principal",
                                  command=lambda: self.show_frame(self.frame_intro),
                                  font=("Arial", 20), fg_color="green")
        btn_retour.place(relx=0.5, rely=0.6, anchor="center")

        self.show_frame(self.frame_fin)

    def lancer_jeu(self):
        pseudo1 = self.entry_pseudo1.get().strip() or "Joueur 1"
        pseudo2 = self.entry_pseudo2.get().strip() or "Joueur 2"
        couleur1 = self.color_var1.get()
        couleur2 = self.color_var2.get()
        arme1 = self.weapon_var1.get()
        arme2 = self.weapon_var2.get()
        image_perso1 = f"./assets/{couleur1}.png"
        image_perso2 = f"./assets/{couleur2}.png"
        image_arme1 = arme1
        image_arme2 = arme2
        fichiers = [f"./{image_perso1}", f"./{image_perso2}", f"./{image_arme1}", f"./{image_arme2}"]
        manquants = [f for f in fichiers if not os.path.isfile(f)]
        if manquants:
            messagebox.showerror("Erreur", "Fichiers manquants :\n" + "\n".join(manquants))
            return
        try:
            subprocess.Popen([sys.executable, self.selected_map_script, pseudo1, pseudo2, image_perso1, image_perso2, image_arme1, image_arme2])
            # self.root.after(5000, self.lire_et_sauvegarder_gagnant)
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lancer le jeu : {e}")

if __name__ == "__main__":
    root = tk.CTk()
    app = SmashGunApp(root)
    root.mainloop()

