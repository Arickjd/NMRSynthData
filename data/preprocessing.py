import pandas as pd
import numpy as np
import os

def preprocess():
    # Definir caminhos de entrada e saída
    input_path = 'raw/GulfCoast_NMR.xlsx'
    output_dir = 'processed'
    output_path = os.path.join(output_dir, 'df_filtered.csv')
    
    print(f"Carregando os dados brutos de: {input_path}")
    # Carregar os dados brutos
    df = pd.read_excel(input_path)

    print("Realizando o recorte amostral (linhas 960 a 1534)...")
    # Selecionar entre as linhas 960-1534
    df_filtered = df.loc[960:1534].copy()

    print("Calculando saturação de água irredutível (Swirr_PHIX)...")
    # Criar coluna de saturação de água irredutível
    df_filtered['Swirr_PHIX'] = df_filtered['MBVI'] / df_filtered['PHIX']

    print("Filtrando e reordenando colunas...")
    # Manter apenas as colunas desejadas e reordenar o índice
    df_filtered = df_filtered[['PHIX', 'MBVI', 'MPHI', 'Swirr_PHIX']]
    df_filtered = df_filtered.sort_index().reset_index(drop=True)

    # Exportar os dados processados
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    df_filtered.to_csv(output_path, index=False)
    print(f"Sucesso! Dados processados exportados para: {output_path}")
    print("\nVisualização dos primeiros registros:")
    print(df_filtered.head())

if __name__ == "__main__":
    preprocess()

