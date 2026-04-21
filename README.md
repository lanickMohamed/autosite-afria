# GenesisBusiness AutoSite™
Génération automatique de sites vitrine pour PME ouest-africaines
**Prix:** 25 000 FCFA / site

## Déploiement Railway
1. `railway login`
2. `railway init`
3. Ajoute variable: ANTHROPIC_API_KEY
4. `railway up`

## Endpoints
- GET  /        → statut
- POST /generer-site → génère un site
- GET  /apercu/{id} → voir le site
- GET  /admin   → dashboard
- GET  /sante   → health check
