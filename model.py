import random
import json

STEVILO_DOVOLJENIH_NAPAK = 10

PRAVILNA_CRKA = "+"
PONOVLJENA_CRKA = "o"
NAPACNA_CRKA = "-"

ZMAGA = "W"
PORAZ = "X"
ZACETEK = "A"
DATOTEKA_S_STANJEM = "podatki.json"

class Vislice:
    """
    Krovni objekt, ki upravlja z vsemi igrami
    """
    def __init__(self, zacetne_igre, datoteka_s_stanjem=DATOTEKA_S_STANJEM):
        self.igre = zacetne_igre
        self.datoteka_s_stanjem = datoteka_s_stanjem
    
    def prost_id_igre(self):
        if not self.igre:
            return 1
        else:
            return max(self.igre.keys()) + 1
    
    def nova_igra(self):
        nov_id = self.prost_id_igre()
        sveza = nova_igra()
        self.igre[nov_id] = (sveza, ZACETEK)
        return nov_id
   
    def ugibaj(self, id_igre, crka):
        igra, stanje = self.igre[id_igre]
        novo_stanje = igra.ugibaj(crka)
        self.igre[id_igre] = (igra, novo_stanje)
    
    def dobi_json_slovar(self):
        slovar_iger = {}
        for (id_igre, (igra, stanje)) in self.igre.items():
            slovar_iger[id_igre] = [
                igra.dobi_json_slovar(), #Kličem serializacijo igre
                stanje,
            ]
        return {
            "igre": slovar_iger,
            "datoteka_s_stanjem": self.datoteka_s_stanjem,
        }
    
    @staticmethod
    def preberi_iz_datoteke(ime_datoteke="podatki.json"):
        with open(ime_datoteke, "r", encoding="utf-8") as in_file:
            slovar = json.load(in_file) # Slovar
        return Vislice.dobi_vislice_iz_slovarja(slovar)

    @staticmethod
    def dobi_vislice_iz_slovarja(slovar):
        slovar_iger = {} # To je slovar objektov "Igra"
        for id_igre, (igra_slovar, stanje) in slovar["igre"].items():
            slovar_iger[int(id_igre)] = (
                Igra.dobi_igro_iz_slovarja(igra_slovar),
                stanje
            )
        return Vislice(slovar_iger, slovar["datoteka_s_stanjem"])



    def zapisi_v_datoteko(self):
        # Naredi slovar
        slovar = self.dobi_json_slovar()
        # Zapiši ga v datoteko
        with open(self.datoteka_s_stanjem, "w", encoding="utf-8") as out_file:
            json.dump(slovar, out_file)
    
    
    
    






class Igra:
    
    def __init__(self, geslo, crke=None):
        self.geslo = geslo
        if crke is None:
            self.crke = []
        else:
            self.crke = crke
    
    def dobi_json_slovar(self):
        return {
            "geslo": self.geslo,
            "crke": self.crke,
        }
    
    @staticmethod
    def dobi_igro_iz_slovarja(slovar):
        return Igra(
            slovar["geslo"], slovar.get("crke",""),      #.get metoda vrne vrednost slovarja, ce obstaja tak kljuc, sicer pa 2. vrednost, ki jo podamo metodi .get

        )
    def napacne_crke(self):
        return [crka for crka in self.crke if crka not in self.geslo]

    def pravilne_crke(self):
        return [crka for crka in self.crke if crka in self.geslo]

    def stevilo_napak(self):
        return len(self.napacne_crke())

    def zmaga(self):
        return all(crka in self.crke for crka in self.geslo)

    def poraz(self):
        return self.stevilo_napak() > STEVILO_DOVOLJENIH_NAPAK

    def pravilni_del_gesla(self):
        s = ""
        for crka in self.geslo:
            if crka in self.crke:
                s += crka + " "
            else:
                s += "_ "
        return s

    def nepravilni_ugibi(self):
        return " ".join(self.napacne_crke())

    def ugibaj(self, crka):
        crka = crka.upper()
        if crka in self.crke:
            return PONOVLJENA_CRKA
        else:
            self.crke.append(crka)
            if crka in self.geslo:
                if self.zmaga():
                    return ZMAGA
                else:
                    return PRAVILNA_CRKA
            else:
                if self.poraz():
                    return PORAZ
                else:
                    return NAPACNA_CRKA

with open("besede.txt", encoding="utf-8") as f:
    bazen_besed = [vrstica.strip().upper() for vrstica in f] #.strip() zbriše znake, ki nimajo graficne podobe(presledek, \n,...)

def nova_igra():
    return Igra(random.choice(bazen_besed))