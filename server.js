import express from "express";
import sqlite3 from "sqlite3";
import cors from "cors";
import path from "path";

const app = express();
app.use(express.json());
app.use(cors());

// Caminho absoluto do banco de dados
const dbPath = path.resolve("./vendas_carros_esportivos.db");
const db = new sqlite3.Database(dbPath, (err) => {
  if (err) console.error("❌ Erro ao conectar ao banco:", err.message);
  else console.log("✅ Conectado ao SQLite:", dbPath);
});

// ==================== ROTAS ==================== //

// Rota principal
app.get("/", (req, res) => {
  res.send("🚗 API - Sistema de Vendas de Carros Esportivos");
});

// ---------------- CLIENTES ----------------
app.get("/clientes", (req, res) => {
  db.all("SELECT * FROM clientes", [], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
});

app.post("/clientes", (req, res) => {
  const { nome, email, telefone, data_nascimento, genero, cidade, estado, renda_anual, profissao } = req.body;
  const sql = `
    INSERT INTO clientes (nome, email, telefone, data_nascimento, genero, cidade, estado, renda_anual, profissao)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
  `;
  db.run(sql, [nome, email, telefone, data_nascimento, genero, cidade, estado, renda_anual, profissao], function (err) {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ cliente_id: this.lastID });
  });
});

// ---------------- VENDEDORES ----------------
app.get("/vendedores", (req, res) => {
  db.all("SELECT * FROM vendedores", [], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
});

app.post("/vendedores", (req, res) => {
  const { nome, email, data_contratacao, comissao_percentual, regiao_atuacao, ativo } = req.body;
  const sql = `
    INSERT INTO vendedores (nome, email, data_contratacao, comissao_percentual, regiao_atuacao, ativo)
    VALUES (?, ?, ?, ?, ?, ?)
  `;
  db.run(sql, [nome, email, data_contratacao, comissao_percentual, regiao_atuacao, ativo], function (err) {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ vendedor_id: this.lastID });
  });
});

// ---------------- VEÍCULOS ----------------
app.get("/veiculos", (req, res) => {
  db.all("SELECT * FROM veiculos", [], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
});

app.post("/veiculos", (req, res) => {
  const {
    marca, modelo, ano_fabricacao, cor, tipo_motor,
    potencia_cv, cilindradas, transmissao, tracao,
    preco_base, estoque, categoria
  } = req.body;
  const sql = `
    INSERT INTO veiculos (marca, modelo, ano_fabricacao, cor, tipo_motor, potencia_cv, cilindradas, transmissao, tracao, preco_base, estoque, categoria)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `;
  db.run(sql, [marca, modelo, ano_fabricacao, cor, tipo_motor, potencia_cv, cilindradas, transmissao, tracao, preco_base, estoque, categoria], function (err) {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ veiculo_id: this.lastID });
  });
});

// ---------------- VENDAS ----------------
app.get("/vendas", (req, res) => {
  db.all("SELECT * FROM vendas", [], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
});

app.post("/vendas", (req, res) => {
  const {
    cliente_id, veiculo_id, vendedor_id, data_venda,
    valor_venda, desconto_percentual, forma_pagamento,
    numero_parcelas, valor_entrada, status_venda
  } = req.body;

  const sql = `
    INSERT INTO vendas (cliente_id, veiculo_id, vendedor_id, data_venda, valor_venda, desconto_percentual, forma_pagamento, numero_parcelas, valor_entrada, status_venda)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `;
  db.run(sql, [cliente_id, veiculo_id, vendedor_id, data_venda, valor_venda, desconto_percentual, forma_pagamento, numero_parcelas, valor_entrada, status_venda], function (err) {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ venda_id: this.lastID });
  });
});

// ---------------- TEST DRIVES ----------------
app.get("/test_drives", (req, res) => {
  db.all("SELECT * FROM test_drives", [], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
});

app.post("/test_drives", (req, res) => {
  const { cliente_id, veiculo_id, data_test_drive, avaliacao, comentario, resultou_venda, vendedor_responsavel_id } = req.body;
  const sql = `
    INSERT INTO test_drives (cliente_id, veiculo_id, data_test_drive, avaliacao, comentario, resultou_venda, vendedor_responsavel_id)
    VALUES (?, ?, ?, ?, ?, ?, ?)
  `;
  db.run(sql, [cliente_id, veiculo_id, data_test_drive, avaliacao, comentario, resultou_venda, vendedor_responsavel_id], function (err) {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ test_drive_id: this.lastID });
  });
});

// ---------------- SERVIÇOS PÓS-VENDA ----------------
app.get("/servicos_pos_venda", (req, res) => {
  db.all("SELECT * FROM servicos_pos_venda", [], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
});

app.post("/servicos_pos_venda", (req, res) => {
  const { venda_id, tipo_servico, data_servico, valor_servico, satisfacao_cliente, observacoes } = req.body;
  const sql = `
    INSERT INTO servicos_pos_venda (venda_id, tipo_servico, data_servico, valor_servico, satisfacao_cliente, observacoes)
    VALUES (?, ?, ?, ?, ?, ?)
  `;
  db.run(sql, [venda_id, tipo_servico, data_servico, valor_servico, satisfacao_cliente, observacoes], function (err) {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ servico_id: this.lastID });
  });
});

// ---------------- VIEWS ----------------
app.get("/views/:nome", (req, res) => {
  const nome = req.params.nome;
  db.all(`SELECT * FROM ${nome}`, [], (err, rows) => {
    if (err) return res.status(400).json({ error: "View inválida ou inexistente" });
    res.json(rows);
  });
});

// =====================================
const PORT = 3000;
app.listen(PORT, () => console.log(`🚀 API rodando em http://localhost:${PORT}`));
