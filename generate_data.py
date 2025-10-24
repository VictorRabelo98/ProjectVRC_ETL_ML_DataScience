"""
Script de Geração de Dados Sintéticos
Projeto: Sistema de Análise de Vendas de Carros Esportivos

Este script gera dados realistas para popular o banco de dados.
Inclui correlações lógicas entre variáveis para simular comportamento real.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from faker import Faker
import random

# Configurar seed para reprodutibilidade
np.random.seed(42)
random.seed(42)
fake = Faker('pt_BR')
Faker.seed(42)

# ===============================================
# CONFIGURAÇÕES GLOBAIS
# ===============================================

N_CLIENTES = 2000
N_VENDEDORES = 15
N_VEICULOS = 50
N_VENDAS = 1500
N_TEST_DRIVES = 3000
N_SERVICOS = 800

DATA_INICIO = datetime(2023, 1, 1)
DATA_FIM = datetime(2024, 12, 31)

# ===============================================
# FUNÇÃO: GERAR CLIENTES
# ===============================================

def gerar_clientes(n=N_CLIENTES):
    """
    Gera dados sintéticos de clientes com perfil adequado para compradores
    de carros esportivos (maior renda, profissões específicas)
    """
    print(f"Gerando {n} clientes...")
    
    # Profissões típicas de compradores de carros esportivos
    profissoes_alto_poder = [
        'Empresário', 'Médico', 'Advogado', 'Engenheiro', 'Arquiteto',
        'Consultor', 'Executivo', 'Investidor', 'Dentista', 'Piloto',
        'Diretor de Empresa', 'Contador', 'Professor Universitário',
        'Desenvolvedor de Software', 'Gestor de TI', 'Cirurgião',
        'Juiz', 'Promotor', 'Delegado', 'Produtor', 'Agente Esportivo'
    ]
    
    cidades_estados = [
        ('São Paulo', 'SP'), ('Rio de Janeiro', 'RJ'), ('Brasília', 'DF'),
        ('Belo Horizonte', 'MG'), ('Curitiba', 'PR'), ('Porto Alegre', 'RS'),
        ('Salvador', 'BA'), ('Fortaleza', 'CE'), ('Recife', 'PE'),
        ('Goiânia', 'GO'), ('Campinas', 'SP'), ('São José dos Campos', 'SP'),
        ('Florianópolis', 'SC'), ('Manaus', 'AM'), ('Vitória', 'ES')
    ]
    
    generos = ['Masculino', 'Feminino', 'Outro', 'Prefiro não informar']
    pesos_generos = [0.65, 0.30, 0.03, 0.02]  # Mais homens compram carros esportivos (estatística)
    
    clientes = []
    
    for i in range(n):
        # Idade entre 25 e 70 anos (concentrada entre 30-55)
        idade = int(np.random.beta(2, 3) * 45 + 25)
        data_nascimento = datetime.now() - timedelta(days=idade*365.25)
        
        # Renda correlacionada com idade (peak entre 40-50 anos)
        if idade < 35:
            renda_base = np.random.uniform(150000, 500000)
        elif idade < 50:
            renda_base = np.random.uniform(300000, 1500000)
        else:
            renda_base = np.random.uniform(200000, 1000000)
        
        # Adicionar variação
        renda_anual = round(renda_base * np.random.uniform(0.8, 1.5), 2)
        
        # Data de cadastro aleatória nos últimos 3 anos
        dias_cadastro = random.randint(0, 1095)
        data_cadastro = DATA_FIM - timedelta(days=dias_cadastro)
        
        cidade, estado = random.choice(cidades_estados)
        genero = np.random.choice(generos, p=pesos_generos)
        
        cliente = {
            'cliente_id': i + 1,
            'nome': fake.name(),
            'email': fake.email(),
            'telefone': fake.phone_number(),
            'data_nascimento': data_nascimento.date(),
            'genero': genero,
            'cidade': cidade,
            'estado': estado,
            'renda_anual': renda_anual,
            'profissao': random.choice(profissoes_alto_poder),
            'data_cadastro': data_cadastro
        }
        clientes.append(cliente)
    
    df_clientes = pd.DataFrame(clientes)
    print(f"✓ {len(df_clientes)} clientes gerados")
    return df_clientes

# ===============================================
# FUNÇÃO: GERAR VENDEDORES
# ===============================================

def gerar_vendedores(n=N_VENDEDORES):
    """
    Gera dados de vendedores
    """
    print(f"Gerando {n} vendedores...")
    
    regioes = ['Sul', 'Sudeste', 'Centro-Oeste', 'Norte', 'Nordeste']
    
    vendedores = []
    
    for i in range(n):
        # Data de contratação nos últimos 5 anos
        dias_contratacao = random.randint(0, 1825)
        data_contratacao = DATA_FIM - timedelta(days=dias_contratacao)
        
        # Comissão varia entre 2% e 5%
        comissao = round(np.random.uniform(2.0, 5.0), 2)
        
        vendedor = {
            'vendedor_id': i + 1,
            'nome': fake.name(),
            'email': fake.email(),
            'data_contratacao': data_contratacao.date(),
            'comissao_percentual': comissao,
            'regiao_atuacao': random.choice(regioes),
            'ativo': True
        }
        vendedores.append(vendedor)
    
    df_vendedores = pd.DataFrame(vendedores)
    print(f"✓ {len(df_vendedores)} vendedores gerados")
    return df_vendedores

# ===============================================
# FUNÇÃO: GERAR VEÍCULOS
# ===============================================

def gerar_veiculos(n=N_VEICULOS):
    """
    Gera catálogo de veículos esportivos com características realistas
    """
    print(f"Gerando {n} veículos...")
    
    # Definição de marcas e modelos de carros esportivos
    carros_esportivos = {
        'Ferrari': [
            ('488 GTB', 670, 3.9, 850000, 'Superesportivo'),
            ('F8 Tributo', 720, 3.9, 1200000, 'Superesportivo'),
            ('Roma', 620, 3.9, 950000, 'Gran Turismo'),
            ('Portofino', 600, 3.9, 800000, 'Conversível'),
            ('812 Superfast', 800, 6.5, 1500000, 'Gran Turismo')
        ],
        'Lamborghini': [
            ('Huracán', 640, 5.2, 1100000, 'Superesportivo'),
            ('Aventador', 770, 6.5, 2000000, 'Superesportivo'),
            ('Urus', 650, 4.0, 1300000, 'SUV Esportivo')
        ],
        'Porsche': [
            ('911 Carrera', 385, 3.0, 550000, 'Esportivo'),
            ('911 Turbo', 580, 3.8, 950000, 'Superesportivo'),
            ('718 Cayman', 300, 2.0, 350000, 'Esportivo'),
            ('718 Boxster', 300, 2.0, 380000, 'Conversível'),
            ('Panamera', 330, 3.0, 650000, 'Gran Turismo'),
            ('Taycan', 560, 0.0, 700000, 'Esportivo Elétrico')
        ],
        'McLaren': [
            ('720S', 720, 4.0, 1400000, 'Superesportivo'),
            ('GT', 620, 4.0, 1100000, 'Gran Turismo'),
            ('Artura', 680, 3.0, 1250000, 'Superesportivo Híbrido')
        ],
        'Aston Martin': [
            ('Vantage', 510, 4.0, 850000, 'Esportivo'),
            ('DB11', 630, 5.2, 1100000, 'Gran Turismo'),
            ('DBS Superleggera', 725, 5.2, 1600000, 'Superesportivo')
        ],
        'Chevrolet': [
            ('Corvette C8', 495, 6.2, 450000, 'Esportivo'),
            ('Camaro SS', 455, 6.2, 350000, 'Muscle Car'),
            ('Camaro ZL1', 650, 6.2, 550000, 'Muscle Car')
        ],
        'Ford': [
            ('Mustang GT', 460, 5.0, 400000, 'Muscle Car'),
            ('Mustang Shelby GT500', 760, 5.2, 700000, 'Muscle Car')
        ],
        'Dodge': [
            ('Challenger SRT Hellcat', 717, 6.2, 550000, 'Muscle Car'),
            ('Charger SRT Hellcat', 707, 6.2, 520000, 'Muscle Car')
        ],
        'BMW': [
            ('M3 Competition', 510, 3.0, 600000, 'Esportivo'),
            ('M4 Competition', 510, 3.0, 620000, 'Esportivo'),
            ('M5 Competition', 625, 4.4, 850000, 'Esportivo'),
            ('M8 Competition', 625, 4.4, 950000, 'Gran Turismo')
        ],
        'Mercedes-AMG': [
            ('GT', 530, 4.0, 750000, 'Esportivo'),
            ('GT R', 585, 4.0, 950000, 'Superesportivo'),
            ('C63 S', 510, 4.0, 600000, 'Esportivo'),
            ('E63 S', 612, 4.0, 750000, 'Esportivo')
        ],
        'Audi': [
            ('R8 V10', 570, 5.2, 1200000, 'Superesportivo'),
            ('RS5', 450, 2.9, 550000, 'Esportivo'),
            ('RS7', 600, 4.0, 850000, 'Gran Turismo')
        ]
    }
    
    cores_disponiveis = [
        'Vermelho', 'Preto', 'Branco', 'Prata', 'Azul', 'Amarelo',
        'Verde', 'Cinza', 'Laranja', 'Dourado'
    ]
    
    transmissoes = ['Automática', 'Automatizada', 'Manual']
    tracoes = ['Traseira', 'Integral', 'AWD']
    
    veiculos = []
    veiculo_id = 1
    
    for marca, modelos in carros_esportivos.items():
        for modelo_info in modelos:
            modelo, potencia, cilindradas, preco_base, categoria = modelo_info
            
            # Gerar variações de ano e cor
            anos_disponiveis = [2022, 2023, 2024, 2025]
            
            for _ in range(max(1, n // (len(carros_esportivos) * 3))):  # Distribuir os 50 veículos
                ano = random.choice(anos_disponiveis)
                cor = random.choice(cores_disponiveis)
                
                # Ajustar preço baseado no ano
                ajuste_ano = 1.0 + (ano - 2022) * 0.05
                preco_final = round(preco_base * ajuste_ano * np.random.uniform(0.95, 1.05), 2)
                
                # Tipo de motor
                if cilindradas == 0.0:
                    tipo_motor = 'Elétrico'
                elif cilindradas < 3.0:
                    tipo_motor = 'Turbo 4 cilindros'
                elif cilindradas < 4.5:
                    tipo_motor = 'V6 Turbo' if potencia > 400 else 'V6'
                else:
                    tipo_motor = 'V8' if cilindradas < 6.0 else 'V10' if cilindradas < 7.0 else 'V12'
                
                # Transmissão (Ferraris modernas são todas automáticas)
                if marca in ['Ferrari', 'Lamborghini', 'McLaren']:
                    transmissao = 'Automatizada'
                else:
                    transmissao = random.choice(transmissoes)
                
                # Tração
                if marca in ['Ferrari', 'Lamborghini', 'Audi']:
                    tracao = 'AWD' if np.random.random() > 0.3 else 'Traseira'
                elif marca in ['Porsche', 'Mercedes-AMG', 'BMW']:
                    tracao = random.choice(['Traseira', 'AWD'])
                else:
                    tracao = 'Traseira'
                
                # Estoque (alguns modelos mais raros)
                if preco_final > 1000000:
                    estoque = random.randint(0, 2)
                else:
                    estoque = random.randint(1, 5)
                
                veiculo = {
                    'veiculo_id': veiculo_id,
                    'marca': marca,
                    'modelo': modelo,
                    'ano_fabricacao': ano,
                    'cor': cor,
                    'tipo_motor': tipo_motor,
                    'potencia_cv': potencia,
                    'cilindradas': cilindradas,
                    'transmissao': transmissao,
                    'tracao': tracao,
                    'preco_base': preco_final,
                    'estoque': estoque,
                    'categoria': categoria
                }
                veiculos.append(veiculo)
                veiculo_id += 1
                
                if veiculo_id > n:
                    break
            
            if veiculo_id > n:
                break
        
        if veiculo_id > n:
            break
    
    df_veiculos = pd.DataFrame(veiculos[:n])
    print(f"✓ {len(df_veiculos)} veículos gerados")
    return df_veiculos

# ===============================================
# FUNÇÃO: GERAR VENDAS
# ===============================================

def gerar_vendas(df_clientes, df_veiculos, df_vendedores, n=N_VENDAS):
    """
    Gera vendas com correlações realistas:
    - Clientes com maior renda compram carros mais caros
    - Sazonalidade (mais vendas em dezembro e junho)
    - Descontos ocasionais
    """
    print(f"Gerando {n} vendas...")
    
    formas_pagamento = ['À vista', 'Financiamento', 'Consórcio', 'Leasing']
    pesos_pagamento = [0.25, 0.50, 0.15, 0.10]
    
    status_venda = ['Concluída', 'Cancelada']
    pesos_status = [0.95, 0.05]
    
    vendas = []
    
    for i in range(n):
        # Data de venda com sazonalidade
        # Mais vendas em dezembro (fim de ano) e junho (meio do ano)
        mes_prob = [0.06, 0.06, 0.07, 0.07, 0.08, 0.12, 0.08, 0.07, 0.07, 0.08, 0.09, 0.15]
        mes = np.random.choice(range(1, 13), p=mes_prob)
        
        ano = random.choice([2023, 2024])
        if ano == 2024 and mes > 12:
            mes = 12
        
        dia = random.randint(1, 28)
        data_venda = datetime(ano, mes, dia).date()
        
        # Selecionar cliente (clientes com maior renda têm mais probabilidade de comprar)
        cliente = df_clientes.sample(1, weights=df_clientes['renda_anual']).iloc[0]
        
        # Selecionar veículo correlacionado com a renda do cliente
        # Clientes com renda > 800k têm mais chance de comprar carros > 1M
        if cliente['renda_anual'] > 800000:
            veiculos_disponiveis = df_veiculos[df_veiculos['preco_base'] > 600000]
        elif cliente['renda_anual'] > 500000:
            veiculos_disponiveis = df_veiculos[
                (df_veiculos['preco_base'] > 400000) & 
                (df_veiculos['preco_base'] < 1200000)
            ]
        else:
            veiculos_disponiveis = df_veiculos[df_veiculos['preco_base'] < 800000]
        
        if len(veiculos_disponiveis) == 0:
            veiculos_disponiveis = df_veiculos
        
        veiculo = veiculos_disponiveis.sample(1).iloc[0]
        
        # Vendedor aleatório
        vendedor = df_vendedores.sample(1).iloc[0]
        
        # Desconto (0-15%, maior para carros mais caros ou fim de ano)
        if mes == 12 or veiculo['preco_base'] > 1000000:
            desconto = round(np.random.uniform(0, 15), 2)
        else:
            desconto = round(np.random.uniform(0, 8), 2)
        
        # Valor da venda
        valor_venda = round(veiculo['preco_base'] * (1 - desconto/100), 2)
        
        # Forma de pagamento
        forma_pagamento = np.random.choice(formas_pagamento, p=pesos_pagamento)
        
        # Parcelas e entrada
        if forma_pagamento == 'À vista':
            numero_parcelas = 1
            valor_entrada = valor_venda
        elif forma_pagamento == 'Financiamento':
            numero_parcelas = random.choice([12, 24, 36, 48, 60])
            valor_entrada = round(valor_venda * np.random.uniform(0.20, 0.40), 2)
        elif forma_pagamento == 'Consórcio':
            numero_parcelas = random.choice([60, 72, 84])
            valor_entrada = 0
        else:  # Leasing
            numero_parcelas = random.choice([24, 36, 48])
            valor_entrada = round(valor_venda * 0.10, 2)
        
        status = np.random.choice(status_venda, p=pesos_status)
        
        venda = {
            'venda_id': i + 1,
            'cliente_id': cliente['cliente_id'],
            'veiculo_id': veiculo['veiculo_id'],
            'vendedor_id': vendedor['vendedor_id'],
            'data_venda': data_venda,
            'valor_venda': valor_venda,
            'desconto_percentual': desconto,
            'forma_pagamento': forma_pagamento,
            'numero_parcelas': numero_parcelas,
            'valor_entrada': valor_entrada,
            'status_venda': status
        }
        vendas.append(venda)
    
    df_vendas = pd.DataFrame(vendas)
    print(f"✓ {len(df_vendas)} vendas geradas")
    return df_vendas

# ===============================================
# FUNÇÃO: GERAR TEST DRIVES
# ===============================================

def gerar_test_drives(df_clientes, df_veiculos, df_vendedores, df_vendas, n=N_TEST_DRIVES):
    """
    Gera test drives, alguns resultando em vendas (35% de conversão)
    """
    print(f"Gerando {n} test drives...")
    
    test_drives = []
    vendas_com_test = set()
    
    # Primeiro, criar test drives para vendas realizadas (nem todas têm test drive)
    vendas_com_td = df_vendas[df_vendas['status_venda'] == 'Concluída'].sample(
        frac=0.70
    )  # 70% das vendas tiveram test drive
    
    for _, venda in vendas_com_td.iterrows():
        # Test drive alguns dias antes da venda
        dias_antes = random.randint(1, 30)
        data_test_drive = venda['data_venda'] - timedelta(days=dias_antes)
        
        # Adicionar horário
        hora = random.randint(9, 18)
        minuto = random.choice([0, 30])
        data_test_drive = datetime.combine(data_test_drive, datetime.min.time()).replace(
            hour=hora, minute=minuto
        )
        
        # Avaliação alta (4-5) pois resultou em venda
        avaliacao = random.choice([4, 5])
        
        comentarios_positivos = [
            'Excelente desempenho e conforto!',
            'Carro incrível, superou expectativas.',
            'Potência impressionante, adorei dirigir.',
            'Muito confortável e tecnológico.',
            'Design fantástico e performance excelente.',
            'Melhor test drive que já fiz!',
            'Estou impressionado com a qualidade.'
        ]
        
        test_drive = {
            'test_drive_id': len(test_drives) + 1,
            'cliente_id': venda['cliente_id'],
            'veiculo_id': venda['veiculo_id'],
            'data_test_drive': data_test_drive,
            'avaliacao': avaliacao,
            'comentario': random.choice(comentarios_positivos),
            'resultou_venda': True,
            'vendedor_responsavel_id': venda['vendedor_id']
        }
        test_drives.append(test_drive)
        vendas_com_test.add(venda['venda_id'])
    
    # Agora gerar test drives que NÃO resultaram em venda
    n_restante = n - len(test_drives)
    
    comentarios_neutros_negativos = [
        'Bom carro, mas vou pensar mais um pouco.',
        'Gostei, mas está acima do meu orçamento.',
        'Ótimo carro, vou avaliar outras opções.',
        'Performance boa, mas esperava mais.',
        'Confortável, mas prefiro outro modelo.',
        'Interessante, mas não é exatamente o que procuro.',
        'Bom test drive, vou comparar com concorrentes.'
    ]
    
    for i in range(n_restante):
        cliente = df_clientes.sample(1).iloc[0]
        veiculo = df_veiculos.sample(1).iloc[0]
        vendedor = df_vendedores.sample(1).iloc[0]
        
        # Data aleatória
        dias = random.randint(0, 730)
        data_test_drive = DATA_FIM - timedelta(days=dias)
        hora = random.randint(9, 18)
        minuto = random.choice([0, 30])
        data_test_drive = data_test_drive.replace(hour=hora, minute=minuto)
        
        # Avaliação variada (1-5)
        avaliacao = random.choices([1, 2, 3, 4, 5], weights=[0.05, 0.10, 0.25, 0.35, 0.25])[0]
        
        test_drive = {
            'test_drive_id': len(test_drives) + 1,
            'cliente_id': cliente['cliente_id'],
            'veiculo_id': veiculo['veiculo_id'],
            'data_test_drive': data_test_drive,
            'avaliacao': avaliacao,
            'comentario': random.choice(comentarios_neutros_negativos),
            'resultou_venda': False,
            'vendedor_responsavel_id': vendedor['vendedor_id']
        }
        test_drives.append(test_drive)
    
    df_test_drives = pd.DataFrame(test_drives)
    print(f"✓ {len(df_test_drives)} test drives gerados")
    print(f"  Taxa de conversão: {df_test_drives['resultou_venda'].mean()*100:.1f}%")
    return df_test_drives

# ===============================================
# FUNÇÃO: GERAR SERVIÇOS PÓS-VENDA
# ===============================================

def gerar_servicos_pos_venda(df_vendas, n=N_SERVICOS):
    """
    Gera serviços pós-venda apenas para vendas concluídas
    """
    print(f"Gerando {n} serviços pós-venda...")
    
    tipos_servico = ['Revisão', 'Manutenção', 'Reparo', 'Personalização', 'Garantia', 'Detalhamento']
    
    # Valores típicos por tipo de serviço
    valores_servico = {
        'Revisão': (2000, 8000),
        'Manutenção': (3000, 15000),
        'Reparo': (5000, 50000),
        'Personalização': (10000, 100000),
        'Garantia': (0, 5000),
        'Detalhamento': (1500, 5000)
    }
    
    vendas_concluidas = df_vendas[df_vendas['status_venda'] == 'Concluída']
    
    servicos = []
    
    for i in range(n):
        venda = vendas_concluidas.sample(1).iloc[0]
        
        # Serviço ocorre após a venda (30 a 700 dias depois)
        dias_depois = random.randint(30, 700)
        data_servico = venda['data_venda'] + timedelta(days=dias_depois)
        
        # Garantir que não ultrapasse data final
        if data_servico > DATA_FIM.date():
            data_servico = DATA_FIM.date()
        
        tipo_servico = random.choice(tipos_servico)
        
        # Valor baseado no tipo
        min_val, max_val = valores_servico[tipo_servico]
        valor_servico = round(np.random.uniform(min_val, max_val), 2)
        
        # Satisfação (geralmente alta em serviços de carros de luxo)
        satisfacao = random.choices([1, 2, 3, 4, 5], weights=[0.02, 0.05, 0.13, 0.35, 0.45])[0]
        
        observacoes_servico = [
            'Serviço realizado conforme esperado.',
            'Cliente satisfeito com o atendimento.',
            'Tudo certo, sem problemas.',
            'Serviço de excelência.',
            'Cliente elogiou a agilidade.',
            'Atendimento impecável.',
            'Serviço dentro do prazo.'
        ]
        
        servico = {
            'servico_id': i + 1,
            'venda_id': venda['venda_id'],
            'tipo_servico': tipo_servico,
            'data_servico': data_servico,
            'valor_servico': valor_servico,
            'satisfacao_cliente': satisfacao,
            'observacoes': random.choice(observacoes_servico)
        }
        servicos.append(servico)
    
    df_servicos = pd.DataFrame(servicos)
    print(f"✓ {len(df_servicos)} serviços pós-venda gerados")
    return df_servicos

# ===============================================
# FUNÇÃO PRINCIPAL
# ===============================================

def gerar_todos_dados():
    """
    Função principal que gera todos os dados e salva em CSV
    """
    print("\n" + "="*60)
    print("INICIANDO GERAÇÃO DE DADOS SINTÉTICOS")
    print("="*60 + "\n")
    
    # Gerar dados
    df_clientes = gerar_clientes()
    df_vendedores = gerar_vendedores()
    df_veiculos = gerar_veiculos()
    df_vendas = gerar_vendas(df_clientes, df_veiculos, df_vendedores)
    df_test_drives = gerar_test_drives(df_clientes, df_veiculos, df_vendedores, df_vendas)
    df_servicos = gerar_servicos_pos_venda(df_vendas)
    
    # Criar diretório de saída
    import os
    os.makedirs('C:/Users/Luciano/Documents/Projeto_ELT_ML/Dados', exist_ok=True)
    
    # Salvar em CSV
    print("\n" + "="*60)
    print("SALVANDO DADOS EM CSV")
    print("="*60 + "\n")
    
    df_clientes.to_csv('C:/Users/Luciano/Documents/Projeto_ELT_ML/Dados/clientes.csv', index=False, encoding='utf-8')
    print("✓ clientes.csv salvo")
    
    df_vendedores.to_csv('C:/Users/Luciano/Documents/Projeto_ELT_ML/Dados/vendedores.csv', index=False, encoding='utf-8')
    print("✓ vendedores.csv salvo")
    
    df_veiculos.to_csv('C:/Users/Luciano/Documents/Projeto_ELT_ML/Dados/veiculos.csv', index=False, encoding='utf-8')
    print("✓ veiculos.csv salvo")
    
    df_vendas.to_csv('C:/Users/Luciano/Documents/Projeto_ELT_ML/Dados/vendas.csv', index=False, encoding='utf-8')
    print("✓ vendas.csv salvo")
    
    df_test_drives.to_csv('C:/Users/Luciano/Documents/Projeto_ELT_ML/Dados/test_drives.csv', index=False, encoding='utf-8')
    print("✓ test_drives.csv salvo")
    
    df_servicos.to_csv('C:/Users/Luciano/Documents/Projeto_ELT_ML/Dados/servicos_pos_venda.csv', index=False, encoding='utf-8')
    print("✓ servicos_pos_venda.csv salvo")
    
    # Estatísticas finais
    print("\n" + "="*60)
    print("RESUMO DOS DADOS GERADOS")
    print("="*60 + "\n")
    
    print(f"📊 Clientes: {len(df_clientes):,}")
    print(f"   - Renda média: R$ {df_clientes['renda_anual'].mean():,.2f}")
    print(f"   - Idade média: {((datetime.now() - pd.to_datetime(df_clientes['data_nascimento'])).dt.days / 365.25).mean():.1f} anos")
    
    print(f"\n👔 Vendedores: {len(df_vendedores):,}")
    print(f"   - Comissão média: {df_vendedores['comissao_percentual'].mean():.2f}%")
    
    print(f"\n🚗 Veículos: {len(df_veiculos):,}")
    print(f"   - Preço médio: R$ {df_veiculos['preco_base'].mean():,.2f}")
    print(f"   - Potência média: {df_veiculos['potencia_cv'].mean():.0f} cv")
    
    print(f"\n💰 Vendas: {len(df_vendas):,}")
    vendas_concluidas = df_vendas[df_vendas['status_venda'] == 'Concluída']
    print(f"   - Concluídas: {len(vendas_concluidas):,} ({len(vendas_concluidas)/len(df_vendas)*100:.1f}%)")
    print(f"   - Valor total: R$ {vendas_concluidas['valor_venda'].sum():,.2f}")
    print(f"   - Ticket médio: R$ {vendas_concluidas['valor_venda'].mean():,.2f}")
    
    print(f"\n🏎️  Test Drives: {len(df_test_drives):,}")
    print(f"   - Taxa de conversão: {df_test_drives['resultou_venda'].mean()*100:.1f}%")
    print(f"   - Avaliação média: {df_test_drives['avaliacao'].mean():.2f}/5")
    
    print(f"\n🔧 Serviços Pós-Venda: {len(df_servicos):,}")
    print(f"   - Valor total: R$ {df_servicos['valor_servico'].sum():,.2f}")
    print(f"   - Satisfação média: {df_servicos['satisfacao_cliente'].mean():.2f}/5")
    
    print("\n" + "="*60)
    print("✅ GERAÇÃO CONCLUÍDA COM SUCESSO!")
    print("="*60 + "\n")
    
    return {
        'clientes': df_clientes,
        'vendedores': df_vendedores,
        'veiculos': df_veiculos,
        'vendas': df_vendas,
        'test_drives': df_test_drives,
        'servicos': df_servicos
    }

# ===============================================
# EXECUTAR
# ===============================================

if __name__ == "__main__":
    dados = gerar_todos_dados()
