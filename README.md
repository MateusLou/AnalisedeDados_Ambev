# Análise de Dados — Ambev Long Neck NENO

Análise completa de supply chain e logística para o case **Malzbier Brahma Long Neck** da região Nordeste (NENO), desenvolvida para o processo seletivo da Insper Junior.

---

## Contexto

Em fevereiro de 2026, a demanda por Malzbier Brahma na região NENO cresceu **30%**, gerando um gap de **4.500 HL** a ser coberto. A análise avalia as opções de abastecimento considerando capacidade das plantas, modais de transporte e restrições de DOI.

---

## Arquivos

| Arquivo | Descrição |
|---|---|
| `analise_longneck_exec.ipynb` | Notebook principal com análise completa executada |
| `analise_longneck.ipynb` | Notebook auxiliar de exploração |
| `nb1_data_contract.ipynb` | Contrato de dados |
| `nb2_univariada.ipynb` | Análise univariada |
| `nb3_hipoteses.ipynb` | Árvore de hipóteses |
| `nb4_bivariada.ipynb` | Análise bivariada |
| `Analise_LongNeck_WSNP - Sem repostas.xlsx` | Base de dados com 6 planilhas |
| `fig_*.png` | Visualizações geradas (300 DPI) |

---

## Estrutura da Análise

### 1. Data Contract
Mapeamento formal das fontes de dados:
- **Plantas:** AQ541 (Aquiraz/CE) e PE541 (Nassau/PE)
- **SKUs:** Patagonia, Goose Island, Malzbier Brahma, Colorado
- **Modais:** Cabotagem (25 dias) e Rodoviário (6 dias)
- **Sub-regiões NENO:** Mapapi, NE Norte, NE Sul, NO Araguaia, NO Centro

### 2. Análise Univariada
Capacidade produtiva em fevereiro:

| Planta | Capacidade | Utilização | SKU crítico |
|---|---|---|---|
| AQ541 — Aquiraz/CE | 50 kHL/mês | 63,6% | Patagonia |
| PE541 — Nassau/PE | 108 kHL/mês | 41,2% | Malzbier |

### 3. Árvore MECE de Hipóteses
Estrutura MECE com dois vetores principais:
- **Volume Disponível:** capacidade ociosa de AQ541 e PE541
- **Viabilidade Logística:** lead time por modal vs. DOI mínimo exigido

### 4. Análise Bivariada
Trade-offs principais:

| Comparação | Cabotagem | Rodoviário |
|---|---|---|
| Custo | R$ 84,58/HL | R$ 135,33/HL |
| Lead time | 25 dias | 6 dias |
| DOI | Viola (mín. 12d) | Atende |

### 5. Simulação de Cenários

| Cenário | Descrição | Custo Total | Custo/HL | Lead Time | DOI |
|---|---|---|---|---|---|
| **A** | Realocação total (AQ541 + PE541) | R$ 321.336 | R$ 71,41 | 25 dias | Risco médio |
| **B** | Rodoviário emergencial (100%) | R$ 596.760 | R$ 132,61 | 6 dias | Seguro |
| **C** ✅ | Híbrido 50% local + 50% rodoviário | R$ 458.858 | R$ 102,01 | 6 dias | Seguro |

### 6. Recomendação Final

**Cenário C — Híbrido (recomendado)**
- 2.250 HL via reajuste de produção (AQ541 + PE541)
- 2.250 HL via transferência rodoviária de SP
- 23% mais barato que o Cenário B
- Lead time de 6 dias — DOI garantido

**Plano de ação:**

| Área | Ação |
|---|---|
| PCP | Reduzir Patagonia AQ541: 12.600 → 11.475 HL/semana |
| PCP | Aumentar Malzbier PE541: 3.060 → 3.615 HL/semana |
| Logística | Contratar 590 HL/semana rodoviário (4 semanas) |
| Comercial | Comunicar confirmação de aumento ao NENO |
| Finance | Budget incremental R$ 458.858 para fevereiro |

---

## Métricas-Chave

| Métrica | Antes | Depois (Cen. C) |
|---|---|---|
| Demanda Malzbier NENO | 15.000 HL | 19.500 HL (+30%) |
| Gap a cobrir | — | 4.500 HL (100% coberto) |
| Custo incremental | — | R$ 458.858 / R$ 102,01 por HL |
| Lead time | 25 dias (cabo) | 6 dias (rodo) |
| DOI NENO | Crítico | Seguro |
| Margem Malzbier | R$ 136/HL | R$ 183/HL |

---

## Como Executar

```bash
# Instalar dependências
pip install pandas numpy matplotlib seaborn openpyxl jupyter

# Executar notebook principal
jupyter notebook analise_longneck_exec.ipynb

# Gerar relatório HTML
jupyter nbconvert --to html analise_longneck_exec.ipynb
```

---

## Planilhas da Base de Dados (Excel)

| Aba | Conteúdo |
|---|---|
| Cenário atual BR | Demanda, produção e estoque por região (Jan/Fev) |
| Custos de transferência | Matriz de custos R$/HL por rota e SKU |
| Produção PCP | Produção semanal por planta (4 semanas Fev) |
| Transferências programadas | Transferências já contratadas |
| Cenário divulgado | Forecast original por sub-região NENO |
| Cenário nova demanda | Forecast com Malzbier +30% |

---

## Contexto Acadêmico

**Projeto:** Case Ambev Long Neck — Processo Seletivo Insper Junior
**Linguagem:** Python 3 (Pandas, Matplotlib, Seaborn)
**Data:** Março de 2026
**Repositório do dashboard:** [dashboard_ambev](https://github.com/MateusLou/dashboard_ambev)
