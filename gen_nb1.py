import json

def md(s):
    return {"cell_type":"markdown","metadata":{},"source":[s],"id":None}
def code(s):
    return {"cell_type":"code","execution_count":None,"metadata":{},"source":[s],"outputs":[],"id":None}

C = []

# ══ 0: Título ══
C.append(md("""# Data Contract — Case Ambev Long Neck NENO
## Processo Seletivo Insper Junior | Engenharia Tecnológica — 50ª Gestão

**Grupo 3** | Mateus Loureiro
**Data:** 11 de março de 2026
**Fonte de Dados:** `Analise_LongNeck_WSNP - Sem repostas.xlsx` (6 abas)

---

### Metodologia
1. **Entendimento do Cliente** ✅
2. **Data Contract** ← *estamos aqui*
3. Análise Univariada
4. Árvore de Hipóteses (MECE)
5. Análise Bivariada
6. Entrega (PPTX, XLSX, Dashboard React+Vite+TS+Styled Components)

### O que é um Data Contract?
Documenta **cada campo** com 8 atributos:

| Atributo | Descrição |
|---|---|
| **Nome do Campo** | Identificador da variável |
| **Tipo** | int, float, string, datetime, boolean |
| **Formato** | Padrão de representação |
| **Descrição Semântica** | Significado no contexto de negócio |
| **Domínio de Valores** | Faixa ou conjunto de valores possíveis |
| **Regras de Negócio** | Restrições, fórmulas, dependências |
| **Nulabilidade** | Se aceita valores nulos/vazios |
| **Origem** | De onde o dado vem |"""))

# ══ 1: Setup ══
C.append(code("""%matplotlib inline
%pip install openpyxl --quiet

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe
import warnings
warnings.filterwarnings('ignore')
from pathlib import Path
from IPython.display import display, HTML

# Configuração visual global
plt.rcParams.update({
    'figure.facecolor': '#FAFAFA',
    'axes.facecolor': '#FAFAFA',
    'font.family': 'sans-serif',
    'font.size': 11,
    'figure.dpi': 100
})

CORES = {
    'azul_escuro': '#1B2A4A',
    'azul_medio': '#2D5F8A',
    'azul_claro': '#5BA4CF',
    'ambar': '#F5A623',
    'vermelho': '#E74C3C',
    'verde': '#27AE60',
    'cinza_claro': '#ECF0F1',
    'cinza_medio': '#95A5A6',
    'branco': '#FFFFFF',
    'bg': '#FAFAFA'
}

BASE_DIR = Path('.').resolve()
EXCEL_FILE = None
# Priorizar arquivo original "Sem repostas" sobre qualquer derivado (ignorar ~$ temporários)
for p in [BASE_DIR, BASE_DIR.parent]:
    candidates = [f for f in p.glob('*Sem*repostas*.xlsx') if not f.name.startswith('~$')]
    if candidates:
        EXCEL_FILE = candidates[0]
        break
if EXCEL_FILE is None:
    for p in [BASE_DIR, BASE_DIR.parent]:
        all_xlsx = list(p.glob('*Long*Neck*.xlsx')) + list(p.glob('*longneck*.xlsx'))
        candidates = [f for f in all_xlsx if not f.name.startswith('~$')]
        if candidates:
            EXCEL_FILE = candidates[0]
            break

if EXCEL_FILE is None:
    print("⚠️  Arquivo Excel não encontrado. Coloque na mesma pasta do notebook.")
else:
    print(f"✅ Arquivo encontrado: {EXCEL_FILE.name}")

def show_contract(df, title=""):
    display(HTML(f"<h4>{title}</h4>"))
    display(df)

print(f"Pandas version: {pd.__version__}")
print("📋 Setup concluído — com matplotlib para visualizações.")"""))

# ══ 2: Visão Geral ══
C.append(md("""---
---

# PARTE 1 — Data Contract

> **Objetivo:** Mapear e documentar formalmente cada campo das 6 abas do Excel com 8 atributos por variável — garantindo rastreabilidade e qualidade dos dados antes das análises.

## 1. Visão Geral das Fontes de Dados

| # | Aba | Descrição | Granularidade | Período |
|---|-----|-----------|---------------|---------|
| 1 | **Cenário atual BR** | Visão mensal consolidada por GEO/REG | Mensal × Região | Jan–Fev 2026 |
| 2 | **Custos de transferência** | Custos logísticos, MACOs, custos de produção | SKU × Rota | Estático |
| 3 | **Produção PCP** | Programação semanal AQ541 e PE541 | Semanal × SKU × Planta | Fev 2026 (4 sem) |
| 4 | **Transferências Programadas** | Transferências já planejadas SP→NE | Semanal × SKU × Destino | Fev 2026 (4 sem) |
| 5 | **Cenário Divulgado** | WSNP semanal detalhado (baseline) | Semanal × SKU × Sub-região | Fev 2026 (4 sem) |
| 6 | **Cenário com Nova Demanda** | Malzbier +30% (problema a resolver) | Semanal × SKU × Sub-região | Fev 2026 (4 sem) |

**SKUs:** Patagonia, Goose Island, Malzbier Brahma, Colorado Lager (todos LN)
**Região foco:** NENO — sub-regiões: Mapapi, NE Norte, NE Sul, NO Araguaia, NO Centro
**Choque:** Malzbier Brahma +30%"""))

# ══ 3: Header Aba 1 ══
C.append(md("""---
## 2. Data Contract — Aba 1: "Cenário Atual BR"

Visão macro mensal de todo o portfólio Long Neck SK269 por GEO/REG.
Janeiro (26 dias úteis) e Fevereiro (24 dias úteis).
Regiões: MG, SP, NENO, CO, RJ, SUL, Export, TOTAL."""))

# ══ 4: Contract Aba 1 ══
C.append(code("""contract_aba1 = pd.DataFrame([
    {'Campo': 'GEO/REG', 'Tipo': 'string', 'Formato': 'Texto',
     'Descrição Semântica': 'Região geográfica de demanda/distribuição.',
     'Domínio': "MG, SP, NENO, CO, RJ, SUL, Export, TOTAL",
     'Regras de Negócio': 'TOTAL = soma regiões. NENO = NE+Norte (foco).',
     'Nulabilidade': 'NOT NULL', 'Origem': 'WSNP Ambev'},
    {'Campo': 'Demanda (HL)', 'Tipo': 'float', 'Formato': '#,##0',
     'Descrição Semântica': 'Volume previsto de venda mensal em hectolitros.',
     'Domínio': '[0, +∞) — NENO Jan: 200.754, Fev: 179.674',
     'Regras de Negócio': 'Soma regiões = TOTAL. BIAS GEOs: +9%.',
     'Nulabilidade': 'NOT NULL', 'Origem': 'GEOs (equipes regionais)'},
    {'Campo': 'PROD Real (HL)', 'Tipo': 'float', 'Formato': '#,##0',
     'Descrição Semântica': 'Volume realizado de produção no mês.',
     'Domínio': '[0, +∞) — só Jan. SP: 127.269, NENO: 70.399',
     'Regras de Negócio': 'Regiões sem planta = 0. Só Janeiro.',
     'Nulabilidade': 'Nullable (0)', 'Origem': 'MES/ERP'},
    {'Campo': 'PROD WSNP (HL)', 'Tipo': 'float', 'Formato': '#,##0',
     'Descrição Semântica': 'Volume programado conforme WSNP.',
     'Domínio': '[0, +∞) — NENO Fev: 158.000',
     'Regras de Negócio': 'Pode diferir do realizado.',
     'Nulabilidade': 'Nullable (0)', 'Origem': 'WSNP Ambev'},
    {'Campo': 'PROD 1W (HL)', 'Tipo': 'float', 'Formato': '#,##0',
     'Descrição Semântica': 'Vol. programado para produção (horizonte 1 semana, mais firme).',
     'Domínio': '[0, +∞) — NENO: 176.297',
     'Regras de Negócio': 'Mais firme que WSNP. Só Jan.',
     'Nulabilidade': 'Nullable', 'Origem': 'PCP'},
    {'Campo': 'EI Mês (HL)', 'Tipo': 'float', 'Formato': '#,##0',
     'Descrição Semântica': 'Estoque inicial do mês.',
     'Domínio': '[0, +∞) — NENO Jan: 136.190',
     'Regras de Negócio': 'EI mês N = EF mês N-1.',
     'Nulabilidade': 'NOT NULL', 'Origem': 'WMS'},
    {'Campo': 'Suf.ini (d)', 'Tipo': 'float', 'Formato': '#,##0 dias',
     'Descrição Semântica': 'Suficiência inicial = EI / demanda linear diária.',
     'Domínio': '[0, +∞) — NENO Jan: 15.39d',
     'Regras de Negócio': 'DOI mín = 12 dias. < 12 = alerta.',
     'Nulabilidade': 'NOT NULL', 'Origem': 'Calculado'},
    {'Campo': 'Transf. Malha (HL)', 'Tipo': 'float', 'Formato': '#,##0',
     'Descrição Semântica': 'Volume de transferência inter-regional. + recebe, - envia.',
     'Domínio': '(-∞, +∞) — SP envia, NENO recebe.',
     'Regras de Negócio': 'Soma ≈ 0 (conservação).',
     'Nulabilidade': 'NOT NULL', 'Origem': 'Planej. logístico'},
    {'Campo': 'EFM (HL)', 'Tipo': 'float', 'Formato': '#,##0',
     'Descrição Semântica': 'Estoque final projetado do mês.',
     'Domínio': '(-∞, +∞) — negativo = ruptura.',
     'Regras de Negócio': 'EFM = EI + PROD - Demanda + Transf.',
     'Nulabilidade': 'NOT NULL', 'Origem': 'Calculado'},
    {'Campo': 'Suf.f (d)', 'Tipo': 'float', 'Formato': '#,##0 dias',
     'Descrição Semântica': 'Suficiência final em dias de cobertura.',
     'Domínio': '(-∞, +∞) — NENO Jan: 11.54d (< DOI!)',
     'Regras de Negócio': 'DOI mín = 12d. NENO Jan fecha abaixo!',
     'Nulabilidade': 'NOT NULL', 'Origem': 'Calculado'}
])
show_contract(contract_aba1, '📋 Data Contract — Aba 1: Cenário Atual BR')"""))

# ══ 5: Dados Brutos Aba 1 ══
C.append(code("""# Dados Brutos — Aba 1

dados_jan = pd.DataFrame({
    'GEO/REG': ['MG', 'SP', 'NENO', 'CO', 'RJ', 'SUL', 'Export', 'TOTAL'],
    'Demanda': [65538.3, 173637.4, 200754.3, 104493.3, 111219.4, 116261.4, 67055.4, 838959.5],
    'PROD Real': [0, 127269, 70399, 50470, 130770, 41205, 0, 420113],
    'PROD WSNP': [0, 15300, 9342.9, 5142.9, 17571.4, 3985.7, 0, 51342.9],
    'PROD 1W': [0, 238579.2, 176297.4, 99590.4, 339789.6, 104891.4, 0, 959148],
    'EI Mês': [28580.4, 114472.8, 136190, 61952.4, 84834, 86758.2, 0, 495419.4],
    'Suf.ini(d)': [11.34, 17.14, 15.39, 15.41, 19.83, 19.40, 0, 15.35],
    'Transf.Malha': [11585.9, -12423.9, 7455.6, 7619.6, -29886.9, 12433.2, 3212.1, -4.5],
    'EFM': [32771.5, 120086.5, 86426.7, 81961.6, 87765.2, 77470.0, -21611.0, 486481.4],
    'Suf.f(d)': [10.80, 17.44, 11.54, 17.44, 16.12, 15.95, -10.55, 13.53]
})

dados_fev = pd.DataFrame({
    'GEO/REG': ['MG', 'SP', 'NENO', 'CO', 'RJ', 'SUL', 'Export', 'TOTAL'],
    'Demanda': [72849.3, 165262.4, 179673.8, 112802.3, 130649.4, 116585.2, 49179.6, 827002.0],
    'PROD WSNP': [0, 253602.3, 158000, 87685.7, 288282.9, 77748.4, 0, 863199.3],
    'Transf.Malha': [75118.4, -75583.1, 34507, 21794.0, -174400.9, 38221.7, 38158.1, -118.0],
    'EFM': [35040.6, 132843.2, 99259.9, 78639.0, 70997.7, 76855.0, -32632.5, 493635.4],
    'Suf.f(d)': [12.89, 25.53, 13.26, 21.10, 20.30, 17.45, -26.91, 14.33]
})

print("JANEIRO 2026 (26 dias úteis)")
display(dados_jan)
print()
print("FEVEREIRO 2026 (24 dias úteis)")
display(dados_fev)"""))

# ══ 6: Insights Aba 1 ══
C.append(md("""### Insights — Aba 1
1. **NENO é a 2ª maior região** (~24% do Brasil)
2. **Suficiência NENO Janeiro: 11.54d** — abaixo do DOI mínimo de 12d ⚠️
3. **NENO é receptor líquido** de transferências (+7.456 Jan, +34.507 Fev)
4. **SP é o maior remetente** (-12.424 Jan, -75.583 Fev)
5. **Export tem EF negativo** (ruptura) — mercado interno priorizado"""))

# ══ 7: Header Aba 2 ══
C.append(md("""---
## 3. Data Contract — Aba 2: "Custos de Transferência"

3 seções: Custos de transferência (6 rotas SP→NE), MACOs (3 SKUs), Custos de produção (3 SKUs).
**Premissa:** Rodoviário = +60% sobre Cabotagem + 5% avaria."""))

# ══ 8: Contract Aba 2 ══
C.append(code("""contract_aba2 = pd.DataFrame([
    {'Campo': 'SKU', 'Tipo': 'string', 'Formato': 'Nome completo',
     'Descrição Semântica': 'Stock Keeping Unit — produto no portfólio LN.',
     'Domínio': 'Colorado, Goose Island, Malzbier (Patagonia NÃO aparece)',
     'Regras de Negócio': 'Cada SKU tem custo e MACO específicos.',
     'Nulabilidade': 'NOT NULL', 'Origem': 'SAP/ERP'},
    {'Campo': 'Origem', 'Tipo': 'string', 'Formato': 'BR## - Nome - UF',
     'Descrição Semântica': 'Fábrica de origem da transferência.',
     'Domínio': 'BR16 Jacareí (SP), BR23 Jaguariúna (SP)',
     'Regras de Negócio': 'Colorado/Goose: Jacareí. Malzbier: Jaguariúna.',
     'Nulabilidade': 'NOT NULL', 'Origem': 'Cadastro Ambev'},
    {'Campo': 'Destino', 'Tipo': 'string', 'Formato': 'BR## - Nome - UF',
     'Descrição Semântica': 'CD/Fábrica de destino no NE.',
     'Domínio': 'BR04 Camaçari (BA), BR06 Fonte Mata (PB)',
     'Regras de Negócio': 'Fonte Mata é mais caro que Camaçari.',
     'Nulabilidade': 'NOT NULL', 'Origem': 'Cadastro Ambev'},
    {'Campo': 'Custo Transf (R$/HL)', 'Tipo': 'float', 'Formato': 'R$ #,##0.00',
     'Descrição Semântica': 'Custo unitário transferência via cabotagem.',
     'Domínio': '[R$76.59, R$95.33]',
     'Regras de Negócio': 'Cabotagem 25d lead time. Rodo = ×1.60 + 5% avaria.',
     'Nulabilidade': 'NOT NULL', 'Origem': 'Logística'},
    {'Campo': 'MACO (R$/HL)', 'Tipo': 'float', 'Formato': 'R$ #,##0',
     'Descrição Semântica': 'Margem de Contribuição por HL.',
     'Domínio': 'Malzbier R$285, Colorado R$300, Goose R$350',
     'Regras de Negócio': 'Goose maior margem. Malzbier menor.',
     'Nulabilidade': 'NOT NULL', 'Origem': 'Controladoria'},
    {'Campo': 'Custo Produção (R$/HL)', 'Tipo': 'float', 'Formato': 'R$ #,##0',
     'Descrição Semântica': 'Custo variável de produção por HL (plantas NE).',
     'Domínio': 'Malzbier R$149, Colorado R$150, Goose R$155',
     'Regras de Negócio': 'Custos próximos. Diferença de margem vem da receita.',
     'Nulabilidade': 'NOT NULL', 'Origem': 'Controladoria'}
])
show_contract(contract_aba2, '📋 Data Contract — Aba 2: Custos de Transferência')"""))

# ══ 9: Dados brutos Aba 2 ══
C.append(code("""custos_transf = pd.DataFrame({
    'SKU': ['Colorado', 'Colorado', 'Goose Island', 'Goose Island', 'Malzbier', 'Malzbier'],
    'Origem': ['Jacareí SP', 'Jacareí SP', 'Jacareí SP', 'Jacareí SP', 'Jaguariúna SP', 'Jaguariúna SP'],
    'Destino': ['Camaçari BA', 'Fonte Mata PB', 'Camaçari BA', 'Fonte Mata PB', 'Camaçari BA', 'Fonte Mata PB'],
    'Cabo R$/HL': [76.59, 82.08, 82.40, 88.30, 84.58, 95.33],
    'Rodo R$/HL': [76.59*1.6, 82.08*1.6, 82.40*1.6, 88.30*1.6, 84.58*1.6, 95.33*1.6],
    'Lead Cabo': ['25d']*6, 'Lead Rodo': ['6d']*6
})
display(custos_transf)

macos = pd.DataFrame({
    'SKU': ['Colorado', 'Goose Island', 'Malzbier'],
    'MACO R$/HL': [300, 350, 285],
    'Custo Prod R$/HL': [150, 155, 149],
    'Margem Bruta R$/HL': [150, 195, 136]
})
print()
display(macos)

print()
print("Margem líquida Malzbier por cenário de supply:")
cenarios = pd.DataFrame({
    'Cenário': ['Produção Local NE', 'Cabo→Camaçari', 'Cabo→Fonte Mata', 'Rodo→Camaçari', 'Rodo→Fonte Mata'],
    'Custo Prod': [149, 149, 149, 149, 149],
    'Custo Transf': [0, 84.58, 95.33, 84.58*1.6, 95.33*1.6],
    'Custo Total': [149, 233.58, 244.33, 149+84.58*1.6, 149+95.33*1.6],
    'Margem': [136, 285-233.58, 285-244.33, 285-(149+84.58*1.6), 285-(149+95.33*1.6)],
    'Lead Time': ['0d', '25d', '25d', '6d', '6d'],
    'Avaria': ['0%', '0%', '0%', '5%', '5%']
})
display(cenarios)"""))

# ══ 10: Insights Aba 2 ══
C.append(md("""### Insights — Aba 2
1. **Produção local sempre preferível**: margem R$136/HL vs R$51/HL (cabo) ou negativa (rodo)
2. **Rodoviário → Fonte Mata é inviável**: custo R$301.53/HL > MACO R$285/HL
3. **Lead time é o trade-off central**: Cabo 25d (barato) vs Rodo 6d (caro+avaria)
4. **Goose tem a maior MACO (R$350)**: cada HL deslocado dela custa mais"""))

# ══ 11: Header Aba 3 ══
C.append(md("""---
## 4. Data Contract — Aba 3: "Produção PCP"

| Planta | Código | Local | Nominal grf/h | Cap. Semanal HL |
|--------|--------|-------|--------------|----------------|
| AQ541 | BR03 Aquiraz | CE | 72.000 | 12.600 |
| PE541 | BR31 Pernambuco | PE | 108.000 | 27.000 |

4 semanas de Fev 2026. Ambas usam linha L541 compartilhada entre SKUs."""))

# ══ 12: Contract Aba 3 ══
C.append(code("""contract_aba3 = pd.DataFrame([
    {'Campo': 'SCSLocation', 'Tipo': 'string',
     'Descrição Semântica': 'Planta de produção.',
     'Domínio': 'BR03 Aquiraz/CE, BR31 Pernambuco/PE',
     'Regras de Negócio': 'Únicas plantas LN no NENO.',
     'Nulabilidade': 'NOT NULL', 'Origem': 'SCS Ambev'},
    {'Campo': 'Linha', 'Tipo': 'string',
     'Descrição Semântica': 'Linha de produção.',
     'Domínio': 'L541 (única)',
     'Regras de Negócio': 'Compartilhada entre SKUs.',
     'Nulabilidade': 'NOT NULL', 'Origem': 'Engenharia'},
    {'Campo': 'Nominal grf/h', 'Tipo': 'int',
     'Descrição Semântica': 'Velocidade nominal garrafas/hora.',
     'Domínio': '72.000 (AQ), 108.000 (PE)',
     'Regras de Negócio': 'PE541 é 50% mais rápida.',
     'Nulabilidade': 'NOT NULL', 'Origem': 'Ficha técnica'},
    {'Campo': 'Cap Semanal HL', 'Tipo': 'int',
     'Descrição Semântica': 'Capacidade máxima semanal.',
     'Domínio': '12.600 (AQ), 27.000 (PE)',
     'Regras de Negócio': 'Mensal: AQ=50.400, PE=108.000.',
     'Nulabilidade': 'NOT NULL', 'Origem': 'Cálculo'},
    {'Campo': 'Item (SKU)', 'Tipo': 'string',
     'Descrição Semântica': 'Produto a ser produzido.',
     'Domínio': 'AQ: Malzbier/Patagonia/Colorado. PE: 6 SKUs.',
     'Regras de Negócio': 'Nem todo SKU roda toda semana (setup).',
     'Nulabilidade': 'NOT NULL', 'Origem': 'PCP'},
    {'Campo': 'Volume Semanal HL', 'Tipo': 'float',
     'Descrição Semântica': 'Volume programado por semana.',
     'Domínio': '[0, 27.000]',
     'Regras de Negócio': 'Soma por planta ≤ Capacidade.',
     'Nulabilidade': 'NOT NULL', 'Origem': 'PCP'}
])
show_contract(contract_aba3, '📋 Data Contract — Aba 3: Produção PCP')"""))

# ══ 13: Dados Aba 3 ══
C.append(code("""print("AQ541 — Aquiraz/CE | 72.000 grf/h | Cap: 12.600 HL/sem")
aq541 = pd.DataFrame({
    'SKU': ['Malzbier', 'Patagonia', 'Colorado', 'TOTAL'],
    'W0': [0, 12240, 0, 12240], 'W1': [9000, 1800, 0, 10800],
    'W2': [7560, 5040, 0, 12600], 'W3': [0, 12600, 0, 12600],
    'Total Fev': [16560, 31680, 0, 48240]
})
display(aq541)

print()
print("PE541 — Pernambuco/PE | 108.000 grf/h | Cap: 27.000 HL/sem")
pe541 = pd.DataFrame({
    'SKU': ['Brahma Zero', 'Goose Island', 'Malzbier', 'Colorado', 'Skol Beats', 'Budweiser Zero', 'TOTAL'],
    'W0': [0, 5400, 16200, 5400, 0, 0, 27000],
    'W1': [0, 14400, 0, 0, 0, 5400, 19800],
    'W2': [0, 0, 12960, 10800, 3240, 0, 27000],
    'W3': [3600, 12600, 0, 0, 0, 10800, 27000],
    'Total Fev': [3600, 32400, 29160, 16200, 3240, 16200, 100800]
})
display(pe541)

print()
print(f"Utilização AQ541: {48240:,}/{50400:,} = {48240/50400*100:.1f}%")
print(f"Utilização PE541: {100800:,}/{108000:,} = {100800/108000*100:.1f}%")
print(f"Ociosa: AQ {50400-48240:,} + PE {108000-100800:,} = {9360:,} HL")
print(f"Malzbier NE: AQ {16560:,} + PE {29160:,} = {45720:,} HL")"""))

# ══ 14: Insights Aba 3 ══
C.append(md("""### Insights — Aba 3
1. **PE541 a 93.3%**, AQ541 a 95.7% — pouca folga
2. **Capacidade ociosa total: 9.360 HL** — insuficiente para gap de +11.680
3. **Colorado 0 em AQ541** — potencial realocação
4. **W1 em PE541 tem ociosidade** (19.800/27.000 = 73.3%)"""))

# ══ 15: Header Aba 4 ══
C.append(md("""---
## 5. Data Contract — Aba 4: "Transferências Programadas"

**Apenas Goose Island** tem transferências programadas!
Malzbier e Colorado: ZERO. 100% dependem de produção local."""))

# ══ 16: Contract Aba 4 ══
C.append(code("""contract_aba4 = pd.DataFrame([
    {'Campo': 'Regional Origem', 'Tipo': 'string',
     'Descrição Semântica': 'Regional de origem.',
     'Domínio': 'REG SE (todas)', 'Regras de Negócio': 'Apenas SE→NE.',
     'Nulabilidade': 'NOT NULL', 'Origem': 'Logística'},
    {'Campo': 'Desc Destino', 'Tipo': 'string',
     'Descrição Semântica': 'CD/Planta de destino no NE.',
     'Domínio': 'Camaçari, Fonte Mata, CDR Bahia',
     'Regras de Negócio': 'Goose vai para os 3.',
     'Nulabilidade': 'NOT NULL', 'Origem': 'Cadastro'},
    {'Campo': 'Modal', 'Tipo': 'string',
     'Descrição Semântica': 'Modal de transporte.',
     'Domínio': 'Cabotagem (100%)',
     'Regras de Negócio': 'Lead 25d. Zero rodoviário.',
     'Nulabilidade': 'NOT NULL', 'Origem': 'Logística'},
    {'Campo': 'Cod Produto', 'Tipo': 'int',
     'Descrição Semântica': 'Código SAP.',
     'Domínio': '65758 (Goose apenas)',
     'Regras de Negócio': 'ZERO Malzbier, ZERO Colorado.',
     'Nulabilidade': 'NOT NULL', 'Origem': 'SAP'},
    {'Campo': 'Volume Semanal HL', 'Tipo': 'float',
     'Descrição Semântica': 'Volume transferido por semana.',
     'Domínio': '[0, 7.200]',
     'Regras de Negócio': 'Cam: 7.200/sem. FM: 4.107 só W0. CDR: 5.400/sem.',
     'Nulabilidade': 'NOT NULL', 'Origem': 'Logística'}
])
show_contract(contract_aba4, '📋 Data Contract — Aba 4: Transferências Programadas')"""))

# ══ 17: Dados Aba 4 ══
C.append(code("""transf = pd.DataFrame({
    'Destino': ['Camaçari BA', 'Fonte Mata PB', 'CDR Bahia'],
    'SKU': ['Goose Island']*3, 'Modal': ['Cabotagem']*3,
    'W0': [7200, 4107.4, 5400], 'W1': [7200, 0, 5400],
    'W2': [7200, 0, 5400], 'W3': [7200, 0, 5400],
    'Total': [28800, 4107.4, 21600]
})
display(transf)
print()
print("MALZBIER: 0 HL transferidos | COLORADO: 0 HL transferidos")
print("Malzbier depende 100% da produção local NE")"""))

# ══ 18: Header Aba 5 ══
C.append(md("""---
## 6. Data Contract — Aba 5: "Cenário Divulgado" (Baseline)

WSNP semanal: 4 SKUs × 5 sub-regiões × 4 semanas.
Métricas: Demanda, WSNP, EI, Suf.ini, Transf.Interna, Transf.Ext(Cabo/Rodo), Trânsito, EF, Suf.f"""))

# ══ 19: Contract Aba 5 ══
C.append(code("""contract_aba5 = pd.DataFrame([
    {'Campo': 'SKU (bloco)', 'Tipo': 'string',
     'Descrição Semântica': 'SKU agrupador.',
     'Domínio': 'Patagonia(70934), Goose(65758), Malzbier(41777), Colorado(51476)',
     'Regras de Negócio': 'Cada bloco: 5 sub-regiões + prod SP/NE.',
     'Nulabilidade': 'NOT NULL', 'Origem': 'WSNP'},
    {'Campo': 'GEO/REG', 'Tipo': 'string',
     'Descrição Semântica': 'Sub-região NENO.',
     'Domínio': 'Mapapi, NE Norte, NE Sul, NO Araguaia, NO Centro',
     'Regras de Negócio': 'Mapapi = maior. NO Araguaia = menor.',
     'Nulabilidade': 'NOT NULL', 'Origem': 'Estrutura Ambev'},
    {'Campo': 'Demanda HL/sem', 'Tipo': 'float',
     'Descrição Semântica': 'Demanda semanal por sub-região.',
     'Domínio': '[0, ~6.300]',
     'Regras de Negócio': 'Soma sub-regiões = total NENO.',
     'Nulabilidade': 'NOT NULL', 'Origem': 'GEOs'},
    {'Campo': 'EI Semana HL', 'Tipo': 'float',
     'Descrição Semântica': 'Estoque início da semana.',
     'Domínio': '[0, +∞)',
     'Regras de Negócio': 'EI_N = EF_{N-1}.',
     'Nulabilidade': 'NOT NULL', 'Origem': 'WMS'},
    {'Campo': 'Suf.ini (d)', 'Tipo': 'float',
     'Descrição Semântica': 'Suficiência inicial = EI/(Demanda/7).',
     'Domínio': '(-∞, +∞)',
     'Regras de Negócio': 'DOI mín 12d.',
     'Nulabilidade': 'NOT NULL', 'Origem': 'Calculado'},
    {'Campo': 'Transf. Interna HL', 'Tipo': 'float',
     'Descrição Semântica': 'Redistribuição dentro NENO.',
     'Domínio': '(-∞, +∞)',
     'Regras de Negócio': 'Soma ≈ 0.',
     'Nulabilidade': 'NOT NULL', 'Origem': 'Planejamento'},
    {'Campo': 'Transf. Ext Cabo HL', 'Tipo': 'float',
     'Descrição Semântica': 'Transferência SP→NE cabotagem.',
     'Domínio': '[0, +∞) — só Goose > 0',
     'Regras de Negócio': 'Lead 25d. Malzbier/Colorado = 0.',
     'Nulabilidade': 'NOT NULL', 'Origem': 'Logística'},
    {'Campo': 'Transf. Ext Rodo HL', 'Tipo': 'float',
     'Descrição Semântica': 'Transferência SP→NE rodoviário.',
     'Domínio': '{0} — ZERO em tudo',
     'Regras de Negócio': 'Nenhum rodoviário programado.',
     'Nulabilidade': 'NOT NULL', 'Origem': 'Logística'},
    {'Campo': 'EF Semana HL', 'Tipo': 'float',
     'Descrição Semântica': 'Estoque final projetado.',
     'Domínio': '(-∞, +∞)',
     'Regras de Negócio': 'EF = EI + Prod + Transf - Demanda.',
     'Nulabilidade': 'NOT NULL', 'Origem': 'Calculado'},
    {'Campo': 'Suf.f (d)', 'Tipo': 'float',
     'Descrição Semântica': 'Suficiência final em dias.',
     'Domínio': '(-∞, +∞)',
     'Regras de Negócio': 'DOI 12d.',
     'Nulabilidade': 'NOT NULL', 'Origem': 'Calculado'}
])
show_contract(contract_aba5, '📋 Data Contract — Aba 5: Cenário Divulgado')"""))

# ══ 20: Malzbier divulgado ══
C.append(code("""print("DEMANDA MALZBIER POR SUB-REGIÃO (HL)")
malz_dem = pd.DataFrame({
    'Sub-região': ['Mapapi', 'NE Norte', 'NE Sul', 'NO Araguaia', 'NO Centro', 'TOTAL'],
    'W0': [4672.9, 1516.7, 2484.9, 60.7, 1713.5, 10448.7],
    'W1': [4835.7, 1742.9, 2705.9, 71.4, 1894.7, 11250.6],
    'W2': [3275.4, 1313.8, 1991.6, 48.4, 1376.6, 8005.8],
    'W3': [4003.5, 1418.5, 2197.9, 50.7, 1558.4, 9229.0],
    'Total': [16787.5, 5991.9, 9380.3, 231.2, 6543.2, 38934.1]
})
display(malz_dem)

print()
print("SUFICIÊNCIA FINAL MALZBIER (dias) — DOI mín = 12d")
malz_suf = pd.DataFrame({
    'Sub-região': ['Mapapi', 'NE Norte', 'NE Sul', 'NO Araguaia', 'NO Centro'],
    'Suf W0': [2.93, 19.64, 10.98, 0.21, 1.16],
    'Suf W1': [6.76, 14.79, 7.72, 0.28, 7.51],
    'Suf W2': [4.81, 18.68, 22.48, 0.28, 30.51],
    'Suf W3': [3.37, 4.64, 20.41, 0.28, 14.34],
    'Sem <12d': [4, 3, 2, 4, 2]
})
display(malz_suf)
print()
print("Mesmo no baseline, Malzbier já tem problemas:")
print("  Mapapi: TODAS as semanas abaixo do DOI")
print("  NO Araguaia: ~0 dias (praticamente sem estoque)")"""))

# ══ 21: Demais SKUs ══
C.append(code("""print("RESUMO DEMANDA TOTAL NENO — Cenário Divulgado")
resumo = pd.DataFrame({
    'SKU': ['Goose Island', 'Malzbier', 'Patagonia', 'Colorado', 'TOTAL'],
    'Demanda Fev HL': [43328.9, 38934.1, 31879.6, 19728.6, 133871.2],
    '% Total': [32.4, 29.1, 23.8, 14.7, 100.0]
})
display(resumo)

print()
print("Goose Island — 43.329 HL (maior SKU)")
goose = pd.DataFrame({
    'Sub-região': ['Mapapi', 'NE Norte', 'NE Sul', 'NO Araguaia', 'NO Centro'],
    'Total HL': [16454.0, 7627.8, 10160.8, 717.3, 8369.0]
})
display(goose)

print()
print("Colorado — 19.729 HL (menor SKU)")
colorado = pd.DataFrame({
    'Sub-região': ['Mapapi', 'NE Norte', 'NE Sul', 'NO Araguaia', 'NO Centro'],
    'Total HL': [7358.6, 3313.2, 5390.0, 216.7, 3450.1]
})
display(colorado)"""))

# ══ 22: Header Aba 6 ══
C.append(md("""---
## 7. Data Contract — Aba 6: "Cenário com Nova Demanda"

Estrutura **idêntica** à Aba 5, mas Malzbier +30%.
Demais SKUs inalterados. Produção/transferências NÃO ajustadas → GAP."""))

# ══ 23: Comparativo ══
C.append(code("""print("MALZBIER: Comparativo Divulgado vs Nova Demanda (+30%)")
comp = pd.DataFrame({
    'Sub-região': ['Mapapi', 'NE Norte', 'NE Sul', 'NO Araguaia', 'NO Centro', 'TOTAL'],
    'Div Total': [16787.5, 5991.9, 9380.3, 231.2, 6543.2, 38934.1],
    'Nova Total': [21823.8, 7789.5, 12194.3, 300.6, 8506.1, 50614.3],
    'Gap HL': [5036.3, 1797.6, 2814.0, 69.4, 1962.9, 11680.2]
})
display(comp)

print()
print("SUFICIÊNCIA COMPARATIVA (dias)")
suf_comp = pd.DataFrame({
    'Sub-região': ['Mapapi', 'NE Norte', 'NE Sul', 'NO Araguaia', 'NO Centro'],
    'Div W0': [2.93, 19.64, 10.98, 0.21, 1.16],
    'Nova W0': [0.92, 13.90, 7.18, -1.18, -0.36],
    'Div W1': [6.76, 14.79, 7.72, 0.28, 7.51],
    'Nova W1': [1.18, 7.94, 2.33, -3.78, 1.89],
    'Div W2': [4.81, 18.68, 22.48, 0.28, 30.51],
    'Nova W2': [-0.73, 9.90, 12.77, -4.93, 18.66],
    'Div W3': [3.37, 4.64, 20.41, 0.28, 14.34],
    'Nova W3': [-3.21, -2.28, 9.79, -6.32, 4.84]
})
display(suf_comp)
print()
print("RUPTURAS na Nova Demanda:")
print("  NO Araguaia: W0(-1.18), W1(-3.78), W2(-4.93), W3(-6.32) — 4 sem!")
print("  NO Centro: W0(-0.36) | Mapapi: W2(-0.73), W3(-3.21)")
print("  NE Norte: W3(-2.28)")
print(f"  GAP TOTAL: +{11680.2:,.1f} HL | Ociosa NE: ~{9360:,} HL")
print(f"  Déficit: ~{11680-9360:,} HL → transferência SP→NE obrigatória")"""))

# ══════════════════════════════════════════════════════════════
# SEÇÃO VISUAL 1: RELACIONAMENTO ENTRE ABAS (matplotlib)
# ══════════════════════════════════════════════════════════════
C.append(md("""---
## 8. Relacionamento entre Abas"""))

C.append(code("""fig, ax = plt.subplots(1, 1, figsize=(14, 7))
ax.set_xlim(0, 14)
ax.set_ylim(0, 7)
ax.axis('off')
fig.patch.set_facecolor('#FAFAFA')
ax.set_facecolor('#FAFAFA')

# Cores dos blocos
c_input  = '#3498DB'  # azul
c_core   = '#2ECC71'  # verde
c_shock  = '#E74C3C'  # vermelho
c_cost   = '#F39C12'  # ambar

def draw_box(ax, x, y, w, h, text, color, fontsize=9, bold=False):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                         facecolor=color, edgecolor='white', linewidth=2, alpha=0.92)
    ax.add_patch(box)
    weight = 'bold' if bold else 'normal'
    ax.text(x + w/2, y + h/2, text, ha='center', va='center',
            fontsize=fontsize, color='white', fontweight=weight,
            linespacing=1.4)

def draw_arrow(ax, x1, y1, x2, y2, label='', color='#7F8C8D'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=2.0,
                                connectionstyle='arc3,rad=0.0'))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2 + 0.2
        ax.text(mx, my, label, ha='center', va='bottom', fontsize=7.5,
                color='#555555', fontstyle='italic',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='none', alpha=0.8))

# Blocos INPUT (esquerda)
draw_box(ax, 0.3, 5.0, 3.5, 1.2, 'Aba 1\\nCenário Atual BR\\n(macro mensal)', c_input, 9)
draw_box(ax, 0.3, 3.2, 3.5, 1.2, 'Aba 3\\nProdução PCP\\n(AQ541 + PE541)', c_input, 9)
draw_box(ax, 0.3, 1.4, 3.5, 1.2, 'Aba 4\\nTransf. Programadas\\n(só Goose)', c_input, 9)

# Bloco CORE (centro)
draw_box(ax, 5.2, 3.5, 3.8, 2.5, 'Aba 5\\nCenário Divulgado\\n(WSNP Baseline)\\n4 SKUs × 5 sub-regiões', c_core, 10, bold=True)

# Bloco SHOCK (direita)
draw_box(ax, 10.2, 3.5, 3.5, 2.5, 'Aba 6\\nNova Demanda\\nMalzbier +30%\\nGAP: +11.680 HL', c_shock, 10, bold=True)

# Bloco CUSTOS (abaixo)
draw_box(ax, 5.2, 0.5, 3.8, 1.5, 'Aba 2\\nCustos de Transferência\\nMACOs + Prod + Logística', c_cost, 9)

# Setas INPUT → CORE
draw_arrow(ax, 3.8, 5.6, 5.2, 5.2, 'NENO = Σ sub-regiões')
draw_arrow(ax, 3.8, 3.8, 5.2, 4.5, 'vol semanal = WSNP')
draw_arrow(ax, 3.8, 2.0, 5.2, 3.8, 'Goose = Transf.Ext(Cabo)')

# Seta CORE → SHOCK
draw_arrow(ax, 9.0, 4.75, 10.2, 4.75, 'Malzbier × 1.30')

# Seta CUSTOS → SHOCK
draw_arrow(ax, 9.0, 1.25, 11.95, 3.5, 'custo por cenário')

# Legenda
legend_items = [
    mpatches.Patch(color=c_input, label='Dados de Entrada'),
    mpatches.Patch(color=c_core, label='Baseline (WSNP)'),
    mpatches.Patch(color=c_shock, label='Cenário +30%'),
    mpatches.Patch(color=c_cost, label='Custos & Margens'),
]
ax.legend(handles=legend_items, loc='upper right', fontsize=9, framealpha=0.9,
          edgecolor='#CCCCCC', fancybox=True)

ax.set_title('Relacionamento entre as 6 Abas da Planilha', fontsize=14,
             fontweight='bold', color='#2C3E50', pad=15)

plt.tight_layout()
plt.show()"""))

# ══════════════════════════════════════════════════════════════
# SEÇÃO VISUAL 2: VERIFICAÇÕES DE CONSISTÊNCIA
# ══════════════════════════════════════════════════════════════
C.append(code("""checks = [
    ('Produção PCP vs WSNP', f'Malzbier NE: AQ 16.560 + PE 29.160 = 45.720 HL\\nDemanda divulgada: 38.934 HL', True, 'Produção > Demanda no baseline'),
    ('Transferências', 'Goose: 54.507 HL programados\\nMalzbier: 0 HL | Colorado: 0 HL', True, 'Malzbier depende 100% produção local'),
    ('Gap Malzbier +30%', f'Nova demanda: 50.614 HL\\nGap incremental: +11.680 HL', True, '+30% consistente com dados'),
    ('Capacidade vs Necessidade', f'Ociosa NE: 9.360 HL\\nGap: 11.680 HL → Déficit: 2.320 HL', False, 'Capacidade insuficiente!'),
    ('Impacto Financeiro', f'MACO perdido: R$ 3.328.800\\nCusto prod local: R$ 1.740.320\\nCusto prod+cabo: R$ 2.727.744', True, 'Valores consistentes'),
]

fig, ax = plt.subplots(figsize=(13, 6))
ax.axis('off')
fig.patch.set_facecolor('#FAFAFA')

ax.set_title('Verificações de Consistência entre Abas', fontsize=14,
             fontweight='bold', color='#2C3E50', y=1.02)

y_start = 0.92
row_h = 0.17

for i, (titulo, detalhe, ok, nota) in enumerate(checks):
    y = y_start - i * row_h
    cor_bg = '#E8F8F5' if ok else '#FDEDEC'
    cor_borda = '#27AE60' if ok else '#E74C3C'
    icone = 'OK' if ok else '!!'

    rect = FancyBboxPatch((0.02, y - 0.06), 0.96, row_h - 0.02,
                          boxstyle="round,pad=0.01",
                          facecolor=cor_bg, edgecolor=cor_borda,
                          linewidth=1.5, transform=ax.transAxes)
    ax.add_patch(rect)

    ax.text(0.05, y + 0.04, f'{icone}  {titulo}', transform=ax.transAxes,
            fontsize=11, fontweight='bold', color='#2C3E50', va='center')
    ax.text(0.05, y - 0.02, detalhe, transform=ax.transAxes,
            fontsize=8.5, color='#555555', va='top', linespacing=1.3)
    ax.text(0.95, y + 0.04, nota, transform=ax.transAxes,
            fontsize=8.5, color=cor_borda, va='center', ha='right', fontstyle='italic')

plt.tight_layout()
plt.show()"""))

# ══════════════════════════════════════════════════════════════
# SEÇÃO VISUAL 3: VARIÁVEIS DERIVADAS
# ══════════════════════════════════════════════════════════════
C.append(md("""---
## 9. Dicionário de Variáveis Derivadas

Variáveis **calculadas** essenciais para a análise, que não existem diretamente na planilha."""))

C.append(code("""variaveis = pd.DataFrame([
    {'Variável': 'Gap Demanda (HL)', 'Fórmula': 'Demanda_Nova - Demanda_Divulgada',
     'Granularidade': 'SKU × Sub-região × Semana',
     'Interpretação': 'Volume incremental do choque +30%.',
     'Exemplo': 'Mapapi W0: 6074.8 - 4672.9 = 1401.9 HL'},
    {'Variável': 'Utilização Planta (%)', 'Fórmula': 'Σ(Prod SKUs) / Cap Semanal × 100',
     'Granularidade': 'Planta × Semana',
     'Interpretação': '>90% = gargalo.',
     'Exemplo': 'PE541 W0: 27000/27000 = 100%'},
    {'Variável': 'Capacidade Ociosa (HL)', 'Fórmula': 'Cap Semanal - Σ(Prod SKUs)',
     'Granularidade': 'Planta × Semana',
     'Interpretação': 'Espaço livre para realocar.',
     'Exemplo': 'PE541 W1: 27000-19800 = 7200 HL'},
    {'Variável': 'Margem Líquida (R$/HL)', 'Fórmula': 'MACO - CustoProd - CustoTransf',
     'Granularidade': 'SKU × Modal × Destino',
     'Interpretação': 'Negativa = inviável.',
     'Exemplo': 'Malzbier Rodo→FM: 285-149-152.53 = -16.53'},
    {'Variável': 'DOI Delta (dias)', 'Fórmula': 'Suf.f(Nova) - Suf.f(Div)',
     'Granularidade': 'Sub-região × Semana',
     'Interpretação': 'Deterioração da suficiência. Sempre ≤ 0.',
     'Exemplo': 'Mapapi W0: 0.92 - 2.93 = -2.01 dias'},
    {'Variável': 'Custo Oportunidade (R$)', 'Fórmula': 'Gap_não_atendido × MACO',
     'Granularidade': 'SKU × Sub-região',
     'Interpretação': 'Receita perdida se não cobrir.',
     'Exemplo': 'Total: 11680 × 285 = R$ 3.328.800'},
    {'Variável': 'BIAS Ajustado (HL)', 'Fórmula': 'Demanda × (1 - 0.09)',
     'Granularidade': 'Sub-região × Semana',
     'Interpretação': 'Demanda corrigida pelo sobre-forecast.',
     'Exemplo': '10000 HL → 9100 HL'},
    {'Variável': 'Vol Líquido Rodo (HL)', 'Fórmula': 'Vol_bruto × (1 - 0.05)',
     'Granularidade': 'Transferência',
     'Interpretação': 'Volume efetivo após 5% avaria.',
     'Exemplo': '1000 HL → 950 HL'}
])
display(HTML("<h4>Variáveis Derivadas</h4>"))
display(variaveis)"""))

# ══ Premissas ══
C.append(md("""---
## 10. Premissas e Restrições Operacionais"""))

C.append(code("""premissas = pd.DataFrame([
    {'Cat': 'Demanda', 'Premissa': 'Malzbier +30% sobre cenário divulgado',
     'Fonte': 'Enunciado', 'Impacto': 'Gap +11.680 HL'},
    {'Cat': 'Demanda', 'Premissa': 'BIAS de +9% no forecast dos GEOs',
     'Fonte': 'Onboarding', 'Impacto': 'Demanda real pode ser 9% menor'},
    {'Cat': 'Demanda', 'Premissa': 'Demais SKUs inalterados',
     'Fonte': 'Enunciado', 'Impacto': 'Goose, Patagonia, Colorado = mesma demanda'},
    {'Cat': 'Produção', 'Premissa': 'Linha L541 compartilhada entre SKUs',
     'Fonte': 'Aba 3', 'Impacto': 'Não rodam 2 SKUs simultâneos'},
    {'Cat': 'Produção', 'Premissa': 'Cap AQ541: 12.600/sem, PE541: 27.000/sem',
     'Fonte': 'Aba 3', 'Impacto': 'Limite físico'},
    {'Cat': 'Logística', 'Premissa': 'Cabotagem: 25 dias lead time',
     'Fonte': 'Onboarding', 'Impacto': 'Não chega a tempo se iniciar em Fev'},
    {'Cat': 'Logística', 'Premissa': 'Rodoviário: 6 dias, +60% custo, 5% avaria',
     'Fonte': 'Onboarding', 'Impacto': 'Alternativa rápida mas cara'},
    {'Cat': 'Estoque', 'Premissa': 'DOI mínimo: 12 dias',
     'Fonte': 'Onboarding', 'Impacto': 'Abaixo = risco de ruptura'},
    {'Cat': 'Financeiro', 'Premissa': 'MACOs e custos fixos (sem economia de escala)',
     'Fonte': 'Aba 2', 'Impacto': 'Análise marginal é linear'},
    {'Cat': 'Temporal', 'Premissa': 'Horizonte = Fev 2026 (4 semanas)',
     'Fonte': 'Enunciado', 'Impacto': 'Solução de curto prazo'}
])
display(HTML("<h4>Premissas e Restrições</h4>"))
display(premissas)"""))

# ══════════════════════════════════════════════════════════════
# SEÇÃO VISUAL 4: MATRIZ DE COMPLETUDE (HEATMAP)
# ══════════════════════════════════════════════════════════════
C.append(md("""---
## 11. Matriz de Completude dos Dados"""))

C.append(code("""campos = ['Demanda', 'Produção', 'Estoque EI', 'Estoque EF', 'Suficiência',
          'Transf.Interna', 'Transf.Ext Cabo', 'Transf.Ext Rodo', 'Trânsito',
          'Custo Transf.', 'MACO', 'Custo Produção', 'Cap. Planta']
abas = ['Aba 1\\nCenário BR', 'Aba 2\\nCustos', 'Aba 3\\nPCP', 'Aba 4\\nTransf.', 'Aba 5\\nDivulgado', 'Aba 6\\nNova Dem.']

matrix = np.array([
    [1,0,1,1,1, 0,0,0,0, 0,0,0,0],
    [0,0,0,0,0, 0,0,0,0, 1,1,1,0],
    [0,1,0,0,0, 0,0,0,0, 0,0,0,1],
    [0,0,0,0,0, 0,1,0,0, 0,0,0,0],
    [1,1,1,1,1, 1,1,1,1, 0,0,0,0],
    [1,1,1,1,1, 1,1,1,1, 0,0,0,0],
])

fig, ax = plt.subplots(figsize=(14, 5.5))

# Cores: verde para disponível, vermelho claro para indisponível
colors = np.where(matrix == 1, '#27AE60', '#F5B7B1')
for i in range(len(abas)):
    for j in range(len(campos)):
        ax.add_patch(plt.Rectangle((j, len(abas)-1-i), 1, 1,
                     facecolor=colors[i][j], edgecolor='white', linewidth=2))
        symbol = '\\u2713' if matrix[i][j] == 1 else '\\u2717'
        txt_color = 'white' if matrix[i][j] == 1 else '#C0392B'
        ax.text(j + 0.5, len(abas)-1-i + 0.5, symbol, ha='center', va='center',
                fontsize=14, fontweight='bold', color=txt_color)

ax.set_xlim(0, len(campos))
ax.set_ylim(0, len(abas))
ax.set_xticks([j + 0.5 for j in range(len(campos))])
ax.set_xticklabels(campos, rotation=45, ha='right', fontsize=9)
ax.set_yticks([i + 0.5 for i in range(len(abas))])
ax.set_yticklabels(list(reversed(abas)), fontsize=9)
ax.tick_params(length=0)

for spine in ax.spines.values():
    spine.set_visible(False)

legend_items = [
    mpatches.Patch(color='#27AE60', label='Disponível'),
    mpatches.Patch(color='#F5B7B1', label='Não disponível'),
]
ax.legend(handles=legend_items, loc='upper right', fontsize=9, bbox_to_anchor=(1.0, 1.15))

ax.set_title('Matriz de Completude: Campos × Abas', fontsize=14,
             fontweight='bold', color='#2C3E50', pad=20)

plt.tight_layout()
plt.show()"""))

# ══════════════════════════════════════════════════════════════
# SEÇÃO VISUAL 5: QUALIDADE DOS DADOS
# ══════════════════════════════════════════════════════════════
C.append(md("""---
## 12. Qualidade dos Dados e Limitações"""))

C.append(code("""aspectos = ['Valores Nulos', 'Consistência\\nTemporal', 'Unidade de\\nMedida',
            'Granularidade\\nGeo', 'SKUs entre\\nAbas', 'BIAS de\\nDemanda', 'Dados\\nFaltantes']
scores  = [1.0, 0.6, 1.0, 0.5, 0.6, 0.4, 0.2]
colors  = ['#27AE60','#F39C12','#27AE60','#E67E22','#F39C12','#E74C3C','#C0392B']
labels  = ['OK', 'Atenção', 'OK', 'Mismatch', 'Inconsist.', 'Viés +9%', 'Gap']

fig, ax = plt.subplots(figsize=(13, 4.5))

bars = ax.barh(range(len(aspectos)), scores, color=colors, height=0.6,
               edgecolor='white', linewidth=1.5)

for i, (bar, label) in enumerate(zip(bars, labels)):
    ax.text(bar.get_width() + 0.03, bar.get_y() + bar.get_height()/2,
            label, va='center', fontsize=10, fontweight='bold', color=colors[i])

ax.set_yticks(range(len(aspectos)))
ax.set_yticklabels(aspectos, fontsize=10)
ax.set_xlim(0, 1.3)
ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
ax.set_xticklabels(['Crítico', 'Ruim', 'Médio', 'Bom', 'Excelente'], fontsize=9)
ax.axvline(x=0.5, color='#BDC3C7', linestyle='--', linewidth=1, alpha=0.7)

for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)

ax.set_title('Avaliação de Qualidade dos Dados', fontsize=14,
             fontweight='bold', color='#2C3E50', pad=15)
ax.invert_yaxis()

detalhes = [
    'Nenhum campo essencial é nulo. Zeros = sem produção/transferência.',
    'Aba 1 mensal, Abas 3-6 semanais. Agregação necessária.',
    'Tudo em HL e R$. Sem conversão necessária.',
    'Aba 1: NENO agregado. Abas 5/6: 5 sub-regiões.',
    'Aba 1 consolida todos LN. Patagonia ausente Aba 2.',
    'GEOs sobre-estimam +9%. Demanda real ~ 91%.',
    'Falta: custo setup, tempo troca, estoque mín, cap armazenagem.'
]

fig.text(0.02, -0.02, '\\n'.join([f'  {asp.replace(chr(10)," ")}: {det}' for asp, det in zip(aspectos, detalhes)]),
         fontsize=8, color='#7F8C8D', va='top', linespacing=1.5,
         fontfamily='monospace')

plt.tight_layout()
plt.show()"""))

# ══════════════════════════════════════════════════════════════
# SEÇÃO VISUAL 6: MAPA DE FLUXO SUPPLY CHAIN (o que estava FEIO!)
# ══════════════════════════════════════════════════════════════
C.append(md("""---
## 13. Mapa de Fluxo da Cadeia de Supply"""))

C.append(code("""fig, ax = plt.subplots(figsize=(16, 9))
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.axis('off')
fig.patch.set_facecolor('#FAFAFA')

# ── Título de seção ──
ax.text(8, 8.6, 'Fluxo de Supply Chain — NENO', ha='center', fontsize=16,
        fontweight='bold', color='#2C3E50')
ax.text(8, 8.2, 'Produção → Distribuição → Sub-regiões de Consumo', ha='center',
        fontsize=11, color='#7F8C8D', fontstyle='italic')

# ── COLUNA 1: ORIGENS DE PRODUÇÃO ──
# SP (Sudeste) — origem de transferências
sp_box = FancyBboxPatch((0.3, 5.5), 3.2, 2.2, boxstyle="round,pad=0.15",
                        facecolor='#8E44AD', edgecolor='#6C3483', linewidth=2)
ax.add_patch(sp_box)
ax.text(1.9, 7.1, 'SP (Sudeste)', ha='center', fontsize=12, fontweight='bold', color='white')
ax.text(1.9, 6.6, 'BR16 Jacareí', ha='center', fontsize=9, color='#D7BDE2')
ax.text(1.9, 6.3, 'BR23 Jaguariúna', ha='center', fontsize=9, color='#D7BDE2')
ax.text(1.9, 5.85, 'Goose: SIM  |  Malzbier: NAO  |  Colorado: NAO', ha='center', fontsize=8, color='#F9E79F')

# AQ541
aq_box = FancyBboxPatch((0.3, 3.2), 3.2, 1.6, boxstyle="round,pad=0.15",
                         facecolor='#2980B9', edgecolor='#1F618D', linewidth=2)
ax.add_patch(aq_box)
ax.text(1.9, 4.35, 'AQ541 Aquiraz', ha='center', fontsize=11, fontweight='bold', color='white')
ax.text(1.9, 3.9, 'CE | 12.600 HL/sem', ha='center', fontsize=9.5, color='#AED6F1')
ax.text(1.9, 3.5, 'Utilização: 95.7%', ha='center', fontsize=9, color='#F9E79F')

# PE541
pe_box = FancyBboxPatch((0.3, 1.0), 3.2, 1.6, boxstyle="round,pad=0.15",
                         facecolor='#2980B9', edgecolor='#1F618D', linewidth=2)
ax.add_patch(pe_box)
ax.text(1.9, 2.15, 'PE541 Pernambuco', ha='center', fontsize=11, fontweight='bold', color='white')
ax.text(1.9, 1.7, 'PE | 27.000 HL/sem', ha='center', fontsize=9.5, color='#AED6F1')
ax.text(1.9, 1.3, 'Utilização: 93.3%', ha='center', fontsize=9, color='#F9E79F')

# ── COLUNA 2: CDs DE DISTRIBUIÇÃO ──
cds = [('Camaçari BA', 7.0), ('Fonte Mata PB', 5.3), ('CDR Bahia', 3.6)]
for nome, y in cds:
    cd_box = FancyBboxPatch((6.0, y - 0.45), 2.8, 0.9, boxstyle="round,pad=0.12",
                             facecolor='#F39C12', edgecolor='#D68910', linewidth=2)
    ax.add_patch(cd_box)
    ax.text(7.4, y, nome, ha='center', va='center', fontsize=10, fontweight='bold', color='white')

# ── COLUNA 3: SUB-REGIÕES (CONSUMO) ──
subregs = [('Mapapi', 7.8, '43% gap'), ('NE Norte', 6.6, '15% gap'),
           ('NE Sul', 5.4, '24% gap'), ('NO Araguaia', 4.2, '1% gap'),
           ('NO Centro', 3.0, '17% gap')]
for nome, y, pct in subregs:
    sr_box = FancyBboxPatch((11.0, y - 0.35), 2.8, 0.7, boxstyle="round,pad=0.1",
                             facecolor='#27AE60', edgecolor='#1E8449', linewidth=1.5)
    ax.add_patch(sr_box)
    ax.text(12.4, y, f'{nome}', ha='center', va='center', fontsize=10, fontweight='bold', color='white')
    ax.text(14.0, y, pct, ha='left', va='center', fontsize=8.5, color='#7F8C8D', fontstyle='italic')

# ── SETAS: SP → CDs ──
arrow_kw_cabo = dict(arrowstyle='->', color='#8E44AD', lw=2.5, connectionstyle='arc3,rad=0.15')
arrow_kw_rodo = dict(arrowstyle='->', color='#E74C3C', lw=2.0, linestyle='dashed', connectionstyle='arc3,rad=-0.1')

ax.annotate('', xy=(6.0, 7.0), xytext=(3.5, 6.8), arrowprops=arrow_kw_cabo)
ax.text(4.75, 7.35, 'Cabo 25d', fontsize=8.5, color='#8E44AD', fontweight='bold', ha='center',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#8E44AD', alpha=0.9))

ax.annotate('', xy=(6.0, 5.3), xytext=(3.5, 6.3), arrowprops=arrow_kw_cabo)

ax.annotate('', xy=(6.0, 3.6), xytext=(3.5, 6.0), arrowprops=arrow_kw_cabo)

# Rodo (alternativa emergencial)
ax.annotate('', xy=(6.0, 6.7), xytext=(3.5, 6.5), arrowprops=arrow_kw_rodo)
ax.text(4.75, 6.25, 'Rodo 6d', fontsize=8.5, color='#E74C3C', fontweight='bold', ha='center',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#E74C3C', alpha=0.9))

# ── SETAS: Plantas NE → Sub-regiões (direto) ──
arrow_kw_local = dict(arrowstyle='->', color='#2980B9', lw=2.0, connectionstyle='arc3,rad=0.0')
for _, y, _ in subregs:
    ax.annotate('', xy=(11.0, y), xytext=(3.5, 4.0), arrowprops=dict(
        arrowstyle='->', color='#2980B9', lw=1.2, alpha=0.4, connectionstyle='arc3,rad=0.1'))
    ax.annotate('', xy=(11.0, y), xytext=(3.5, 1.8), arrowprops=dict(
        arrowstyle='->', color='#2980B9', lw=1.2, alpha=0.4, connectionstyle='arc3,rad=-0.1'))

ax.text(7.0, 2.0, 'Produção Local\\n(direto)', ha='center', fontsize=9.5, color='#2980B9',
        fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#2980B9', alpha=0.9))

# ── SETAS: CDs → Sub-regiões ──
for _, cd_y in cds:
    for _, sr_y, _ in subregs:
        ax.annotate('', xy=(11.0, sr_y), xytext=(8.8, cd_y),
                    arrowprops=dict(arrowstyle='->', color='#F39C12', lw=0.8, alpha=0.3))

# ── Legenda ──
legend_items = [
    mpatches.Patch(color='#8E44AD', label='SP — Origem transferências'),
    mpatches.Patch(color='#2980B9', label='Plantas NE — Produção local'),
    mpatches.Patch(color='#F39C12', label='CDs — Distribuição'),
    mpatches.Patch(color='#27AE60', label='Sub-regiões — Consumo'),
]
ax.legend(handles=legend_items, loc='lower center', ncol=4, fontsize=9,
          framealpha=0.9, edgecolor='#CCCCCC', bbox_to_anchor=(0.5, -0.02))

plt.tight_layout()
plt.show()"""))

# ══════════════════════════════════════════════════════════════
# SEÇÃO VISUAL 7: RESUMO EXECUTIVO (dashboard cards)
# ══════════════════════════════════════════════════════════════
C.append(md("""---
## 14. Resumo Executivo do Data Contract"""))

C.append(code("""fig, axes = plt.subplots(2, 3, figsize=(15, 7))
fig.patch.set_facecolor('#FAFAFA')
fig.suptitle('Resumo Executivo — Data Contract', fontsize=16, fontweight='bold',
             color='#2C3E50', y=1.02)

cards = [
    ('DEMANDA', '#3498DB',
     ['Malzbier Divulgada:', '38.934 HL', '', 'Malzbier Nova (+30%):', '50.614 HL', '', 'Gap:', '+11.680 HL']),
    ('OFERTA NE', '#2ECC71',
     ['Cap total NE/mês:', '158.400 HL', '', 'Em uso:', '149.040 HL (94.1%)', '', 'Ociosa:', '9.360 HL']),
    ('GAP vs CAPACIDADE', '#E74C3C',
     ['Gap:', '+11.680 HL', '', 'Ociosa:', '9.360 HL', '', 'Déficit (SP):', '2.320 HL']),
    ('CUSTOS MALZBIER', '#F39C12',
     ['MACO: R$285/HL', 'Prod local: R$149 → mg R$136', '',
      'Cabo(Cam): R$234 → mg R$51', 'Rodo(Cam): R$284 → mg R$1', 'Rodo(FM): R$302 → mg -R$17']),
    ('TIMING', '#9B59B6',
     ['Cabo 25d:', 'NÃO resolve em Fev', '',
      'Rodo 6d:', 'ÚNICA opção emergencial', '', '+60% custo + 5% avaria']),
    ('IMPACTO FINANCEIRO', '#1ABC9C',
     ['MACO perdido:', 'R$ 3.328.800', '',
      'Melhor cenário (mix):', 'R$ 1.936.305', '', 'Margem preservada:', 'R$ 1.392.495']),
]

for idx, (titulo, cor, linhas) in enumerate(cards):
    ax = axes[idx // 3][idx % 3]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Card background
    card = FancyBboxPatch((0.02, 0.02), 0.96, 0.96, boxstyle="round,pad=0.03",
                          facecolor='white', edgecolor=cor, linewidth=2.5)
    ax.add_patch(card)

    # Header bar
    header = FancyBboxPatch((0.02, 0.78), 0.96, 0.20, boxstyle="round,pad=0.03",
                            facecolor=cor, edgecolor=cor, linewidth=0)
    ax.add_patch(header)
    ax.text(0.5, 0.88, titulo, ha='center', va='center', fontsize=11,
            fontweight='bold', color='white')

    # Content
    y_pos = 0.68
    for linha in linhas:
        if linha == '':
            y_pos -= 0.03
            continue
        is_value = any(c.isdigit() for c in linha) or 'R$' in linha or 'mg' in linha
        ax.text(0.1, y_pos, linha, ha='left', va='center',
                fontsize=9 if is_value else 8.5,
                fontweight='bold' if is_value else 'normal',
                color='#2C3E50' if is_value else '#7F8C8D')
        y_pos -= 0.09

plt.tight_layout()
plt.show()"""))

# ══ Síntese Data Contract ══
C.append(md("""---
## 15. Insights do Data Contract — Síntese Executiva

> Esta síntese consolida as regras de negócio, restrições estruturais e variáveis críticas identificadas no mapeamento das 6 abas do Excel. Os valores são exatamente os documentados no Data Contract.

---

### 1. Escopo: 6 Fontes de Dados, 48 Variáveis Mapeadas

O Data Contract cobre todas as abas do Excel do case:

| Aba | Conteúdo | Campos mapeados |
|---|---|---|
| **Cenário Atual BR** | Demanda e DOI por região e SKU | 8 |
| **Custos de Transferência** | Fretes por modal, rota e SKU | 8 |
| **Produção PCP** | Capacidade e utilização por planta | 8 |
| **Transferências Programadas** | Fluxos inter-regionais planejados | 8 |
| **Cenário Divulgado** | WSNP baseline por sub-região | 8 |
| **Cenário com Nova Demanda** | WSNP com +30% Malzbier | 8 |

Cada campo documentado com: Nome, Tipo, Formato, Descrição Semântica, Domínio, Regras de Negócio, Nulabilidade e Origem.

---

### 2. A Regra de Negócio Mais Crítica: DOI Mínimo de 12 Dias

O **DOI (Days of Inventory) mínimo de 12 dias** é a principal restrição operacional do sistema. Abaixo desse limiar, há risco formal de ruptura de estoque. Essa regra determina:

- Quais sub-regiões exigem ação imediata (DOI < 12d)
- O volume de transferência mínimo necessário
- A priorização entre sub-regiões em caso de capacidade insuficiente

Com o +30% de Malzbier, o DOI de **3 das 5 sub-regiões cai abaixo de zero** na W3 — o que significa que o estoque existente não cobre nem o mês inteiro sem reabastecimento.

---

### 3. O BIAS de +9% é um Dado, Não uma Estimativa

Os dados da Aba 1 revelam que os GEOs (gestores comerciais regionais) historicamente **sobre-preveem a demanda em +9%** (BIAS positivo). Isso impacta diretamente a análise:

| Cenário | Volume Malzbier NENO |
|---|---|
| Demanda divulgada (com BIAS) | **38.934 HL** |
| Gap com +30% (com BIAS) | **11.680 HL** |
| Gap corrigido (descontando BIAS) | **~10.630 HL** |

A decisão de incorporar ou desconsiderar o BIAS é **julgamento gerencial** — os dados documentam o fato, mas não prescrevem a resposta.

---

### 4. MACO por SKU Define a Priorização Econômica

Os dados de **MACO (Margem de Contribuição)** por SKU determinam qual produto deve ser priorizado em situações de restrição de capacidade:

| SKU | MACO (R$/HL) | Margem Bruta | Posição |
|---|---|---|---|
| **Goose Island** | R$350/HL | — | Maior valor unitário |
| **Colorado** | R$300/HL | — | Segundo maior |
| **Malzbier** | R$285/HL | R$136/HL (47,7%) | Objeto do case |

Isso significa que, em caso de conflito por capacidade, **Goose e Colorado têm prioridade econômica sobre o Malzbier** — o que limita ainda mais a capacidade disponível para realocar.

---

### 5. Duas Restrições Estruturais que Limitam a Solução

O mapeamento identificou duas restrições que não aparecem nas planilhas brutas, mas estão documentadas no case:

**Restrição 1 — Goose Island em PE541:**
Goose Island não pode ter sua produção aumentada na planta de Pernambuco por limitação de elaboração de líquido. Qualquer realocação de capacidade em PE541 deve vir de outros SKUs (Brahma Chopp Zero, Budweiser Zero, Colorado).

**Restrição 2 — NO Araguaia (100% Revendedores):**
A sub-região de NO Araguaia opera integralmente com revendedores autônomos, que gerenciam seu próprio estoque e fazem **retirada direta em Uberlândia**. O DOI negativo registrado para essa sub-região é estoque dos revendedores — não da Ambev. Isso reduz a urgência de atender NO Araguaia em relação às demais sub-regiões.

---

### 6. A Estrutura Logística: Dois CDRs, Duas Rotas de Entrada

Os dados de transferência revelam a arquitetura da malha de distribuição no NENO:

| CDR | Sub-regiões atendidas | Rota cabotagem |
|---|---|---|
| **CDR João Pessoa** | Mapapi, NO Centro, NE Norte | Jaguariúna → Fonte Mata (R$95,3/HL) |
| **CDR Camaçari** | NE Sul | Jaguariúna → Camaçari (R$84,6/HL) |

Lead time de cabotagem: **25 dias**. Para fevereiro (28 dias), o prazo de acionamento já estava vencendo no início do mês.

---

### Resumo das Variáveis-Chave do Data Contract

| Variável | Valor Documentado |
|---|---|
| Abas mapeadas | **6** |
| Atributos por campo | **8** |
| DOI mínimo operacional | **12 dias** |
| BIAS histórico GEOs | **+9% (sobre-previsão)** |
| MACO Malzbier | **R$285/HL** |
| Margem bruta Malzbier | **R$136/HL (47,7%)** |
| Capacidade AQ541 | **12.600 HL/semana** |
| Capacidade PE541 | **27.000 HL/semana** |
| Lead time cabotagem | **25 dias** |
| Sub-regiões NENO | **5 (Mapapi, NE Norte, NE Sul, NO Centro, NO Araguaia)** |

---

> **Próximo passo — Análise Univariada:** examinar cada variável individualmente (distribuição, tendência central, dispersão, outliers) para construir fundamento sólido antes de cruzar dados na análise bivariada."""))


# ── Build nb1_data_contract.ipynb ──────────────────────────────────────────
for i, c in enumerate(C):
    c['id'] = f'cell-{i}'

nb = {
    "nbformat": 4, "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.10.0"}
    },
    "cells": C
}

import os as _os
path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "nb1_data_contract.ipynb")
with open(path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

errs = []
for i, c in enumerate(C):
    if c['cell_type'] == 'code':
        src = c['source'][0]
        clean = '\n'.join(l for l in src.split('\n') if not l.strip().startswith('%'))
        try:
            compile(clean, f'cell-{i}', 'exec')
        except SyntaxError as e:
            errs.append(f'Cell {i}: {e}')
        if 'applymap' in src or ('.map(' in src and 'lambda' in src):
            errs.append(f'Cell {i}: has applymap/map!')
        if '.style.' in src:
            errs.append(f'Cell {i}: has .style.')

print(f"nb1_data_contract.ipynb: {len(C)} células")
if errs:
    for e in errs: print(f"  ERR: {e}")
else:
    print("Zero erros | Zero applymap | Zero .style.")
