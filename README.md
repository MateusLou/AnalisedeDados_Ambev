# Análise de Dados — Case Ambev: Malzbier Longneck NENO

> **Projeto:** Processo Seletivo Insper Junior — Engenharia de Dados
> **Cliente:** Ambev
> **Período analisado:** Fevereiro–Maio de 2026
> **Autor:** Mateus Loureiro, Nicole Lima da Silva, Bianca dos Reis Habr

---

## Sumário Executivo

Em fevereiro de 2026, a demanda por **Malzbier Brahma Longneck** na região **NENO** (Nordeste + Norte do Brasil) cresceu **+30%**, gerando um gap de **11.680 HL** a ser coberto sem violação do DOI mínimo de 12 dias.

A análise identificou que **9.000 HL** podem ser absorvidos pela capacidade ociosa das plantas regionais (PE541 e AQ541), deixando **2.680 HL** a serem supridos via modal de transporte pago. A recomendação é uma **estratégia bifásica**: rodoviário emergencial em fevereiro (Fase 1) e cabotagem estrutural a partir de maio (Fase 3), com avaliação de roteamento entre **Camaçari (BA)** e **Fonte da Mata (PB)**.

---

## Contexto do Problema

| Dimensão | Detalhe |
|---|---|
| SKU crítico | Malzbier Brahma Longneck (Longneck WSNP) |
| Região | NENO — 5 sub-regiões: Mapapi, NE Norte, NE Sul, NO Araguaia, NO Centro |
| Choque de demanda | +30% em fevereiro de 2026 vs. plano |
| Gap total | **11.680 HL** em aberto |
| CDR crítico | João Pessoa (PB) — abastece Mapapi, NE Norte e NO Centro |
| DOI mínimo (política) | 12 dias de cobertura de estoque |

---

## Estrutura da Análise

```
analise-dados/
├── analise_longneck_exec.ipynb   ← Notebook principal (executado, 103 células)
├── nb1_data_contract.ipynb       ← Contrato de dados e mapeamento de fontes
├── nb2_univariada.ipynb          ← Análise univariada (plantas, SKUs, capacidade)
├── nb3_hipoteses.ipynb           ← Árvore MECE de hipóteses
├── nb4_bivariada.ipynb           ← Análise bivariada (custo vs. lead time vs. DOI)
└── Analise_LongNeck_WSNP.xlsx    ← Base de dados (6 abas)
```

O notebook **`analise_longneck_exec.ipynb`** é o entregável principal. Está estruturado em 6 partes:

| Parte | Conteúdo |
|---|---|
| 1 — Data Contract | Mapeamento das 6 abas do Excel, tipos, granularidade e qualidade |
| 2 — Univariada | Capacidade instalada e utilização por planta e semana |
| 3 — Hipóteses (MECE) | Árvore estruturada: volume disponível × viabilidade logística |
| 4 — Bivariada | Heatmaps de demanda, DOI por sub-região, correlações custo/lead time |
| 5 — Cenários | Simulação financeira de 3 cenários e plano de ação |
| 6 — Roteamento | Análise Camaçari (BA) vs. Fonte da Mata (PB) com break-even e scorecard |

---

## Fontes de Dados (Planilha Excel)

| Aba | Conteúdo |
|---|---|
| Cenário Atual BR | Demanda, produção e estoque por região (Jan/Fev) |
| Custos de Transferência | Matriz de custos R$/HL por rota, modal e SKU |
| Produção PCP | Produção semanal por planta (4 semanas de Fev) |
| Transferências Programadas | Transferências já contratadas no período |
| Cenário Divulgado | Forecast original por sub-região NENO |
| Cenário Nova Demanda | Forecast com Malzbier Longneck +30% |

---

## Capacidade das Plantas

| Planta | Localização | Capacidade | Utilização W1 | Ociosidade W2 |
|---|---|---|---|---|
| **AQ541** | Aquiraz — CE | 12.600 HL/sem | 97,1% | **1.800 HL (14,3%)** |
| **PE541** | Nassau — PE | 27.000 HL/sem | 73,3% | **7.200 HL (26,7%)** |

A ociosidade combinada de W2 (1.800 + 7.200 = **9.000 HL**) cobre 77% do gap total, evitando custos de transporte para essa parcela do volume.

---

## DOI por Sub-Região — Semana 4, Nova Demanda

| Sub-Região | CDR | DOI W4 (dias) | Status |
|---|---|---|---|
| Mapapi | João Pessoa (PB) | **−3,2** | 🔴 Ruptura |
| NE Norte | João Pessoa (PB) | **−2,3** | 🔴 Ruptura |
| NO Araguaia | — | **−6,3** | 🔴 Ruptura crítica |
| NO Centro | João Pessoa (PB) | +4,8 | 🟡 Abaixo do mínimo |
| NE Sul | — | +9,8 | 🟢 Adequado |

As 3 sub-regiões em ruptura (**Mapapi, NE Norte, NO Centro**) são todas atendidas pelo **CDR João Pessoa (PB)**, o que tem implicação direta na decisão de roteamento.

---

## Modais de Transporte

| Modal | Origem | Destino | Custo/HL | Lead Time | Avaria | DOI |
|---|---|---|---|---|---|---|
| **Rodoviário** | Camaçari (BA) | NENO | R$ 135,33 | D+6 | 5% | ✅ Atende |
| **Cabotagem** | Camaçari (BA) | NENO | R$ 84,58 | D+25 | 0% | ⚠️ Risco W1 |
| **Rodoviário** | Fonte da Mata (PB) | NENO | R$ 152,53 | D+6 | 5% | ✅ Atende |
| **Cabotagem** | Fonte da Mata (PB) | NENO | R$ 95,33 | D+25 | 0% | ⚠️ Risco W1 |

---

## Simulação de Cenários

| Cenário | Descrição | Custo Total | Margem Bruta | Lead Time | DOI |
|---|---|---|---|---|---|
| **Fase 1 — Rodo Camaçari** | Emergencial (Fev/26) | R$ 2,143M | R$ 1,186M | D+6 | ✅ Seguro |
| **Fase 3 — Cabo Camaçari** | Estrutural (Mai/26+) | R$ 1,967M | R$ 1,362M | D+25 | ⚠️ Atenção |
| **Fase 3 — Cabo Fonte da Mata** | Alternativo (Mai/26+) | R$ 1,993M | R$ 1,336M | D+25 | ⚠️ Atenção |

A transição de Rodo (Fase 1) para Cabotagem (Fase 3) gera uma **economia de R$ 176k/mês** em custo de frete e elimina 141 HL de avaria de transporte.

---

## Parte 6 — Análise de Roteamento: Camaçari (BA) vs. Fonte da Mata (PB)

### Por que avaliar Fonte da Mata?

O heatmap de demanda confirmou que **Mapapi concentra ~37% do volume total Malzbier NENO** e que as 3 sub-regiões em ruptura (Mapapi, NE Norte, NO Centro) são todas servidas pelo **CDR João Pessoa (PB)**.

- **Camaçari (BA)** está a ~500 km do CDR JP
- **Fonte da Mata (PB)** está a ~50 km do CDR JP

Apesar de o frete de transferência SP → FM ser **+12,7% mais caro**, a proximidade geográfica pode compensar esse custo.

### Break-Even de Roteamento

O break-even representa o custo de distribuição intra-regional que Camaçari precisaria incorrer para chegar ao CDR João Pessoa — custo esse que Fonte da Mata praticamente não tem.

| Modal | Break-Even (R$/HL) | Interpretação |
|---|---|---|
| **Cabotagem** | R$ 10,75/HL | Se o custo BA → CDR JP superar R$10,75, Fonte da Mata é mais barata |
| **Rodoviário** | R$ 17,20/HL | Mesma lógica; janela maior pois FM também custa mais no modal rodo |

> Com ~500 km entre Camaçari e o CDR João Pessoa, o custo de distribuição intra-regional estimado é de **R$20–25/HL** — superando o break-even em ambos os modais.

### Scorecard de Decisão

| Critério | Peso | Camaçari | Fonte da Mata |
|---|---|---|---|
| Custo de frete/HL — Rodo | 25% | **10** | 7 |
| Custo de frete/HL — Cabo | 20% | **10** | 7 |
| Proximidade CDR JP (PB) | 30% | 5 | **10** |
| Cobertura CDR JP (3 sub-regiões) | 25% | 6 | **10** |
| Risco de ruptura | 20% | 5 | **9** |
| Flexibilidade operacional | 15% | **10** | 8 |
| Lead time intra-regional | 20% | 6 | **10** |

| | Camaçari (BA) | Fonte da Mata (PB) |
|---|---|---|
| **Pontuação ponderada** | 82,5 pts | **104,5 pts** |
| **Recomendação** | | ✅ **Vencedora** |

### Recomendação Final de Roteamento

- **Fase 1 (urgência — Fev/26):** Rodoviário via Camaçari (BA) — menor custo de frete bruto, D+6
- **Fase 3 (estrutural — Mai/26+):** Cabotagem via Fonte da Mata (PB) — quando custo intra-regional é considerado, FM vence o break-even em ambos os modais

---

## Plano de Ação Integrado (12 Semanas)

| Fase | Período | Ação | Volume | Custo |
|---|---|---|---|---|
| **Fase 1** | Fev/26 (S1–S4) | Rebalancear PCP PE541 + AQ541 | 9.000 HL | — |
| **Fase 1** | Fev/26 (S1–S4) | Frete rodoviário emergencial — Camaçari BA | 2.680 HL | R$ 135,33/HL |
| **Fase 2** | Mar–Abr/26 (S5–S8) | Negociação e contratação do navio de cabotagem | — | — |
| **Fase 3** | Mai/26+ (S9+) | Cabotagem regular quinzenal — Fonte da Mata PB | 2.680 HL | R$ 95,33/HL |

| Área | Ação Imediata |
|---|---|
| **PCP** | Alocar ociosidade PE541 W2: +7.200 HL Malzbier |
| **PCP** | Alocar ociosidade AQ541 W2: +1.800 HL Malzbier |
| **Logística** | Contratar rodoviário Camaçari → NENO (2.680 HL, D+6) |
| **Logística** | Iniciar negociação cabotagem Fonte da Mata → CDR JP |
| **Finance** | Provisionar custo incremental de frete (Fase 1 → Fase 3) |
| **Comercial** | Confirmar aumento de demanda NENO e alinhamento de forecast |

---

## Gráficos Gerados

O notebook executa e salva automaticamente os seguintes gráficos:

| Arquivo | Conteúdo |
|---|---|
| `graficos_cat1_cat3.png` | G2: Capacidade vs. Utilização por planta; G6: Evolução do DOI |
| `graficos_gantt_g11.png` | G11: Gantt executivo — cronograma 12 semanas (Fev–Mai/26) |
| `analise_roteamento_camacari_fontemata.png` | G1: Concentração demanda; G5: Break-even; G6: Scorecard |
| `fig_*.png` (45+ arquivos) | Análises exploratórias e evidências das hipóteses |

---

## Métricas-Chave

| Métrica | Valor |
|---|---|
| Gap total Malzbier NENO | 11.680 HL (+30% vs. plano) |
| Coberto por produção local | 9.000 HL (PE541 + AQ541, Semana 2) |
| Coberto por modal de transporte | 2.680 HL líquidos |
| Custo Fase 1 — Rodo Camaçari | R$ 2,143M / Margem R$ 1,186M |
| Custo Fase 3 — Cabo Fonte da Mata | R$ 1,993M / Margem R$ 1,336M |
| Economia na transição Rodo → Cabo | ~R$ 176k/mês |
| Break-even Cabo (FM vs. CAM) | R$ 10,75/HL de distribuição intra-regional |
| Break-even Rodo (FM vs. CAM) | R$ 17,20/HL de distribuição intra-regional |
| MACO Malzbier Longneck | R$ 285/HL |
| DOI mínimo NENO | 12 dias |
| Sub-regiões em ruptura (W4) | 3 de 5 (Mapapi −3,2d · NE Norte −2,3d · NO Araguaia −6,3d) |

---

## Como Executar

```bash
# Instalar dependências
pip install pandas numpy matplotlib seaborn openpyxl jupyter

# Executar o notebook principal completo
jupyter notebook analise_longneck_exec.ipynb

# Gerar relatório HTML exportável
jupyter nbconvert --to html --execute analise_longneck_exec.ipynb

# Regenerar gráficos PNG isoladamente
python gen_visual.py
```

---

## Stack Tecnológica

| Ferramenta | Uso |
|---|---|
| Python 3 | Linguagem principal |
| Pandas | Manipulação e agregação de dados |
| NumPy | Cálculos numéricos e break-even |
| Matplotlib | Todos os gráficos (45+ visualizações) |
| OpenPyXL | Leitura da planilha Excel |
| Jupyter Notebook | Ambiente interativo de análise |

---

*Repositório: [AnalisedeDados_Ambev](https://github.com/MateusLou/AnalisedeDados_Ambev) — Insper Junior · Março de 2026*
