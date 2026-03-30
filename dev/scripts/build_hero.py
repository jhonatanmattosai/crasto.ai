import os
import re

outfile = r"c:\Users\jm881\OneDrive\CRASTO.AI\index.html"
ent_idx = r"c:\Users\jm881\OneDrive\CRASTO.AI\Assets\Templates\enterprise-ai-58.aura.build\index.html"

with open(ent_idx, 'r', encoding='utf-8') as f:
    html = f.read()

# Grab the head
head_end = html.find('</head>') + 7
head = html[:head_end]

# Fix asset paths in head
head = head.replace('assets/', '../Templates/enterprise-ai-58.aura.build/assets/')

# Add our custom title
head = re.sub(r'<title>.*?</title>', '<title>CRASTO.AI — Agentes de Inteligência Artificial</title>', head)

# Grab the opening body tag
body_start = html.find('<body')
body_tag_end = html.find('>', body_start) + 1
body_tag = html[body_start:body_tag_end]

# Grab the NEW HERO CONTAINER block
# It starts at <!-- NEW HERO CONTAINER --> or <div class="flex flex-col overflow-hidden min-h-[850px]
hero_start = html.find('<div class="flex flex-col overflow-hidden min-h-[850px]')
# Hero ends right before <!-- Main Content -->
hero_end = html.find('<!-- Main Content -->')

hero_html = html[hero_start:hero_end]

# Now, we perform string replacements to inject our COPY while maintaining EXACT classes!

# 1. Navbar
hero_html = hero_html.replace('NODEX', 'CRASTO.AI')
hero_html = hero_html.replace('>Platform<', '>Por que agentes de IA<')
hero_html = hero_html.replace('>Solutions<', '>Planos<')
hero_html = hero_html.replace('>Enterprise<', '>Como começar<')
hero_html = hero_html.replace('>Developers<', '>FAQ<')
hero_html = hero_html.replace('Contact Sales', 'Falar com especialista &rarr;')

# 2. Hero Badge
hero_html = hero_html.replace('Enterprise AI Workforce • Now Live', 'Operando em até 24h · Suporte humano em IA')

# 3. Hero Title
# Original: "The Operating System<br/>\n<span class="opacity-60">for Your AI Workforce</span>"
hero_html = hero_html.replace(
    'The Operating System<br/>\n<span class="opacity-60">for Your AI Workforce</span>', 
    'Clientes sem resposta,<br/>\n<span class="opacity-60">vendas escapando e operação travada?</span>'
)

# 4. Hero Paragraph
# Original: "NODEX deploys autonomous AI agents that execute complex workflows, optimize decisions, and scale across your enterprise infrastructure."
hero_html = hero_html.replace(
    'NODEX deploys autonomous AI agents that execute complex workflows, optimize decisions, and scale across your\n      enterprise infrastructure.',
    'Sua equipe não dá conta. Clientes desistem e vão pro concorrente. Nossos agentes de IA assumem o comercial, a gestão e o executivo para sua empresa parar de perder dinheiro.'
)

# 5. Hero Button
hero_html = hero_html.replace('DEPLOY YOUR AGENTS', 'QUERO MEU AGENTE AGORA &rarr;')

# We need to add the CTA secundario and the Social Proof numbers below the button.
# Let's locate the end of the button block.
btn_end_str = '</button>\n</div>\n</div>\n</div>'
btn_end_pos = hero_html.find(btn_end_str)

html_add = """
<div class="mt-8 mb-4 [animation:animationIn_0.8s_ease-out_0.6s_both]">
    <a href="#como-comecar" class="px-8 py-3 text-white/50 hover:text-white transition-colors text-sm font-medium tracking-widest uppercase border border-white/10 rounded-full hover:bg-white/5 backdrop-blur-md">
        Ver como funciona
    </a>
</div>

<div class="mt-12 w-full max-w-3xl border-t border-white/10 pt-10 [animation:animationIn_0.8s_ease-out_0.7s_both]">
    <div class="flex flex-wrap justify-between items-center gap-8 px-4">
        <div class="flex flex-col items-center">
            <span class="text-4xl lg:text-5xl font-light tracking-tighter text-white font-manrope">24h</span>
            <span class="text-[10px] uppercase font-bold tracking-[0.2em] text-cyan-400/80 mt-2 text-center">Primeiro agente no ar</span>
        </div>
        <div class="flex flex-col items-center">
            <span class="text-4xl lg:text-5xl font-light tracking-tighter text-white font-manrope">3</span>
            <span class="text-[10px] uppercase font-bold tracking-[0.2em] text-cyan-400/80 mt-2 text-center">Perfis de agentes</span>
        </div>
        <div class="flex flex-col items-center">
            <span class="text-4xl lg:text-5xl font-light tracking-tighter text-white font-manrope">100%</span>
            <span class="text-[10px] uppercase font-bold tracking-[0.2em] text-cyan-400/80 mt-2 text-center">Assistido por humanos</span>
        </div>
    </div>
    
    <div class="mt-12 flex flex-wrap justify-center gap-3 opacity-60">
        <span class="px-3 py-1 rounded-full border border-white/20 bg-white/5 text-[10px] text-white uppercase tracking-wider font-semibold">Saúde</span>
        <span class="px-3 py-1 rounded-full border border-white/20 bg-white/5 text-[10px] text-white uppercase tracking-wider font-semibold">Moda</span>
        <span class="px-3 py-1 rounded-full border border-white/20 bg-white/5 text-[10px] text-white uppercase tracking-wider font-semibold">Têxtil</span>
        <span class="px-3 py-1 rounded-full border border-white/20 bg-white/5 text-[10px] text-white uppercase tracking-wider font-semibold">Agronegócio</span>
        <span class="px-3 py-1 rounded-full border border-white/20 bg-white/5 text-[10px] text-white uppercase tracking-wider font-semibold">Financeiro</span>
        <span class="px-3 py-1 rounded-full border border-white/20 bg-white/5 text-[10px] text-white uppercase tracking-wider font-semibold">Tecnologia</span>
        <span class="px-3 py-1 rounded-full border border-white/20 bg-white/5 text-[10px] text-white uppercase tracking-wider font-semibold">Alimentício</span>
        <span class="px-3 py-1 rounded-full border border-white/20 bg-white/5 text-[10px] text-white uppercase tracking-wider font-semibold">Indústria</span>
    </div>
</div>
"""

# Insert the new elements right after the button
hero_html = hero_html[:btn_end_pos] + '</button>\n</div>\n' + html_add + '\n</div>\n</div>'

final_source = head + body_tag + "\n" + hero_html + "\n</body></html>"

with open(outfile, 'w', encoding='utf-8') as f:
    f.write(final_source)

print("Page replaced successfully!")
