# GUIA DO ZERO — Site + Blog Ygor Soares

Este guia recomeça do zero, de forma simples e à prova de erro. Leia na ordem.

> **O que mudou em relação à tentativa anterior (e por que falhou):**
> O Netlify tentou rodar o `python3 build-blog.py` e quebrou, porque os arquivos não estavam na estrutura certa e o Netlify não roda Python de forma confiável. Agora o site é **100% estático**: o Netlify só serve os arquivos, sem rodar nada. As páginas dos artigos já vêm prontas. Isso elimina a causa do erro.

---

## PARTE 1 — Organizar os arquivos no GitHub (a parte que deu errado antes)

### A regra de ouro
Todos os arquivos devem ficar na **raiz** do repositório — NÃO dentro de uma pasta `blog-setup` ou `site-completo`. A estrutura final no GitHub tem que ser exatamente esta:

```
index.html                  ← página principal
blog.html
politica-de-privacidade.html
netlify.toml                ← NOVO: impede o erro de build
sitemap.xml
robots.txt
build-blog.py               ← fica aqui, mas o Netlify NÃO usa
favicon.ico
favicon-32.png
favicon-180.png
og-image.png
admin/
   ├── index.html
   └── config.yml
artigos/
   ├── 2025-06-02-demissao-sem-justa-causa-direitos.md
   ├── 2025-06-02-demissao-sem-justa-causa-direitos.html
   ├── (todos os outros .md e .html)
   └── index.json
```

### Como subir do jeito certo

**Passo 1 — Limpe o repositório atual.**
No seu repositório no GitHub, apague tudo o que está lá hoje (já que ficou bagunçado). Para apagar uma pasta/arquivo: abra o item, clique no ícone de lixeira, e confirme com "Commit changes".
*Dica:* se for mais fácil, você pode até apagar o repositório inteiro (Settings → Danger Zone → Delete) e criar um novo limpo. Se fizer isso, será preciso reconectar no Netlify (Parte 2).

**Passo 2 — Baixe a pasta `site-completo` que eu preparei.**
Ela já está com TUDO na estrutura certa. Descompacte no seu computador.

**Passo 3 — Suba o CONTEÚDO da pasta (não a pasta em si).**
Aqui está o pulo do gato que faltou antes: você deve subir o que está **dentro** de `site-completo`, e não a pasta `site-completo` inteira.

1. No repositório, clique em **Add file → Upload files**.
2. Abra a pasta `site-completo` no seu computador.
3. Selecione TODOS os itens de dentro dela (os arquivos + as pastas `admin` e `artigos`) e arraste para a área de upload do GitHub.
4. O GitHub mantém as subpastas automaticamente.
5. Escreva uma descrição qualquer ("site completo") e clique em **Commit changes**.

**Passo 4 — Confira.**
A página inicial do repositório deve mostrar `index.html`, `blog.html`, `admin`, `artigos` etc. logo de cara — sem nenhuma pasta `site-completo` ou `blog-setup` no caminho. Se aparecer, está errado: entre na pasta, e será preciso mover os arquivos para a raiz (ou refazer o upload do jeito do Passo 3).

---

## PARTE 2 — Conectar ao Netlify (corrigindo o build)

Se o Netlify já está conectado ao repositório, só precisamos corrigir a configuração que causou o erro.

1. No Netlify, abra seu site → **Site configuration → Build & deploy → Build settings**.
2. Em **Build command**: APAGUE o `python3 build-blog.py` e deixe **em branco**.
3. Em **Publish directory**: coloque um ponto `.` (ou deixe em branco).
4. Salve.

> O arquivo `netlify.toml` que incluí já força essa configuração sozinho. Mas limpar o campo na interface evita conflito.

5. Vá em **Deploys → Trigger deploy → Deploy site** para republicar.
6. Aguarde aparecer **"Published"** em verde.

Agora teste:
- `seusite.netlify.app` → deve abrir o site
- `seusite.netlify.app/blog.html` → deve abrir o blog com os 5 artigos
- `seusite.netlify.app/admin/` → deve abrir a tela de login do painel (com a barra no fim!)

Se as três abrirem, a base está pronta. Só falta o login do painel (Parte 3).

---

## PARTE 3 — Entrar no painel de artigos (método simples: Token)

Existem duas formas de logar no painel. Vamos pela mais simples para você começar hoje. O login de "um clique" (OAuth) pode ser configurado depois.

### Antes: edite o config.yml com seu repositório
No GitHub, abra `admin/config.yml`, clique no lápis (editar) e troque a linha:
```
repo: SEU_USUARIO/SEU_REPOSITORIO
```
pelo seu usuário e o nome real do repositório. Exemplo: se seu usuário é `ygorsoares` e o repositório `ygorsoares-site`, fica `repo: ygorsoares/ygorsoares-site`. Salve (Commit changes).

### Gerar o token de acesso (3 minutos)
1. No GitHub, clique na sua **foto (canto superior direito) → Settings**.
2. Desça a barra lateral até o final → **Developer settings**.
3. Clique em **Personal access tokens → Fine-grained tokens**.
4. Clique em **Generate new token**.
5. Preencha:
   - **Token name:** `painel blog` (qualquer nome)
   - **Expiration:** 90 dias (você renova depois — o GitHub não permite token sem validade)
   - **Repository access:** escolha **Only select repositories** e selecione o repositório do site
   - **Permissions:** expanda **Repository permissions**, procure **Contents** e marque **Read and write**. (A permissão *Metadata: Read* é marcada sozinha junto. Só isso basta.)
6. Clique em **Generate token**.
7. **COPIE o token agora** — o GitHub mostra ele só uma vez. Guarde num lugar seguro.

### Entrar no painel
1. Acesse `seusite.netlify.app/admin/`
2. Na tela de login, escolha **"Sign in with Token"** (entrar com token).
3. Cole o token e confirme.
4. Pronto! Você verá a lista "Artigos do Blog" com os 5 textos já lá.

> O token expira em 90 dias. Quando isso acontecer, é só repetir "Gerar o token" e logar de novo. Coloque um lembrete no celular.

---

## PARTE 4 — O dia a dia (publicar um artigo)

1. Acesse `seusite.netlify.app/admin/` e entre com o token.
2. **Artigos do Blog → New Artigo**.
3. Preencha título, resumo, data, conteúdo (escreve como no Word).
4. Clique em **Publish → Publish now**.
5. Em 1-2 minutos o artigo está no ar e aparece no blog.

> O Sveltia salva o `.md` E gera o `.html` no repositório automaticamente. O Netlify republica sozinho. Você não roda script nenhum.

---

## (OPCIONAL) Login de um clique no futuro

Quando quiser trocar o token pelo botão "Sign in with GitHub" (sem renovar a cada 90 dias), me avise. Como você usa Netlify, o caminho é registrar um "OAuth App" no GitHub e vinculá-lo ao Netlify em Access & Security. É um pouco mais de configuração, mas faço o passo a passo com você. Para começar, o token é suficiente.

---

## (OPCIONAL) Rodar o build-blog.py no seu computador

Você NÃO precisa disso para o site funcionar. Serve apenas se um dia quiser regenerar todas as páginas de uma vez no seu PC (requer Python instalado). Rodando `python3 build-blog.py` dentro da pasta do site, ele regenera os `.html` dos artigos, o `index.json` e o `sitemap.xml`. Para o uso normal pelo painel, ignore este passo.
