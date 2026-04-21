from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from anthropic import Anthropic
import os, json
from datetime import datetime

app = FastAPI(title="GenesisBusiness AutoSite™", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
client = Anthropic()
sites_db = {}

class BusinessInfo(BaseModel):
    nom: str
    type_activite: str
    telephone: str
    localisation: str
    description: str
    couleur: str = "orange"

@app.get("/")
def root():
    return {"status": "✅ GenesisBusiness AutoSite™ opérationnel", "version": "1.0.0", "prix": "25 000 FCFA/site"}

@app.post("/generer-site")
async def generer_site(info: BusinessInfo):
    prompt = f"""Tu es un expert web designer. Crée un site HTML complet, professionnel et moderne pour cette entreprise africaine.

Entreprise: {info.nom}
Activité: {info.type_activite}
Téléphone: {info.telephone}
Localisation: {info.localisation}
Description: {info.description}
Couleur principale: {info.couleur}

RÈGLES ABSOLUES:
- HTML complet en UNE seule page (<!DOCTYPE html> jusqu'à </html>)
- CSS intégré dans <style> (pas de fichier externe)
- Design moderne, mobile-first, professionnel
- Section: Hero + Services + À propos + Contact
- Bouton WhatsApp avec le numéro {info.telephone}
- Footer avec © {datetime.now().year} {info.nom}
- Couleur dominante: {info.couleur}
- Texte en français
- Aucun lien cassé, aucune image externe

Retourne UNIQUEMENT le code HTML complet, sans explication."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    html = response.content[0].text
    site_id = f"site_{len(sites_db)+1}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    sites_db[site_id] = {"info": info.dict(), "html": html, "cree_le": datetime.now().isoformat()}
    
    return {"site_id": site_id, "message": "✅ Site généré avec succès", "apercu_url": f"/apercu/{site_id}"}

@app.get("/apercu/{site_id}", response_class=HTMLResponse)
def apercu_site(site_id: str):
    if site_id not in sites_db:
        raise HTTPException(404, "Site non trouvé")
    return HTMLResponse(content=sites_db[site_id]["html"])

@app.get("/admin", response_class=HTMLResponse)
def admin():
    sites_list = ""
    for sid, s in sites_db.items():
        sites_list += f'<tr><td>{s["info"]["nom"]}</td><td>{s["info"]["type_activite"]}</td><td>{s["info"]["localisation"]}</td><td><a href="/apercu/{sid}" target="_blank">Voir</a></td></tr>'
    
    return HTMLResponse(f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8"><title>Admin AutoSite™</title>
<style>
body{{font-family:Arial,sans-serif;background:#0f0f0f;color:#fff;margin:0;padding:20px}}
h1{{color:#f97316}}table{{width:100%;border-collapse:collapse;margin-top:20px}}
th,td{{border:1px solid #333;padding:10px;text-align:left}}
th{{background:#f97316;color:#000}}
a{{color:#f97316}}
.badge{{background:#22c55e;color:#000;padding:4px 10px;border-radius:20px;font-size:12px}}
</style></head>
<body>
<h1>🏭 GenesisBusiness AutoSite™ — Admin</h1>
<span class="badge">✅ {len(sites_db)} sites générés</span>
<p>Prix: <strong>25 000 FCFA / site</strong></p>
<table><tr><th>Entreprise</th><th>Activité</th><th>Localisation</th><th>Action</th></tr>
{sites_list if sites_list else '<tr><td colspan="4">Aucun site encore généré</td></tr>'}
</table>
<hr style="border-color:#333;margin-top:30px">
<p style="color:#666;font-size:12px">afrIAgenesis® — Infrastructure IA Souveraine Africaine</p>
</body></html>""")

@app.get("/sante")
def sante():
    return {"status": "ok", "sites_generes": len(sites_db), "timestamp": datetime.now().isoformat()}
