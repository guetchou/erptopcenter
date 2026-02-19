# LVAClean Post-Install Checklist

Contexte: deploiement local WSL pour LVAClean (agents en reseau local).

## 1) Validation technique immediate

- Verifier les conteneurs:
  - `docker compose -f deploy/docker/compose.prod.yaml ps`
- Verifier backend ping:
  - `docker compose -f deploy/docker/compose.prod.yaml exec -T backend curl -fsS http://localhost:8000/api/method/ping`
- Verifier apps installees:
  - `docker compose -f deploy/docker/compose.prod.yaml exec -T backend bench --site lvaclean.local list-apps`
- Attendu minimum:
  - `erpnext`, `hrms`, `topcenter_core`, `topcenter_branding`, `crm`, `topcenter_cleaning`, `topcenter_hr`, `topcenter_finance`

## 2) CRM (prospection, pipeline, suivi client)

- Creer un lead test et convertir en customer.
- Creer une opportunite + prochaine action.
- Verifier vues pipeline et filtres commerciaux.
- Verifier champs obligatoires LVAClean (telephone, zone, source, priorite).
- Test marketing/fidelisation:
  - segmenter 10 clients,
  - lancer une campagne test,
  - verifier traces dans timeline CRM.

## 3) Cleaning (commandes, RDV, interventions)

- Creer 1 commande de nettoyage (service, adresse, date, agent).
- Generer 1 RDV et confirmer statut (Planifie -> En cours -> Termine).
- Creer 1 intervention terrain avec compte rendu.
- Verifier la liaison Client -> Commande -> Intervention -> Facture.
- Verifier que les pages print/PDF n affichent aucune URL technique.

## 4) Notifications temps reel

- Verifier websocket en sante:
  - `docker compose -f deploy/docker/compose.prod.yaml logs --since 10m websocket | tail -n 80`
- Test fonctionnel:
  - ouvrir 2 navigateurs avec 2 utilisateurs,
  - modifier une opportunite / intervention,
  - confirmer apparition en temps reel (notification/list refresh).
- Si echec, verifier redis-queue et websocket puis redemarrer services.

## 5) Geolocalisation client

- Verifier configuration provider carto (API key si Google/Mapbox).
- Geocoder 5 adresses clients reelles.
- Controler lat/lng stockees et affichage carte dans fiche client/intervention.
- Tester affectation agent par zone (rayon ou secteur).

## 6) RH et finance (coherence metier)

- RH:
  - Creer 2 agents,
  - affecter planning intervention,
  - verifier disponibilites.
- Finance:
  - Generer 1 facture depuis commande,
  - enregistrer 1 paiement,
  - verifier impact comptable.

## 7) Reseau local WSL (agents)

- Recuperer IP Windows hote.
- Ouvrir le port frontend dans pare-feu Windows.
- Depuis un poste agent, tester URL `http://IP_HOTE:PORT`.
- Option: DNS local/hosts vers `erp.lvaclean.local`.

## 8) Securite et exploitation

- Changer tous les mots de passe par defaut.
- Activer sauvegarde quotidienne DB + `sites`.
- Tester une restauration a blanc (obligatoire avant go-live).
- Documenter version deployee (`v1.0.1`) + date + operateur.
