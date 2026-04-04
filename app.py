import streamlit as st
import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.tools import tool
import plotly.graph_objects as go

load_dotenv("/Users/aminatadiallo/assistant-edf/assistant-edf/.env")

st.set_page_config(
    page_title="Assistant Energetique IA",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
html, body, [data-testid="stAppViewContainer"] { font-family: 'Inter', sans-serif; }
[data-testid="stAppViewContainer"] {
    background-image: url('https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?w=1920&q=80');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(2, 27, 58, 0.82);
    z-index: 0;
}
[data-testid="stMain"] { position: relative; z-index: 1; }
[data-testid="stSidebar"] {
    background: rgba(2, 27, 58, 0.95) !important;
    border-right: 2px solid #F0A500;
    position: relative;
    z-index: 2;
}
[data-testid="stSidebar"] * { color: white !important; }
.header-box {
    background: linear-gradient(135deg, rgba(6,90,130,0.9), rgba(2,195,154,0.8));
    padding: 32px 24px;
    border-radius: 20px;
    text-align: center;
    color: white;
    margin-bottom: 28px;
    border: 1px solid rgba(240,165,0,0.5);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.header-box h1 { font-size: 2.2rem; font-weight: 700; margin: 0 0 8px 0; }
.header-box p { margin: 4px 0; opacity: 0.9; font-size: 0.95rem; }
.header-badge {
    display: inline-block;
    background: rgba(240,165,0,0.3);
    border: 1px solid #F0A500;
    color: #F0A500;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 11px;
    margin: 3px;
    font-weight: 600;
}
.agent-pill {
    display: inline-block;
    background: linear-gradient(135deg, #065A82, #1C7293);
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 11px;
    margin: 2px;
    font-weight: 600;
}
.rag-pill {
    display: inline-block;
    background: linear-gradient(135deg, #F0A500, #E8930A);
    color: #021B3A;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 11px;
    margin: 2px;
    font-weight: 700;
}
.source-box {
    background: rgba(240,165,0,0.15);
    border-left: 4px solid #F0A500;
    border-radius: 0 10px 10px 0;
    padding: 10px 14px;
    margin-top: 10px;
    color: #F0A500 !important;
    font-size: 13px;
    font-weight: 600;
}
.hors-sujet-box {
    background: rgba(214,39,40,0.15);
    border-left: 4px solid #D62728;
    border-radius: 0 10px 10px 0;
    padding: 14px 18px;
    margin-top: 8px;
    color: #FF6B6B !important;
    font-size: 14px;
}
.bonjour-box {
    background: rgba(2,195,154,0.15);
    border-left: 4px solid #02C39A;
    border-radius: 0 10px 10px 0;
    padding: 14px 18px;
    margin-top: 8px;
    color: #02C39A !important;
    font-size: 14px;
}
.welcome-box {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(240,165,0,0.3);
    border-radius: 20px;
    padding: 40px;
    text-align: center;
    color: white;
    backdrop-filter: blur(10px);
}
.stat-card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    color: white;
    backdrop-filter: blur(8px);
}
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.06) !important;
    border-radius: 16px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    backdrop-filter: blur(8px) !important;
    color: white !important;
}
p, span, div, label { color: white; }
.stMarkdown p { color: white !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-box">
    <h1>⚡ Assistant Energetique IA</h1>
    <p>Systeme multi-agents pour les donnees energetiques francaises</p>
    <br>
    <span class="header-badge">Agent Analyse</span>
    <span class="header-badge">Agent Donnees MCP</span>
    <span class="header-badge">Agent Visualisation</span>
    <span class="header-badge">Agent Interpretation</span>
    <span class="header-badge">Agent RAG</span>
</div>
""", unsafe_allow_html=True)

@st.cache_resource
def initialiser_systeme():
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    documents_energie = [
        Document(page_content="Le mix energetique francais est domine par le nucleaire qui represente environ 70 a 75% de la production electrique. La France possede 56 reacteurs nucleaires repartis sur 18 centrales. EDF exploite la totalite du parc nucleaire francais. Le nucleaire permet a la France d avoir l electricite la moins carbonee d Europe.", metadata={"source": "Rapport RTE 2024", "theme": "nucleaire"}),
        Document(page_content="La consommation electrique en France est d environ 450 TWh par an. Elle est plus elevee en hiver a cause du chauffage electrique. Les pics de consommation se situent entre 18h et 20h en hiver. L Ile-de-France consomme environ 15% de la consommation nationale totale.", metadata={"source": "Rapport RTE 2024", "theme": "consommation"}),
        Document(page_content="Les energies renouvelables representent environ 25% du mix energetique francais. L eolien represente 8% avec plus de 21000 eoliennes. Le solaire represente 4% avec 18 GW installes. L hydraulique est la premiere source renouvelable avec 12% de la production. Objectif 40% renouvelables en 2030.", metadata={"source": "Rapport ADEME 2024", "theme": "renouvelables"}),
        Document(page_content="Le prix de l electricite en France est fixe par le marche europeen EPEX SPOT. En 2024 le prix moyen etait d environ 80 euros par MWh. Les prix sont plus eleves en hiver. La France exporte de l electricite quand la production est excedentaire.", metadata={"source": "Rapport CRE 2024", "theme": "prix"}),
        Document(page_content="La transition energetique en France vise a reduire la dependance aux energies fossiles. EDF investit dans la construction de nouveaux reacteurs EPR2. Six nouveaux reacteurs sont prevus d ici 2035. L objectif est d atteindre la neutralite carbone en 2050.", metadata={"source": "Ministere de l Energie 2024", "theme": "transition"}),
    ]
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents_energie)
    vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings, collection_name="energie_france_v5")
    return llm, vectorstore

llm, vectorstore = initialiser_systeme()

@tool
def get_consommation_electrique(date_debut: str, date_fin: str, region: str = "France") -> str:
    """Recupere les donnees de consommation electrique francaise."""
    return json.dumps({"region": region, "periode": date_debut + " a " + date_fin, "consommation_mwh": 45230, "variation_vs_annee_precedente": "-3.2%", "pic_journalier": "19h00", "source": "API RTE Open Data"}, ensure_ascii=False, indent=2)

@tool
def get_mix_energetique(date: str) -> str:
    """Recupere le mix de production energetique francais."""
    return json.dumps({"date": date, "production_totale_mwh": 52100, "repartition": {"nucleaire": 71.2, "hydraulique": 12.4, "eolien": 8.1, "solaire": 4.3, "thermique": 3.8, "autres": 0.2}, "taux_co2_gco2_kwh": 38, "source": "API RTE Open Data"}, ensure_ascii=False, indent=2)

@tool
def get_prix_electricite(date_debut: str, date_fin: str) -> str:
    """Recupere les prix de l electricite en France."""
    return json.dumps({"periode": date_debut + " a " + date_fin, "prix_moyen_eur_mwh": 87.50, "prix_min_eur_mwh": 42.10, "prix_max_eur_mwh": 156.80, "tendance": "hausse", "source": "EPEX SPOT"}, ensure_ascii=False, indent=2)

def agent_analyse(question):
    try:
        prompt = f"""Extrais les informations de cette question en JSON valide :
{{"type_donnee": "consommation" ou "mix_energetique" ou "prix", "region": "region ou France", "date_debut": "YYYY-MM-DD", "date_fin": "YYYY-MM-DD", "date_unique": "YYYY-MM-DD"}}
Question : {question}
JSON uniquement :"""
        response = llm.invoke([HumanMessage(content=prompt)])
        return json.loads(response.content)
    except:
        return {"type_donnee": "mix_energetique", "region": "France", "date_debut": "2024-01-01", "date_fin": "2024-01-31", "date_unique": "2024-01-15"}

def agent_donnees(params):
    try:
        type_donnee = params.get("type_donnee", "mix_energetique")
        if type_donnee == "mix_energetique":
            date = params.get("date_unique", params.get("date_debut", "2024-01-15"))
            return get_mix_energetique.invoke({"date": date}), type_donnee
        elif type_donnee == "consommation":
            return get_consommation_electrique.invoke({"date_debut": params.get("date_debut", "2024-01-01"), "date_fin": params.get("date_fin", "2024-01-31"), "region": params.get("region", "France")}), type_donnee
        else:
            return get_prix_electricite.invoke({"date_debut": params.get("date_debut", "2024-01-01"), "date_fin": params.get("date_fin", "2024-01-31")}), type_donnee
    except Exception as e:
        return json.dumps({"erreur": str(e)}), "mix_energetique"

def agent_visualisation(data, type_donnee):
    try:
        d = json.loads(data)
        layout_base = dict(title_x=0.5, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white"), title_font=dict(color="#F0A500", size=16))
        if type_donnee == "mix_energetique":
            repartition = d["repartition"]
            fig = go.Figure(data=[go.Pie(labels=list(repartition.keys()), values=list(repartition.values()), marker=dict(colors=["#1f77b4","#2ca02c","#17becf","#F0A500","#d62728","#9467bd"], line=dict(color="white", width=2)), hole=0.4, textfont=dict(size=13, color="white"))])
            fig.update_layout(title="Mix energetique France — " + d.get("date",""), **layout_base)
            return fig
        elif type_donnee == "consommation":
            mois = ["Jan","Fev","Mar","Avr","Mai","Jun","Jul","Aou","Sep","Oct","Nov","Dec"]
            valeurs = [45230,42100,38900,35200,32100,28900,27500,28100,31200,36800,41200,44900]
            fig = go.Figure(data=[go.Bar(x=mois, y=valeurs, marker=dict(color=valeurs, colorscale="Blues", showscale=False), text=[f"{v:,}" for v in valeurs], textposition="outside", textfont=dict(color="white"))])
            fig.update_layout(title="Consommation electrique — " + d.get("region",""), yaxis_title="MWh", yaxis=dict(gridcolor="rgba(255,255,255,0.1)", color="white"), xaxis=dict(color="white"), **layout_base)
            return fig
        else:
            categories = ["Prix minimum", "Prix moyen", "Prix maximum"]
            valeurs = [d.get("prix_min_eur_mwh",0), d.get("prix_moyen_eur_mwh",0), d.get("prix_max_eur_mwh",0)]
            fig = go.Figure(data=[go.Bar(x=categories, y=valeurs, marker_color=["#2ca02c","#1f77b4","#d62728"], text=[str(v)+" EUR/MWh" for v in valeurs], textposition="auto", textfont=dict(color="white", size=13))])
            fig.update_layout(title="Prix electricite — " + d.get("periode",""), yaxis_title="EUR/MWh", yaxis=dict(gridcolor="rgba(255,255,255,0.1)", color="white"), xaxis=dict(color="white"), **layout_base)
            return fig
    except:
        return None

def agent_interpretation(question, data, type_donnee):
    try:
        prompt = f"""Expert en energie francaise. Question : {question}
Donnees : {data}
Reponse claire en francais, chiffres cles, source citee, max 4 phrases :"""
        return llm.invoke([HumanMessage(content=prompt)]).content
    except:
        return "Erreur lors de l interpretation."

def agent_rag(question):
    try:
        docs = vectorstore.similarity_search(question, k=3)
        contexte = "\n\n".join([f"Source : {d.metadata['source']}\n{d.page_content}" for d in docs])
        prompt = f"""Expert en energie francaise. Reponds UNIQUEMENT avec les documents fournis. Cite les sources.
Si la question ne concerne pas la France ou ne correspond pas aux documents, dis-le clairement.
Documents : {contexte}
Question : {question}
Reponse en francais :"""
        reponse = llm.invoke([HumanMessage(content=prompt)]).content
        sources = list(set([d.metadata["source"] for d in docs]))
        return reponse, sources
    except:
        return "Erreur lors de la recherche documentaire.", []

def orchestrateur(question):
    try:
        salutations = ["bonjour", "bonsoir", "salut", "hello", "hi", "coucou", "hey", "bonne journee", "bonne soiree"]
        if any(s in question.lower() for s in salutations) and len(question.split()) <= 5:
            return "SALUTATION"

        prompt_routage = f"""Tu es un assistant specialise UNIQUEMENT dans les donnees energetiques FRANCAISES.
Classe cette question dans UNE categorie et reponds avec UN SEUL MOT :

DONNEES : question sur des chiffres, statistiques, consommation electrique en France, mix energetique francais, production electrique francaise, prix electricite en France
CONTEXTE : question sur une explication, historique, strategie, pourquoi ou comment dans le domaine de l energie EN FRANCE
HORSUJET : question qui ne concerne PAS l energie francaise — inclut les questions sur d autres pays, d autres energies non electriques comme le gaz, le petrole, ou tout autre sujet

Exemples DONNEES : "consommation en ile de france", "mix energetique janvier 2024", "prix electricite france"
Exemples CONTEXTE : "pourquoi le nucleaire en france", "transition energetique francaise", "comment fonctionne l eolien"
Exemples HORSUJET : "prix du gaz en allemagne", "petrole en arabie saoudite", "recette gateau", "meteo paris", "electricite en espagne", "gaz naturel france"

Question : {question}
UN SEUL MOT :"""
        routage = llm.invoke([HumanMessage(content=prompt_routage)]).content.strip().upper()
        if "DONNEES" in routage:
            return "DONNEES"
        elif "CONTEXTE" in routage:
            return "CONTEXTE"
        else:
            return "HORSUJET"
    except:
        return "HORSUJET"

with st.sidebar:
    st.markdown("## ⚡ Assistant IA")
    st.markdown("---")
    st.markdown("### Les 5 agents")
    for num, nom, desc in [("1","Analyse","Comprend la question"),("2","Donnees MCP","Recupere les donnees"),("3","Visualisation","Genere le graphique"),("4","Interpretation","Redige la reponse"),("5","RAG","Recherche documentaire")]:
        st.markdown(f"**{num}. {nom}**")
        st.caption(desc)
    st.markdown("---")
    st.markdown("### Exemples")
    for ex in ["Mix energetique janvier 2024", "Consommation Ile-de-France ?", "Pourquoi le nucleaire ?", "Prix electricite 2024", "Transition energetique ?"]:
        st.markdown(f"• *{ex}*")
    st.markdown("---")
    st.markdown("**Aminata Diallo**")
    st.caption("Master 1 CSSD · Paris 8")
    if st.button("Effacer la conversation", type="secondary", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

col1, col2, col3, col4 = st.columns(4)
for col, (icon, val, label) in zip([col1,col2,col3,col4], [("🏭","71.2%","Part nucleaire"),("🌊","12.4%","Hydraulique"),("💨","8.1%","Eolien"),("☀️","4.3%","Solaire")]):
    with col:
        st.markdown(f'<div class="stat-card"><div style="font-size:1.8rem">{icon}</div><div style="font-size:1.4rem; font-weight:700; color:#F0A500">{val}</div><div style="font-size:0.8rem; opacity:0.8">{label}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="welcome-box">
        <div style="font-size:3rem">⚡</div>
        <h3 style="color:#F0A500; margin:12px 0">Bonjour ! Je suis votre assistante energetique.</h3>
        <p style="opacity:0.9">Posez-moi une question sur les donnees energetiques francaises.</p>
        <p style="opacity:0.7; font-size:0.9rem">Consommation · Mix energetique · Prix · Transition energetique</p>
    </div>""", unsafe_allow_html=True)

for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "figure" in msg and msg["figure"] is not None:
            st.plotly_chart(msg["figure"], use_container_width=True, key=f"chart_hist_{i}")
        if "sources" in msg and msg["sources"]:
            st.markdown('<div class="source-box">Sources : ' + " · ".join(msg["sources"]) + '</div>', unsafe_allow_html=True)
        if "agent" in msg:
            pill_class = "rag-pill" if "RAG" in msg["agent"] else "agent-pill"
            st.markdown(f'<span class="{pill_class}">{msg["agent"]}</span>', unsafe_allow_html=True)

if question := st.chat_input("Posez votre question sur les donnees energetiques francaises..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Analyse en cours..."):
            routage = orchestrateur(question)
            nb = len(st.session_state.messages)

            if routage == "SALUTATION":
                reponse = "Bonjour ! Je suis votre assistante specialisee dans les donnees energetiques francaises. Comment puis-je vous aider ? Je peux vous renseigner sur la consommation electrique, le mix energetique, les prix ou la transition energetique en France."
                st.markdown(f'<div class="bonjour-box">{reponse}</div>', unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": reponse})

            elif routage == "HORSUJET":
                reponse = "Je suis specialisee uniquement dans les donnees energetiques francaises. Je ne peux pas repondre aux questions sur d autres pays ou d autres types d energie. Posez-moi une question sur la consommation electrique, le mix energetique ou les prix en France !"
                st.markdown(f'<div class="hors-sujet-box">⚠️ {reponse}</div>', unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": reponse})

            elif routage == "CONTEXTE":
                reponse, sources = agent_rag(question)
                st.markdown(reponse)
                if sources:
                    st.markdown('<div class="source-box">Sources : ' + " · ".join(sources) + '</div>', unsafe_allow_html=True)
                st.markdown('<span class="rag-pill">Agent RAG actif</span>', unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": reponse, "sources": sources, "agent": "Agent RAG actif"})

            else:
                params = agent_analyse(question)
                data, type_donnee = agent_donnees(params)
                fig = agent_visualisation(data, type_donnee)
                reponse = agent_interpretation(question, data, type_donnee)
                if fig is not None:
                    st.plotly_chart(fig, use_container_width=True, key=f"chart_new_{nb}")
                st.markdown(reponse)
                st.markdown('<span class="agent-pill">Agents Donnees actifs</span>', unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": reponse, "figure": fig, "agent": "Agents Donnees actifs"})
