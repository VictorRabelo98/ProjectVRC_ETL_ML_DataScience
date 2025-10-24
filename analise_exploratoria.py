import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configura o estilo dos gráficos
sns.set(style="whitegrid", palette="muted")

# Carrega os dados
clientes = pd.read_csv("dados/clientes.csv")
vendas = pd.read_csv("dados/vendas.csv")
veiculos = pd.read_csv("dados/veiculos.csv")
vendedores = pd.read_csv("dados/vendedores.csv")

# Exibe informações iniciais
print("=== Clientes ===")
print(clientes.info(), "\n")
print(clientes.describe(), "\n")

print("=== Vendas ===")
print(vendas.info(), "\n")
print(vendas.describe(), "\n")

# Exemplo 1: quantidade de vendas por estado
vendas_clientes = vendas.merge(clientes, on="cliente_id", how="left")
estado_vendas = vendas_clientes["estado"].value_counts().head(10)

plt.figure(figsize=(10,5))
sns.barplot(x=estado_vendas.index, y=estado_vendas.values)
plt.title("Vendas por Estado")
plt.xlabel("Estado")
plt.ylabel("Quantidade de Vendas")
plt.show()

# Exemplo 2: ticket médio por vendedor
vendas_vendedores = vendas.merge(vendedores, on="vendedor_id", how="left")
ticket_medio = vendas_vendedores.groupby("nome")["valor_venda"].mean().sort_values(ascending=False)

plt.figure(figsize=(10,5))
ticket_medio.head(10).plot(kind="bar")
plt.title("Top 10 Vendedores por Ticket Médio")
plt.ylabel("Ticket Médio (R$)")
plt.show()
