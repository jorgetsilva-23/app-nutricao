
import streamlit as st
import json
import os

FICHEIRO = "nutricao_diaria.json"

META_PADRAO = {
    "kcal": 1700,
    "proteina": 130,
    "gordura": 50,
    "hidratos": 190
}

# Alimentos por 100g (peso)
ALIMENTOS_PESO = {
    "Peito de Frango": {"kcal": 110, "proteina": 22, "gordura": 2, "hidratos": 0},
    "Peito de Peru": {"kcal": 105, "proteina": 21, "gordura": 1, "hidratos": 0},
    "Arroz Basmati Cozido": {"kcal": 119, "proteina": 2.5, "gordura": 0.3, "hidratos": 26},
    "Grão-de-bico Cozido": {"kcal": 164, "proteina": 8, "gordura": 2, "hidratos": 27}
}

# Alimentos por unidade
ALIMENTOS_UNIDADE = {
    "Ovo Cozido (1 unidade = 50g)": {"kcal": 78, "proteina": 6.3, "gordura": 5.3, "hidratos": 0.6},
    "Banana Média (1 unidade = 120g)": {"kcal": 105, "proteina": 1.3, "gordura": 0.3, "hidratos": 27}
}

# Refeições completas predefinidas
REFEICOES_COMPLETAS = {
    "Almoço Frango com Arroz": {"kcal": 540, "proteina": 45, "gordura": 12, "hidratos": 55},
    "Jantar Atum e Batata-doce": {"kcal": 620, "proteina": 40, "gordura": 15, "hidratos": 65},
    "Pequeno-almoço Proteico": {"kcal": 410, "proteina": 30, "gordura": 10, "hidratos": 35}
}

if not os.path.exists(FICHEIRO):
    with open(FICHEIRO, "w") as f:
        json.dump([], f)

with open(FICHEIRO, "r") as f:
    refeicoes_registadas = json.load(f)

# Calcular total consumido
total_consumido = {"kcal": 0, "proteina": 0, "gordura": 0, "hidratos": 0}
for r in refeicoes_registadas:
    for k in total_consumido:
        total_consumido[k] += r[k]

# Calcular quanto falta
faltam = {k: round(META_PADRAO[k] - total_consumido[k], 1) for k in META_PADRAO}

st.title("📊 App Nutricional com 3 Tipos de Entrada")

st.header("🎯 Metas Nutricionais Diárias")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Objetivo", f"{META_PADRAO['kcal']} kcal", label_visibility="visible")
col2.metric("Consumido", f"{total_consumido['kcal']} kcal")
col3.metric("Falta", f"{faltam['kcal']} kcal")
col4.metric(" ", "")  # espaço visual

st.subheader("Detalhes")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Proteína", f"{total_consumido['proteina']} / {META_PADRAO['proteina']} g")
col2.metric("Gordura", f"{total_consumido['gordura']} / {META_PADRAO['gordura']} g")
col3.metric("Hidratos", f"{total_consumido['hidratos']} / {META_PADRAO['hidratos']} g")

st.subheader("➕ Adicionar alimento ou refeição")

tipo = st.radio("Tipo de registo:", ["Por Peso (g)", "Por Unidade", "Refeição Completa"])

with st.form("adicionar"):
    if tipo == "Por Peso (g)":
        alimento = st.selectbox("Alimento:", list(ALIMENTOS_PESO.keys()))
        quantidade = st.number_input("Quantidade (g):", min_value=0, step=10)
        macros = ALIMENTOS_PESO[alimento]
        fator = quantidade / 100
        entrada = {
            "descricao": f"{quantidade}g de {alimento}",
            "kcal": round(macros["kcal"] * fator, 1),
            "proteina": round(macros["proteina"] * fator, 1),
            "gordura": round(macros["gordura"] * fator, 1),
            "hidratos": round(macros["hidratos"] * fator, 1)
        }

    elif tipo == "Por Unidade":
        alimento = st.selectbox("Alimento:", list(ALIMENTOS_UNIDADE.keys()))
        unidades = st.number_input("Unidades:", min_value=0, step=1)
        macros = ALIMENTOS_UNIDADE[alimento]
        entrada = {
            "descricao": f"{unidades}x {alimento}",
            "kcal": round(macros["kcal"] * unidades, 1),
            "proteina": round(macros["proteina"] * unidades, 1),
            "gordura": round(macros["gordura"] * unidades, 1),
            "hidratos": round(macros["hidratos"] * unidades, 1)
        }

    else:
        refeicao = st.selectbox("Escolhe a refeição:", list(REFEICOES_COMPLETAS.keys()))
        macros = REFEICOES_COMPLETAS[refeicao]
        entrada = {
            "descricao": refeicao,
            "kcal": macros["kcal"],
            "proteina": macros["proteina"],
            "gordura": macros["gordura"],
            "hidratos": macros["hidratos"]
        }

    confirmar = st.form_submit_button("Adicionar")
    if confirmar:
        refeicoes_registadas.append(entrada)
        with open(FICHEIRO, "w") as f:
            json.dump(refeicoes_registadas, f)
        st.success("Adicionado com sucesso!")
        st.rerun()

if refeicoes_registadas:
    st.subheader("📋 Histórico de Refeições de Hoje")
    st.table(refeicoes_registadas)

if st.button("🔄 Reiniciar dia"):
    with open(FICHEIRO, "w") as f:
        json.dump([], f)
    st.success("Registos limpos!")
    st.rerun()
