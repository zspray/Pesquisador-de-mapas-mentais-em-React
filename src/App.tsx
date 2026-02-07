import { useState, useRef, useEffect } from 'react'

interface Resultado {
  titulo: string
  link: string
  imagem: string
  fonte: string
}

function App() {
  const [termo, setTermo] = useState('')
  const [pagina, setPagina] = useState(1)
  const [resultados, setResultados] = useState<Resultado[]>([])
  const [buscando, setBuscando] = useState(false)
  const [status, setStatus] = useState<{ msg: string; type?: string }>({
    msg: '',
  })
  const [termoAtual, setTermoAtual] = useState('')
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    inputRef.current?.focus()
  }, [])

  const escapeHtml = (str: string) => {
    const div = document.createElement('div')
    div.textContent = str
    return div.innerHTML
  }

  const setStatusMsg = (msg: string, type?: string) => {
    setStatus({ msg, type })
  }

  const buscar = async (pageNum: number = 1) => {
    const searchTerm = (inputRef.current?.value || '').trim()
    if (!searchTerm && pageNum === 1) {
      setStatusMsg('Digite um termo para buscar.', 'error')
      inputRef.current?.focus()
      return
    }

    setTermoAtual(searchTerm || termoAtual)
    setPagina(pageNum)
    setBuscando(true)
    setStatusMsg(
      'Consultando a API e baixando imagens para o servidor (isso pode levar alguns segundos)...',
      ''
    )

    try {
      const resp = await fetch('/buscar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          termo: searchTerm || termoAtual,
          pagina: pageNum,
        }),
      })

      if (!resp.ok) {
        const txt = await resp.text().catch(() => '')
        throw new Error(`Erro ${resp.status} ao buscar. ${txt}`)
      }

      const data: Resultado[] = await resp.json()
      setResultados(data)
      setStatusMsg(
        `Ok! Mostrando resultados para "${searchTerm || termoAtual}".`,
        'ok'
      )
    } catch (err) {
      console.error(err)
      setResultados([])
      setStatusMsg(
        String(err instanceof Error ? err.message : 'Falha ao buscar.'),
        'error'
      )
    } finally {
      setBuscando(false)
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setPagina(1)
    buscar(1)
  }

  const handleClear = () => {
    setPagina(1)
    setTermo('')
    setTermoAtual('')
    setResultados([])
    setStatusMsg('', '')
    if (inputRef.current) {
      inputRef.current.value = ''
      inputRef.current.focus()
    }
  }

  const handleAnterior = async () => {
    if (buscando || pagina <= 1) return
    const newPage = pagina - 1
    await buscar(newPage)
  }

  const handleProxima = async () => {
    if (buscando) return
    const newPage = pagina + 1
    await buscar(newPage)
  }

  return (
    <div className="wrap">
      <header>
        <div className="title">
          <h1>Maps4Study</h1>
          <p>
            Pesquise mapas mentais e baixe com um clique. A API salva imagens em{' '}
            <code>/static/mapas_salvos</code>.
          </p>
        </div>
        <div className="pill" title="Rotas da API">
          <span>API:</span>
          <code>POST /buscar</code>
          <code>GET /baixar_imagem</code>
        </div>
      </header>

      <section className="card" aria-label="Busca">
        <form className="search" onSubmit={handleSubmit} autoComplete="off">
          <div className="field" title="Digite o tema (ex: bhaskara, sistema nervoso...)">
            <span aria-hidden="true">🔎</span>
            <input
              ref={inputRef}
              id="termo"
              name="termo"
              placeholder="Digite um tema… (ex: bhaskara, guerra fria, sistema nervoso)"
              disabled={buscando}
              onChange={(e) => setTermo(e.target.value)}
              value={termo}
            />
          </div>
          <button
            className="btn primary"
            id="btnBuscar"
            type="submit"
            disabled={buscando}
          >
            <span aria-hidden="true">⚡</span>
            {buscando ? 'Buscando...' : 'Buscar'}
          </button>
          <button
            className="btn"
            id="btnLimpar"
            type="button"
            title="Limpa resultados e volta para página 1"
            onClick={handleClear}
            disabled={buscando}
          >
            Limpar
          </button>
          <div className="meta">
            <span>
              Página: <code id="paginaAtual">{pagina}</code>
            </span>
            <span>
              Itens: <code id="qtdAtual">{resultados.length}</code>
            </span>
          </div>
        </form>

        {status.msg && (
          <div
            className={`status show ${status.type || ''}`}
            role="status"
            aria-live="polite"
          >
            {status.msg}
          </div>
        )}

        <div className="content">
          <div className="grid" id="grid">
            {resultados.length === 0 && !buscando && termoAtual && (
              <div style={{ gridColumn: '1 / -1', padding: '10px', color: 'rgba(255,255,255,.75)' }}>
                Nenhum resultado. Tente outro termo.
              </div>
            )}
            {resultados.map((r, idx) => {
              const urlBaixar =
                '/baixar_imagem?url=' + encodeURIComponent(r.imagem)
              console.log(`Imagem ${idx}:`, r.imagem) // Debug
              return (
                <div key={idx} className="item">
                  <div className="thumb">
                    {r.imagem && (
                      <img
                        src={r.imagem}
                        alt={r.titulo}
                        loading="lazy"
                        onError={(e) => {
                          console.error(`Erro ao carregar imagem: ${r.imagem}`, e)
                          ;(e.target as HTMLImageElement).src = '/placeholder.png'
                        }}
                      />
                    )}
                    {r.fonte && <span className="badge">{r.fonte}</span>}
                  </div>
                  <div className="body">
                    <p className="h" title={r.titulo}>
                      {r.titulo}
                    </p>
                    <div className="sub">
                      <span>{termoAtual}</span>
                      <span>Pág. {pagina}</span>
                    </div>
                    <div className="actions">
                      <a
                        className="btn"
                        href={r.link}
                        target="_blank"
                        rel="noreferrer"
                      >
                        Abrir fonte
                      </a>
                      <a className="btn primary" href={urlBaixar}>
                        Baixar
                      </a>
                    </div>
                  </div>
                </div>
              )
            })}
          </div>

          {resultados.length > 0 && (
            <div className="pager">
              <div className="left">
                <button
                  className="btn"
                  id="btnAnterior"
                  type="button"
                  onClick={handleAnterior}
                  disabled={buscando || pagina <= 1}
                >
                  ← Anterior
                </button>
                <button
                  className="btn"
                  id="btnProxima"
                  type="button"
                  onClick={handleProxima}
                  disabled={buscando}
                >
                  Próxima →
                </button>
              </div>
              <div className="right">
                <span id="pagerInfo">Página {pagina}</span>
              </div>
            </div>
          )}

          <div className="hint">
            Dica: aperte <span className="kbd">Enter</span> para buscar e{' '}
            <span className="kbd">Ctrl</span>+<span className="kbd">L</span> para
            focar a barra de endereço do navegador.
          </div>
        </div>
      </section>
    </div>
  )
}

export default App
