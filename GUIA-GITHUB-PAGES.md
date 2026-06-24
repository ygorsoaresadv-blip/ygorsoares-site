# GUIA — Migrar do Netlify para o GitHub Pages

Vamos publicar o site direto pelo GitHub Pages, de graça e sem o problema dos créditos do Netlify. Seus arquivos já estão no GitHub, então a migração é rápida.

> **A ORDEM IMPORTA.** Faça os passos exatamente nesta sequência. Se subir os arquivos antes de ativar o Pages, a automação não roda.

---

## PASSO 1 — Ativar o GitHub Pages (FAZER ANTES DE TUDO)

1. No seu repositório no GitHub, clique em **Settings** (no menu do topo do repositório).
2. Na barra lateral esquerda, em "Code and automation", clique em **Pages**.
3. Em **"Build and deployment"**, no campo **"Source"**, troque de "Deploy from a branch" para **"GitHub Actions"**.
4. Só isso nesta tela. Não precisa salvar botão nenhum — a seleção já vale.

---

## PASSO 2 — Subir os arquivos novos e atualizados

Agora suba o conteúdo do pacote `migracao-github-pages` que eu preparei. Ele tem os arquivos com as URLs já corrigidas + a automação.

Atenção a uma pasta especial: o pacote contém uma pasta chamada **`.github`** (com ponto na frente) que tem a automação dentro. Ela é essencial. Pelo navegador, a forma mais segura de criar essa pasta é usar o endereço de upload direto:

### 2a. Subir a automação (a pasta .github)
1. No navegador, vá para: `github.com/ygorsoaresadv-blip/ygorsoares-site/upload/main/.github/workflows`
   (repare no `.github/workflows` no final — isso cria as pastas certas)
2. Arraste o arquivo `deploy.yml` (que está em `.github/workflows/` do pacote).
3. Commit changes.

### 2b. Subir os arquivos da raiz
1. Vá para: `github.com/ygorsoaresadv-blip/ygorsoares-site/upload/main`
2. Arraste estes arquivos: `index.html`, `blog.html`, `politica-de-privacidade.html`, `build-blog.py`, `robots.txt`, `sitemap.xml`, `runtime.txt`, e o arquivo `.nojekyll`.
   - **Observação sobre o `.nojekyll`:** é um arquivo vazio, sem extensão. Se o seu computador esconder ou bloquear ele, me avise — dá para criar direto pelo GitHub (te explico).
3. Commit changes.

### 2c. Atualizar os artigos
1. Vá para: `github.com/ygorsoaresadv-blip/ygorsoares-site/upload/main/artigos`
2. Arraste os 5 arquivos `.html` + o `index.json` (da pasta `artigos/` do pacote).
3. Commit changes.

### 2d. Atualizar o admin
1. Vá para: `github.com/ygorsoaresadv-blip/ygorsoares-site/upload/main/admin`
2. Arraste o `index.html` e o `config.yml` da pasta `admin/` do pacote.
3. Commit changes.

---

## PASSO 3 — Acompanhar a primeira publicação

1. No repositório, clique na aba **Actions** (no topo).
2. Você verá uma execução chamada "Publicar site" rodando (bolinha amarela girando).
3. Aguarde ela ficar **verde** (✓). Leva 1-2 minutos.
4. Se ficar **vermelha** (✗), clique nela, depois no job, e me copie a parte do erro — eu ajusto.

---

## PASSO 4 — Ver o site no ar

Quando a automação ficar verde, seu site estará em:

**https://ygorsoaresadv-blip.github.io/ygorsoares-site/**

Abra esse endereço (no computador e no celular) e confira:
- A página principal carrega com o visual certo?
- O menu hambúrguer funciona no celular?
- O blog (`/blog.html`) mostra os artigos?
- Um artigo abre certinho?

---

## PASSO 5 — Apontar o painel Sveltia para o novo endereço

O painel de artigos (`/admin/`) continua funcionando igual, com o mesmo login por token. O endereço agora é:

**https://ygorsoaresadv-blip.github.io/ygorsoares-site/admin/**

Salve esse link. O fluxo de publicar artigos é o mesmo de antes: escreve no painel, publica, e a automação do GitHub gera a página e atualiza o site sozinha — sem custo, sem créditos.

---

## DEPOIS: pode desligar o Netlify

Com o GitHub Pages funcionando, o Netlify não é mais necessário. Você pode simplesmente deixá-lo de lado (ele não cobra nada no plano grátis) ou, se quiser, excluir o site lá depois. Não tenha pressa — confirme primeiro que o GitHub Pages está 100% no ar.

---

## Sobre o endereço e o domínio próprio (futuro)

O endereço `ygorsoaresadv-blip.github.io/ygorsoares-site` é o gratuito. Quando você registrar um domínio próprio (ex: `ygorsoares.adv.br`), dá para apontá-lo para o GitHub Pages, e aí o endereço fica limpo, sem o `/ygorsoares-site`. Quando chegar essa hora, me chame que faço o passo a passo.
