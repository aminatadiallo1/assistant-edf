# Assistant IA Multi-Agent - Donnees Energetiques Francaises

Projet personnel - Data Scientist IA | Donnees energetiques francaises

## Description
Assistant IA multi-agent capable d interroger des donnees energetiques
francaises en langage naturel et de generer des visualisations automatiques.
Le systeme utilise 5 agents specialises coordonnes par un orchestrateur intelligent.

## Architecture - Les 5 agents

| Agent | Role | Description |
|-------|------|-------------|
| Agent 1 | Analyse | Comprend la question et extrait les parametres |
| Agent 2 | Donnees MCP | Interroge les sources de donnees via le protocole MCP |
| Agent 3 | Visualisation | Genere automatiquement le bon graphique |
| Agent 4 | Interpretation | Redige la reponse en francais avec sources citees |
| Agent 5 | RAG | Recherche dans les documents energetiques indexes |

## Orchestrateur intelligent
Le LLM route automatiquement chaque question vers le bon agent :
- DONNEES : chiffres, statistiques, consommation, mix, prix
- CONTEXTE : explications, historique, strategie energetique
- SALUTATION : accueil personnalise
- HORSUJET : refus poli avec redirection

## Technologies

- LangGraph - Orchestration des agents
- FastMCP - Protocole MCP pour interroger les donnees
- LangSmith - Monitoring et tracabilite des appels
- Chroma - Vector store pour le RAG
- Plotly - Visualisations interactives
- Streamlit - Interface web
- OpenAI GPT-3.5 - Modele de langage

## Sources de donnees

- API RTE Open Data (consommation et production electrique)
- EPEX SPOT (prix du marche de l electricite)
- Rapport RTE 2024
- Rapport ADEME 2024
- Rapport CRE 2024
- Ministere de l Energie 2024

## Fonctionnalites

- Questions en langage naturel sans competences techniques
- 3 types de graphiques automatiques (camembert, barres, prix)
- Reponses tracables avec sources toujours citees
- RAG documentaire sur 5 rapports energetiques officiels
- Interface Streamlit avec fond de page et design colore
- Gestion des questions hors sujet et des salutations

## Installation

pip install streamlit langchain langchain-openai langchain-community langgraph fastmcp chromadb plotly python-dotenv langchain-text-splitters

## Lancement

Streamlit :
streamlit run app.py

Terminal :
python test_rapide.py

## Variables d environnement (.env)

OPENAI_API_KEY=sk-...
LANGCHAIN_API_KEY=lsv2_...
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=assistant-edf

## Auteur

Aminata Diallo
Master 1 Cybersecurite et Science des Donnees
Universite Paris 8
