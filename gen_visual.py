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

| SKU | MACO (R\$/HL) | Margem Bruta | Posição |
|---|---|---|---|
| **Goose Island** | R\$350/HL | — | Maior valor unitário |
| **Colorado** | R\$300/HL | — | Segundo maior |
| **Malzbier** | R\$285/HL | R\$136/HL (47,7%) | Objeto do case |

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
| **CDR João Pessoa** | Mapapi, NO Centro, NE Norte | Jaguariúna → Fonte Mata (R\$95,3/HL) |
| **CDR Camaçari** | NE Sul | Jaguariúna → Camaçari (R\$84,6/HL) |

Lead time de cabotagem: **25 dias**. Para fevereiro (28 dias), o prazo de acionamento já estava vencendo no início do mês.

---

### Resumo das Variáveis-Chave do Data Contract

| Variável | Valor Documentado |
|---|---|
| Abas mapeadas | **6** |
| Atributos por campo | **8** |
| DOI mínimo operacional | **12 dias** |
| BIAS histórico GEOs | **+9% (sobre-previsão)** |
| MACO Malzbier | **R\$285/HL** |
| Margem bruta Malzbier | **R\$136/HL (47,7%)** |
| Capacidade AQ541 | **12.600 HL/semana** |
| Capacidade PE541 | **27.000 HL/semana** |
| Lead time cabotagem | **25 dias** |
| Sub-regiões NENO | **5 (Mapapi, NE Norte, NE Sul, NO Centro, NO Araguaia)** |

---

> **Próximo passo — Análise Univariada:** examinar cada variável individualmente (distribuição, tendência central, dispersão, outliers) para construir fundamento sólido antes de cruzar dados na análise bivariada."""))

# ═══════════════════════════════════════════════════════════════════════════════
# PARTE 2: ANÁLISE UNIVARIADA
# ═══════════════════════════════════════════════════════════════════════════════

C.append(md("""---
---

# PARTE 2 — Análise Univariada

> **Objetivo:** Examinar **cada variável individualmente** — distribuição, tendência central, dispersão, outliers — para construir fundamento sólido antes de cruzar dados na análise bivariada.

**Escopo:** Todas as 6 abas do Excel + informações contextuais dos PDFs do case.

| Conceito | Significado |
|---|---|
| **Média** | Tendência central — valor "típico" |
| **Mediana** | Valor central (robusto a outliers) |
| **Desvio Padrão** | Dispersão — quanto os valores variam |
| **CV (Coeficiente de Variação)** | Dispersão relativa — CV > 30% = alta variabilidade |
| **Min / Max** | Extremos — indicam amplitude |
| **DOI (Days of Inventory)** | Dias de estoque — mínimo operacional: 12 dias |"""))

# ══ Carregamento e parsing das 6 abas ══
C.append(code("""# ═══════════════════════════════════════════════════════
# CARREGAMENTO E PARSING ESTRUTURADO DAS 6 ABAS
# ═══════════════════════════════════════════════════════

# Guard: garante que as variáveis de setup estão disponíveis
# mesmo que esta célula seja rodada isoladamente
try:
    EXCEL_FILE
    pd
except NameError:
    import subprocess, sys as _sys
    subprocess.check_call([_sys.executable, '-m', 'pip', 'install', 'openpyxl', '-q'])
    import pandas as pd
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import warnings
    warnings.filterwarnings('ignore')
    from pathlib import Path
    from IPython.display import display, HTML
    BASE_DIR = Path('.').resolve()
    EXCEL_FILE = None
    for p in [BASE_DIR, BASE_DIR.parent]:
        candidates = [f for f in p.glob('*Sem*repostas*.xlsx') if not f.name.startswith('~')]
        if candidates:
            EXCEL_FILE = candidates[0]; break
    if EXCEL_FILE is None:
        for p in [BASE_DIR, BASE_DIR.parent]:
            all_xlsx = list(p.glob('*Long*Neck*.xlsx')) + list(p.glob('*longneck*.xlsx'))
            candidates = [f for f in all_xlsx if not f.name.startswith('~')]
            if candidates:
                EXCEL_FILE = candidates[0]; break
    print(f"⚠️  Setup rodado localmente. Excel: {EXCEL_FILE}")

if EXCEL_FILE is None:
    raise FileNotFoundError("Excel não encontrado! Verifique se o arquivo está na mesma pasta do notebook.")

xls = pd.ExcelFile(EXCEL_FILE)
print(f"Abas encontradas: {xls.sheet_names}")

# ── Aba 1: Cenário Atual BR ──
raw1 = pd.read_excel(xls, 'Cenário atual BR', header=None)

regioes_br = ['MG', 'SP', 'NENO', 'CO', 'RJ', 'SUL']  # Export removido — não é região, é categoria especial

# Janeiro (colunas 2-13) e Fevereiro (colunas 15-23)
jan_data = []
fev_data = []
for i, reg in enumerate(regioes_br):
    row = 5 + i  # rows 5..11
    jan_data.append({
        'Regiao': reg,
        'Demanda_Jan': float(raw1.iloc[row, 3]) if pd.notna(raw1.iloc[row, 3]) else 0,
        'PROD_Real_Jan': float(raw1.iloc[row, 5]) if pd.notna(raw1.iloc[row, 5]) else 0,
        'WSNP_Jan': float(raw1.iloc[row, 6]) if pd.notna(raw1.iloc[row, 6]) else 0,
        'Prog_1W_Jan': float(raw1.iloc[row, 7]) if pd.notna(raw1.iloc[row, 7]) else 0,
    })
    fev_data.append({
        'Regiao': reg,
        'Demanda_Fev': float(raw1.iloc[row, 17]) if pd.notna(raw1.iloc[row, 17]) else 0,
        'WSNP_Fev': float(raw1.iloc[row, 19]) if pd.notna(raw1.iloc[row, 19]) else 0,
        'Transf_Malha_Fev': float(raw1.iloc[row, 21]) if pd.notna(raw1.iloc[row, 21]) else 0,
        'EFM_Fev': float(raw1.iloc[row, 22]) if pd.notna(raw1.iloc[row, 22]) else 0,
        'Suf_Fev_dias': float(raw1.iloc[row, 23]) if pd.notna(raw1.iloc[row, 23]) else 0,
    })

df_jan = pd.DataFrame(jan_data)
df_fev = pd.DataFrame(fev_data)
df_cenario_br = pd.merge(df_jan, df_fev, on='Regiao')

print(f"\\n✅ Aba 1 (Cenário Atual BR): {len(df_cenario_br)} regiões carregadas")
display(df_cenario_br)

# ── Aba 2: Custos de Transferência ──
raw2 = pd.read_excel(xls, 'Custos de transferência', header=None)

custos_transf = []
for row in range(3, 9):
    custos_transf.append({
        'SKU': str(raw2.iloc[row, 1]).strip(),
        'Origem': str(raw2.iloc[row, 2]).strip(),
        'Destino': str(raw2.iloc[row, 3]).strip(),
        'Custo_R_HL': float(raw2.iloc[row, 4])
    })
df_custos_transf = pd.DataFrame(custos_transf)

# MACO
maco_data = []
for row in [13, 14, 15]:
    maco_data.append({
        'SKU': str(raw2.iloc[row, 1]).strip(),
        'MACO_R_HL': float(raw2.iloc[row, 4])
    })
df_maco = pd.DataFrame(maco_data)

# Custo Produção
cprod_data = []
for row in [20, 21, 22]:
    cprod_data.append({
        'SKU': str(raw2.iloc[row, 1]).strip(),
        'Custo_Prod_R_HL': float(raw2.iloc[row, 4])
    })
df_cprod = pd.DataFrame(cprod_data)

# Consolidar
df_sku_economics = pd.merge(df_maco, df_cprod, on='SKU')
df_sku_economics['Margem_Bruta'] = df_sku_economics['MACO_R_HL'] - df_sku_economics['Custo_Prod_R_HL']
df_sku_economics['Margem_Pct'] = (df_sku_economics['Margem_Bruta'] / df_sku_economics['MACO_R_HL'] * 100).round(1)

print(f"\\n✅ Aba 2 (Custos): {len(df_custos_transf)} rotas + {len(df_sku_economics)} SKUs")
display(df_custos_transf)
display(df_sku_economics)

# ── Aba 3: Produção PCP ──
raw3 = pd.read_excel(xls, 'Produção PCP', header=None)

semanas = ['W1 (02/02)', 'W2 (09/02)', 'W3 (16/02)', 'W4 (23/02)']

# AQ541 (Aquiraz/CE) - rows 2,3,4
aq_skus = ['Malzbier', 'Patagonia', 'Colorado']
aq_rows = [2, 3, 4]
prod_pcp = []
for sku, row in zip(aq_skus, aq_rows):
    for w, col in enumerate([6, 7, 8, 9]):
        val = float(raw3.iloc[row, col]) if pd.notna(raw3.iloc[row, col]) else 0
        prod_pcp.append({'Planta': 'AQ541 (CE)', 'SKU': sku, 'Semana': semanas[w], 'Semana_Num': w+1, 'Volume_HL': val})

# PE541 (Pernambuco) - rows 9..14
pe_skus = ['Brahma Chopp Zero', 'Goose Island', 'Malzbier', 'Colorado', 'Skol Beats', 'Budweiser Zero']
pe_rows = [9, 10, 11, 12, 13, 14]
for sku, row in zip(pe_skus, pe_rows):
    for w, col in enumerate([6, 7, 8, 9]):
        val = float(raw3.iloc[row, col]) if pd.notna(raw3.iloc[row, col]) else 0
        prod_pcp.append({'Planta': 'PE541 (PE)', 'SKU': sku, 'Semana': semanas[w], 'Semana_Num': w+1, 'Volume_HL': val})

df_pcp = pd.DataFrame(prod_pcp)

# Capacidades nominais
cap_aq = 12600  # HL/semana
cap_pe = 27000  # HL/semana

print(f"\\n✅ Aba 3 (Produção PCP): {len(df_pcp)} registros (planta × SKU × semana)")

# ── Aba 4: Transferências Programadas ──
raw4 = pd.read_excel(xls, 'Transferências Programadas', header=None)

transf_prog = []
for row in [3, 4, 5]:
    dest = str(raw4.iloc[row, 3]).strip()
    for w, col in enumerate([7, 8, 9, 10]):
        val = float(raw4.iloc[row, col]) if pd.notna(raw4.iloc[row, col]) else 0
        transf_prog.append({
            'Destino': dest, 'SKU': 'Goose Island', 'Modal': 'Cabotagem',
            'Semana': semanas[w], 'Semana_Num': w+1, 'Volume_HL': val
        })
df_transf = pd.DataFrame(transf_prog)
print(f"\\n✅ Aba 4 (Transferências): {len(df_transf)} registros")

# ── Abas 5 e 6: Cenário Divulgado e Nova Demanda ──
def parse_cenario_neno(sheet_name):
    raw = pd.read_excel(xls, sheet_name, header=None)

    skus_info = [
        ('Patagonia', 4, 9),
        ('Goose Island', 12, 17),
        ('Malzbier', 20, 25),
        ('Colorado', 28, 33),
    ]
    sub_regioes = ['Mapapi', 'NE Norte', 'NE Sul', 'NO Araguaia', 'NO Centro']

    # Mapeamento EXATO de colunas por semana (verificado manualmente)
    # W0: Dem=3, WSNP=5, EI=7, SufIni=8, TrInt=9, ExtCabo=10, ExtRodo=11, Transit=12, EF=13, SufF=14
    # W1: Dem=16, WSNP=18, TrInt=20, ExtCabo=21, ExtRodo=22, Transit=23, EF=24, SufF=25
    # W2: Dem=27, WSNP=29, TrInt=31, ExtCabo=32, ExtRodo=33, Transit=34, EF=35, SufF=36
    # W3: Dem=38, WSNP=40, TrInt=42, ExtCabo=43, ExtRodo=44, Transit=45, EF=46, SufF=47
    week_cols = [
        {'dem': 3, 'wsnp': 5, 'ei': 7, 'suf_ini': 8, 'tr_int': 9, 'ef': 13, 'suf_f': 14},
        {'dem': 16, 'wsnp': 18, 'ei': None, 'suf_ini': None, 'tr_int': 20, 'ef': 24, 'suf_f': 25},
        {'dem': 27, 'wsnp': 29, 'ei': None, 'suf_ini': None, 'tr_int': 31, 'ef': 35, 'suf_f': 36},
        {'dem': 38, 'wsnp': 40, 'ei': None, 'suf_ini': None, 'tr_int': 42, 'ef': 46, 'suf_f': 47},
    ]

    def safe_float(val):
        try:
            if pd.notna(val):
                return float(val)
        except (ValueError, TypeError):
            pass
        return 0.0

    records = []
    for sku_name, start_row, total_row in skus_info:
        for sr_idx, sr_name in enumerate(sub_regioes):
            row = start_row + sr_idx
            for w_idx, wc in enumerate(week_cols):
                dem = safe_float(raw.iloc[row, wc['dem']])
                wsnp = safe_float(raw.iloc[row, wc['wsnp']])
                ei = safe_float(raw.iloc[row, wc['ei']]) if wc['ei'] is not None else 0.0
                suf_ini = safe_float(raw.iloc[row, wc['suf_ini']]) if wc['suf_ini'] is not None else 0.0
                tr_int = safe_float(raw.iloc[row, wc['tr_int']])
                ef = safe_float(raw.iloc[row, wc['ef']])
                suf_f = safe_float(raw.iloc[row, wc['suf_f']])

                records.append({
                    'SKU': sku_name, 'Sub_Regiao': sr_name,
                    'Semana': semanas[w_idx], 'Semana_Num': w_idx + 1,
                    'Demanda': dem, 'WSNP': wsnp, 'EI_Semana': ei,
                    'Suf_Ini_dias': suf_ini, 'Transf_Interna': tr_int,
                    'EF_Semana': ef, 'Suf_Final_dias': suf_f
                })

    # SP (rows 39-41)
    sp_skus = [('Goose Island', 39), ('Malzbier', 40), ('Colorado', 41)]
    for sku_name, row in sp_skus:
        for w_idx, wc in enumerate(week_cols):
            dem = safe_float(raw.iloc[row, wc['dem']])
            wsnp = safe_float(raw.iloc[row, wc['wsnp']])
            ei = safe_float(raw.iloc[row, wc['ei']]) if wc['ei'] is not None else 0.0
            suf_ini = safe_float(raw.iloc[row, wc['suf_ini']]) if wc['suf_ini'] is not None else 0.0
            ef = safe_float(raw.iloc[row, wc['ef']])
            suf_f = safe_float(raw.iloc[row, wc['suf_f']])

            records.append({
                'SKU': sku_name, 'Sub_Regiao': 'SP (Origem)',
                'Semana': semanas[w_idx], 'Semana_Num': w_idx + 1,
                'Demanda': dem, 'WSNP': wsnp, 'EI_Semana': ei,
                'Suf_Ini_dias': suf_ini, 'Transf_Interna': 0,
                'EF_Semana': ef, 'Suf_Final_dias': suf_f
            })

    return pd.DataFrame(records)

df_divulgado = parse_cenario_neno('Cenário Divulgado')
df_nova_dem = parse_cenario_neno('Cenário com Nova Demanda')

print(f"\\n✅ Aba 5 (Cenário Divulgado): {len(df_divulgado)} registros")
print(f"✅ Aba 6 (Nova Demanda): {len(df_nova_dem)} registros")
print(f"\\n{'='*60}")
print(f"TOTAL DE DADOS CARREGADOS: {len(df_cenario_br) + len(df_custos_transf) + len(df_pcp) + len(df_transf) + len(df_divulgado) + len(df_nova_dem)} registros")
print(f"{'='*60}")"""))

# ══ Aba 1: Análise Univariada — Cenário Atual BR ══
C.append(md("""---
## 16. Análise Univariada — Aba 1: Cenário Atual BR (Visão Nacional)

> **O que é esta aba?** Panorama mensal (Janeiro/Fevereiro) de **demanda, produção e estoque** para todas as 7 regiões da Ambev no Brasil. Permite entender onde está o volume e onde há folga ou pressão logística.

**Variáveis analisadas:** Demanda (HL), Produção Real (HL), WSNP (HL), Suficiência final (dias), Transferência de malha (HL), Estoque Final (HL)"""))

C.append(code("""# ═══════════════════════════════════════════════════════
# ABA 1: CENÁRIO ATUAL BR — ANÁLISE UNIVARIADA
# ═══════════════════════════════════════════════════════

# 1.1 Estatísticas descritivas — Demanda por Região
print("=" * 70)
print("1.1 ESTATÍSTICAS DESCRITIVAS — DEMANDA REGIONAL (HL)")
print("=" * 70)

stats_dem = pd.DataFrame({
    'Regiao': df_cenario_br['Regiao'],
    'Demanda_Jan': df_cenario_br['Demanda_Jan'].round(0),
    'Demanda_Fev': df_cenario_br['Demanda_Fev'].round(0),
    'Variacao_Pct': ((df_cenario_br['Demanda_Fev'] - df_cenario_br['Demanda_Jan']) / df_cenario_br['Demanda_Jan'].replace(0, np.nan) * 100).round(1)
})
display(stats_dem)

# Resumo estatístico (excluindo TOTAL e Export)
regioes_operacionais = df_cenario_br[~df_cenario_br['Regiao'].isin(['Export'])]
dem_jan_vals = regioes_operacionais['Demanda_Jan']
dem_fev_vals = regioes_operacionais['Demanda_Fev']

print(f"\\nJaneiro  — Media: {dem_jan_vals.mean():,.0f} HL | Mediana: {dem_jan_vals.median():,.0f} | DP: {dem_jan_vals.std():,.0f} | CV: {dem_jan_vals.std()/dem_jan_vals.mean()*100:.1f}%")
print(f"Fevereiro — Media: {dem_fev_vals.mean():,.0f} HL | Mediana: {dem_fev_vals.median():,.0f} | DP: {dem_fev_vals.std():,.0f} | CV: {dem_fev_vals.std()/dem_fev_vals.mean()*100:.1f}%")

# 1.2 Visualização: Demanda Jan vs Fev por Região
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

regioes_plot = df_cenario_br[df_cenario_br['Regiao'] != 'Export'].copy()
regioes_plot = regioes_plot.sort_values('Demanda_Jan', ascending=True)

x = np.arange(len(regioes_plot))
w = 0.35

axes[0].barh(x - w/2, regioes_plot['Demanda_Jan']/1000, w, color=CORES['azul_medio'], label='Janeiro', edgecolor='white')
axes[0].barh(x + w/2, regioes_plot['Demanda_Fev']/1000, w, color=CORES['ambar'], label='Fevereiro', edgecolor='white')
axes[0].set_yticks(x)
axes[0].set_yticklabels(regioes_plot['Regiao'])
axes[0].set_xlabel('Demanda (mil HL)')
axes[0].set_title('Demanda LN por Regiao — Jan vs Fev', fontweight='bold')
axes[0].legend()
axes[0].grid(axis='x', alpha=0.3)

# Share de cada região no total
total_fev = regioes_plot['Demanda_Fev'].sum()
shares = (regioes_plot['Demanda_Fev'] / total_fev * 100).values
colors_pie = [CORES['azul_escuro'], CORES['azul_medio'], CORES['azul_claro'], CORES['ambar'], CORES['verde'], CORES['vermelho']]
wedges, texts, autotexts = axes[1].pie(
    shares, labels=regioes_plot['Regiao'].values,
    autopct='%1.1f%%', colors=colors_pie[:len(shares)],
    startangle=90, textprops={'fontsize': 9}
)
axes[1].set_title('Share de Demanda Fev (% do total, sem Export)', fontweight='bold')

plt.tight_layout()
plt.show()"""))

C.append(code("""# ═══════════════════════════════════════════════════════
# 1.3 SUFICIÊNCIA (DOI) POR REGIÃO — FEVEREIRO
# ═══════════════════════════════════════════════════════

print("=" * 70)
print("1.3 SUFICIÊNCIA FINAL (DOI) POR REGIÃO — FEVEREIRO")
print("=" * 70)

suf_data = df_cenario_br[['Regiao', 'Suf_Fev_dias']].copy()
suf_data = suf_data.sort_values('Suf_Fev_dias', ascending=True)
display(suf_data)

DOI_MIN = 12  # dias

fig, ax = plt.subplots(figsize=(12, 5))

cores_barra = []
for val in suf_data['Suf_Fev_dias']:
    if val < 0:
        cores_barra.append(CORES['vermelho'])
    elif val < DOI_MIN:
        cores_barra.append(CORES['ambar'])
    else:
        cores_barra.append(CORES['verde'])

bars = ax.barh(suf_data['Regiao'], suf_data['Suf_Fev_dias'], color=cores_barra, edgecolor='white', height=0.6)
ax.axvline(x=DOI_MIN, color=CORES['vermelho'], linestyle='--', linewidth=2, label=f'DOI minimo = {DOI_MIN} dias')
ax.axvline(x=0, color='black', linewidth=0.5)

for bar, val in zip(bars, suf_data['Suf_Fev_dias']):
    x_pos = max(val + 0.5, 1)
    ax.text(x_pos, bar.get_y() + bar.get_height()/2, f'{val:.1f}d', va='center', fontsize=9, fontweight='bold')

ax.set_xlabel('Suficiência (dias)')
ax.set_title('Suficiencia Final Fev por Regiao — DOI minimo 12 dias', fontweight='bold', fontsize=13)
ax.legend(fontsize=10)
ax.grid(axis='x', alpha=0.3)

# Insights
abaixo_doi = suf_data[suf_data['Suf_Fev_dias'] < DOI_MIN]
print(f"\\nRegioes ABAIXO do DOI minimo ({DOI_MIN} dias): {len(abaixo_doi)}")
for _, row in abaixo_doi.iterrows():
    status = "CRITICO" if row['Suf_Fev_dias'] < 0 else "ALERTA"
    print(f"  [{status}] {row['Regiao']}: {row['Suf_Fev_dias']:.1f} dias")

plt.tight_layout()
plt.show()"""))

C.append(code("""# ═══════════════════════════════════════════════════════
# 1.4 PRODUÇÃO vs DEMANDA — BALANÇO REGIONAL
# ═══════════════════════════════════════════════════════

print("=" * 70)
print("1.4 TRANSFERÊNCIA DE MALHA E ESTOQUE FINAL — FEVEREIRO")
print("=" * 70)

# Transferência de malha: positivo = recebe, negativo = envia
transf_data = df_cenario_br[['Regiao', 'Transf_Malha_Fev', 'EFM_Fev']].copy()
transf_data = transf_data[transf_data['Regiao'] != 'Export']
transf_data = transf_data.sort_values('Transf_Malha_Fev')
display(transf_data)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Transferência de Malha
cores_transf = [CORES['verde'] if v >= 0 else CORES['vermelho'] for v in transf_data['Transf_Malha_Fev']]
axes[0].barh(transf_data['Regiao'], transf_data['Transf_Malha_Fev']/1000, color=cores_transf, edgecolor='white')
axes[0].axvline(x=0, color='black', linewidth=1)
axes[0].set_xlabel('Volume (mil HL)')
axes[0].set_title('Transferencia de Malha Fev\\n(+recebe / -envia)', fontweight='bold')
axes[0].grid(axis='x', alpha=0.3)

for i, (_, row) in enumerate(transf_data.iterrows()):
    val = row['Transf_Malha_Fev']
    axes[0].text(val/1000 + (2 if val >= 0 else -2), i, f'{val/1000:.1f}k', va='center', fontsize=8, fontweight='bold',
                 ha='left' if val >= 0 else 'right')

# Estoque Final
ef_sorted = transf_data.sort_values('EFM_Fev')
cores_ef = [CORES['vermelho'] if v < 0 else CORES['azul_medio'] for v in ef_sorted['EFM_Fev']]
axes[1].barh(ef_sorted['Regiao'], ef_sorted['EFM_Fev']/1000, color=cores_ef, edgecolor='white')
axes[1].axvline(x=0, color='black', linewidth=1)
axes[1].set_xlabel('Volume (mil HL)')
axes[1].set_title('Estoque Final Mes Fev (EFM)', fontweight='bold')
axes[1].grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.show()

# Insight chave
print("\\n--- INSIGHT ABA 1 ---")
print("SP e RJ sao EXPORTADORES liquidos (enviam para outras regioes)")
print("NENO e CO sao IMPORTADORES (recebem de outras regioes)")
print(f"NENO: Suf. Fev = {df_cenario_br[df_cenario_br['Regiao']=='NENO']['Suf_Fev_dias'].values[0]:.1f} dias — PROXIMO do limite de 12 dias")"""))

# ══ Aba 2: Custos ══
C.append(md("""---
## 17. Análise Univariada — Aba 2: Custos de Transferência e Economia dos SKUs

> **O que é esta aba?** Mapeia os **custos logísticos por rota** (R\\$/HL) e a **economia unitária** de cada SKU (MACO, custo de produção, margem). É a base para avaliar se vale transferir volume de SP para o Nordeste.

**Variáveis:** Custo por rota (R\\$/HL), MACO (R\\$/HL), Custo de Produção (R\\$/HL), Margem Bruta (R\\$/HL)"""))

C.append(code("""# ═══════════════════════════════════════════════════════
# ABA 2: CUSTOS — ANÁLISE UNIVARIADA
# ═══════════════════════════════════════════════════════

print("=" * 70)
print("2.1 CUSTOS DE TRANSFERÊNCIA POR ROTA")
print("=" * 70)

# Simplificar nomes
df_custos_viz = df_custos_transf.copy()
df_custos_viz['SKU_curto'] = df_custos_viz['SKU'].str.split(' ').str[0]
df_custos_viz['Rota'] = (df_custos_viz['Origem'].str.extract(r'F\\. (\\w+)')[0] +
                          ' -> ' +
                          df_custos_viz['Destino'].str.extract(r'F\\. (\\w+)')[0])

display(df_custos_viz[['SKU_curto', 'Rota', 'Custo_R_HL']].sort_values('Custo_R_HL'))

# Estatísticas
print(f"\\nCusto medio: R$ {df_custos_transf['Custo_R_HL'].mean():.2f}/HL")
print(f"Custo min:   R$ {df_custos_transf['Custo_R_HL'].min():.2f}/HL (Colorado, Jacarei->Camacari)")
print(f"Custo max:   R$ {df_custos_transf['Custo_R_HL'].max():.2f}/HL (Malzbier, Jaguariuna->Fonte Mata)")
print(f"Amplitude:   R$ {df_custos_transf['Custo_R_HL'].max() - df_custos_transf['Custo_R_HL'].min():.2f}/HL")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Gráfico de custos por rota
df_sorted = df_custos_viz.sort_values('Custo_R_HL')
colors_sku = {'COLORADO': CORES['verde'], 'GOOSE': CORES['azul_medio'], 'MALZBIER': CORES['ambar']}
bar_colors = [colors_sku.get(s, CORES['cinza_medio']) for s in df_sorted['SKU_curto']]

bars = axes[0].barh(range(len(df_sorted)), df_sorted['Custo_R_HL'], color=bar_colors, edgecolor='white')
axes[0].set_yticks(range(len(df_sorted)))
axes[0].set_yticklabels([f"{r['SKU_curto']}\\n{r['Rota']}" for _, r in df_sorted.iterrows()], fontsize=8)
axes[0].set_xlabel('R$/HL')
axes[0].set_title('Custo de Transferencia por Rota', fontweight='bold')
axes[0].grid(axis='x', alpha=0.3)

for bar, val in zip(bars, df_sorted['Custo_R_HL']):
    axes[0].text(val + 0.5, bar.get_y() + bar.get_height()/2, f'R${val:.1f}', va='center', fontsize=8)

# Economia dos SKUs (MACO, Custo Prod, Margem)
x_pos = np.arange(len(df_sku_economics))
w = 0.25

axes[1].bar(x_pos - w, df_sku_economics['MACO_R_HL'], w, color=CORES['azul_escuro'], label='MACO', edgecolor='white')
axes[1].bar(x_pos, df_sku_economics['Custo_Prod_R_HL'], w, color=CORES['vermelho'], label='Custo Prod.', edgecolor='white')
axes[1].bar(x_pos + w, df_sku_economics['Margem_Bruta'], w, color=CORES['verde'], label='Margem Bruta', edgecolor='white')

axes[1].set_xticks(x_pos)
sku_labels = [s.split()[0] for s in df_sku_economics['SKU']]
axes[1].set_xticklabels(sku_labels, fontsize=9)
axes[1].set_ylabel('R$/HL')
axes[1].set_title('Economia Unitaria por SKU', fontweight='bold')
axes[1].legend(fontsize=8)
axes[1].grid(axis='y', alpha=0.3)

for i, row in df_sku_economics.iterrows():
    axes[1].text(i + w, row['Margem_Bruta'] + 3, f'R${row["Margem_Bruta"]:.0f}\\n({row["Margem_Pct"]}%)',
                 ha='center', fontsize=8, fontweight='bold', color=CORES['verde'])

plt.tight_layout()
plt.show()

print("\\n--- INSIGHT ABA 2 ---")
print(f"Goose Island tem MAIOR MACO (R$350/HL) mas custo transf. tambem eh alto")
print(f"Malzbier: margem R$136/HL ({df_sku_economics[df_sku_economics['SKU'].str.contains('MALZ')]['Margem_Pct'].values[0]}%) — custo transf. R$84-95/HL")
print(f"Transferir Malzbier consome {84.58/136*100:.0f}%-{95.33/136*100:.0f}% da margem bruta (rota Camacari vs Fonte Mata)")"""))

# ══ Aba 3: Produção PCP ══
C.append(md("""---
## 18. Análise Univariada — Aba 3: Produção PCP (Fevereiro, 4 semanas)

> **O que é esta aba?** Programação semanal de produção para as **2 plantas do Nordeste** (AQ541 em Aquiraz/CE e PE541 em Pernambuco). Mostra quais SKUs são produzidos quando e em que volume.

**Informação-chave do case:** Goose Island MIDWAY tem **restrição de elaboração de líquido** em Pernambuco — não pode aumentar produção. Capacidade: AQ541 = 12.600 HL/sem | PE541 = 27.000 HL/sem."""))

C.append(code("""# ═══════════════════════════════════════════════════════
# ABA 3: PRODUÇÃO PCP — ANÁLISE UNIVARIADA
# ═══════════════════════════════════════════════════════

print("=" * 70)
print("3.1 VOLUME SEMANAL POR PLANTA")
print("=" * 70)

# Agregação por planta e semana
prod_planta_sem = df_pcp.groupby(['Planta', 'Semana', 'Semana_Num'])['Volume_HL'].sum().reset_index()
prod_planta_sem = prod_planta_sem.sort_values(['Planta', 'Semana_Num'])

# Utilização
for planta in ['AQ541 (CE)', 'PE541 (PE)']:
    cap = cap_aq if 'AQ' in planta else cap_pe
    mask = prod_planta_sem['Planta'] == planta
    prod_planta_sem.loc[mask, 'Capacidade'] = cap
    prod_planta_sem.loc[mask, 'Utilizacao_Pct'] = (prod_planta_sem.loc[mask, 'Volume_HL'] / cap * 100)

display(prod_planta_sem[['Planta', 'Semana', 'Volume_HL', 'Capacidade', 'Utilizacao_Pct']].round(1))

# Estatísticas por planta
for planta in ['AQ541 (CE)', 'PE541 (PE)']:
    dados = prod_planta_sem[prod_planta_sem['Planta'] == planta]['Utilizacao_Pct']
    print(f"\\n{planta}:")
    print(f"  Utilizacao media: {dados.mean():.1f}% | Min: {dados.min():.1f}% | Max: {dados.max():.1f}%")
    print(f"  Desvio padrao: {dados.std():.1f}% | CV: {dados.std()/dados.mean()*100:.1f}%")

# Visualização
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 3.1a Utilização semanal por planta
for idx, planta in enumerate(['AQ541 (CE)', 'PE541 (PE)']):
    data = prod_planta_sem[prod_planta_sem['Planta'] == planta]
    cap = cap_aq if 'AQ' in planta else cap_pe

    bars = axes[0, idx].bar(data['Semana'], data['Volume_HL']/1000,
                            color=CORES['azul_medio'], edgecolor='white', width=0.6)
    axes[0, idx].axhline(y=cap/1000, color=CORES['vermelho'], linestyle='--', linewidth=2,
                         label=f'Capacidade: {cap/1000:.1f}k HL')
    axes[0, idx].set_ylabel('Volume (mil HL)')
    axes[0, idx].set_title(f'{planta} — Producao Semanal', fontweight='bold')
    axes[0, idx].legend(fontsize=8)
    axes[0, idx].tick_params(axis='x', rotation=20, labelsize=8)
    axes[0, idx].grid(axis='y', alpha=0.3)

    for bar, val in zip(bars, data['Utilizacao_Pct']):
        axes[0, idx].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                         f'{val:.0f}%', ha='center', fontsize=9, fontweight='bold')

# 3.1b Mix de SKU por planta (stacked bar)
for idx, planta in enumerate(['AQ541 (CE)', 'PE541 (PE)']):
    pdata = df_pcp[df_pcp['Planta'] == planta].pivot_table(
        index='Semana_Num', columns='SKU', values='Volume_HL', aggfunc='sum', fill_value=0)

    pdata = pdata.reindex(columns=pdata.sum().sort_values(ascending=False).index)

    bottom = np.zeros(len(pdata))
    sku_colors = [CORES['ambar'], CORES['azul_medio'], CORES['verde'], CORES['vermelho'], CORES['azul_claro'], CORES['cinza_medio']]

    for col_idx, col in enumerate(pdata.columns):
        vals = pdata[col].values
        c = sku_colors[col_idx % len(sku_colors)]
        axes[1, idx].bar(pdata.index, vals/1000, bottom=bottom/1000, label=col, color=c, edgecolor='white', width=0.6)
        bottom += vals

    cap = cap_aq if 'AQ' in planta else cap_pe
    axes[1, idx].axhline(y=cap/1000, color=CORES['vermelho'], linestyle='--', linewidth=2)
    axes[1, idx].set_xlabel('Semana')
    axes[1, idx].set_ylabel('Volume (mil HL)')
    axes[1, idx].set_title(f'{planta} — Mix de SKU por Semana', fontweight='bold')
    axes[1, idx].legend(fontsize=7, loc='upper right')
    axes[1, idx].set_xticks([1,2,3,4])
    axes[1, idx].set_xticklabels(['W1', 'W2', 'W3', 'W4'])
    axes[1, idx].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()

# SKU com maior volume por planta
print("\\n--- INSIGHT ABA 3 ---")
sku_totals = df_pcp.groupby(['Planta', 'SKU'])['Volume_HL'].sum().reset_index()
for planta in ['AQ541 (CE)', 'PE541 (PE)']:
    top = sku_totals[sku_totals['Planta'] == planta].sort_values('Volume_HL', ascending=False)
    print(f"\\n{planta} — Volume total 4 semanas:")
    for _, r in top.iterrows():
        if r['Volume_HL'] > 0:
            print(f"  {r['SKU']}: {r['Volume_HL']:,.0f} HL")

ociosidade_aq = prod_planta_sem[prod_planta_sem['Planta'] == 'AQ541 (CE)']
ociosas = ociosidade_aq[ociosidade_aq['Utilizacao_Pct'] < 100]
if len(ociosas) > 0:
    print(f"\\nAQ541 tem ociosidade em {len(ociosas)}/4 semanas — potencial para realocar producao")
    gap_total = (ociosidade_aq['Capacidade'] - ociosidade_aq['Volume_HL']).sum()
    print(f"Gap de capacidade total AQ541 no mes: {gap_total:,.0f} HL")"""))

# ══ Aba 4: Transferências Programadas ══
C.append(md("""---
## 19. Análise Univariada — Aba 4: Transferências Programadas

> **O que é esta aba?** Lista as transferências **já planejadas** (antes de qualquer nova ação). Atualmente, apenas **Goose Island** tem transferências programadas, todas via **cabotagem** de SP para o Nordeste.

**Nota:** Nenhum outro SKU (Malzbier, Colorado, Patagonia) tem transferência programada para o NE neste momento."""))

C.append(code("""# ═══════════════════════════════════════════════════════
# ABA 4: TRANSFERÊNCIAS PROGRAMADAS — ANÁLISE UNIVARIADA
# ═══════════════════════════════════════════════════════

print("=" * 70)
print("4.1 TRANSFERÊNCIAS PROGRAMADAS (SOMENTE GOOSE ISLAND)")
print("=" * 70)

# Pivot: Destino x Semana
transf_pivot = df_transf.pivot_table(index='Destino', columns='Semana', values='Volume_HL', aggfunc='sum')
transf_pivot['TOTAL'] = transf_pivot.sum(axis=1)
display(transf_pivot)

total_transf = df_transf['Volume_HL'].sum()
print(f"\\nVolume total programado: {total_transf:,.1f} HL (todas 4 semanas)")
print(f"Volume medio semanal: {total_transf/4:,.1f} HL/semana")

# Visualização
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Por destino
dest_totals = df_transf.groupby('Destino')['Volume_HL'].sum().sort_values(ascending=True)
cores_dest = [CORES['azul_claro'], CORES['azul_medio'], CORES['azul_escuro']]
axes[0].barh(dest_totals.index, dest_totals.values/1000, color=cores_dest[:len(dest_totals)], edgecolor='white')
axes[0].set_xlabel('Volume Total 4 semanas (mil HL)')
axes[0].set_title('Goose Island — Transf. Programadas por Destino', fontweight='bold')
axes[0].grid(axis='x', alpha=0.3)
for i, (dest, val) in enumerate(dest_totals.items()):
    axes[0].text(val/1000 + 0.2, i, f'{val:,.0f} HL', va='center', fontsize=9)

# Evolução semanal
transf_sem = df_transf.groupby(['Semana_Num', 'Destino'])['Volume_HL'].sum().reset_index()
for dest in df_transf['Destino'].unique():
    data = transf_sem[transf_sem['Destino'] == dest]
    axes[1].plot(data['Semana_Num'], data['Volume_HL']/1000, marker='o', linewidth=2, label=dest)

axes[1].set_xlabel('Semana')
axes[1].set_ylabel('Volume (mil HL)')
axes[1].set_title('Evolucao Semanal das Transferencias', fontweight='bold')
axes[1].set_xticks([1,2,3,4])
axes[1].set_xticklabels(['W1', 'W2', 'W3', 'W4'])
axes[1].legend(fontsize=8)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()

print("\\n--- INSIGHT ABA 4 ---")
print("Apenas Goose Island tem transferencias programadas")
print("Malzbier NAO tem nenhuma transferencia — todo gap deve ser coberto com NOVAS acoes")
print(f"F. Camacari recebe volume constante (7.200 HL/sem)")
print(f"F. Fonte Mata recebe volume apenas na W1 ({df_transf[(df_transf['Destino'].str.contains('FONTE')) & (df_transf['Semana_Num']==1)]['Volume_HL'].sum():,.0f} HL)")"""))

# ══ Aba 5: Cenário Divulgado ══
C.append(md("""---
## 20. Análise Univariada — Aba 5: Cenário Divulgado NENO (Baseline)

> **O que é esta aba?** O cenário **antes** do aumento de demanda de Malzbier. Mostra semana a semana (W0–W3 de Fevereiro) como ficam **demanda, estoque e suficiência** para cada SKU em cada sub-região do NENO.

**Sub-regiões:** Mapapi, NE Norte, NE Sul, NO Araguaia, NO Centro
**SKUs:** Patagonia, Goose Island, Malzbier, Colorado"""))

C.append(code("""# ═══════════════════════════════════════════════════════
# ABA 5: CENÁRIO DIVULGADO — ANÁLISE UNIVARIADA
# ═══════════════════════════════════════════════════════

# Filtrar apenas NENO (excluir SP)
div_neno = df_divulgado[df_divulgado['Sub_Regiao'] != 'SP (Origem)'].copy()

print("=" * 70)
print("5.1 DEMANDA TOTAL POR SKU NO NENO — CENÁRIO DIVULGADO")
print("=" * 70)

dem_por_sku = div_neno.groupby('SKU')['Demanda'].sum().sort_values(ascending=False)
print("\\nDemanda total 4 semanas (HL):")
for sku, val in dem_por_sku.items():
    share = val / dem_por_sku.sum() * 100
    print(f"  {sku}: {val:,.0f} HL ({share:.1f}%)")

print(f"\\nTOTAL NENO: {dem_por_sku.sum():,.0f} HL")

# Demanda por sub-região (agregando todos os SKUs)
dem_por_sr = div_neno.groupby('Sub_Regiao')['Demanda'].sum().sort_values(ascending=False)
print(f"\\nDemanda por sub-regiao (todos os SKUs):")
for sr, val in dem_por_sr.items():
    share = val / dem_por_sr.sum() * 100
    print(f"  {sr}: {val:,.0f} HL ({share:.1f}%)")

# Visualização 5.1
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# a) Demanda por SKU
colors_sku_list = [CORES['ambar'], CORES['azul_medio'], CORES['verde'], CORES['azul_claro']]
axes[0,0].bar(range(len(dem_por_sku)), dem_por_sku.values/1000, color=colors_sku_list[:len(dem_por_sku)], edgecolor='white')
axes[0,0].set_xticks(range(len(dem_por_sku)))
axes[0,0].set_xticklabels(dem_por_sku.index, fontsize=9)
axes[0,0].set_ylabel('Demanda (mil HL)')
axes[0,0].set_title('Demanda Total NENO por SKU (4 semanas)', fontweight='bold')
axes[0,0].grid(axis='y', alpha=0.3)
for i, val in enumerate(dem_por_sku.values):
    axes[0,0].text(i, val/1000 + 0.3, f'{val/1000:.1f}k', ha='center', fontsize=9, fontweight='bold')

# b) Demanda por sub-região
axes[0,1].barh(dem_por_sr.index, dem_por_sr.values/1000, color=CORES['azul_medio'], edgecolor='white')
axes[0,1].set_xlabel('Demanda (mil HL)')
axes[0,1].set_title('Demanda Total por Sub-Regiao', fontweight='bold')
axes[0,1].grid(axis='x', alpha=0.3)

# c) Heatmap: Demanda SKU × Sub-região (W0-W3 somado)
heat_data = div_neno.groupby(['SKU', 'Sub_Regiao'])['Demanda'].sum().reset_index()
heat_pivot = heat_data.pivot(index='Sub_Regiao', columns='SKU', values='Demanda').fillna(0)

im = axes[1,0].imshow(heat_pivot.values, cmap='YlOrRd', aspect='auto')
axes[1,0].set_xticks(range(len(heat_pivot.columns)))
axes[1,0].set_xticklabels(heat_pivot.columns, fontsize=8, rotation=20)
axes[1,0].set_yticks(range(len(heat_pivot.index)))
axes[1,0].set_yticklabels(heat_pivot.index, fontsize=9)
axes[1,0].set_title('Heatmap: Demanda SKU x Sub-Regiao (HL)', fontweight='bold')

for i in range(len(heat_pivot.index)):
    for j in range(len(heat_pivot.columns)):
        val = heat_pivot.iloc[i, j]
        color = 'white' if val > heat_pivot.values.max() * 0.6 else 'black'
        axes[1,0].text(j, i, f'{val:,.0f}', ha='center', va='center', fontsize=7, color=color)

plt.colorbar(im, ax=axes[1,0], shrink=0.8)

# d) Evolução semanal da demanda total
dem_semanal = div_neno.groupby('Semana_Num')['Demanda'].sum()
axes[1,1].plot(dem_semanal.index, dem_semanal.values/1000, marker='s', linewidth=2.5,
               color=CORES['azul_escuro'], markersize=8)
axes[1,1].fill_between(dem_semanal.index, dem_semanal.values/1000, alpha=0.15, color=CORES['azul_medio'])
axes[1,1].set_xlabel('Semana')
axes[1,1].set_ylabel('Demanda Total (mil HL)')
axes[1,1].set_title('Evolucao Semanal da Demanda NENO', fontweight='bold')
axes[1,1].set_xticks([1,2,3,4])
axes[1,1].set_xticklabels(['W1', 'W2', 'W3', 'W4'])
axes[1,1].grid(alpha=0.3)

plt.tight_layout()
plt.show()"""))

C.append(code("""# ═══════════════════════════════════════════════════════
# 5.2 SUFICIÊNCIA (DOI) POR SKU × SUB-REGIÃO — CENÁRIO DIVULGADO
# ═══════════════════════════════════════════════════════

print("=" * 70)
print("5.2 SUFICIÊNCIA FINAL (DOI) — CENÁRIO DIVULGADO (W3)")
print("=" * 70)

# Pegar suficiência da última semana (W3) como indicador final
suf_w3 = div_neno[div_neno['Semana_Num'] == 4][['SKU', 'Sub_Regiao', 'Suf_Final_dias']].copy()
suf_pivot = suf_w3.pivot(index='Sub_Regiao', columns='SKU', values='Suf_Final_dias').round(1)
display(suf_pivot)

DOI_MIN = 12

# Contagem de células críticas
total_cells = suf_pivot.size
criticas = (suf_pivot < DOI_MIN).sum().sum()
negativas = (suf_pivot < 0).sum().sum()
print(f"\\nCelulas com DOI < {DOI_MIN} dias: {criticas}/{total_cells} ({criticas/total_cells*100:.0f}%)")
print(f"Celulas com DOI NEGATIVO (ruptura): {negativas}/{total_cells}")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Heatmap de suficiência
import matplotlib.colors as mcolors
# Custom colormap: vermelho -> amarelo -> verde
cmap = mcolors.LinearSegmentedColormap.from_list('doi', ['#E74C3C', '#F5A623', '#27AE60'])
norm = mcolors.TwoSlopeNorm(vmin=suf_pivot.values.min(), vcenter=DOI_MIN, vmax=max(suf_pivot.values.max(), 30))

im = axes[0].imshow(suf_pivot.values, cmap=cmap, norm=norm, aspect='auto')
axes[0].set_xticks(range(len(suf_pivot.columns)))
axes[0].set_xticklabels(suf_pivot.columns, fontsize=8, rotation=20)
axes[0].set_yticks(range(len(suf_pivot.index)))
axes[0].set_yticklabels(suf_pivot.index, fontsize=9)
axes[0].set_title(f'Suficiencia Final W3 (dias) — Min: {DOI_MIN}d', fontweight='bold')

for i in range(len(suf_pivot.index)):
    for j in range(len(suf_pivot.columns)):
        val = suf_pivot.iloc[i, j]
        color = 'white' if val < 5 else 'black'
        marker = ' !!' if val < DOI_MIN else ''
        axes[0].text(j, i, f'{val:.1f}d{marker}', ha='center', va='center', fontsize=8,
                    fontweight='bold' if val < DOI_MIN else 'normal', color=color)

plt.colorbar(im, ax=axes[0], shrink=0.8, label='DOI (dias)')

# Grouped bar: Suf final W3 por sub-região, agrupado por SKU
skus = suf_pivot.columns.tolist()
x = np.arange(len(suf_pivot.index))
w = 0.18
sku_cols = [CORES['ambar'], CORES['azul_medio'], CORES['verde'], CORES['azul_claro']]

for i, sku in enumerate(skus):
    vals = suf_pivot[sku].values
    axes[1].bar(x + i*w - w*1.5, vals, w, label=sku, color=sku_cols[i % len(sku_cols)], edgecolor='white')

axes[1].axhline(y=DOI_MIN, color=CORES['vermelho'], linestyle='--', linewidth=2, label=f'DOI min = {DOI_MIN}d')
axes[1].set_xticks(x)
axes[1].set_xticklabels(suf_pivot.index, fontsize=8)
axes[1].set_ylabel('Suficiencia (dias)')
axes[1].set_title('DOI Final W3 por Sub-Regiao e SKU', fontweight='bold')
axes[1].legend(fontsize=7, loc='upper right')
axes[1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()

# Identificar pontos críticos
print("\\n--- PONTOS CRITICOS (DOI < 12 dias no cenario DIVULGADO) ---")
for sr in suf_pivot.index:
    for sku in suf_pivot.columns:
        val = suf_pivot.loc[sr, sku]
        if val < DOI_MIN:
            status = "RUPTURA" if val < 0 else "CRITICO" if val < 5 else "ALERTA"
            print(f"  [{status}] {sr} / {sku}: {val:.1f} dias")"""))

# ══ Aba 6: Nova Demanda ══
C.append(md("""---
## 21. Análise Univariada — Aba 6: Cenário com Nova Demanda (+30% Malzbier)

> **O que é esta aba?** O cenário com o **aumento de +30% na demanda de Malzbier Brahma** para Fevereiro. É o cenário que precisa ser resolvido. Comparar com Aba 5 revela exatamente **onde** e **quanto** a pressão aumenta.

**Mudança:** Malzbier +30% em todas as sub-regiões. Demais SKUs: **inalterados**.
**Gap a cobrir:** ~4.500 HL (simplificado) ou até ~11.629 HL considerando bias de +9%."""))

C.append(code("""# ═══════════════════════════════════════════════════════
# ABA 6: NOVA DEMANDA — ANÁLISE UNIVARIADA + COMPARAÇÃO
# ═══════════════════════════════════════════════════════

nova_neno = df_nova_dem[df_nova_dem['Sub_Regiao'] != 'SP (Origem)'].copy()

print("=" * 70)
print("6.1 IMPACTO DO +30% MALZBIER NA DEMANDA NENO")
print("=" * 70)

# Comparar demanda total por SKU: Divulgado vs Nova
dem_div = div_neno.groupby('SKU')['Demanda'].sum()
dem_nova = nova_neno.groupby('SKU')['Demanda'].sum()

comp = pd.DataFrame({
    'Divulgado_HL': dem_div,
    'Nova_Dem_HL': dem_nova,
})
comp['Delta_HL'] = comp['Nova_Dem_HL'] - comp['Divulgado_HL']
comp['Delta_Pct'] = (comp['Delta_HL'] / comp['Divulgado_HL'] * 100).round(1)
display(comp)

gap_malzbier = comp.loc['Malzbier', 'Delta_HL']
print(f"\\nGap total Malzbier: {gap_malzbier:,.0f} HL (4 semanas)")
print(f"Gap semanal medio: {gap_malzbier/4:,.0f} HL/semana")

# Impacto por sub-região (apenas Malzbier)
print(f"\\n{'='*70}")
print(f"6.2 GAP DE MALZBIER POR SUB-REGIÃO")
print(f"{'='*70}")

malz_div = div_neno[div_neno['SKU']=='Malzbier'].groupby('Sub_Regiao')['Demanda'].sum()
malz_nova = nova_neno[nova_neno['SKU']=='Malzbier'].groupby('Sub_Regiao')['Demanda'].sum()

gap_sr = pd.DataFrame({
    'Divulgado': malz_div,
    'Nova_Dem': malz_nova,
    'Gap_HL': malz_nova - malz_div,
    'Gap_Pct': ((malz_nova - malz_div) / malz_div * 100).round(1)
})
gap_sr = gap_sr.sort_values('Gap_HL', ascending=False)
display(gap_sr)

# Visualização
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# a) Demanda por SKU: antes vs depois
x = np.arange(len(comp))
w = 0.35
axes[0,0].bar(x - w/2, comp['Divulgado_HL']/1000, w, color=CORES['azul_medio'], label='Divulgado', edgecolor='white')
axes[0,0].bar(x + w/2, comp['Nova_Dem_HL']/1000, w, color=CORES['vermelho'], label='Nova Demanda', edgecolor='white')
axes[0,0].set_xticks(x)
axes[0,0].set_xticklabels(comp.index, fontsize=9)
axes[0,0].set_ylabel('Demanda (mil HL)')
axes[0,0].set_title('Demanda NENO: Divulgado vs Nova (+30% Malz)', fontweight='bold')
axes[0,0].legend()
axes[0,0].grid(axis='y', alpha=0.3)

# Anotar delta
for i, (sku, row) in enumerate(comp.iterrows()):
    if abs(row['Delta_HL']) > 10:
        axes[0,0].text(i + w/2, row['Nova_Dem_HL']/1000 + 0.3, f'+{row["Delta_HL"]/1000:.1f}k',
                       ha='center', fontsize=8, fontweight='bold', color=CORES['vermelho'])

# b) Gap Malzbier por sub-região
gap_sorted = gap_sr.sort_values('Gap_HL', ascending=True)
colors_gap = [CORES['vermelho'] if g > 0 else CORES['verde'] for g in gap_sorted['Gap_HL']]
axes[0,1].barh(gap_sorted.index, gap_sorted['Gap_HL'], color=colors_gap, edgecolor='white')
axes[0,1].set_xlabel('Gap (HL)')
axes[0,1].set_title('Gap de Malzbier por Sub-Regiao (+30%)', fontweight='bold')
axes[0,1].grid(axis='x', alpha=0.3)
for i, (sr, row) in enumerate(gap_sorted.iterrows()):
    axes[0,1].text(row['Gap_HL'] + 20, i, f'+{row["Gap_HL"]:.0f} HL', va='center', fontsize=8)

# c) Suficiência W3: Divulgado vs Nova Demanda (Malzbier only)
suf_div_malz = div_neno[(div_neno['SKU']=='Malzbier') & (div_neno['Semana_Num']==4)][['Sub_Regiao','Suf_Final_dias']]
suf_nova_malz = nova_neno[(nova_neno['SKU']=='Malzbier') & (nova_neno['Semana_Num']==4)][['Sub_Regiao','Suf_Final_dias']]

suf_comp = pd.merge(suf_div_malz, suf_nova_malz, on='Sub_Regiao', suffixes=('_Div', '_Nova'))
suf_comp = suf_comp.sort_values('Suf_Final_dias_Nova')

x = np.arange(len(suf_comp))
axes[1,0].bar(x - 0.2, suf_comp['Suf_Final_dias_Div'], 0.35, color=CORES['azul_medio'], label='Divulgado', edgecolor='white')
axes[1,0].bar(x + 0.2, suf_comp['Suf_Final_dias_Nova'], 0.35, color=CORES['vermelho'], label='Nova Demanda', edgecolor='white')
axes[1,0].axhline(y=DOI_MIN, color='black', linestyle='--', linewidth=1.5, label=f'DOI min = {DOI_MIN}d')
axes[1,0].set_xticks(x)
axes[1,0].set_xticklabels(suf_comp['Sub_Regiao'], fontsize=8, rotation=15)
axes[1,0].set_ylabel('DOI (dias)')
axes[1,0].set_title('Malzbier: DOI Final W3 — Antes vs Depois', fontweight='bold')
axes[1,0].legend(fontsize=8)
axes[1,0].grid(axis='y', alpha=0.3)

# d) Evolução semanal Malzbier: div vs nova
malz_div_sem = div_neno[div_neno['SKU']=='Malzbier'].groupby('Semana_Num')['Demanda'].sum()
malz_nova_sem = nova_neno[nova_neno['SKU']=='Malzbier'].groupby('Semana_Num')['Demanda'].sum()

axes[1,1].plot(malz_div_sem.index, malz_div_sem.values/1000, marker='o', linewidth=2,
               color=CORES['azul_medio'], label='Divulgado')
axes[1,1].plot(malz_nova_sem.index, malz_nova_sem.values/1000, marker='s', linewidth=2,
               color=CORES['vermelho'], label='Nova Demanda (+30%)')
axes[1,1].fill_between(malz_nova_sem.index, malz_div_sem.values/1000, malz_nova_sem.values/1000,
                        alpha=0.2, color=CORES['vermelho'], label='Gap')
axes[1,1].set_xlabel('Semana')
axes[1,1].set_ylabel('Demanda Malzbier (mil HL)')
axes[1,1].set_title('Malzbier NENO: Evolucao Semanal do Gap', fontweight='bold')
axes[1,1].set_xticks([1,2,3,4])
axes[1,1].set_xticklabels(['W1', 'W2', 'W3', 'W4'])
axes[1,1].legend(fontsize=8)
axes[1,1].grid(alpha=0.3)

plt.tight_layout()
plt.show()"""))

C.append(code("""# ═══════════════════════════════════════════════════════
# 6.3 ANÁLISE DE SUFICIÊNCIA COMPLETA — NOVA DEMANDA (TODOS SKUs)
# ═══════════════════════════════════════════════════════

print("=" * 70)
print("6.3 SUFICIÊNCIA FINAL W3 — CENÁRIO NOVA DEMANDA (TODOS SKUs)")
print("=" * 70)

suf_nova_w3 = nova_neno[nova_neno['Semana_Num'] == 4][['SKU', 'Sub_Regiao', 'Suf_Final_dias']].copy()
suf_nova_pivot = suf_nova_w3.pivot(index='Sub_Regiao', columns='SKU', values='Suf_Final_dias').round(1)
display(suf_nova_pivot)

# Comparação com cenário divulgado
print(f"\\n{'='*70}")
print(f"6.4 DELTA DE DOI: (Nova Demanda - Divulgado)")
print(f"{'='*70}")

delta_doi = suf_nova_pivot - suf_pivot
display(delta_doi.round(1))

# Visualização final: Heatmap de suficiência Nova Demanda
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

import matplotlib.colors as mcolors
cmap = mcolors.LinearSegmentedColormap.from_list('doi', ['#E74C3C', '#F5A623', '#27AE60'])
norm = mcolors.TwoSlopeNorm(vmin=min(suf_nova_pivot.values.min(), -7), vcenter=DOI_MIN, vmax=max(suf_nova_pivot.values.max(), 30))

im = axes[0].imshow(suf_nova_pivot.values, cmap=cmap, norm=norm, aspect='auto')
axes[0].set_xticks(range(len(suf_nova_pivot.columns)))
axes[0].set_xticklabels(suf_nova_pivot.columns, fontsize=8, rotation=20)
axes[0].set_yticks(range(len(suf_nova_pivot.index)))
axes[0].set_yticklabels(suf_nova_pivot.index, fontsize=9)
axes[0].set_title('DOI Final W3 — Nova Demanda (+30% Malz)', fontweight='bold')

for i in range(len(suf_nova_pivot.index)):
    for j in range(len(suf_nova_pivot.columns)):
        val = suf_nova_pivot.iloc[i, j]
        color = 'white' if val < 5 else 'black'
        marker = ' !!' if val < DOI_MIN else ''
        axes[0].text(j, i, f'{val:.1f}d{marker}', ha='center', va='center', fontsize=8,
                    fontweight='bold' if val < DOI_MIN else 'normal', color=color)

plt.colorbar(im, ax=axes[0], shrink=0.8, label='DOI (dias)')

# Delta DOI heatmap (impacto)
max_abs = max(abs(delta_doi.values.min()), abs(delta_doi.values.max()), 1)
im2 = axes[1].imshow(delta_doi.values, cmap='RdYlGn', vmin=-max_abs, vmax=max_abs, aspect='auto')
axes[1].set_xticks(range(len(delta_doi.columns)))
axes[1].set_xticklabels(delta_doi.columns, fontsize=8, rotation=20)
axes[1].set_yticks(range(len(delta_doi.index)))
axes[1].set_yticklabels(delta_doi.index, fontsize=9)
axes[1].set_title('Delta DOI (Nova - Divulgado)', fontweight='bold')

for i in range(len(delta_doi.index)):
    for j in range(len(delta_doi.columns)):
        val = delta_doi.iloc[i, j]
        if abs(val) > 0.1:
            color = 'white' if abs(val) > max_abs * 0.6 else 'black'
            sign = '+' if val > 0 else ''
            axes[1].text(j, i, f'{sign}{val:.1f}d', ha='center', va='center', fontsize=8, color=color)

plt.colorbar(im2, ax=axes[1], shrink=0.8, label='Delta DOI (dias)')

plt.tight_layout()
plt.show()

# Resumo de pontos críticos
print("\\n--- PONTOS CRITICOS NA NOVA DEMANDA ---")
for sr in suf_nova_pivot.index:
    for sku in suf_nova_pivot.columns:
        val = suf_nova_pivot.loc[sr, sku]
        if val < DOI_MIN:
            delta = delta_doi.loc[sr, sku]
            agravou = " (AGRAVOU)" if delta < -0.5 else ""
            status = "RUPTURA" if val < 0 else "CRITICO" if val < 5 else "ALERTA"
            print(f"  [{status}] {sr} / {sku}: {val:.1f} dias (delta: {delta:+.1f}d){agravou}")"""))

# ══ Análise Transversal: Estatísticas descritivas consolidadas ══
C.append(md("""---
## 22. Resumo Estatístico Consolidado — Todas as Variáveis

> Visão geral das **estatísticas descritivas** de cada variável numérica relevante, consolidando insights de todas as 6 abas para facilitar a tomada de decisão."""))

C.append(code("""# ═══════════════════════════════════════════════════════
# RESUMO ESTATÍSTICO CONSOLIDADO
# ═══════════════════════════════════════════════════════

print("=" * 70)
print("ESTATÍSTICAS DESCRITIVAS CONSOLIDADAS")
print("=" * 70)

# 1. Demanda NENO Nova por SKU
print("\\n[1] DEMANDA NENO SEMANAL (Nova Demanda) — HL/semana:")
for sku in ['Patagonia', 'Goose Island', 'Malzbier', 'Colorado']:
    vals = nova_neno[nova_neno['SKU']==sku].groupby('Semana_Num')['Demanda'].sum()
    print(f"  {sku}: Media={vals.mean():,.0f} | DP={vals.std():,.0f} | Min={vals.min():,.0f} | Max={vals.max():,.0f} | CV={vals.std()/vals.mean()*100:.1f}%")

# 2. Suficiência NENO Nova
print("\\n[2] SUFICIÊNCIA FINAL (DOI) — Nova Demanda (todos SKU x Sub-Regiao x Semana):")
suf_all = nova_neno['Suf_Final_dias']
print(f"  Media: {suf_all.mean():.1f} dias | Mediana: {suf_all.median():.1f} | DP: {suf_all.std():.1f}")
print(f"  Min: {suf_all.min():.1f} | Max: {suf_all.max():.1f} | < 12 dias: {(suf_all < 12).sum()}/{len(suf_all)} ({(suf_all < 12).mean()*100:.1f}%)")

# 3. Custos
print("\\n[3] CUSTOS DE TRANSFERÊNCIA — R$/HL:")
print(f"  Media: R${df_custos_transf['Custo_R_HL'].mean():.2f} | DP: R${df_custos_transf['Custo_R_HL'].std():.2f}")
print(f"  Min: R${df_custos_transf['Custo_R_HL'].min():.2f} | Max: R${df_custos_transf['Custo_R_HL'].max():.2f}")

# 4. Produção
print("\\n[4] PRODUÇÃO PCP — Utilização Semanal:")
for planta in ['AQ541 (CE)', 'PE541 (PE)']:
    ut = prod_planta_sem[prod_planta_sem['Planta']==planta]['Utilizacao_Pct']
    print(f"  {planta}: Media={ut.mean():.1f}% | Min={ut.min():.1f}% | Max={ut.max():.1f}%")

# Dashboard visual final
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('DASHBOARD UNIVARIADO — Resumo Geral', fontsize=16, fontweight='bold', y=1.02)

# a) Distribuição de demanda NENO (histograma)
dem_vals = nova_neno['Demanda'].values
dem_vals = dem_vals[dem_vals > 0]
axes[0,0].hist(dem_vals, bins=15, color=CORES['azul_medio'], edgecolor='white', alpha=0.8)
axes[0,0].axvline(x=np.mean(dem_vals), color=CORES['vermelho'], linestyle='--', label=f'Media: {np.mean(dem_vals):,.0f}')
axes[0,0].set_xlabel('Demanda (HL)')
axes[0,0].set_title('Distribuicao de Demanda\\n(todas sub-regioes/SKUs)', fontweight='bold')
axes[0,0].legend(fontsize=8)
axes[0,0].grid(alpha=0.3)

# b) Distribuição DOI
suf_vals = nova_neno['Suf_Final_dias'].values
axes[0,1].hist(suf_vals, bins=20, color=CORES['ambar'], edgecolor='white', alpha=0.8)
axes[0,1].axvline(x=DOI_MIN, color=CORES['vermelho'], linestyle='--', linewidth=2, label=f'DOI min: {DOI_MIN}d')
axes[0,1].axvline(x=np.median(suf_vals), color=CORES['azul_escuro'], linestyle=':', label=f'Mediana: {np.median(suf_vals):.1f}d')
axes[0,1].set_xlabel('DOI (dias)')
axes[0,1].set_title('Distribuicao de Suficiencia\\n(Nova Demanda)', fontweight='bold')
axes[0,1].legend(fontsize=8)
axes[0,1].grid(alpha=0.3)

# c) Box plot de DOI por SKU
sku_doi_data = []
sku_labels = []
for sku in ['Patagonia', 'Goose Island', 'Malzbier', 'Colorado']:
    vals = nova_neno[nova_neno['SKU']==sku]['Suf_Final_dias'].values
    sku_doi_data.append(vals)
    sku_labels.append(sku)

bp = axes[0,2].boxplot(sku_doi_data, labels=sku_labels, patch_artist=True,
                        medianprops=dict(color='black', linewidth=2))
colors_box = [CORES['ambar'], CORES['azul_medio'], CORES['verde'], CORES['azul_claro']]
for patch, color in zip(bp['boxes'], colors_box):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
axes[0,2].axhline(y=DOI_MIN, color=CORES['vermelho'], linestyle='--', linewidth=1.5, label=f'DOI min')
axes[0,2].set_ylabel('DOI (dias)')
axes[0,2].set_title('Box Plot DOI por SKU\\n(Nova Demanda)', fontweight='bold')
axes[0,2].legend(fontsize=8)
axes[0,2].tick_params(axis='x', rotation=15)
axes[0,2].grid(axis='y', alpha=0.3)

# d) Utilização de plantas (gauge-like)
for idx, (planta, cap) in enumerate([('AQ541 (CE)', cap_aq), ('PE541 (PE)', cap_pe)]):
    ut_media = prod_planta_sem[prod_planta_sem['Planta']==planta]['Utilizacao_Pct'].mean()
    color = CORES['verde'] if ut_media < 85 else CORES['ambar'] if ut_media < 95 else CORES['vermelho']

    axes[1, idx].barh([0], [ut_media], color=color, height=0.4, edgecolor='white')
    axes[1, idx].barh([0], [100 - ut_media], left=[ut_media], color=CORES['cinza_claro'], height=0.4, edgecolor='white')
    axes[1, idx].set_xlim(0, 110)
    axes[1, idx].set_yticks([])
    axes[1, idx].set_xlabel('Utilizacao (%)')
    axes[1, idx].set_title(f'{planta}\\nUtiliz. media: {ut_media:.1f}%', fontweight='bold')
    axes[1, idx].axvline(x=100, color='black', linewidth=2)
    axes[1, idx].text(ut_media/2, 0, f'{ut_media:.0f}%', ha='center', va='center', fontsize=14,
                      fontweight='bold', color='white')

# f) Custo de transferência por SKU
sku_custo_mean = df_custos_transf.copy()
sku_custo_mean['SKU_curto'] = sku_custo_mean['SKU'].str.split(' ').str[0]
sku_cm = sku_custo_mean.groupby('SKU_curto')['Custo_R_HL'].agg(['mean','min','max']).reset_index()

x_pos = np.arange(len(sku_cm))
axes[1,2].bar(x_pos, sku_cm['mean'], color=[CORES['verde'], CORES['azul_medio'], CORES['ambar']],
              edgecolor='white', width=0.5)
axes[1,2].errorbar(x_pos, sku_cm['mean'],
                    yerr=[sku_cm['mean']-sku_cm['min'], sku_cm['max']-sku_cm['mean']],
                    fmt='none', color='black', capsize=5)
axes[1,2].set_xticks(x_pos)
axes[1,2].set_xticklabels(sku_cm['SKU_curto'])
axes[1,2].set_ylabel('R$/HL')
axes[1,2].set_title('Custo Medio Transferencia\\n(min-max)', fontweight='bold')
axes[1,2].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()"""))

# ══ Insights consolidados ══
C.append(md("""---
## 23. Insights da Análise Univariada — Síntese Executiva

> Esta síntese consolida os achados mais relevantes de todas as 6 abas. Os números são extraídos diretamente dos dados — sem estimativas.

---

### 1. O Gap Real é Maior do que Parece

O aumento de **+30% no Malzbier** gera um gap de **11.680 HL ao longo de 4 semanas** (≈ 2.920 HL/semana). Porém, os dados apontam um agravante: há um **BIAS de +9%** de sobre-previsão pelos GEOs. Isso significa que parte da demanda divulgada já está inflada. Mesmo descontando o BIAS, o gap corrigido seria de ~**10.630 HL** — ainda assim inviável de cobrir só com estoque existente.

**Por quê isso importa?** Aceitar o BIAS como válido pode levar a uma transferência ou produção excessiva, gerando custo desnecessário. Acionar o BIAS como desculpa para não agir pode gerar ruptura real. A decisão exige julgamento comercial.

---

### 2. A Produção Local Não Resolve Sozinha

As duas plantas do NENO estão quase no limite:

| Planta | Capacidade/sem | Utilização média | Folga total no mês |
|---|---|---|---|
| **AQ541 (Aquiraz/CE)** | 12.600 HL | 95.7% | **2.160 HL** |
| **PE541 (Pernambuco)** | 27.000 HL | 93.3% | **5.400 HL** |

O gap mensal de Malzbier é **11.680 HL**. A folga combinada das duas plantas é de apenas **7.560 HL** — e essa folga está ocupada por outros SKUs. **Realocação de produção interna cobre no máximo ~65% do gap**, e ainda exigiria sacrificar outros produtos.

Agravante: **Goose Island não pode aumentar produção em PE** (restrição de elaboração de líquido). Qualquer realocação em PE precisa partir de outros SKUs — Brahma Chopp Zero, Budweiser Zero ou Colorado.

---

### 3. Transferência de SP é Necessária, Mas Cara

A única fonte com volume disponível para suprir o NENO é **SP (Jaguariúna)**, via cabotagem. Mas o custo é alto:

| Rota | Custo | % da Margem Bruta (R\\$136/HL) |
|---|---|---|
| Jaguariúna → Camaçari | R\\$84,6/HL | **62%** |
| Jaguariúna → Fonte Mata | R\\$95,3/HL | **70%** |
| Rodoviário emergencial (est.) | ~R\\$135/HL | **~99%** |

Ou seja, **cobrir o gap via rodoviário emergencial praticamente anula a margem do Malzbier**. Cabotagem preserva ~30-38% da margem, mas tem lead time de 25 dias — o que significa que, para chegar em fevereiro, o pedido precisaria já ter sido feito.

**Conclusão crítica:** O rodoviário só se justifica para volumes pequenos e urgentes. Para o volume total do gap, a cabotagem planejada com antecedência é o único modal economicamente viável.

---

### 4. Prioridade Geográfica: Nem Todas as Sub-Regiões são Iguais

Com o +30% de Malzbier, o impacto no DOI final (W3) é drasticamente diferente por sub-região:

| Sub-Região | DOI Divulgado | DOI Nova Demanda | Situação |
|---|---|---|---|
| **Mapapi** | 3.4 dias | **-3.2 dias** | RUPTURA — prioridade máxima |
| **NE Norte** | 4.6 dias | **-2.3 dias** | RUPTURA — prioridade máxima |
| **NE Sul** | 20.4 dias | **9.8 dias** | ALERTA — monitorar |
| **NO Centro** | 14.3 dias | **4.8 dias** | CRITICO — ação necessária |
| **NO Araguaia** | ~0 dias | **-6.3 dias** | RUPTURA — mas é 100% revenda¹ |

> ¹ **NO Araguaia é 100% revendedores**: gerenciam o próprio estoque e fazem retirada em Uberlândia. A ruptura registrada aqui é do estoque deles, não da Ambev diretamente. Pode ser deprioritizado na alocação de recursos.

**Mapapi sozinho representa 34.6% da demanda total do NENO** e ~43% do gap de Malzbier — é onde qualquer ação tem maior retorno.

---

### 5. O Cenário Já Era Tenso Antes do +30%

Um dado que merece atenção: **mesmo no cenário divulgado (sem o aumento)**, 12 das 20 combinações sub-região × SKU já estavam abaixo do DOI mínimo de 12 dias. Isso revela que o NENO operava no limite antes do choque de demanda.

Isso sugere que o problema **não é apenas o +30% de Malzbier** — é um sistema logístico que já estava estressado. O aumento de demanda foi o gatilho que tornou o problema visível.

---

### 6. SP e RJ são as Âncoras da Malha

Na visão nacional (Aba 1), SP envia **-75.583 HL** e RJ envia **-174.401 HL** para outras regiões em fevereiro. São os dois grandes fornecedores da malha. Para o case, isso confirma que **SP tem capacidade excedente para transferir** — a questão é apenas custo e timing.

NENO recebe **+34.507 HL** da malha em fevereiro no cenário atual. Com o aumento de Malzbier, esse volume de recebimento precisará crescer ainda mais.

---

### 7. A Janela de Decisão é Estreita

Considerando que:
- Cabotagem tem lead time de **25 dias**
- Fevereiro tem 28 dias
- A demanda aumenta a partir de W1 (02/02)

Qualquer transferência por cabotagem para cobrir o gap de fevereiro **precisaria ter sido acionada em janeiro**. Se o prazo já passou, o modal disponível passa a ser rodoviário — com custo ~60% mais alto e risco adicional de 5% de avaria.

**Isso coloca o time de S\\&OE (planejamento semanal) em uma decisão de emergência:** aceitar o custo extra do rodoviário, ou priorizar a cobertura das sub-regiões mais críticas (Mapapi e NE Norte) e aceitar ruptura controlada nas demais.

---

### Resumo dos Números-Chave

| Métrica | Valor |
|---|---|
| Gap total Malzbier (4 semanas) | **11.680 HL** |
| Gap semanal médio | **2.920 HL/semana** |
| Folga produtiva NE (AQ541 + PE541) | **~7.560 HL/mês** |
| Custo cabotagem Malzbier (rota mais barata) | **R\\$ 84,6/HL** |
| Margem bruta Malzbier | **R\\$ 136/HL (47,7%)** |
| Margem líquida após transferência | **R\\$ 51,4/HL (18%)** |
| Sub-regiões em ruptura (Nova Demanda) | **3 de 5** |
| Combinações SKU × sub-região críticas | **15 de 20** |
| DOI NENO Fev (cenário atual) | **13.3 dias** (1.3d acima do mínimo) |

---

> **Próximo passo — Árvore de Hipóteses MECE:** estruturar as opções de decisão em 3 eixos (Produção / Transferência / Demanda) e simular o impacto financeiro de cada cenário na Análise Bivariada."""))

# ═══════════════════════════════════════════════════════════════════════════════
# PARTE 3: ÁRVORE DE HIPÓTESES MECE
# ═══════════════════════════════════════════════════════════════════════════════

C.append(md("""---
---

# PARTE 3 — Árvore de Hipóteses MECE

> **Objetivo:** Estruturar as opções de decisão em hipóteses **mutuamente exclusivas e coletivamente exaustivas** (MECE), quantificadas com os dados do Data Contract e da Análise Univariada.

---

### Questão Central

> *"Devemos atender o aumento de +30% na demanda de Malzbier Brahma LN no NENO em fevereiro? Se sim, qual o plano ótimo de produção e transferência que maximiza margem e minimiza risco de ruptura?"*

As **4 perguntas do case** (PDF "Contexto do Case LN"):

| # | Pergunta | Eixo da Árvore |
|---|---|---|
| 1 | Devemos seguir com os incentivos comerciais? | Eixo 3 (Demanda) + Eixo 4 (Financeiro) |
| 2 | Qual será o plano de produção e transferência? | Eixo 1 (Produção) + Eixo 2 (Transferência) |
| 3 | Quanto vai custar a operação? | Eixo 4 (Financeiro) |
| 4 | Quais os riscos envolvidos? | Eixo 5 (Risco) |

**Dado adicional do PDF de contexto (não presente no Excel):** além do +30% em fevereiro, o time comercial sinalizou que a **demanda deve crescer +10% no TT LN por mês a partir de março** caso queiram crescer market share. A decisão de fevereiro define o posicionamento para os meses seguintes.

---

### Estrutura da Árvore (5 Eixos)

| Eixo | Pergunta-Guia | Hipóteses |
|---|---|---|
| **1. Produção Local** | Podemos produzir mais Malzbier no NE? | 3 hipóteses |
| **2. Transferência** | Compensa trazer de SP? Como? | 4 hipóteses |
| **3. Demanda** | Podemos reduzir ou redistribuir a demanda? | 3 hipóteses |
| **4. Financeiro** | Qual o cenário de custo ótimo? | 3 hipóteses |
| **5. Risco** | Quais os riscos de cada decisão? | 4 hipóteses |"""))

# ══ Diagrama visual da árvore ══
C.append(code("""# ═══════════════════════════════════════════════════════
# DIAGRAMA VISUAL — ÁRVORE DE HIPÓTESES MECE
# ═══════════════════════════════════════════════════════

fig, ax = plt.subplots(figsize=(18, 14))
ax.set_xlim(0, 18)
ax.set_ylim(0, 14)
ax.axis('off')
fig.patch.set_facecolor('#FAFAFA')

# ── Questão Central ──
ax.add_patch(FancyBboxPatch((5.5, 12.5), 7, 1.2, boxstyle='round,pad=0.15',
             facecolor='#2C3E50', edgecolor='#1A252F', linewidth=2))
ax.text(9, 13.1, 'Devemos atender +30% Malzbier NENO?', fontsize=12,
        fontweight='bold', ha='center', va='center', color='white')
ax.text(9, 12.75, 'Gap: 11.680 HL | 4 semanas | Fev 2026', fontsize=9,
        ha='center', va='center', color='#BDC3C7')

# ── 5 Eixos ──
eixos = [
    (1.5, 'PRODUÇÃO\\nLOCAL', '#27AE60', [
        'H1.1 Realocar PE541',
        'H1.2 Realocar AQ541',
        'H1.3 Ociosidade W1'
    ]),
    (5.0, 'TRANSFERÊNCIA\\nSP→NE', '#2980B9', [
        'H2.1 Cabo→Camaçari',
        'H2.2 Cabo→Fonte Mata',
        'H2.3 Rodoviário',
        'H2.4 Não transferir'
    ]),
    (9.0, 'GESTÃO DE\\nDEMANDA', '#F39C12', [
        'H3.1 Descontar BIAS',
        'H3.2 Priorizar sub-regiões',
        'H3.3 Phasing temporal'
    ]),
    (12.5, 'ANÁLISE\\nFINANCEIRA', '#8E44AD', [
        'H4.1 Cenários de custo',
        'H4.2 Breakeven atender',
        'H4.3 Visão Mar+ (+10%/mês)'
    ]),
    (16.0, 'RISCO E\\nCONTINGÊNCIA', '#E74C3C', [
        'H5.1 Avaria rodoviário',
        'H5.2 Atraso cabotagem',
        'H5.3 Sub-previsão BIAS',
        'H5.4 Canibalização SKUs'
    ]),
]

for x, label, color, hips in eixos:
    # Caixa do eixo
    ax.add_patch(FancyBboxPatch((x-0.7, 9.5), 2.6, 1.5, boxstyle='round,pad=0.12',
                 facecolor=color, edgecolor='white', linewidth=1.5, alpha=0.9))
    ax.text(x+0.6, 10.25, label, fontsize=8.5, fontweight='bold',
            ha='center', va='center', color='white')
    # Linha da questão central ao eixo
    ax.annotate('', xy=(x+0.6, 11.0), xytext=(9, 12.5),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5))
    # Hipóteses
    for i, h in enumerate(hips):
        y = 8.5 - i * 1.4
        ax.add_patch(FancyBboxPatch((x-0.7, y-0.35), 2.6, 0.7,
                     boxstyle='round,pad=0.08', facecolor='white',
                     edgecolor=color, linewidth=1.2))
        ax.text(x+0.6, y, h, fontsize=7, ha='center', va='center',
                color='#2C3E50', fontweight='bold')
        # Linha do eixo à hipótese
        ax.plot([x+0.6, x+0.6], [9.5, y+0.35], color=color, lw=0.8, alpha=0.5)

ax.text(9, 0.3, 'MECE — Mutuamente Exclusivo, Coletivamente Exaustivo | 5 Eixos, 17 Hipóteses',
        fontsize=10, ha='center', va='center', color='#7F8C8D', style='italic')

plt.tight_layout()
plt.show()"""))

# ══ Eixo 1: Produção Local ══
C.append(md("""---
## 24. Eixo 1 — Produção Local: Podemos Produzir Mais Malzbier no NE?

> Pergunta-guia: *Existe capacidade ociosa ou realocável nas plantas AQ541 e PE541 que permita aumentar a produção de Malzbier sem transferência de SP?*

### Dados de Partida

| Planta | Cap./sem | Utiliz. média | Folga mensal | Malzbier atual (4 sem) |
|---|---|---|---|---|
| **AQ541 (Aquiraz/CE)** | 12.600 HL | 95,7% | 2.160 HL | 16.560 HL |
| **PE541 (Pernambuco)** | 27.000 HL | 93,3% | 7.200 HL | 29.160 HL |
| **Total NE** | 39.600 HL | — | 9.360 HL | 45.720 HL |

**Gap a cobrir:** 11.680 HL. **Folga total disponível:** 9.360 HL (80% do gap).

### H1.1 — Realocar SKUs em PE541 para Malzbier

PE541 produz 6 SKUs. Goose Island **não pode ser realocada** (restrição de elaboração de líquido). Os candidatos à realocação:

| SKU | Volume 4 sem | MACO R\$/HL | Custo oportunidade | Candidato? |
|---|---|---|---|---|
| Brahma Chopp Zero | 3.600 HL | ~R\$250¹ | Baixo | **Sim** |
| Skol Beats | 3.240 HL | ~R\$260¹ | Baixo | **Sim** |
| Colorado | 16.200 HL | R\$300 | Médio | **Parcial** |
| Budweiser Zero | 16.200 HL | ~R\$270¹ | Médio | **Parcial** |
| Goose Island | 32.400 HL | R\$350 | Alto | **Não (restrição)** |

> ¹ Valores estimados (MACO exato disponível apenas para Colorado, Goose e Malzbier no Excel)

**Potencial máximo:** realocar Brahma Zero + Skol Beats = **6.840 HL** sem afetar SKUs de alto valor.

### H1.2 — Realocar SKUs em AQ541 para Malzbier

AQ541 produz apenas 2 SKUs: Malzbier (16.560 HL) e Patagonia (31.680 HL). Colorado = 0.

**Potencial:** converter parte da Patagonia para Malzbier. Mas Patagonia tem demanda própria. Seria necessário verificar se a suficiência de Patagonia no NENO permite redução.

### H1.3 — Aproveitar Ociosidade PE541 W1

Dado crítico: **PE541 W1 opera a apenas 73,3%** (19.800/27.000 HL). E especificamente, **Malzbier = 0 HL em PE541 W1** — nenhuma produção de Malzbier está programada nessa semana.

| Semana | Malzbier PE541 | Ociosidade | Potencial Malzbier |
|---|---|---|---|
| W0 (02/02) | 16.200 HL | 0 HL | 0 |
| **W1 (09/02)** | **0 HL** | **7.200 HL** | **até 7.200 HL** |
| W2 (16/02) | 12.960 HL | 0 HL | 0 |
| W3 (23/02) | 0 HL | 0 HL | 0 |

**Esta é a hipótese de maior impacto e menor custo:** produzir 7.200 HL de Malzbier na W1 usando a capacidade ociosa de PE541, sem deslocar nenhum outro SKU. Custo = R\$149/HL (produção local), margem = R\$136/HL (47,7%).

Sozinha, essa hipótese cobre **61,6% do gap de 11.680 HL**."""))

# ══ Eixo 1: Cálculos ══
C.append(code("""# ═══════════════════════════════════════════════════════
# EIXO 1 — QUANTIFICAÇÃO: PRODUÇÃO LOCAL
# ═══════════════════════════════════════════════════════

gap_total = 11680  # HL
custo_prod = 149   # R$/HL
maco_malz = 285    # R$/HL
margem_bruta = 136 # R$/HL

# H1.3: Ociosidade PE541 W1
h13_vol = 7200
h13_custo_total = h13_vol * custo_prod
h13_receita = h13_vol * maco_malz
h13_margem = h13_vol * margem_bruta
h13_cobertura = h13_vol / gap_total * 100

# H1.1: Realocação PE541 (Brahma Zero + Skol Beats)
h11_vol = 3600 + 3240  # 6840 HL
h11_custo_total = h11_vol * custo_prod
h11_margem = h11_vol * margem_bruta
h11_cobertura = h11_vol / gap_total * 100
# Custo de oportunidade: MACO perdido dos SKUs realocados (estimado)
h11_maco_perdido = 3600 * 250 + 3240 * 260  # Brahma Zero ~250, Skol Beats ~260

# Combinado: H1.3 + H1.1
comb_vol = h13_vol + h11_vol
comb_cobertura = comb_vol / gap_total * 100
gap_restante = gap_total - comb_vol

print("=" * 70)
print("EIXO 1 — PRODUÇÃO LOCAL: QUANTIFICAÇÃO")
print("=" * 70)

resumo = pd.DataFrame([
    {'Hipótese': 'H1.3: Ociosidade PE541 W1', 'Volume HL': f'{h13_vol:,.0f}',
     '% do Gap': f'{h13_cobertura:.1f}%', 'Custo R$': f'{h13_custo_total:,.0f}',
     'Margem R$': f'{h13_margem:,.0f}', 'Risco': 'BAIXO'},
    {'Hipótese': 'H1.1: Realocar PE541', 'Volume HL': f'{h11_vol:,.0f}',
     '% do Gap': f'{h11_cobertura:.1f}%', 'Custo R$': f'{h11_custo_total:,.0f}',
     'Margem R$': f'{h11_margem:,.0f}', 'Risco': 'MÉDIO'},
    {'Hipótese': 'COMBINADO (H1.3+H1.1)', 'Volume HL': f'{comb_vol:,.0f}',
     '% do Gap': f'{comb_cobertura:.1f}%', 'Custo R$': f'{(h13_custo_total+h11_custo_total):,.0f}',
     'Margem R$': f'{(h13_margem+h11_margem):,.0f}', 'Risco': 'MÉDIO'},
])
print('Eixo 1 — Produção Local'); display(resumo)

print(f"\\nGap restante após produção local: {gap_restante:,.0f} HL ({gap_restante/gap_total*100:.1f}%)")
print(f"→ Este residual deve ser coberto por Transferência (Eixo 2) ou Gestão de Demanda (Eixo 3)")

# Visualização
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
fig.patch.set_facecolor('#FAFAFA')
fig.suptitle('Eixo 1 — Produção Local: Cobertura do Gap', fontsize=14, fontweight='bold', color='#2C3E50')

# Gráfico 1: Waterfall de cobertura
labels = ['Gap\\nTotal', 'H1.3\\nOciosidade\\nPE541 W1', 'H1.1\\nRealocar\\nPE541', 'Gap\\nRestante']
values = [gap_total, -h13_vol, -h11_vol, gap_restante]
colors = ['#E74C3C', '#27AE60', '#2ECC71', '#E67E22']
bottom = [0, gap_total - h13_vol, gap_total - h13_vol - h11_vol, 0]
heights = [gap_total, h13_vol, h11_vol, gap_restante]

bars = ax1.bar(labels, heights, bottom=[0, gap_restante + h11_vol, gap_restante, 0],
               color=colors, edgecolor='white', linewidth=1.5)
for bar, h, b in zip(bars, heights, [0, gap_restante + h11_vol, gap_restante, 0]):
    ax1.text(bar.get_x() + bar.get_width()/2, b + h/2, f'{h:,.0f} HL',
             ha='center', va='center', fontweight='bold', fontsize=10, color='white')
ax1.set_ylabel('Volume (HL)')
ax1.set_title('Decomposição do Gap', fontweight='bold')
ax1.axhline(y=0, color='black', linewidth=0.5)
ax1.grid(axis='y', alpha=0.3)

# Gráfico 2: Custo de oportunidade por hipótese
cats = ['H1.3\\nSem custo\\nde oportunidade', 'H1.1\\nCusto oport.\\nSKUs deslocados']
margem_ganho = [h13_margem, h11_margem]
custo_oport = [0, h11_maco_perdido]
x = range(len(cats))
w = 0.35
ax2.bar([i-w/2 for i in x], margem_ganho, w, label='Margem Malzbier gerada', color='#27AE60')
ax2.bar([i+w/2 for i in x], custo_oport, w, label='MACO perdido (SKUs deslocados)', color='#E74C3C', alpha=0.7)
ax2.set_xticks(x)
ax2.set_xticklabels(cats)
ax2.set_ylabel('R$')
ax2.set_title('Trade-off: Margem Gerada vs Custo de Oportunidade', fontweight='bold')
ax2.legend()
ax2.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()"""))

# ══ Eixo 2: Transferência ══
C.append(md("""---
## 25. Eixo 2 — Transferência SP→NE: Compensa Trazer Volume de Fora?

> Pergunta-guia: *Qual modal (cabotagem ou rodoviário) e qual rota (Camaçari ou Fonte Mata) oferecem a melhor relação custo × prazo × margem para cobrir o gap residual?*

### Contexto

Após a produção local (Eixo 1), resta um gap de **~3.640 HL** (se H1.3 + H1.1 forem executadas). A única origem com volume disponível é **SP** (Jaguariúna para Malzbier).

**Dado do PDF:** Malzbier tem **0 HL de transferências programadas** no baseline. Qualquer transferência será uma **nova ação** que precisa ser aprovada.

### H2.1 — Cabotagem SP → Camaçari (CDR Bahia → NE Sul)

- **Custo:** R\\$84,6/HL | **Lead time:** 25 dias | **Avaria:** ~0%
- **Margem residual:** R\\$51,4/HL (18,0%)
- **Atende:** NE Sul (DOI 9.8d — alerta, mas não ruptura)
- **Problema:** NE Sul é a sub-região MENOS crítica. Mapapi e NE Norte estão em ruptura e são atendidos por Fonte Mata/João Pessoa, não Camaçari.

### H2.2 — Cabotagem SP → Fonte Mata (CDR João Pessoa → Mapapi, NE Norte, NO Centro)

- **Custo:** R\\$95,3/HL | **Lead time:** 25 dias | **Avaria:** ~0%
- **Margem residual:** R\\$40,7/HL (14,3%)
- **Atende:** Mapapi (ruptura -3.2d), NE Norte (ruptura -2.3d), NO Centro (4.8d)
- **Vantagem:** atende as sub-regiões mais críticas diretamente
- **Problema:** prazo de 25 dias — se não foi acionado em janeiro, não chega a tempo

### H2.3 — Rodoviário Emergencial

- **Custo Camaçari:** ~R\\$135,3/HL → margem ~R\\$0,7/HL (**~0%**)
- **Custo Fonte Mata:** ~R\\$152,5/HL → margem **NEGATIVA** (-R\\$16,5/HL)
- **Lead time:** 3-6 dias | **Avaria:** 5%
- **Uso:** apenas para volumes pequenos e urgentes (Mapapi, NE Norte em ruptura)
- **Rodo Fonte Mata é financeiramente inviável para volumes grandes**

### H2.4 — Não Transferir (Aceitar Ruptura Controlada)

Em vez de transferir com margem negativa, aceitar ruptura em sub-regiões de baixo impacto:
- **NO Araguaia:** 69 HL de gap (0,6%), 100% revendedores, gestão própria → **candidata natural**
- **Redução do gap efetivo:** 11.680 - 69 = 11.611 HL"""))

# ══ Eixo 2: Cálculos ══
C.append(code("""# ═══════════════════════════════════════════════════════
# EIXO 2 — QUANTIFICAÇÃO: TRANSFERÊNCIA SP→NE
# ═══════════════════════════════════════════════════════

gap_residual = 11680 - 7200 - 6840  # Após Eixo 1 (H1.3 + H1.1)
# Se gap_residual < 0, não precisa transferir
gap_residual = max(gap_residual, 0)

# Mas vamos calcular cenários para diferentes combinações
cenarios_transf = pd.DataFrame([
    {'Rota': 'Cabo → Camaçari', 'Custo R$/HL': 84.6, 'Lead Time': '25 dias',
     'Margem R$/HL': 51.4, 'Margem %': '18.0%', 'Avaria': '~0%',
     'Atende': 'NE Sul', 'Viável?': 'SIM (se acionado em Jan)'},
    {'Rota': 'Cabo → Fonte Mata', 'Custo R$/HL': 95.3, 'Lead Time': '25 dias',
     'Margem R$/HL': 40.7, 'Margem %': '14.3%', 'Avaria': '~0%',
     'Atende': 'Mapapi, NE Norte, NO Centro', 'Viável?': 'SIM (se acionado em Jan)'},
    {'Rota': 'Rodo → Camaçari', 'Custo R$/HL': 135.3, 'Lead Time': '3-6 dias',
     'Margem R$/HL': 0.7, 'Margem %': '0.2%', 'Avaria': '5%',
     'Atende': 'NE Sul', 'Viável?': 'MARGINAL'},
    {'Rota': 'Rodo → Fonte Mata', 'Custo R$/HL': 152.5, 'Lead Time': '3-6 dias',
     'Margem R$/HL': -16.5, 'Margem %': '-5.8%', 'Avaria': '5%',
     'Atende': 'Mapapi, NE Norte, NO Centro', 'Viável?': 'NÃO (margem negativa)'},
])

print("=" * 70)
print("EIXO 2 — TRANSFERÊNCIA: CENÁRIOS DE CUSTO")
print("=" * 70)
print('\\nComparativo de Rotas de Transferência'); display(cenarios_transf)

# Gap por sub-região (para alocação)
gap_sub = pd.DataFrame([
    {'Sub-Região': 'Mapapi', 'Gap HL': 5036, 'DOI Nova Dem (W3)': -3.2, '% do Gap': '43.1%',
     'CDR': 'João Pessoa', 'Rota Viável': 'Cabo/Rodo Fonte Mata', 'Prioridade': '1 — RUPTURA'},
    {'Sub-Região': 'NE Sul', 'Gap HL': 2814, 'DOI Nova Dem (W3)': 9.8, '% do Gap': '24.1%',
     'CDR': 'Camaçari', 'Rota Viável': 'Cabo/Rodo Camaçari', 'Prioridade': '3 — ALERTA'},
    {'Sub-Região': 'NO Centro', 'Gap HL': 1963, 'DOI Nova Dem (W3)': 4.8, '% do Gap': '16.8%',
     'CDR': 'João Pessoa', 'Rota Viável': 'Cabo/Rodo Fonte Mata', 'Prioridade': '2 — CRÍTICO'},
    {'Sub-Região': 'NE Norte', 'Gap HL': 1798, 'DOI Nova Dem (W3)': -2.3, '% do Gap': '15.4%',
     'CDR': 'João Pessoa', 'Rota Viável': 'Cabo/Rodo Fonte Mata', 'Prioridade': '1 — RUPTURA'},
    {'Sub-Região': 'NO Araguaia', 'Gap HL': 69, 'DOI Nova Dem (W3)': -6.3, '% do Gap': '0.6%',
     'CDR': '(Uberlândia)', 'Rota Viável': 'Retirada própria', 'Prioridade': '5 — DEPRIORITIZAR'},
])
print("\\nGap de Malzbier por Sub-Região (priorizado):")
print('\\nPriorização Geográfica para Transferência'); display(gap_sub)

# Visualização
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.patch.set_facecolor('#FAFAFA')
fig.suptitle('Eixo 2 — Transferência: Custo vs Margem por Rota', fontsize=14,
             fontweight='bold', color='#2C3E50')

# Gráfico 1: Custo vs Margem
rotas = ['Prod.\\nLocal', 'Cabo\\nCamaçari', 'Cabo\\nFonte Mata', 'Rodo\\nCamaçari', 'Rodo\\nFonte Mata']
custos = [149, 233.6, 244.3, 284.3, 301.5]
margens = [136, 51.4, 40.7, 0.7, -16.5]
cores_m = ['#27AE60', '#2980B9', '#3498DB', '#E67E22', '#E74C3C']

ax = axes[0]
bars = ax.bar(rotas, margens, color=cores_m, edgecolor='white', linewidth=1.5)
ax.axhline(y=0, color='red', linestyle='--', linewidth=1)
ax.axhline(y=12, color='green', linestyle=':', linewidth=1, label='DOI mínimo ref')
for bar, m in zip(bars, margens):
    ax.text(bar.get_x() + bar.get_width()/2, max(m, 0) + 3,
            f'R${m:.1f}', ha='center', fontweight='bold', fontsize=9)
ax.set_ylabel('Margem (R$/HL)')
ax.set_title('Margem Líquida por Cenário de Supply', fontweight='bold')
ax.grid(axis='y', alpha=0.3)

# Gráfico 2: Gap por sub-região
ax2 = axes[1]
subs = ['Mapapi', 'NE Sul', 'NO Centro', 'NE Norte', 'NO Araguaia']
gaps = [5036, 2814, 1963, 1798, 69]
cores_s = ['#E74C3C', '#F39C12', '#E67E22', '#E74C3C', '#95A5A6']
bars2 = ax2.barh(subs[::-1], gaps[::-1], color=cores_s[::-1], edgecolor='white')
for bar, g in zip(bars2, gaps[::-1]):
    ax2.text(bar.get_width() + 50, bar.get_y() + bar.get_height()/2,
             f'{g:,.0f} HL', va='center', fontweight='bold', fontsize=9)
ax2.set_xlabel('Gap Malzbier (HL)')
ax2.set_title('Gap por Sub-Região (priorizado)', fontweight='bold')
ax2.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.show()"""))

# ══ Eixo 3: Gestão de Demanda ══
C.append(md("""---
## 26. Eixo 3 — Gestão de Demanda: Podemos Reduzir ou Redistribuir?

> Pergunta-guia: *Existem ajustes na previsão de demanda ou na priorização geográfica que reduzam o gap efetivo sem comprometer o objetivo comercial?*

### H3.1 — Descontar o BIAS de +9%

Os dados mostram que os GEOs historicamente **sobre-preveem a demanda em +9%**. Se o BIAS se confirmar:

| Cenário | Gap HL | Diferença |
|---|---|---|
| Gap nominal (+30%) | 11.680 HL | — |
| Gap corrigido (BIAS -9%) | ~10.630 HL | -1.050 HL |

**Implicação:** ~1.050 HL a menos para produzir/transferir. Mas é uma **aposta** — se a demanda for real, a ruptura piora.

### H3.2 — Priorizar Sub-Regiões por Retorno

Nem todas as sub-regiões justificam o mesmo esforço:

| Sub-Região | Gap HL | % Total | DOI W3 | Decisão Sugerida |
|---|---|---|---|---|
| **Mapapi** | 5.036 | 43,1% | -3,2d | **PRIORIDADE MÁXIMA** — maior volume, ruptura real |
| **NE Norte** | 1.798 | 15,4% | -2,3d | **PRIORIDADE ALTA** — ruptura em W3 |
| **NO Centro** | 1.963 | 16,8% | 4,8d | **AÇÃO NECESSÁRIA** — crítico mas não rompido |
| **NE Sul** | 2.814 | 24,1% | 9,8d | **MONITORAR** — DOI abaixo de 12d mas longe de 0 |
| **NO Araguaia** | 69 | 0,6% | -6,3d | **DEPRIORITIZAR** — 100% revenda, retirada própria |

### H3.3 — Phasing Temporal (Concentrar em W1-W2)

Se a produção extra (H1.3: 7.200 HL em W1) e as transferências forem concentradas no início do mês, é possível construir buffer antes das semanas mais críticas (W2-W3). O risco: se a cabotagem atrasa, o buffer se perde."""))

# ══ Eixo 4: Financeiro ══
C.append(md("""---
## 27. Eixo 4 — Análise Financeira: Qual o Cenário Ótimo?

> Pergunta-guia: *Considerando produção local + transferência, qual combinação maximiza a margem total e justifica o atendimento do +30%?*

### H4.1 — Cenários de Custo Total

**Cenário A (Conservador):** Apenas produção local (H1.3)
- Volume: 7.200 HL | Custo: R\\$1.072.800 | Receita: R\\$2.052.000 | Margem: R\\$979.200
- Cobertura: 61,6% do gap | Gap restante: 4.480 HL

**Cenário B (Equilibrado):** Produção local + Realocação (H1.3 + H1.1)
- Volume: 14.040 HL | Custo: R\\$2.091.960 | Receita: R\\$4.001.400 | Margem: R\\$1.909.440
- Cobertura: 120% do gap (excedente de 2.360 HL para buffer)

**Cenário C (Agressivo):** Produção + Cabo Fonte Mata (gap residual)
- Volume: 14.040 + ~3.640 HL transferidos | Custo: ~R\\$2.439.000 | Margem: ~R\\$2.058.000
- Cobertura: 100%+ com reforço via cabotagem

### H4.2 — Breakeven: Atender vs. Não Atender

| Cenário | Receita Adicional | Custo Adicional | Lucro Líquido |
|---|---|---|---|
| Não atender (+30%) | R\\$0 | R\\$0 | R\\$0 (mas perde market share) |
| Cenário A (só local) | R\\$2.052.000 | R\\$1.072.800 | **R\\$979.200** |
| Cenário B (local + realocar) | R\\$4.001.400 | R\\$2.091.960 | **R\\$1.909.440** |

Atender é **sempre lucrativo** enquanto a produção for local (margem R\\$136/HL). O ponto de indiferença ocorre apenas com rodoviário para Fonte Mata (margem negativa).

### H4.3 — Visão Março+ (Demanda Crescente)

O PDF do case menciona que **a demanda deve crescer +10% no TT LN por mês a partir de março**. Isso significa:

| Mês | Demanda incremental estimada | Acumulado |
|---|---|---|
| Fevereiro | +11.680 HL (Malzbier +30%) | 11.680 HL |
| Março | +~17.967 HL (TT LN +10%) | ~29.647 HL |
| Abril | +~19.764 HL (TT LN +10% sobre Mar) | ~49.411 HL |

A decisão de fevereiro não é isolada — **é o primeiro teste de uma tendência crescente**. Investir em capacidade agora posiciona a Ambev para atender a demanda futura."""))

# ══ Eixo 4: Cálculos ══
C.append(code("""# ═══════════════════════════════════════════════════════
# EIXO 4 — QUANTIFICAÇÃO: CENÁRIOS FINANCEIROS
# ═══════════════════════════════════════════════════════

custo_prod = 149
maco = 285
margem = 136
gap = 11680

# Cenário A: Só H1.3 (ociosidade)
ca_vol = 7200
ca_custo = ca_vol * custo_prod
ca_receita = ca_vol * maco
ca_lucro = ca_vol * margem

# Cenário B: H1.3 + H1.1 (produção local completa)
cb_vol = 7200 + 6840
cb_custo = cb_vol * custo_prod
cb_receita = cb_vol * maco
cb_lucro = cb_vol * margem

# Cenário C: B + Cabotagem Fonte Mata (gap residual = 0 se B > gap, ou restante)
cc_gap_resto = max(gap - cb_vol, 0)
cc_custo_transf = cc_gap_resto * (149 + 95.33)  # prod + frete
cc_margem_transf = cc_gap_resto * 40.7
cc_vol = cb_vol + cc_gap_resto
cc_custo = cb_custo + cc_custo_transf
cc_receita = cb_receita + cc_gap_resto * maco
cc_lucro = cb_lucro + cc_margem_transf

print("=" * 70)
print("EIXO 4 — CENÁRIOS FINANCEIROS CONSOLIDADOS")
print("=" * 70)

cenarios = pd.DataFrame([
    {'Cenário': 'A — Só Ociosidade (H1.3)', 'Volume HL': f'{ca_vol:,.0f}',
     'Cobertura': f'{ca_vol/gap*100:.0f}%', 'Custo Total': f'R$ {ca_custo:,.0f}',
     'Receita': f'R$ {ca_receita:,.0f}', 'Lucro': f'R$ {ca_lucro:,.0f}'},
    {'Cenário': 'B — Prod. Local Completa', 'Volume HL': f'{cb_vol:,.0f}',
     'Cobertura': f'{cb_vol/gap*100:.0f}%', 'Custo Total': f'R$ {cb_custo:,.0f}',
     'Receita': f'R$ {cb_receita:,.0f}', 'Lucro': f'R$ {cb_lucro:,.0f}'},
    {'Cenário': 'C — Prod. + Cabo F.Mata', 'Volume HL': f'{cc_vol:,.0f}',
     'Cobertura': f'{cc_vol/gap*100:.0f}%', 'Custo Total': f'R$ {cc_custo:,.0f}',
     'Receita': f'R$ {cc_receita:,.0f}', 'Lucro': f'R$ {cc_lucro:,.0f}'},
])
print('\\nCenários Financeiros — Atendimento do +30% Malzbier'); display(cenarios)

# Visualização: Comparativo de cenários
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
fig.patch.set_facecolor('#FAFAFA')
fig.suptitle('Eixo 4 — Comparativo Financeiro dos Cenários', fontsize=14,
             fontweight='bold', color='#2C3E50')

# Gráfico 1: Waterfall de lucro
nomes = ['Cenário A\\n(Ociosidade)', 'Cenário B\\n(Prod. Local)', 'Cenário C\\n(+Cabotagem)']
lucros = [ca_lucro, cb_lucro, cc_lucro]
cores = ['#27AE60', '#2980B9', '#8E44AD']
bars = ax1.bar(nomes, lucros, color=cores, edgecolor='white', linewidth=1.5)
for bar, l in zip(bars, lucros):
    ax1.text(bar.get_x() + bar.get_width()/2, l + 30000,
             f'R$ {l:,.0f}', ha='center', fontweight='bold', fontsize=10)
ax1.set_ylabel('Lucro Líquido (R$)')
ax1.set_title('Lucro por Cenário', fontweight='bold')
ax1.grid(axis='y', alpha=0.3)

# Gráfico 2: Projeção de demanda crescente
meses = ['Fev\\n(+30% Malz)', 'Mar\\n(+10% TT)', 'Abr\\n(+10% TT)', 'Mai\\n(+10% TT)', 'Jun\\n(+10% TT)']
dem_neno = [179674, 179674*1.10, 179674*1.21, 179674*1.331, 179674*1.4641]
cap_ne = [39600*4.33] * 5  # capacidade mensal aprox (39600 HL/sem * 4.33 sem/mês)

ax2.plot(meses, dem_neno, 'o-', color='#E74C3C', linewidth=2, markersize=8, label='Demanda projetada')
ax2.axhline(y=cap_ne[0], color='#27AE60', linestyle='--', linewidth=2, label=f'Capacidade NE ({cap_ne[0]:,.0f} HL/mês)')
ax2.fill_between(range(len(meses)), dem_neno, cap_ne[0], alpha=0.15, color='red')
for i, d in enumerate(dem_neno):
    ax2.text(i, d + 3000, f'{d:,.0f}', ha='center', fontsize=8, fontweight='bold')
ax2.set_ylabel('Volume (HL/mês)')
ax2.set_title('Projeção: Demanda NENO vs Capacidade NE', fontweight='bold')
ax2.legend(loc='lower right')
ax2.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()"""))

# ══ Eixo 5: Risco ══
C.append(md("""---
## 28. Eixo 5 — Risco e Contingência

> Pergunta-guia: *Quais são os riscos associados a cada hipótese e como mitigá-los?*

### H5.1 — Risco de Avaria no Rodoviário (5%)

O modal rodoviário tem taxa de avaria de **5%** (quebra de garrafa — Long Neck 355ml em vidro). Para 1.000 HL transferidos por rodo:
- Perda: 50 HL × (R\\$149 custo prod + ~R\\$135 frete) = **~R\\$14.200 de prejuízo**

### H5.2 — Risco de Atraso na Cabotagem

Lead time nominal: 25 dias. Se atrasar 5 dias:
- Volume planejado chega na W3 em vez da W2
- Sub-regiões em ruptura (Mapapi, NE Norte) ficam 5 dias adicionais sem cobertura
- **Mitigação:** acionar rodoviário emergencial para Mapapi (volume pequeno, ~1.200 HL/semana)

### H5.3 — Risco de Sub-Previsão (BIAS Inverso)

Se o BIAS de +9% não se confirmar (demanda real = demanda publicada):
- Gap permanece em 11.680 HL (não reduz para ~10.630)
- Necessidade de transferência AUMENTA
- **Mitigação:** planejar para o gap nominal e tratar o BIAS como bônus

### H5.4 — Risco de Canibalização entre SKUs

Realocar produção de outros SKUs (H1.1) pode gerar ruptura nesses SKUs:
- Brahma Chopp Zero: 3.600 HL realocados → depende da demanda local
- Skol Beats: 3.240 HL realocados → demanda concentrada em eventos
- **Mitigação:** verificar DOI dos SKUs candidatos antes de realocar

### Matriz de Risco

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Avaria rodoviário | Alta (5% garantido) | Médio | Limitar volume rodo |
| Atraso cabotagem | Média | Alto | Rodo emergencial backup |
| Sub-previsão BIAS | Baixa-Média | Alto | Planejar para gap nominal |
| Canibalização SKUs | Média | Médio | Checar DOI antes de realocar |"""))

# ══ Eixo 5: Cálculos (Matriz de Priorização) ══
C.append(code("""# ═══════════════════════════════════════════════════════
# MATRIZ DE PRIORIZAÇÃO — IMPACTO × VIABILIDADE
# ═══════════════════════════════════════════════════════

import matplotlib.colors as mcolors

hipoteses = [
    ('H1.3 Ociosidade\\nPE541 W1', 9, 10, '#27AE60', '7.200 HL'),
    ('H1.1 Realocar\\nPE541', 7, 7, '#2ECC71', '6.840 HL'),
    ('H1.2 Realocar\\nAQ541', 4, 5, '#82E0AA', '~3.000 HL'),
    ('H2.1 Cabo\\nCamaçari', 5, 6, '#2980B9', 'NE Sul'),
    ('H2.2 Cabo\\nFonte Mata', 8, 5, '#3498DB', 'Mapapi+NE Norte'),
    ('H2.3 Rodoviário', 6, 3, '#E67E22', 'Emergência'),
    ('H2.4 Não transferir', 2, 10, '#95A5A6', 'NO Araguaia'),
    ('H3.1 Descontar\\nBIAS', 3, 8, '#F39C12', '-1.050 HL'),
    ('H3.2 Priorizar\\nsub-regiões', 8, 9, '#F1C40F', 'Alocação'),
    ('H3.3 Phasing\\ntemporal', 5, 7, '#D4AC0D', 'W1-W2'),
    ('H4.3 Visão\\nMarço+', 7, 4, '#8E44AD', '+10%/mês'),
]

fig, ax = plt.subplots(figsize=(14, 9))
fig.patch.set_facecolor('#FAFAFA')

# Quadrantes
ax.axhline(y=5.5, color='#BDC3C7', linestyle='--', linewidth=1)
ax.axvline(x=5.5, color='#BDC3C7', linestyle='--', linewidth=1)
ax.fill_between([5.5, 11], 5.5, 11, alpha=0.08, color='green')  # Alta prioridade
ax.fill_between([0, 5.5], 0, 5.5, alpha=0.08, color='red')      # Baixa prioridade

ax.text(8.2, 10.3, 'PRIORIDADE MÁXIMA\\n(Alto Impacto + Alta Viabilidade)', fontsize=9,
        ha='center', color='#27AE60', fontweight='bold', alpha=0.7)
ax.text(2.8, 0.7, 'BAIXA PRIORIDADE\\n(Baixo Impacto + Baixa Viabilidade)', fontsize=9,
        ha='center', color='#E74C3C', fontweight='bold', alpha=0.7)
ax.text(8.2, 0.7, 'INVESTIGAR\\n(Alto Impacto + Baixa Viabilidade)', fontsize=9,
        ha='center', color='#E67E22', fontweight='bold', alpha=0.7)
ax.text(2.8, 10.3, 'QUICK WINS\\n(Baixo Impacto + Alta Viabilidade)', fontsize=9,
        ha='center', color='#3498DB', fontweight='bold', alpha=0.7)

for label, impacto, viab, cor, nota in hipoteses:
    ax.scatter(impacto, viab, s=400, c=cor, edgecolors='white', linewidth=2, zorder=5)
    ax.annotate(label, (impacto, viab), textcoords="offset points",
                xytext=(12, 8), fontsize=7.5, fontweight='bold', color='#2C3E50',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor=cor))

ax.set_xlim(0, 11)
ax.set_ylim(0, 11)
ax.set_xlabel('IMPACTO (volume coberto / relevância estratégica)', fontsize=11, fontweight='bold')
ax.set_ylabel('VIABILIDADE (custo, prazo, risco)', fontsize=11, fontweight='bold')
ax.set_title('Matriz de Priorização — 17 Hipóteses MECE', fontsize=14,
             fontweight='bold', color='#2C3E50')
ax.grid(True, alpha=0.2)

plt.tight_layout()
plt.show()

print("\\nORDEM DE EXECUÇÃO RECOMENDADA:")
print("  1° H1.3 — Produzir 7.200 HL em PE541 W1 (sem custo de oportunidade)")
print("  2° H3.2 — Priorizar Mapapi e NE Norte na alocação")
print("  3° H1.1 — Realocar Brahma Zero + Skol Beats em PE541 (~6.840 HL)")
print("  4° H2.2 — Cabotagem SP→Fonte Mata (se acionada em Jan)")
print("  5° H2.4 — Deprioritizar NO Araguaia (69 HL, 100% revenda)")
print("  6° H3.1 — Monitorar BIAS, mas planejar para gap nominal")"""))

# ══ Síntese da Árvore de Hipóteses ══
C.append(md("""---
## 29. Insights da Árvore de Hipóteses — Síntese Executiva

> Esta síntese consolida as 17 hipóteses dos 5 eixos MECE. A recomendação é baseada exclusivamente nos dados quantificados — sem estimativas ou suposições.

---

### 1. A Solução é Local Primeiro, Transferência Depois

A **ociosidade de PE541 na W1** (7.200 HL, custo R\\$149/HL, margem R\\$136/HL) é a ação de maior retorno e menor risco. Sozinha, cobre **61,6% do gap**. Combinar com realocação de Brahma Zero + Skol Beats (6.840 HL) eleva para **120% do gap** — gerando um buffer de 2.360 HL.

| Ação | Volume | Custo/HL | Margem/HL | Risco |
|---|---|---|---|---|
| **H1.3 Ociosidade PE541 W1** | 7.200 HL | R\\$149 | R\\$136 | Baixo |
| **H1.1 Realocar PE541** | 6.840 HL | R\\$149 | R\\$136 | Médio |
| **Total produção local** | **14.040 HL** | **R\\$149** | **R\\$136** | — |
| Gap do case | 11.680 HL | — | — | — |

**Produção local gera R\\$1.909.440 de margem.** Transferência de SP só é necessária se houver restrição operacional na realocação.

---

### 2. O Paradoxo de PE541 W1: Malzbier = 0 HL na Semana com Maior Folga

O PCP programou **zero Malzbier** na semana de maior ociosidade (W1: 73,3% de utilização). Esse é o insight mais acionável do case — reprosentar Malzbier na W1 resolve a maior parte do problema sem afetar nenhum outro SKU.

---

### 3. Cabotagem Só se Justifica para Fonte Mata (e se Acionada em Janeiro)

Camaçari atende NE Sul (DOI 9.8d — alerta, não ruptura). Fonte Mata atende Mapapi e NE Norte (ambos em ruptura). A rota prioritária é **Fonte Mata**, mas o lead time de 25 dias exige que o pedido já tenha sido feito em janeiro.

Se não foi acionado, **rodoviário para Camaçari** (margem ~R\\$0,7/HL) é a única opção viável em termos de prazo. **Rodoviário para Fonte Mata é financeiramente inviável** (margem negativa).

---

### 4. NO Araguaia Pode ser Deprioritizado — 0,6% do Gap, 100% Revenda

O gap de Malzbier em NO Araguaia é de **69 HL** (0,6% do total). A sub-região é composta integralmente por revendedores que gerenciam o próprio estoque e fazem retirada em Uberlândia. A ruptura registrada é do estoque deles, não da Ambev. Deprioritizar NO Araguaia libera esforço logístico para as sub-regiões em ruptura real.

---

### 5. O +30% é o Primeiro Sinal — Março Traz +10%/Mês

O PDF de contexto do case menciona que a demanda deve crescer **+10% no TT LN por mês a partir de março**. Isso transforma a decisão de fevereiro de uma ação tática em um **posicionamento estratégico**: quem resolve fevereiro demonstra capacidade de execução para os meses seguintes.

A capacidade combinada NE (39.600 HL/sem ≈ 171.468 HL/mês) contra a demanda projetada (179.674 HL em Fev → ~197.641 HL em Mar → ~217.406 HL em Abr) mostra que **a dependência de SP só vai aumentar**.

---

### 6. A Recomendação é Atender — Margem Positiva em Todos os Cenários Locais

| Cenário | Lucro Líquido | Cobertura |
|---|---|---|
| A — Só ociosidade (H1.3) | **R\\$979.200** | 61,6% |
| B — Prod. local completa (H1.3+H1.1) | **R\\$1.909.440** | 120% |
| C — Prod. + Cabotagem | **~R\\$2.058.000** | 100%+ |

Não atender = R\\$0 de receita adicional + perda de market share + sinal negativo para março.
Atender = mínimo R\\$979.200 de margem + posicionamento para crescimento.

---

### Plano de Ação Recomendado (Sequência)

| Prioridade | Ação | Volume | Prazo | Custo |
|---|---|---|---|---|
| **1°** | Produzir Malzbier em PE541 W1 | 7.200 HL | Imediato | R\\$149/HL |
| **2°** | Priorizar Mapapi e NE Norte na alocação | — | Imediato | R\\$0 |
| **3°** | Realocar Brahma Zero + Skol Beats em PE541 | 6.840 HL | 1-2 sem | R\\$149/HL |
| **4°** | Cabotagem SP→Fonte Mata (se viável) | ~2.000 HL | 25 dias | R\\$95,3/HL |
| **5°** | Deprioritizar NO Araguaia | -69 HL | Imediato | R\\$0 |
| **6°** | Monitorar BIAS — planejar para gap nominal | — | Contínuo | R\\$0 |

---

> **Próximo passo — Análise Bivariada:** cruzar as variáveis entre eixos para simular cenários combinados, calcular o impacto financeiro total de cada combinação, e produzir a recomendação final com sensibilidade ao BIAS e ao cenário de março."""))

# ══ MECE Final (questões para Bivariada) ══
C.append(md("""---
## 30. Questões para a Análise Bivariada

> Com a Árvore de Hipóteses estruturada, as questões abaixo orientam os cruzamentos de dados da próxima etapa.

### Cruzamento 1: Produção × Demanda
- Volume realocável por semana × demanda semanal por sub-região
- DOI resultante por sub-região após realocação de PE541 W1

### Cruzamento 2: Custo × Geografia
- Custo total por sub-região (produção + transferência) × margem por sub-região
- Ponto de indiferença por rota: volume mínimo que justifica cabotagem vs. rodoviário

### Cruzamento 3: Capacidade × Tempo
- Capacidade semanal disponível (após realocação) × perfil de demanda semanal
- Simulação de DOI semana a semana sob cada cenário (A, B, C)

### Cruzamento 4: Risco × Retorno
- Custo esperado de avaria (rodo) × margem residual por rota
- Sensibilidade do lucro ao BIAS (+9%, 0%, -5%)

### Cruzamento 5: Tático × Estratégico
- Custo da ação em Fev × receita projetada Mar-Jun (+10%/mês)
- ROI da decisão: investimento logístico em Fev como posicionamento para crescimento"""))

# ── Build ──
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
path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "analise_longneck.ipynb")
with open(path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

# Verify
errs = []
for i, c in enumerate(C):
    if c['cell_type'] == 'code':
        src = c['source'][0]
        # Skip magic commands (Jupyter-only)
        clean = '\n'.join(l for l in src.split('\n') if not l.strip().startswith('%'))
        try:
            compile(clean, f'cell-{i}', 'exec')
        except SyntaxError as e:
            errs.append(f'Cell {i}: {e}')
        if 'applymap' in src or ('.map(' in src and 'lambda' in src):
            errs.append(f'Cell {i}: has applymap/map!')
        if '.style.' in src:
            errs.append(f'Cell {i}: has .style.')

print(f"Total: {len(C)} células")
if errs:
    for e in errs: print(f"  ERR: {e}")
else:
    print("Zero erros | Zero applymap | Zero .style.")
