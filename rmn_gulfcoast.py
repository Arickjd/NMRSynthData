import pandas as pd
import numpy as np
import os

# Função para gerar a curva T2
def log_normal_t2(T2, mu_t2, sigma, absolute_volume):
    log_T2 = np.log10(T2)
    log_mu = np.log10(mu_t2)
    curve = np.exp(-((log_T2 - log_mu)**2) / (2 * sigma**2))
    
    # Integra para normalizar a área antes de multiplicar pelo volume
    area = np.trapz(curve, log_T2)
    
    # Evita divisão por zero caso a área seja ínfima
    if area == 0:
        return np.zeros_like(T2)
        
    return (curve / area) * absolute_volume

def main():
    # Verifica e carrega o arquivo de origem
    input_path = 'data/GulfCoast.csv'
    if not os.path.exists(input_path):
        print(f"Erro: O arquivo {input_path} não foi encontrado.")
        return

    print("Carregando dados originais...")
    df = pd.read_csv(input_path)
    
    # Parâmetros para geração da RMN
    num_echoes = 3000                # Quantidade de ecos
    TE = 0.2                         # Tempo de Eco (0.2 ms é o padrão)
    t = np.arange(1, num_echoes + 1) * TE 
    T2_bins = np.logspace(-1, 4, 100) # Range T2 de 0.1 ms a 10000 ms, com 100 bins
    noise_level = 0.3             # Nível do ruído sintético
    
    # Matriz de decaimento calculada uma única vez para otimização
    Matriz_Exp = np.exp(-t[:, None] / T2_bins[None, :]) # Matriz de decaimento 
    
    resultados = []
    
    print(f"Processando {len(df)} registros para gerar curvas sintéticas...")
    
    # Iterar por todas as linhas do dataset
    for index, row in df.iterrows():
        # Variáveis extraídas da linha
        vol_irr = row["MBVI"]                  # Volume preso (pico rápido)
        vol_free = row["MPHI"] - row["MBVI"]   # Volume livre (pico lento)
        swirr_phix = row["Swirr_PHIX"]         # Saturação de Água Irredutível (Target)
        
        # Tratamento p evitar valor negativo
        vol_free = max(0, vol_free)
        vol_irr = max(0, vol_irr)
        
        # Dividindo o fluido livre em dois picos
        vol_free1 = vol_free * 0.4
        vol_free2 = vol_free * 0.6
        
        # GERANDO AS CURVAS
        # 15 ms para argila/capilar
        curve_irr = log_normal_t2(T2_bins, mu_t2=15, sigma=0.25, absolute_volume=vol_irr) 
        # 60 ms e 150 ms para poros maiores
        curve_free1 = log_normal_t2(T2_bins, mu_t2=60, sigma=0.2, absolute_volume=vol_free1) 
        curve_free2 = log_normal_t2(T2_bins, mu_t2=150, sigma=0.15, absolute_volume=vol_free2)
        
        P_T2 = curve_irr + curve_free1 + curve_free2
        
        # GERANDO O DECAIMENTO M(t)
        decay_clean = np.dot(Matriz_Exp, P_T2)
        
        # Ruído de leitura sintético
        noise_train = np.random.normal(0, noise_level, size=num_echoes * 2)
        y_real = (decay_clean * np.cos(np.pi / 4)) + noise_train[:num_echoes]
        y_imag = (decay_clean * np.sin(np.pi / 4)) + noise_train[num_echoes:]
        M_noisy = y_real 
        
        # Monta a estrutura da linha: [Eco_1, Eco_2, ..., Eco_1000, Swirr_PHIX]
        linha_registro = M_noisy.tolist() + [swirr_phix]
        resultados.append(linha_registro)

    print("Montando novo dataset...")
    
    # Nomenclatura das colunas para o novo CSV
    colunas_ecos = [f'Echo_{i+1}' for i in range(num_echoes)]
    colunas_dataset = colunas_ecos + ['Swirr_PHIX']
    
    # Criando e salvando DataFrame
    df_rmn = pd.DataFrame(resultados, columns=colunas_dataset)
    
    output_path = 'data/GulfCoast_RMN_Synthetic.csv'
    
    # Garante que a pasta data exista se o usuário rodar de outro diretório
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    df_rmn.to_csv(output_path, index=False)
    
    print(f"Arquivo salvo em: {output_path}")
    print(f"Dimensão do dataset salvo: {df_rmn.shape[0]} linhas x {df_rmn.shape[1]} colunas")

if __name__ == "__main__":
    main()