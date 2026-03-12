"""
data_loader.py — Carregamento e parsing estruturado das 6 abas do Excel.
Use: from data_loader import *  (em qualquer notebook do projeto)
Exporta: CORES, semanas, cap_aq, cap_pe, DOI_MIN,
         df_cenario_br, df_custos_transf, df_maco, df_cprod, df_sku_economics,
         df_pcp, df_transf, df_divulgado, df_nova_dem, div_neno, nova_neno
"""

__all__ = [
    'pd', 'np', 'plt', 'mpatches', 'FancyBboxPatch', 'FancyArrowPatch', 'pe',
    'display', 'HTML', 'warnings', 'Path',
    'CORES', 'semanas', 'cap_aq', 'cap_pe', 'DOI_MIN', 'BASE_DIR', 'EXCEL_FILE',
    'df_cenario_br', 'df_jan', 'df_fev',
    'df_custos_transf', 'df_maco', 'df_cprod', 'df_sku_economics',
    'df_pcp', 'df_transf', 'df_divulgado', 'df_nova_dem',
    'div_neno', 'nova_neno', 'parse_cenario_neno',
]

import subprocess, sys as _sys
subprocess.check_call([_sys.executable, '-m', 'pip', 'install', 'openpyxl', '-q'])

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe
import warnings
warnings.filterwarnings('ignore')
from pathlib import Path
from IPython.display import display, HTML

# ── Configuração visual global ──────────────────────────────────────────────
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

# ── Constantes ───────────────────────────────────────────────────────────────
cap_aq = 12600   # HL/semana AQ541 (Aquiraz/CE)
cap_pe = 27000   # HL/semana PE541 (Nassau/PE)
DOI_MIN = 12     # dias de inventário mínimo NENO
semanas = ['W1 (02/02)', 'W2 (09/02)', 'W3 (16/02)', 'W4 (23/02)']

# ── Localização do Excel ─────────────────────────────────────────────────────
BASE_DIR = Path('.').resolve()
EXCEL_FILE = None
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
    raise FileNotFoundError("Excel não encontrado! Coloque o arquivo na mesma pasta do notebook.")

print(f"✅ Excel: {EXCEL_FILE.name}")
xls = pd.ExcelFile(EXCEL_FILE)
print(f"Abas: {xls.sheet_names}")

# ── Aba 1: Cenário Atual BR ──────────────────────────────────────────────────
raw1 = pd.read_excel(xls, 'Cenário atual BR', header=None)
regioes_br = ['MG', 'SP', 'NENO', 'CO', 'RJ', 'SUL']
jan_data, fev_data = [], []
for i, reg in enumerate(regioes_br):
    row = 5 + i
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
print(f"✅ Aba 1 (Cenário Atual BR): {len(df_cenario_br)} regiões")

# ── Aba 2: Custos de Transferência ───────────────────────────────────────────
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

maco_data = []
for row in [13, 14, 15]:
    maco_data.append({'SKU': str(raw2.iloc[row, 1]).strip(), 'MACO_R_HL': float(raw2.iloc[row, 4])})
df_maco = pd.DataFrame(maco_data)

cprod_data = []
for row in [20, 21, 22]:
    cprod_data.append({'SKU': str(raw2.iloc[row, 1]).strip(), 'Custo_Prod_R_HL': float(raw2.iloc[row, 4])})
df_cprod = pd.DataFrame(cprod_data)

df_sku_economics = pd.merge(df_maco, df_cprod, on='SKU')
df_sku_economics['Margem_Bruta'] = df_sku_economics['MACO_R_HL'] - df_sku_economics['Custo_Prod_R_HL']
df_sku_economics['Margem_Pct'] = (df_sku_economics['Margem_Bruta'] / df_sku_economics['MACO_R_HL'] * 100).round(1)
print(f"✅ Aba 2 (Custos): {len(df_custos_transf)} rotas + {len(df_sku_economics)} SKUs")

# ── Aba 3: Produção PCP ──────────────────────────────────────────────────────
raw3 = pd.read_excel(xls, 'Produção PCP', header=None)
aq_skus = ['Malzbier', 'Patagonia', 'Colorado']
aq_rows = [2, 3, 4]
prod_pcp = []
for sku, row in zip(aq_skus, aq_rows):
    for w, col in enumerate([6, 7, 8, 9]):
        val = float(raw3.iloc[row, col]) if pd.notna(raw3.iloc[row, col]) else 0
        prod_pcp.append({'Planta': 'AQ541 (CE)', 'SKU': sku, 'Semana': semanas[w], 'Semana_Num': w+1, 'Volume_HL': val})
pe_skus = ['Brahma Chopp Zero', 'Goose Island', 'Malzbier', 'Colorado', 'Skol Beats', 'Budweiser Zero']
pe_rows = [9, 10, 11, 12, 13, 14]
for sku, row in zip(pe_skus, pe_rows):
    for w, col in enumerate([6, 7, 8, 9]):
        val = float(raw3.iloc[row, col]) if pd.notna(raw3.iloc[row, col]) else 0
        prod_pcp.append({'Planta': 'PE541 (PE)', 'SKU': sku, 'Semana': semanas[w], 'Semana_Num': w+1, 'Volume_HL': val})
df_pcp = pd.DataFrame(prod_pcp)
print(f"✅ Aba 3 (Produção PCP): {len(df_pcp)} registros")

# ── Aba 4: Transferências Programadas ────────────────────────────────────────
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
print(f"✅ Aba 4 (Transferências): {len(df_transf)} registros")

# ── Abas 5 e 6: Cenário Divulgado e Nova Demanda ─────────────────────────────
def parse_cenario_neno(sheet_name):
    raw = pd.read_excel(xls, sheet_name, header=None)
    skus_info = [
        ('Patagonia', 4, 9),
        ('Goose Island', 12, 17),
        ('Malzbier', 20, 25),
        ('Colorado', 28, 33),
    ]
    sub_regioes = ['Mapapi', 'NE Norte', 'NE Sul', 'NO Araguaia', 'NO Centro']
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
                records.append({
                    'SKU': sku_name, 'Sub_Regiao': sr_name,
                    'Semana': semanas[w_idx], 'Semana_Num': w_idx + 1,
                    'Demanda': safe_float(raw.iloc[row, wc['dem']]),
                    'WSNP': safe_float(raw.iloc[row, wc['wsnp']]),
                    'EI_Semana': safe_float(raw.iloc[row, wc['ei']]) if wc['ei'] is not None else 0.0,
                    'Suf_Ini_dias': safe_float(raw.iloc[row, wc['suf_ini']]) if wc['suf_ini'] is not None else 0.0,
                    'Transf_Interna': safe_float(raw.iloc[row, wc['tr_int']]),
                    'EF_Semana': safe_float(raw.iloc[row, wc['ef']]),
                    'Suf_Final_dias': safe_float(raw.iloc[row, wc['suf_f']])
                })
    sp_skus = [('Goose Island', 39), ('Malzbier', 40), ('Colorado', 41)]
    for sku_name, row in sp_skus:
        for w_idx, wc in enumerate(week_cols):
            records.append({
                'SKU': sku_name, 'Sub_Regiao': 'SP (Origem)',
                'Semana': semanas[w_idx], 'Semana_Num': w_idx + 1,
                'Demanda': safe_float(raw.iloc[row, wc['dem']]),
                'WSNP': safe_float(raw.iloc[row, wc['wsnp']]),
                'EI_Semana': safe_float(raw.iloc[row, wc['ei']]) if wc['ei'] is not None else 0.0,
                'Suf_Ini_dias': safe_float(raw.iloc[row, wc['suf_ini']]) if wc['suf_ini'] is not None else 0.0,
                'Transf_Interna': 0,
                'EF_Semana': safe_float(raw.iloc[row, wc['ef']]),
                'Suf_Final_dias': safe_float(raw.iloc[row, wc['suf_f']])
            })
    return pd.DataFrame(records)

df_divulgado = parse_cenario_neno('Cenário Divulgado')
df_nova_dem = parse_cenario_neno('Cenário com Nova Demanda')
print(f"✅ Aba 5 (Cenário Divulgado): {len(df_divulgado)} registros")
print(f"✅ Aba 6 (Nova Demanda): {len(df_nova_dem)} registros")

# ── Sub-DataFrames NENO ───────────────────────────────────────────────────────
div_neno = df_divulgado[df_divulgado['Sub_Regiao'] != 'SP (Origem)'].copy()
nova_neno = df_nova_dem[df_nova_dem['Sub_Regiao'] != 'SP (Origem)'].copy()

total = len(df_cenario_br) + len(df_custos_transf) + len(df_pcp) + len(df_transf) + len(df_divulgado) + len(df_nova_dem)
print(f"\n{'='*60}")
print(f"TOTAL: {total} registros carregados com sucesso")
print(f"{'='*60}")
