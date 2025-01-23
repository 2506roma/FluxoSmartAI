import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Function to generate random dates within a range
def random_date(start, end):
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

# Define the range for random dates
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)

# Load initial data (replace this with your real data loading if needed)
data = pd.DataFrame({
    'Data': pd.date_range(start_date, periods=100).strftime('%Y-%m-%d'),
    'Receitas': np.random.randint(20000, 150000, size=100),
    'Despesas': np.random.randint(10000, 100000, size=100),
    'Categoria': np.random.choice(['Consultoria Financeira', 'Gestão de Investimentos', 'Serviços Bancários', 'Planejamento Financeiro'], size=100),
    'Região': np.random.choice(['Nordeste', 'Norte', 'Sul', 'Sudeste'], size=100),
    'Cliente_Chave': np.random.choice(['Sim', 'Não'], size=100)
})

# Add requested columns with random or calculated data
data['Data da Transação'] = [random_date(start_date, end_date).strftime('%Y-%m-%d') for _ in range(len(data))]
data['Categoria da Transação'] = np.random.choice(['Consultoria', 'Investimentos', 'Empréstimos', 'Taxas Bancárias'], size=len(data))
data['Descrição'] = np.random.choice(['Análise de portfólio', 'Revisão de contratos', 'Abertura de conta', 'Emissão de boletos'], size=len(data))
data['Valor'] = np.random.randint(10000, 200000, size=len(data))
data['Método de Pagamento'] = np.random.choice(['Cartão de Crédito', 'Transferência', 'PIX', 'Boleto'], size=len(data))
data['Contas a Pagar e a Receber'] = np.random.choice(['A Pagar', 'A Receber'], size=len(data))

data['Data de Vencimento'] = [random_date(start_date, end_date).strftime('%Y-%m-%d') for _ in range(len(data))]
data['Valor Contas'] = np.random.randint(10000, 150000, size=len(data))
data['Status'] = np.random.choice(['Pendente', 'Pago', 'Atrasado'], size=len(data))

data['Saldo Inicial'] = np.random.randint(100000, 1000000, size=len(data))
data['Centro de Custo/Departamento'] = np.random.choice(['Consultoria', 'Análise de Riscos', 'Atendimento ao Cliente', 'Compliance'], size=len(data))
data['Receitas Recorrentes'] = np.random.randint(50000, 200000, size=len(data))
data['Previsão de Receita'] = np.random.randint(100000, 500000, size=len(data))
data['Previsão de Despesas'] = np.random.randint(50000, 300000, size=len(data))

data['Valor do Empréstimo'] = np.random.randint(100000, 2000000, size=len(data))
data['Parcelas e Vencimentos'] = [f"{random.randint(1, 60)} parcelas até {random_date(start_date, end_date).strftime('%Y-%m-%d')}" for _ in range(len(data))]

data['Valor de Impostos'] = np.random.randint(10000, 100000, size=len(data))
data['Datas de Vencimento Impostos'] = [random_date(start_date, end_date).strftime('%Y-%m-%d') for _ in range(len(data))]

data['Estoque'] = np.random.randint(0, 10, size=len(data))  # For financial services, inventory might be low or zero
data['Custos de Produção'] = np.random.randint(0, 5000, size=len(data))  # Financial services typically have minimal production costs

# Save the dataset to a CSV file
data.to_csv('fluxo_caixa_empresa_financeira.csv', index=False)

print("Dados gerados e salvos no arquivo 'fluxo_caixa_empresa_financeira.csv'.")
