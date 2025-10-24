-- ===============================================
-- SCRIPT DE CRIAÇÃO DO BANCO DE DADOS - SQLite
-- Projeto: Sistema de Análise de Vendas de Carros Esportivos
-- ===============================================

-- SQLite cria o banco automaticamente ao conectar
-- Não precisa de CREATE DATABASE

-- ===============================================
-- TABELA: clientes
-- ===============================================
CREATE TABLE IF NOT EXISTS clientes (
    cliente_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    telefone TEXT,
    data_nascimento DATE NOT NULL,
    genero TEXT CHECK (genero IN ('Masculino', 'Feminino', 'Outro', 'Prefiro não informar')),
    cidade TEXT,
    estado TEXT,
    renda_anual REAL,
    profissao TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===============================================
-- TABELA: vendedores
-- ===============================================
CREATE TABLE IF NOT EXISTS vendedores (
    vendedor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    data_contratacao DATE NOT NULL,
    comissao_percentual REAL DEFAULT 3.00,
    regiao_atuacao TEXT,
    ativo INTEGER DEFAULT 1  -- SQLite usa INTEGER para BOOLEAN (0=false, 1=true)
);

-- ===============================================
-- TABELA: veiculos
-- ===============================================
CREATE TABLE IF NOT EXISTS veiculos (
    veiculo_id INTEGER PRIMARY KEY AUTOINCREMENT,
    marca TEXT NOT NULL,
    modelo TEXT NOT NULL,
    ano_fabricacao INTEGER NOT NULL CHECK (ano_fabricacao >= 2015 AND ano_fabricacao <= 2025),
    cor TEXT,
    tipo_motor TEXT,
    potencia_cv INTEGER,
    cilindradas REAL,
    transmissao TEXT CHECK (transmissao IN ('Manual', 'Automática', 'Automatizada', 'CVT')),
    tracao TEXT CHECK (tracao IN ('Dianteira', 'Traseira', 'Integral', 'AWD')),
    preco_base REAL NOT NULL,
    estoque INTEGER DEFAULT 0,
    categoria TEXT
);

-- ===============================================
-- TABELA: vendas
-- ===============================================
CREATE TABLE IF NOT EXISTS vendas (
    venda_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    veiculo_id INTEGER NOT NULL,
    vendedor_id INTEGER NOT NULL,
    data_venda DATE NOT NULL,
    valor_venda REAL NOT NULL,
    desconto_percentual REAL DEFAULT 0,
    forma_pagamento TEXT CHECK (forma_pagamento IN ('À vista', 'Financiamento', 'Consórcio', 'Leasing')),
    numero_parcelas INTEGER DEFAULT 1,
    valor_entrada REAL DEFAULT 0,
    status_venda TEXT DEFAULT 'Concluída' CHECK (status_venda IN ('Concluída', 'Cancelada', 'Em Processamento')),
    FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id),
    FOREIGN KEY (veiculo_id) REFERENCES veiculos(veiculo_id),
    FOREIGN KEY (vendedor_id) REFERENCES vendedores(vendedor_id)
);

-- ===============================================
-- TABELA: test_drives
-- ===============================================
CREATE TABLE IF NOT EXISTS test_drives (
    test_drive_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    veiculo_id INTEGER NOT NULL,
    data_test_drive TIMESTAMP NOT NULL,
    avaliacao INTEGER CHECK (avaliacao >= 1 AND avaliacao <= 5),
    comentario TEXT,
    resultou_venda INTEGER DEFAULT 0,  -- BOOLEAN: 0=false, 1=true
    vendedor_responsavel_id INTEGER,
    FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id),
    FOREIGN KEY (veiculo_id) REFERENCES veiculos(veiculo_id),
    FOREIGN KEY (vendedor_responsavel_id) REFERENCES vendedores(vendedor_id)
);

-- ===============================================
-- TABELA: servicos_pos_venda
-- ===============================================
CREATE TABLE IF NOT EXISTS servicos_pos_venda (
    servico_id INTEGER PRIMARY KEY AUTOINCREMENT,
    venda_id INTEGER NOT NULL,
    tipo_servico TEXT NOT NULL CHECK (tipo_servico IN ('Revisão', 'Manutenção', 'Reparo', 'Personalização', 'Garantia', 'Detalhamento')),
    data_servico DATE NOT NULL,
    valor_servico REAL,
    satisfacao_cliente INTEGER CHECK (satisfacao_cliente >= 1 AND satisfacao_cliente <= 5),
    observacoes TEXT,
    FOREIGN KEY (venda_id) REFERENCES vendas(venda_id)
);

-- ===============================================
-- ÍNDICES PARA OTIMIZAÇÃO DE CONSULTAS
-- ===============================================

-- Índices na tabela clientes
CREATE INDEX IF NOT EXISTS idx_clientes_email ON clientes(email);
CREATE INDEX IF NOT EXISTS idx_clientes_cidade_estado ON clientes(cidade, estado);
CREATE INDEX IF NOT EXISTS idx_clientes_renda ON clientes(renda_anual);

-- Índices na tabela vendas
CREATE INDEX IF NOT EXISTS idx_vendas_data ON vendas(data_venda);
CREATE INDEX IF NOT EXISTS idx_vendas_cliente ON vendas(cliente_id);
CREATE INDEX IF NOT EXISTS idx_vendas_veiculo ON vendas(veiculo_id);
CREATE INDEX IF NOT EXISTS idx_vendas_vendedor ON vendas(vendedor_id);
CREATE INDEX IF NOT EXISTS idx_vendas_status ON vendas(status_venda);

-- Índices na tabela veiculos
CREATE INDEX IF NOT EXISTS idx_veiculos_marca_modelo ON veiculos(marca, modelo);
CREATE INDEX IF NOT EXISTS idx_veiculos_preco ON veiculos(preco_base);
CREATE INDEX IF NOT EXISTS idx_veiculos_categoria ON veiculos(categoria);

-- Índices na tabela test_drives
CREATE INDEX IF NOT EXISTS idx_test_drives_data ON test_drives(data_test_drive);
CREATE INDEX IF NOT EXISTS idx_test_drives_cliente ON test_drives(cliente_id);
CREATE INDEX IF NOT EXISTS idx_test_drives_resultou_venda ON test_drives(resultou_venda);

-- Índices na tabela servicos_pos_venda
CREATE INDEX IF NOT EXISTS idx_servicos_data ON servicos_pos_venda(data_servico);
CREATE INDEX IF NOT EXISTS idx_servicos_venda ON servicos_pos_venda(venda_id);

-- ===============================================
-- VIEWS ÚTEIS PARA ANÁLISE
-- ===============================================

-- View: Resumo de vendas por cliente
CREATE VIEW IF NOT EXISTS vw_resumo_vendas_cliente AS
SELECT 
    c.cliente_id,
    c.nome,
    c.email,
    COUNT(v.venda_id) as total_compras,
    SUM(v.valor_venda) as valor_total_gasto,
    AVG(v.valor_venda) as ticket_medio,
    MAX(v.data_venda) as ultima_compra
FROM clientes c
LEFT JOIN vendas v ON c.cliente_id = v.cliente_id AND v.status_venda = 'Concluída'
GROUP BY c.cliente_id, c.nome, c.email;

-- View: Performance de vendedores
CREATE VIEW IF NOT EXISTS vw_performance_vendedores AS
SELECT 
    vd.vendedor_id,
    vd.nome,
    COUNT(v.venda_id) as total_vendas,
    SUM(v.valor_venda) as valor_total_vendido,
    AVG(v.valor_venda) as ticket_medio,
    SUM(v.valor_venda * vd.comissao_percentual / 100) as comissao_total
FROM vendedores vd
LEFT JOIN vendas v ON vd.vendedor_id = v.vendedor_id AND v.status_venda = 'Concluída'
GROUP BY vd.vendedor_id, vd.nome;

-- View: Modelos mais vendidos
CREATE VIEW IF NOT EXISTS vw_modelos_mais_vendidos AS
SELECT 
    ve.marca,
    ve.modelo,
    COUNT(v.venda_id) as quantidade_vendida,
    SUM(v.valor_venda) as receita_total,
    AVG(v.valor_venda) as preco_medio_venda
FROM veiculos ve
INNER JOIN vendas v ON ve.veiculo_id = v.veiculo_id AND v.status_venda = 'Concluída'
GROUP BY ve.marca, ve.modelo
ORDER BY quantidade_vendida DESC;

-- View: Taxa de conversão de test drives
CREATE VIEW IF NOT EXISTS vw_conversao_test_drives AS
SELECT 
    ve.marca,
    ve.modelo,
    COUNT(td.test_drive_id) as total_test_drives,
    SUM(CASE WHEN td.resultou_venda = 1 THEN 1 ELSE 0 END) as total_vendas,
    ROUND(100.0 * SUM(CASE WHEN td.resultou_venda = 1 THEN 1 ELSE 0 END) / COUNT(td.test_drive_id), 2) as taxa_conversao
FROM veiculos ve
INNER JOIN test_drives td ON ve.veiculo_id = td.veiculo_id
GROUP BY ve.marca, ve.modelo
HAVING COUNT(td.test_drive_id) > 0
ORDER BY taxa_conversao DESC;

-- ===============================================
-- OBSERVAÇÕES SOBRE SQLite
-- ===============================================

-- SQLite tem algumas diferenças do PostgreSQL:
-- 1. AUTOINCREMENT ao invés de SERIAL
-- 2. INTEGER para BOOLEAN (0/1)
-- 3. REAL ao invés de DECIMAL
-- 4. Não tem COMMENT ON (comentários são apenas neste arquivo)
-- 5. DATE/TIMESTAMP são armazenados como TEXT ou INTEGER
-- 6. Não precisa de schema "public"
-- 7. Arquivo único (.db) ao invés de servidor

-- Para criar o banco: sqlite3 vendas_carros_esportivos.db < create_tables_sqlite.sql
