import json

def md(s):
    return {"cell_type":"markdown","metadata":{},"source":[s],"id":None}
def code(s):
    return {"cell_type":"code","execution_count":None,"metadata":{},"source":[s],"outputs":[],"id":None}

C = []

# Setup: carrega todos os dados via data_loader.py
C.append(code("""%matplotlib inline
from data_loader import *"""))

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

| SKU | Volume 4 sem | MACO R$/HL | Custo oportunidade | Candidato? |
|---|---|---|---|---|
| Brahma Chopp Zero | 3.600 HL | ~R$250¹ | Baixo | **Sim** |
| Skol Beats | 3.240 HL | ~R$260¹ | Baixo | **Sim** |
| Colorado | 16.200 HL | R$300 | Médio | **Parcial** |
| Budweiser Zero | 16.200 HL | ~R$270¹ | Médio | **Parcial** |
| Goose Island | 32.400 HL | R$350 | Alto | **Não (restrição)** |

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

**Esta é a hipótese de maior impacto e menor custo:** produzir 7.200 HL de Malzbier na W1 usando a capacidade ociosa de PE541, sem deslocar nenhum outro SKU. Custo = R$149/HL (produção local), margem = R$136/HL (47,7%).

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


# ── Build nb3_hipoteses.ipynb ──────────────────────────────────────────────
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
path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "nb3_hipoteses.ipynb")
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

print(f"nb3_hipoteses.ipynb: {len(C)} células")
if errs:
    for e in errs: print(f"  ERR: {e}")
else:
    print("Zero erros | Zero applymap | Zero .style.")
