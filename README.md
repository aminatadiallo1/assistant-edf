# Assistant IA Multi-Agent - Données Énergétiques Françaises

> Projet : Data Scientist IA Agent  
> Aminata Diallo en  Master 1 Cybersécurité & Science des Données à Université Paris 8



## Présentation

Assistant conversationnel multi-agent permettant d'interroger les données énergétiques françaises en **langage naturel** et de générer des **visualisations automatiques**. Conçu pour démontrer une maîtrise concrète des technologies IA appliquées au domaine de l'énergie.

Le système orchestre 5 agents spécialisés via LangGraph, avec un routage intelligent par LLM et une couche RAG documentaire sur des rapports officiels (RTE, ADEME, CRE, Ministère de l'Énergie).



## Architecture

```
Question utilisateur
        │
        ▼
┌─────────────────┐
│  Orchestrateur  │  ← Routage LLM (DONNEES / CONTEXTE / SALUTATION / HORSUJET)
└────────┬────────┘
         │
    ┌────┴─────┬──────────┬──────────┐
    ▼          ▼          ▼          ▼
Agent 1    Agent 2    Agent 3    Agent 5
Analyse    Données    Visuali-    RAG
           MCP        sation
    └────────────────────┬──────────┘
                         ▼
                     Agent 4
                  Interprétation
                         │
                         ▼
              Réponse + graphique + sources
```

### Les 5 agents

| Agent | Rôle | Responsabilité |
|-------|------|----------------|
| **Agent 1** | Analyse | Comprend la question, extrait les entités et paramètres clés |
| **Agent 2** | Données MCP | Interroge les APIs (RTE Open Data, EPEX SPOT) via le protocole MCP |
| **Agent 3** | Visualisation | Sélectionne et génère automatiquement le graphique adapté (Plotly) |
| **Agent 4** | Interprétation | Rédige la réponse en français avec sources systématiquement citées |
| **Agent 5** | RAG | Recherche sémantique dans les rapports énergétiques officiels indexés |

### Routage intelligent

L'orchestrateur classe chaque question en 4 catégories :

| Route | Déclencheurs | Traitement |
|-------|-------------|------------|
| `DONNEES` | chiffres, statistiques, consommation, mix énergétique, prix | Agents 1 → 2 → 3 → 4 |
| `CONTEXTE` | explications, historique, stratégie, réglementation | Agents 1 → 5 → 4 |
| `SALUTATION` | bonjour, hello, comment ça va… | Réponse directe personnalisée |
| `HORSUJET` | questions hors énergie | Refus poli avec redirection |



## Stack technique

| Couche | Technologie | Usage |
|--------|-------------|-------|
| Orchestration | **LangGraph** | Graphe d'agents, gestion des états, transitions |
| LLM | **OpenAI GPT-3.5-turbo** | Routage, interprétation, génération de texte |
| Protocole données | **FastMCP** | Connexion standardisée aux APIs de données |
| RAG | **Chroma** + LangChain | Vectorisation et recherche sémantique documentaire |
| Monitoring | **LangSmith** | Traçabilité complète des appels LLM |
| Visualisation | **Plotly** | Graphiques interactifs (camembert, barres, courbes) |
| Interface | **Streamlit** | Application web avec design personnalisé |



## Sources de données

### APIs temps réel
- **RTE Open Data** - Consommation et production électrique française
- **EPEX SPOT** - Prix de marché de l'électricité (€/MWh)

### Corpus RAG (5 documents indexés)
- Rapport RTE 2024 :Bilan électrique, mix de production, nucléaire
- Rapport ADEME 2024 :Énergies renouvelables, transition bas-carbone
- Rapport CRE 2024 :Régulation, tarifs, évolution des prix
-  Rapport Ministère de l'Énergie 2024 : Stratégie nationale, objectifs 2030

---

## Fonctionnalités

- **Langage naturel** : aucune compétence technique requise de l'utilisateur
- **Visualisation automatique** : le bon graphique est sélectionné selon la question
- **Réponses traçables** : les sources sont toujours citées, les appels LLM loggés via LangSmith
- **RAG documentaire** : recherche sémantique sur des rapports officiels récents
- **Gestion des cas limites** : questions hors-sujet, salutations, ambiguïtés

---

## Installation

```bash
# Installer les dépendances
pip install streamlit langchain langchain-openai langchain-community \
            langgraph fastmcp chromadb plotly python-dotenv \
            langchain-text-splitters
```

## Lancement

```bash
# Interface Streamlit
streamlit run app.py

# Test en terminal (mode interactif)
python test_rapide.py
```

## Structure du projet

```
assistant-edf/
├──  app.py                  # Application Streamlit principale
├──  test_rapide.py          # Test interactif en terminal
├──  projet.ipynb            # Notebook de développement et exploration
├──  .env                    # Variables d'environnement (non versionné)
├── README.md
```


## Roadmap

- [ ] Connecter les vraies APIs RTE (données temps réel)
- [ ] Déployer sur Streamlit Cloud
- [ ] Ajouter des tests unitaires sur les agents
- [ ] Étendre le corpus RAG (données régionales, historiques)


*Aminata Diallo - Master 1 Cybersécurité & Science des Données - Université Paris 8*
