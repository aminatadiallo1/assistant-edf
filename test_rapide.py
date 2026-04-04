import os, json, sys
from dotenv import load_dotenv
load_dotenv("/Users/aminatadiallo/assistant-edf/assistant-edf/.env")

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from typing import TypedDict, Annotated
import operator
from datetime import datetime
import plotly.graph_objects as go

@tool
def get_current_date() -> str:
    """Retourne la date du jour."""
    return datetime.now().strftime("%Y-%m-%d")

@tool
def get_consommation_electrique(date_debut: str, date_fin: str, region: str = "France") -> str:
    """Recupere les donnees de consommation electrique."""
    data = {
        "region": region,
        "periode": date_debut + " a " + date_fin,
        "consommation_mwh": 45230,
        "variation": "-3.2%",
        "source": "API RTE"
    }
    return json.dumps(data)

@tool
def get_mix_energetique(date: str) -> str:
    """Recupere le mix energetique pour une date donnee."""
    data = {
        "date": date,
        "repartition": {
            "nucleaire": 71.2,
            "hydraulique": 12.4,
            "eolien": 8.1,
            "solaire": 4.3,
            "thermique": 3.8,
            "autres": 0.2
        },
        "source": "API RTE"
    }
    return json.dumps(data)

@tool
def get_prix_electricite(date_debut: str, date_fin: str) -> str:
    """Recupere les prix de l electricite sur le marche spot."""
    data = {
        "periode": date_debut + " a " + date_fin,
        "prix_moyen_eur_mwh": 87.5,
        "prix_min_eur_mwh": 42.1,
        "prix_max_eur_mwh": 156.8,
        "source": "EPEX SPOT"
    }
    return json.dumps(data)

tools = [get_current_date, get_consommation_electrique, get_mix_energetique, get_prix_electricite]

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
llm_with_tools = llm.bind_tools(tools)

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]

def call_llm(state):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

def should_continue(state):
    last = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tools"
    return END

graph = StateGraph(AgentState)
graph.add_node("llm", call_llm)
graph.add_node("tools", ToolNode(tools))
graph.set_entry_point("llm")
graph.add_conditional_edges("llm", should_continue, {"tools": "tools", END: END})
graph.add_edge("tools", "llm")
app = graph.compile()

def afficher_graphique(message):
    data = json.loads(message.content)
    if message.name == "get_mix_energetique":
        repartition = data["repartition"]
        labels = list(repartition.keys())
        values = list(repartition.values())
        couleurs = ["#1f77b4", "#2ca02c", "#17becf", "#ffbb00", "#d62728", "#9467bd"]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=couleurs), hole=0.3)])
        fig.update_layout(title="Mix energetique France - " + data["date"], title_x=0.5)
        fig.show()
    elif message.name == "get_consommation_electrique":
        mois = ["Jan", "Fev", "Mar", "Avr", "Mai", "Jun", "Jul", "Aou", "Sep", "Oct", "Nov", "Dec"]
        valeurs = [45230, 42100, 38900, 35200, 32100, 28900, 27500, 28100, 31200, 36800, 41200, 44900]
        fig = go.Figure(data=[go.Bar(x=mois, y=valeurs, marker_color="#1f77b4")])
        fig.update_layout(title="Consommation electrique - " + data["region"], title_x=0.5, xaxis_title="Mois", yaxis_title="MWh")
        fig.show()
    elif message.name == "get_prix_electricite":
        categories = ["Prix minimum", "Prix moyen", "Prix maximum"]
        valeurs = [data["prix_min_eur_mwh"], data["prix_moyen_eur_mwh"], data["prix_max_eur_mwh"]]
        couleurs = ["#2ca02c", "#1f77b4", "#d62728"]
        fig = go.Figure(data=[go.Bar(x=categories, y=valeurs, marker_color=couleurs, text=[str(v) + " EUR/MWh" for v in valeurs], textposition="auto")])
        fig.update_layout(title="Prix electricite - " + data["periode"], title_x=0.5, yaxis_title="EUR/MWh")
        fig.show()

system = SystemMessage(content="""Tu es un assistant specialise dans les donnees energetiques francaises.
Si la question est hors sujet reponds poliment que tu es specialise uniquement dans ce domaine
et propose de poser une question sur la consommation le mix energetique ou les prix.""")

print("Bonjour je suis votre assistant Energetique Interactif")

while True:
    question = input("Votre question : ").strip()
    if question.lower() == "quitter":
        print("\nAu revoir !")
        break
    if question == "":
        print("Veuillez entrer une question !\n")
        continue
    print("Analyse en cours...")
    result = app.invoke({"messages": [system, HumanMessage(content=question)]})
    for message in result["messages"]:
        if hasattr(message, "name") and message.name in ["get_mix_energetique", "get_consommation_electrique", "get_prix_electricite"]:
            afficher_graphique(message)
    print("\nReponse :\n" + result["messages"][-1].content + "\n")
