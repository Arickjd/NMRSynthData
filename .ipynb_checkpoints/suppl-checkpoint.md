# Fundamentação Teórica

a RMN mede a resposta dos núcleos de hidrogênio presentes nos fluidos contidos nos poros.  Esse sinal está em função de:

- Fluido presente no poro →
- Tamanho do poro → tempo de decaimento
- Quantidade do fluido (quant de nucleos de hidrogênio) → amplitude

## 1. Echo Train: o sinal medido

A ferramenta de RMN aplica uma sequência de pulsos e registra uma série de ecos ao longo do tempo, conhecida como **echo train**.

O sinal observado é composto pela soma das contribuições de fluidos localizados em diferentes tipos de poros:

$M(t) =$ 

onde:

- M(t) é o sinal medido;
- Ai é a amplitude associada a um determinado grupo de poros;
- T2,i é o tempo de relaxação transversal daquele grupo de poros.

O echo train é o dado mais próximo da medição física.

## 2. Tempo de Relaxação T₂

Após a aquisição do echo train, busca-se determinar quais componentes de relaxação compõem aquele sinal.

O parâmetro mais utilizado na petrofísica de RMN é o **tempo de relaxação transversal (T2)**.

Fisicamente:

- Poros pequenos → relaxação rápida → T2 curto.
- Poros grandes → relaxação lenta → T2 longo.

## 3. Inversão T₂

O echo train está no domínio do tempo.

Para interpretar o reservatório, é necessário convertê-lo para uma distribuição de tempos de relaxação.

Esse processo é chamado de **inversão T₂**.

Nesse projeto, a inversão assume oito componentes fixas:

| Bin | T₂ (ms) |
| --- | --- |
| P1 | 4 |
| P2 | 8 |
| P3 | 16 |
| P4 | 32 |
| P5 | 64 |
| P6 | 128 |
| P7 | 256 |
| P8 | 512 |

O algoritmo ajusta os valores das amplitudes:

P1,P2,…,P8

de forma que a soma das exponenciais reproduza o echo train observado.

## 4. O que são as Amplitudes?

Cada amplitude representa a quantidade de hidrogênio associada a um determinado intervalo de tempos de relaxação.

Por exemplo:

P1=0.8

significa que existe uma contribuição de magnitude 0.8 proveniente dos poros caracterizados por:

T2≈4ms

Da mesma forma:

P8=1.0

indica uma contribuição associada aos poros com:

T2≈512ms

Como o sinal de RMN é proporcional ao número de núcleos de hidrogênio presentes, as amplitudes são diretamente relacionadas ao volume de fluido existente naquele conjunto de poros.

Em outras palavras:

**Amplitude = volume de fluido associado àquela faixa de T₂.**

## 5. Distribuição T₂

As amplitudes formam o chamado espectro T₂.

Por exemplo:

| Bin | Amplitude |
| --- | --- |
| P1 | 0.8 |
| P2 | 0.6 |
| P3 | 0.1 |
| P4 | 0.0 |
| P5 | 0.0 |
| P6 | 0.2 |
| P7 | 0.6 |
| P8 | 1.0 |

Esse conjunto descreve como o volume de fluido está distribuído entre diferentes tamanhos de poros.

### Exemplo de interpretação

### Caso A

Grande concentração em P1, P2 e P3.

Indica:

- poros pequenos;
- água ligada;
- baixa permeabilidade;
- baixa mobilidade de fluidos.

### Caso B

Grande concentração em P6, P7 e P8.

Indica:

- poros maiores;
- maior permeabilidade;
- maior capacidade de armazenamento;
- maior potencial produtivo.

## 6. MPHI — Porosidade RMN

A porosidade total é calculada pela soma de todas as amplitudes:

$MPHI = \sum_{i-1}^8 P_i$

No primeiro registro do seu CSV:

MPHI=0.796+0.623+0.118+0.013+0.016+0.172+0.556+0.998MPHI≈3.294

Portanto:

**MPHI representa o volume total de fluido detectado pela RMN.**

## 7. Cutoff T₂

Nem todo fluido presente nos poros é móvel.

Para distinguir fluidos móveis de fluidos presos utiliza-se um valor de corte chamado **T₂ cutoff**.

Valores abaixo do cutoff:

- água ligada;
- fluidos imóveis.

Valores acima do cutoff:

- fluidos móveis.

## 8. MBVI — Bound Volume Irreducible

O MBVI corresponde ao volume de fluido associado aos tempos de relaxação menores que o cutoff.

Fisicamente representa:

- água capilar;
- água ligada;
- fluidos presos nos poros menores.

Quanto maior o MBVI:

- maior a quantidade de fluido imóvel;
- menor o potencial produtivo.

## 9. MFFI — Free Fluid Index

O MFFI representa o volume de fluido associado aos tempos de relaxação maiores que o cutoff.

Fisicamente representa:

- fluidos móveis;
- maior conectividade dos poros;
- potencial de fluxo.

Quanto maior o MFFI:

- melhor a qualidade petrofísica do reservatório.

## 10. Saturação Irredutível de Água (Swirr)

Assumindo que o MBVI é composto predominantemente por água ligada:

$S_{wirr}=\frac{MPHI}{MBVI}$

Por exemplo:

$S_{wirr}= 0.467$

ou:

46.7%

Isso significa que aproximadamente 47% do espaço poroso contém água que dificilmente será deslocada durante a produção.