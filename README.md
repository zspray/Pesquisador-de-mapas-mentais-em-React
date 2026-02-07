# Pesquisador de Mapas Mentais

Aplicação React + TypeScript para buscar e baixar mapas mentais com integração com a API backend.

## 🚀 Início Rápido

### Windows (Recomendado)
**Clique duplo** em `start.bat` - pronto! 🎉

### Terminal/PowerShell
```bash
python appduck.py
```
Acesse: **http://localhost:5000**

Para mais detalhes, veja [COMO_INICIAR.md](COMO_INICIAR.md)

---

## 📋 Características

- 🔍 Busca de mapas mentais em tempo real
- 📱 Interface responsiva e moderna
- 🎨 Design com gradientes e glassmorphism
- 📄 Paginação de resultados
- 💾 Download de imagens com um clique
- ⚡ Build otimizado com Vite

## Estrutura do Projeto

```
src/
├── main.tsx         # Entry point
├── App.tsx          # Componente principal com toda a lógica
├── index.css        # Estilos globais
```

## Instalação

### Pré-requisitos

- Node.js 16+ instalado
- npm ou yarn

### Setup

```bash
npm install
```

## Desenvolvimento

Para rodar o servidor de desenvolvimento com hot reload:

```bash
npm run dev
```

O aplicativo estará disponível em `http://localhost:5173`

## Build para Produção

```bash
npm run build
```

Os arquivos compilados estarão em `dist/`

## Preview de Produção

```bash
npm run preview
```

## Configuração da API

O projeto está configurado para fazer proxy das seguintes rotas:

- `POST /buscar` - Buscar mapas mentais
- `GET /baixar_imagem` - Baixar imagem

Configure a URL da API backend no `vite.config.ts` se necessário.

## Tecnologias

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool otimizado
- **CSS3** - Estilos com gradientes e efeitos modernos

## Funcionalidades Principais

### Busca de Mapas

- Campo de entrada com validação
- Busca via `POST /buscar` com termo e número da página
- Display dos resultados em grid responsivo

### Paginação

- Navegação entre páginas
- Botões anterior e próxima desabilitados conforme necessário
- Informações de página e quantidade de itens

### Gerenciamento de Estado

- Termo de busca
- Número da página atual
- Resultados
- Status de carregamento
- Mensagens de status (erro/sucesso)

### UX Enhancements

- Focus automático no campo de entrada
- Botão "Limpar" para resetar a busca
- Mensagens de status com tipo (error/ok)
- Indicador visual de carregamento
- Loading state nos botões
