-- SQL para corrigir tabelas existentes no Supabase
-- Execute este SQL no painel SQL Editor do seu projeto Supabase

-- Adicionar colunas faltantes na tabela questoes
ALTER TABLE questoes ADD COLUMN IF NOT EXISTS id_local INTEGER;
CREATE UNIQUE INDEX IF NOT EXISTS idx_questoes_id_local ON questoes(id_local);

-- Adicionar colunas faltantes na tabela desempenho
ALTER TABLE desempenho ADD COLUMN IF NOT EXISTS id_local INTEGER;
ALTER TABLE desempenho ADD COLUMN IF NOT EXISTS questao_id_local INTEGER;
CREATE UNIQUE INDEX IF NOT EXISTS idx_desempenho_id_local ON desempenho(id_local);
CREATE INDEX IF NOT EXISTS idx_desempenho_questao_id_local ON desempenho(questao_id_local);

-- Adicionar colunas faltantes na tabela plano_estudos
ALTER TABLE plano_estudos ADD COLUMN IF NOT EXISTS id_local INTEGER;
CREATE UNIQUE INDEX IF NOT EXISTS idx_plano_estudos_id_local ON plano_estudos(id_local);

-- Adicionar colunas faltantes na tabela ia_feedback
ALTER TABLE ia_feedback ADD COLUMN IF NOT EXISTS id_local INTEGER;
ALTER TABLE ia_feedback ADD COLUMN IF NOT EXISTS questao_id_local INTEGER;
CREATE UNIQUE INDEX IF NOT EXISTS idx_ia_feedback_id_local ON ia_feedback(id_local);
CREATE INDEX IF NOT EXISTS idx_ia_feedback_questao_id_local ON ia_feedback(questao_id_local);

-- Adicionar colunas de sincronizacao
ALTER TABLE questoes ADD COLUMN IF NOT EXISTS data_sincronizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW();
ALTER TABLE desempenho ADD COLUMN IF NOT EXISTS data_sincronizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW();
ALTER TABLE plano_estudos ADD COLUMN IF NOT EXISTS data_sincronizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW();
ALTER TABLE ia_feedback ADD COLUMN IF NOT EXISTS data_sincronizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW();

-- Adicionar timestamps created_at e updated_at
ALTER TABLE questoes ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
ALTER TABLE questoes ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
ALTER TABLE desempenho ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
ALTER TABLE desempenho ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
ALTER TABLE plano_estudos ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
ALTER TABLE plano_estudos ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
ALTER TABLE ia_feedback ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
ALTER TABLE ia_feedback ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
