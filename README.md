 # Assistant Multi-Agent - Donnees Energetiques

Projet personnel - Data Scientist IA | Donnees energetiques francaises

## Description
Assistant IA multi-agent capable d'interroger des donnees energetiques
en langage naturel et de generer des visualisations automatiques.

## Technologies
- LangGraph - Orchestration multi-agents
- FastMCP - Serveur MCP pour interroger des donnees energetiques
- LangSmith - Monitoring et tracabilite
- LangChain - Framework LLM
- OpenAI GPT-3.5 - Modele de langage

## Architecture
Question utilisateur (langage naturel)
        ↓
Orchestrateur LangGraph
        ↓
Serveur MCP (4 outils energetiques)
        ↓
Donnees structurees JSON
        ↓
Reponse tracee LangSmith

## Outils MCP disponibles
- get_current_date
- get_consommation_electrique
- get_mix_energetique
- get_prix_electricite

## Installation
pip install fastmcp langchain langchain-openai langgraph langsmith

## Auteur
Aminata Diallo - Master 1 Cybersecurite et Science des Donnees
Universite Paris 8

