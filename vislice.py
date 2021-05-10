import bottle
import model

COOKIE_ID_IGRE = "ID_IGRE"
SECRET = "SECRET"


@bottle.get("/")
def index():
    return bottle.template("index.tpl")


@bottle.get("/igra/")
def nova_igra():
    vislice = model.Vislice.preberi_iz_datoteke()

    id_igre = vislice.nova_igra()
    novi_url = f"/igra/{id_igre}/"
    
    vislice.zapisi_v_datoteko()
    
    bottle.response.set_cookie(COOKIE_ID_IGRE, id_igre, path="/", secret=SECRET)
    
    bottle.redirect("/igraj/")

@bottle.get("/igraj/")
def igraj_igro():
    id_igre = int(bottle.request.get_cookie(COOKIE_ID_IGRE, secret=SECRET))
    
    vislice = model.Vislice.preberi_iz_datoteke()
    igra, stanje = vislice.igre[id_igre]
    
    vislice.zapisi_v_datoteko()
    return bottle.template("igra.tpl", igra=igra, stanje=stanje)
@bottle.post("/igraj/")
def ugibaj_crko_igraj():
    id_igre = int(bottle.request.get_cookie(COOKIE_ID_IGRE, secret=SECRET))
    vislice = model.Vislice.preberi_iz_datoteke()
    ugibana_crka = bottle.request.forms["ugibana_crka"]
    vislice.ugibaj(id_igre, ugibana_crka)
    vislice.zapisi_v_datoteko()
    return bottle.redirect(f"/igraj/")

@bottle.get("/igra/<id_igre:int>/")
def poglej_igro(id_igre):
    id_igre = int(bottle.request.get_cookie(COOKIE_ID_IGRE, secret=SECRET))
    vislice = model.Vislice.preberi_iz_datoteke()
    igra, stanje = vislice.igre[id_igre]
    vislice.zapisi_v_datoteko()
    return bottle.template("igra.tpl", igra=igra, stanje=stanje)

@bottle.post("/igra/<id_igre:int>/")
def ugibaj_crko(id_igre):
    vislice = model.Vislice.preberi_iz_datoteke()
    ugibana_crka = bottle.request.forms["ugibana_crka"]
    vislice.ugibaj(id_igre, ugibana_crka)
    vislice.zapisi_v_datoteko()
    return bottle.redirect(f"/igra/{id_igre}/")


#Poženemo celotno zadevo
bottle.run(reloader=True, debug=True)



print("To se ne sme izpisati")