# Maps4Study - Como Iniciar a Aplicação

## 🚀 Início Rápido (Recomendado para Windows)

### Opção 1: Clique duplo no arquivo `start.bat`

1. Navegue até a pasta do projeto
2. **Clique duas vezes** em `start.bat`
3. Uma janela de terminal abrirá
4. Acesse: **http://localhost:5000**

O script fará:
- ✅ Verificar se Python está instalado
- ✅ Instalar dependências faltantes automaticamente
- ✅ Verificar se o React foi buildado
- ✅ Iniciar o servidor Flask

---

## 📋 Início Manual (Terminal/PowerShell)

### Pré-requisitos

1. **Python 3.8+** instalado
   - Download: https://www.python.org/downloads/
   - Certifique-se de marcar "Add Python to PATH"

2. **Dependências Python**
   ```bash
   pip install flask requests duckduckgo-search
   ```

### Passos para Iniciar

1. **Abra um terminal/PowerShell** na pasta do projeto

2. **Rode o servidor:**
   ```bash
   python appduck.py
   ```

3. **Acesse no navegador:**
   ```
   http://localhost:5000
   ```

---

## 🔧 Resolver Erros Comuns

### Erro: "Python não encontrado"
```bash
# Solução: Reinstale Python com "Add to PATH" marcado
# Ou use o caminho completo:
C:\Users\SeuUsuario\AppData\Local\Programs\Python\Python310\python.exe appduck.py
```

### Erro: "Módulo não encontrado"
```bash
# Solução: Instale as dependências
pip install flask requests duckduckgo-search
```

### Erro: "Porta 5000 já está em uso"
```bash
# Edite appduck.py na última linha:
# Altere: app.run(debug=True)
# Para:   app.run(debug=True, port=5001)
```

### Erro: "dist/index.html não encontrado"
```bash
# Solução: Rebuild o React
node .\node_modules\vite\bin\vite.js build
```

---

## 📁 Estrutura dos Arquivos

```
├── appduck.py              # Servidor Flask (BACKEND)
├── start.bat               # Script para iniciar (Windows)
├── dist/                   # React compilado (entregue pelo Flask)
│   ├── index.html
│   ├── assets/
│   │   ├── *.css
│   │   └── *.js
├── src/                    # Código-fonte React (para desenvolvimento)
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── static/                 # Arquivos estáticos
│   └── mapas_salvos/       # Imagens baixadas (criado automaticamente)
└── package.json            # Dependências Node.js (para desenvolvimento)
```

---

## 🛠️ Desenvolvimento

### Para fazer mudanças no React:

1. **Em um terminal**, rode o servidor de dev:
   ```bash
   npm run dev
   ```

2. **Em outro terminal**, rode o backend:
   ```bash
   python appduck.py
   ```

3. **Acesse:** http://localhost:5173 (dev) ou http://localhost:5000 (prod)

4. **Para atualizar em produção**, rebuild:
   ```bash
   npm run build
   ```

---

## 📝 Troubleshooting

| Erro | Solução |
|------|---------|
| `ModuleNotFoundError: No module named 'flask'` | `pip install flask requests duckduckgo-search` |
| `Address already in use` | Feche outra instância ou mude a porta em `appduck.py` |
| `[Errno -2] Name or service not known` | Problema de conexão com DuckDuckGo (tente novamente) |
| Imagens não carregam | Verifique pasta `static/mapas_salvos/` e permissões |

---

## 🎯 Fluxo Típico de Uso

```
1. Clique em start.bat
   ↓
2. Aguarde a mensagem "Running on http://localhost:5000"
   ↓
3. Abra o navegador em http://localhost:5000
   ↓
4. Digite um termo na barra de busca
   ↓
5. Pressione Enter ou clique em "Buscar"
   ↓
6. Veja os mapas mentais encontrados
   ↓
7. Clique em "Baixar" para salvar a imagem
   ↓
8. Imagem salva em static/mapas_salvos/<termo>/
```

---

## 📞 Suporte

Se encontrar problemas:
1. Verifique se Python está instalado: `python --version`
2. Verifique as dependências: `pip list | grep -E "flask|requests|duckduckgo"`
3. Veja os logs na janela do terminal
4. Tente reiniciar o servidor e limpar o cache do navegador (Ctrl+Shift+Delete)

**Pronto para usar! 🎉**
