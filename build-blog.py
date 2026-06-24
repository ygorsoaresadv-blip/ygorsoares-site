#!/usr/bin/env python3
"""
build-blog.py — Converte os artigos .md (criados pelo Decap CMS) em paginas HTML.
Rode com:  python3 build-blog.py
Gera: artigos/<slug>.html  e  artigos/index.json (usado pela blog.html)
"""
import os, re, json, glob
from datetime import datetime

ARTIGOS_DIR = "artigos"

def parse_frontmatter(texto):
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', texto, re.DOTALL)
    if not m:
        return {}, texto
    fm_raw, body = m.group(1), m.group(2)
    fm = {}
    for line in fm_raw.split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, body

def md_to_html(md):
    """Conversor markdown simples e seguro para os recursos que usamos."""
    html, lines = [], md.split('\n')
    in_list = False
    for line in lines:
        s = line.rstrip()
        if re.match(r'^- ', s):
            if not in_list:
                html.append('<ul>'); in_list = True
            item = s[2:]
            item = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item)
            html.append(f'<li>{item}</li>')
            continue
        if in_list:
            html.append('</ul>'); in_list = False
        if s.startswith('### '):
            html.append(f'<h3>{s[4:]}</h3>')
        elif s.startswith('## '):
            html.append(f'<h2>{s[3:]}</h2>')
        elif s.startswith('# '):
            html.append(f'<h2>{s[2:]}</h2>')
        elif s.strip() == '':
            html.append('')
        else:
            p = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
            p = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', p)
            html.append(f'<p>{p}</p>')
    if in_list:
        html.append('</ul>')
    return '\n'.join(html)

PAGE_TEMPLATE = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{description}">
<meta name="keywords" content="{keyword}, direitos trabalhistas, advogado trabalhista">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://ygorsoares.netlify.app/artigos/{slug}.html">
<title>{title} | Dr. Ygor Soares</title>
<link rel="icon" type="image/x-icon" href="../favicon.ico">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="https://ygorsoares.netlify.app/og-image.png">
<meta property="og:url" content="https://ygorsoares.netlify.app/artigos/{slug}.html">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title}",
  "description": "{description}",
  "datePublished": "{date}",
  "author": {{ "@type": "Person", "name": "Ygor Soares" }},
  "publisher": {{ "@type": "LegalService", "name": "Ygor Soares Advocacia Trabalhista" }}
}}
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,400&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--verde-escuro:#0c4632;--verde-medio:#1f6b52;--verde-claro:#3f8f6e;--verde-profundo:#062c1f;--off-white:#f3f7f5;--texto-sec:#5a8a76;--cinza:#555555;--borda:rgba(31,107,82,0.25)}}
html{{scroll-behavior:smooth}}
body{{font-family:'Cormorant Garamond',serif;background:#fff;color:var(--verde-escuro);font-size:19px;line-height:1.8}}
header{{position:sticky;top:0;z-index:100;background:#fff;border-bottom:1px solid var(--borda);padding:0 5%}}
.header-inner{{display:flex;align-items:center;justify-content:space-between;height:72px;max-width:1100px;margin:0 auto}}
.logo-lockup{{display:flex;align-items:center;gap:16px;text-decoration:none}}
.logo-divider{{width:1px;height:36px;background:var(--verde-medio);opacity:0.5}}
.logo-text h1{{font-family:'Playfair Display',serif;font-size:15px;font-weight:500;letter-spacing:4px;color:var(--verde-escuro);text-transform:uppercase}}
.logo-text p{{font-size:10px;letter-spacing:3px;color:var(--texto-sec);text-transform:uppercase}}
nav a{{font-size:12px;letter-spacing:3px;text-transform:uppercase;color:var(--verde-escuro);text-decoration:none;margin-left:24px}}
.btn-nav{{border:1px solid var(--verde-medio);padding:8px 20px;font-size:12px;letter-spacing:3px;text-transform:uppercase;color:var(--verde-escuro);text-decoration:none}}
article{{max-width:720px;margin:0 auto;padding:64px 5% 40px}}
.back{{font-size:13px;letter-spacing:3px;text-transform:uppercase;color:var(--verde-medio);text-decoration:none;margin-bottom:32px;display:inline-block}}
.art-date{{font-size:13px;letter-spacing:2px;text-transform:uppercase;color:var(--texto-sec);margin-bottom:16px}}
article h1.art-title{{font-family:'Playfair Display',serif;font-size:clamp(28px,4vw,42px);font-weight:500;letter-spacing:1px;line-height:1.2;margin-bottom:32px}}
article h2{{font-family:'Playfair Display',serif;font-size:26px;font-weight:500;margin:40px 0 16px;letter-spacing:0.5px}}
article h3{{font-family:'Playfair Display',serif;font-size:21px;font-weight:500;margin:28px 0 12px}}
article p{{margin-bottom:20px;color:#3a4a44}}
article ul{{margin:0 0 20px 24px;color:#3a4a44}}
article li{{margin-bottom:10px}}
article a{{color:var(--verde-medio)}}
.art-divider{{height:1px;background:var(--verde-medio);opacity:0.3;margin:48px 0}}
.art-cta{{background:var(--verde-escuro);padding:40px;text-align:center;margin-top:48px}}
.art-cta h3{{font-family:'Playfair Display',serif;color:#fff;font-size:24px;margin-bottom:12px}}
.art-cta p{{color:rgba(255,255,255,0.7);margin-bottom:24px;font-size:17px}}
.art-cta a{{display:inline-block;border:1px solid rgba(255,255,255,0.5);padding:14px 36px;font-size:12px;letter-spacing:3px;text-transform:uppercase;color:#fff;text-decoration:none;transition:all 0.25s}}
.art-cta a:hover{{background:#fff;color:var(--verde-escuro)}}
.disclaimer{{font-size:14px;color:var(--texto-sec);font-style:italic;margin-top:32px;padding-top:20px;border-top:1px solid var(--borda)}}
footer{{background:var(--verde-profundo);padding:48px 5%;text-align:center;margin-top:0}}
footer p{{font-size:13px;color:rgba(255,255,255,0.4);margin:4px 0}}
footer a{{color:#6fb89a;text-decoration:none}}
</style>
</head>
<body>
<header>
  <div class="header-inner">
    <a class="logo-lockup" href="../index.html">
      <svg width="48" height="48" viewBox="0 0 48 48" fill="none"><circle cx="24" cy="24" r="22" stroke="#1f6b52" stroke-width="2"/><circle cx="24" cy="24" r="17" stroke="#1f6b52" stroke-width="0.75"/><text x="24" y="31" text-anchor="middle" font-family="'Playfair Display',Georgia,serif" font-size="17" font-weight="600" fill="#0c4632" letter-spacing="-1">YS</text></svg>
      <div class="logo-divider"></div>
      <div class="logo-text"><h1>Ygor Soares</h1><p>Advocacia Trabalhista</p></div>
    </a>
    <nav><a href="../blog.html">Blog</a><a class="btn-nav" href="../index.html#chat">Tire Dúvidas</a></nav>
  </div>
</header>
<article>
  <a class="back" href="../blog.html">← Voltar ao blog</a>
  <p class="art-date">{date_fmt}</p>
  <h1 class="art-title">{title}</h1>
  {body}
  <div class="art-cta">
    <h3>Tem dúvidas sobre o seu caso?</h3>
    <p>O Dr. Ygor Soares oferece orientação trabalhista gratuita. Atendimento digital para todo o Brasil.</p>
    <a href="../index.html#chat">Tirar Dúvida Gratuitamente</a>
  </div>
  <p class="disclaimer">Este artigo tem caráter informativo e não substitui a orientação jurídica individualizada. Cada caso deve ser analisado de forma específica.</p>
</article>
<footer>
  <p>© 2025 Ygor Soares · Advogado · OAB/SP XXX.XXX</p>
  <p><a href="../index.html">Início</a> · <a href="../blog.html">Blog</a> · <a href="../politica-de-privacidade.html">Política de Privacidade</a></p>
</footer>
</body>
</html>
'''

MESES = ['janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro']

def main():
    indice = []
    arquivos = glob.glob(os.path.join(ARTIGOS_DIR, "*.md"))
    print(f"Encontrados {len(arquivos)} artigo(s).")
    for caminho in arquivos:
        with open(caminho, encoding='utf-8') as f:
            fm, body_md = parse_frontmatter(f.read())
        slug = os.path.splitext(os.path.basename(caminho))[0]
        title = fm.get('title', 'Sem título')
        desc = fm.get('description', '')
        date = fm.get('date', '')[:10]
        keyword = fm.get('keyword', '')
        thumb = fm.get('thumbnail', '')
        try:
            d = datetime.strptime(date, '%Y-%m-%d')
            date_fmt = f"{d.day} de {MESES[d.month-1]} de {d.year}"
        except Exception:
            date_fmt = date
        body_html = md_to_html(body_md)
        page = PAGE_TEMPLATE.format(title=title, description=desc, keyword=keyword,
                                    slug=slug, date=date, date_fmt=date_fmt, body=body_html)
        out = os.path.join(ARTIGOS_DIR, slug + ".html")
        with open(out, 'w', encoding='utf-8') as f:
            f.write(page)
        print(f"  gerado: {out}")
        indice.append({"slug": slug, "title": title, "description": desc,
                        "date": date, "thumbnail": thumb})
    indice.sort(key=lambda x: x['date'], reverse=True)
    with open(os.path.join(ARTIGOS_DIR, "index.json"), 'w', encoding='utf-8') as f:
        json.dump(indice, f, ensure_ascii=False, indent=2)
    print(f"index.json atualizado com {len(indice)} artigo(s).")
    gerar_sitemap(indice)

SITE = "https://ygorsoares.netlify.app"

def gerar_sitemap(indice):
    """Gera o sitemap.xml incluindo paginas fixas + todos os artigos."""
    fixas = [
        (f"{SITE}/", "1.0", "weekly"),
        (f"{SITE}/#calculadora", "0.8", "monthly"),
        (f"{SITE}/#chat", "0.9", "monthly"),
        (f"{SITE}/blog.html", "0.9", "weekly"),
        (f"{SITE}/politica-de-privacidade.html", "0.5", "yearly"),
    ]
    linhas = ['<?xml version="1.0" encoding="UTF-8"?>',
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, pri, freq in fixas:
        linhas.append(f'  <url><loc>{loc}</loc><changefreq>{freq}</changefreq><priority>{pri}</priority></url>')
    for p in indice:
        linhas.append(f'  <url><loc>{SITE}/artigos/{p["slug"]}.html</loc><lastmod>{p["date"]}</lastmod><priority>0.7</priority></url>')
    linhas.append('</urlset>')
    # O sitemap fica na raiz do site (um nivel acima da pasta artigos)
    destino = os.path.join(os.path.dirname(os.path.abspath(ARTIGOS_DIR)), "sitemap.xml")
    with open("sitemap.xml", 'w', encoding='utf-8') as f:
        f.write('\n'.join(linhas))
    print(f"sitemap.xml regenerado com {len(indice)} artigo(s) + paginas fixas.")

if __name__ == "__main__":
    main()
