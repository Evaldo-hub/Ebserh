#!/bin/bash

# Script de Deploy para Render + GitHub + Supabase
echo "🚀 Iniciando deploy para produção..."

# Verificar se há mudanças
if [ -z "$(git status --porcelain)" ]; then
    echo "✅ Nenhuma mudança para commit"
else
    echo "📝 Commitando mudanças..."
    git add .
    git commit -m "Deploy automático - $(date '+%Y-%m-%d %H:%M:%S')"
fi

# Push para GitHub
echo "📤 Enviando para GitHub..."
git push origin main

echo "✅ Deploy iniciado! Aguarde o Render processar..."
echo "🌐 Acompanhe em: https://dashboard.render.com/"
echo "🔍 Health Check: https://ebserh-study.onrender.com/health"

# Testar health check após 30 segundos
echo "⏳ Aguardando 30 segundos para testar..."
sleep 30

curl -s https://ebserh-study.onrender.com/health | jq '.'

echo "🎉 Deploy concluído!"
