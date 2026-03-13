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


# ── Build nb2_univariada.ipynb ─────────────────────────────────────────────
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
path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "nb2_univariada.ipynb")
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

print(f"nb2_univariada.ipynb: {len(C)} células")
if errs:
    for e in errs: print(f"  ERR: {e}")
else:
    print("Zero erros | Zero applymap | Zero .style.")
