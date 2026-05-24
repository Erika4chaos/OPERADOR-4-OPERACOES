# OPERADOR-4-OPERACOES
# Sistema de Segmentação Estratégica de Clientes e Análise de Riscos (AIG)

## 📝 Descrição do Projeto
Proposta de uma arquitetura híbrida (Software e Hardware) para mitigar a fragmentação de identidade digital e otimizar a tomada de decisão atuarial.

## 🛠️ Arquitetura do Sistema
* **Camada de Software:** Algoritmos de agrupamento não supervisionado (**K-Means**) desenvolvidos em Python para segmentação do perfil geral de clientes, utilizando técnicas de reamostragem (**SMOTE**) para tratamento de bases desequilibradas.
* **Camada de Hardware:** Protótipo em **Edge Computing** voltado para monitoramento telemático (*PHYD/PAYD*) de veículos segurados por meio de coleta de dados de acelerômetro e GPS.

## 🚀 Como Executar o Código
1. Clone o repositório: `git clone ...`
2. Instale as dependências: `pip install -r requirements.txt`
3. Execute o módulo principal: `python src_software/main.py`

## ⚖️ Conformidade e Privacidade
Arquitetura projetada sob os princípios de *Privacy by Design*, em estrita conformidade com as diretrizes da Lei Geral de Proteção de Dados (**LGPD**).
