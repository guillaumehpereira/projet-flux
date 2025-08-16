import streamlit as st
import pandas as pd
import time
import os

st.set_page_config(page_title="Fraud Alerts Dashboard", layout="wide")
st.title("🛡️ Real-Time Fraud Detection - Alerts Dashboard")

PARQUET_DIR = "../parquet_data"

@st.cache_data(ttl=10)
def load_parquet():
    if os.path.exists(PARQUET_DIR):
        try:
            return pd.read_parquet(PARQUET_DIR)
        except Exception as e:
            st.warning("Erreur lecture parquet:")
            st.code(str(e))
            return pd.DataFrame()
    else:
        st.warning("📁 Le dossier 'parquet_data' n'existe pas.")
        return pd.DataFrame()

df = load_parquet()

if df.empty:
    st.info("Aucune alerte détectée pour l’instant.")
else:
    st.metric("Nombre total d'alertes", len(df))
    st.dataframe(df.sort_values("timestamp", ascending=False), use_container_width=True)

    # 🔹 Graphe : répartition par type d’alerte
    st.subheader("📊 Répartition des types d’alerte")
    alert_counts = df["alert_type"].value_counts()
    st.bar_chart(alert_counts)

    # 🔹 Graphe : volume d’alertes dans le temps
    st.subheader("📈 Nombre d’alertes par minute")
    df_time = df.copy()
    df_time["minute"] = pd.to_datetime(df_time["timestamp"]).dt.floor("min")
    count_by_minute = df_time.groupby("minute").size().reset_index(name="nb_alertes")
    st.line_chart(count_by_minute.set_index("minute"))

    # Bouton de refresh
    if st.button("🔄 Rafraîchir"):
        st.rerun()
