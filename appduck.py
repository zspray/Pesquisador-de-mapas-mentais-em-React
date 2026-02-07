from flask import Flask, request, jsonify, send_file, send_from_directory
import requests
import io
import re
import os
import unicodedata

try:
    from duckduckgo_search import DDGS
except ImportError:
    DDGS = None  # pip install duckduckgo-search

app = Flask(__name__, static_folder="dist", static_url_path="")

# Adiciona Static folder para servir imagens baixadas
@app.route('/static/<path:filename>')
def serve_static_files(filename):
    """Serve arquivos da pasta static (mapas_salvos e outros)"""
    file_path = os.path.join('static', filename)
    if not os.path.exists(file_path):
        return f"Arquivo não encontrado: {filename}", 404
    return send_from_directory('static', filename)

# Para debug: lista imagens salvas
@app.route('/debug/imagens')
def debug_imagens():
    """Debug: lista todas as imagens salvas e suas URLs"""
    imagens = {}
    if os.path.exists(PASTA_DOWNLOADS):
        for pasta in os.listdir(PASTA_DOWNLOADS):
            pasta_path = os.path.join(PASTA_DOWNLOADS, pasta)
            if os.path.isdir(pasta_path):
                imagens_pasta = []
                for arquivo in os.listdir(pasta_path):
                    caminho_relativo = f"/static/mapas_salvos/{pasta}/{arquivo}"
                    file_path = os.path.join(pasta_path, arquivo)
                    file_size = os.path.getsize(file_path)
                    imagens_pasta.append({
                        "nome": arquivo,
                        "url": caminho_relativo,
                        "tamanho_bytes": file_size,
                        "existe": os.path.exists(file_path)
                    })
                imagens[pasta] = imagens_pasta
    return jsonify({
        "total_pastas": len(imagens),
        "imagens": imagens,
        "pasta_downloads": PASTA_DOWNLOADS,
        "pasta_existe": os.path.exists(PASTA_DOWNLOADS)
    })

# --- CONFIGURAÇÕES ---
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://duckduckgo.com/",
}

# Pasta base onde as imagens ficam salvas: static/mapas_salvos/<termo_sanitizado>/
PASTA_DOWNLOADS = os.path.join("static", "mapas_salvos")
if not os.path.exists(PASTA_DOWNLOADS):
    os.makedirs(PASTA_DOWNLOADS)


def limpar_texto(texto):
    """Remove acentos e caracteres inválidos para nomes de arquivo/pasta."""
    nfkd = unicodedata.normalize("NFKD", texto)
    texto_sem_acento = "".join([c for c in nfkd if not unicodedata.combining(c)])
    texto_limpo = re.sub(r"[^a-zA-Z0-9 ]", "", texto_sem_acento)
    return texto_limpo.strip()


def gerar_nome_pasta(termo_busca):
    """Pasta por termo, ex: 'Sistema Nervoso' -> 'sistema_nervoso'."""
    return limpar_texto(termo_busca).lower().replace(" ", "_")


def gerar_nome_arquivo(termo_busca, indice_unico):
    """Nome padronizado, ex: MAPA MENTAL SOBRE BIOLOGIA - 3.jpg."""
    nome_limpo = limpar_texto(termo_busca).upper()
    return f"MAPA MENTAL SOBRE {nome_limpo} - {indice_unico}.jpg"


def salvar_imagem_localmente(url_remota, termo_busca, indice_unico):
    """
    Baixa a imagem e salva em static/mapas_salvos/<termo>/NOME.jpg.
    Retorna o caminho relativo (para usar no HTML).
    """
    try:
        nome_pasta = gerar_nome_pasta(termo_busca)
        pasta_termo = os.path.join(PASTA_DOWNLOADS, nome_pasta)
        if not os.path.exists(pasta_termo):
            os.makedirs(pasta_termo)

        nome_arquivo = gerar_nome_arquivo(termo_busca, indice_unico)
        caminho_completo = os.path.join(pasta_termo, nome_arquivo)
        caminho_relativo = f"/static/mapas_salvos/{nome_pasta}/{nome_arquivo}"

        # Se já existe, reutiliza
        if os.path.exists(caminho_completo):
            return caminho_relativo

        resposta = requests.get(url_remota, headers=HEADERS, timeout=5)
        if resposta.status_code == 200:
            with open(caminho_completo, "wb") as f:
                f.write(resposta.content)
            print(f"💾 Imagem salva: {caminho_relativo}")
            return caminho_relativo

    except Exception as e:
        print(f"Erro ao salvar imagem {url_remota}: {e}")

    return None  # Falha no download


def buscar_mapas_backend(termo_busca, offset=0):
    """
    Busca imagens usando a biblioteca duckduckgo_search (API de imagens),
    baixa as imagens para o servidor e retorna os caminhos locais.
    """
    if DDGS is None:
        print("Erro: instale duckduckgo-search com: pip install duckduckgo-search")
        return []

    query = f"mapa mental {termo_busca}"
    print(f"🦆 Busca DuckDuckGo: {query} (offset={offset})")

    resultados = []
    limit = 10
    # Buscamos offset + limit para poder fatiar [offset : offset+limit]
    max_results = offset + limit

    try:
        with DDGS() as ddgs:
            # images() retorna lista de dicts: title, image, thumbnail, url, height, width, source
            imagens = list(
                ddgs.images(
                    keywords=query,
                    region="wt-wt",
                    safesearch="moderate",
                    max_results=max_results,
                )
            )
        subset = imagens[offset : offset + limit]

        for i, item in enumerate(subset):
            try:
                link_imagem_remota = item.get("image")
                if not link_imagem_remota:
                    continue
                titulo = item.get("title") or query
                link_site = item.get("url") or link_imagem_remota

                id_arquivo = offset + i
                caminho_local = salvar_imagem_localmente(
                    link_imagem_remota, termo_busca, id_arquivo
                )
                imagem_final = caminho_local if caminho_local else link_imagem_remota
                fonte_tipo = "Servidor Local" if caminho_local else "Web (Falha Download)"

                resultados.append(
                    {
                        "titulo": titulo,
                        "link": link_site,
                        "imagem": imagem_final,
                        "fonte": fonte_tipo,
                        "descricao_original": f"Arquivo: MAPA MENTAL SOBRE {termo_busca.upper()}",
                    }
                )
            except Exception as e:
                print(f"Erro ao processar resultado DuckDuckGo: {e}")
                continue

    except Exception as e:
        print(f"Erro na busca DuckDuckGo: {e}")

    return resultados


# --- ROTAS ---
@app.route("/")
def home():
    """Serve the React app from dist/index.html"""
    return send_from_directory("dist", "index.html")


@app.route("/buscar", methods=["POST"])
def buscar():
    dados = request.get_json()
    termo = dados.get("termo")
    pagina = dados.get("pagina", 1)

    if not termo or not str(termo).strip():
        return jsonify({"erro": "Campo 'termo' é obrigatório."}), 400

    # Cada "página" nossa pula de 10 em 10 resultados na API do DuckDuckGo
    offset = (int(pagina) - 1) * 10

    resultados = buscar_mapas_backend(termo, offset)

    return jsonify(resultados)


@app.route("/baixar_imagem")
def baixar_imagem():
    """
    Se a imagem for local (/static/...), serve o arquivo local.
    Se for remota, faz o proxy para o usuário baixar.
    """
    img_url = request.args.get("url")
    if not img_url:
        return "URL vazia", 400

    # Se for uma imagem já salva no nosso servidor
    if img_url.startswith("/static/"):
        caminho_disco = img_url.lstrip("/")
        if not os.path.exists(caminho_disco):
            return "Arquivo local não encontrado", 404
        return send_file(caminho_disco, as_attachment=True)

    # Se for externa (fallback)
    try:
        resp = requests.get(img_url, headers=HEADERS, timeout=10)
        return send_file(
            io.BytesIO(resp.content),
            mimetype=resp.headers.get("Content-Type", "image/jpeg"),
            as_attachment=True,
            download_name="mapa_mental.jpg",
        )
    except Exception:
        return "Erro download", 500


@app.route("/<path:path>")
def serve_static(path):
    """Serve static assets or fallback to index.html for SPA routing"""
    full_path = os.path.join("dist", path)
    if os.path.isfile(full_path):
        return send_from_directory("dist", path)
    # Fallback to index.html for client-side routing
    return send_from_directory("dist", "index.html")


if __name__ == "__main__":
    print("🚀 Servidor DuckDuckGo rodando!")
    print(f"📂 As imagens serão salvas em: {os.path.abspath(PASTA_DOWNLOADS)}")
    app.run(debug=True)


