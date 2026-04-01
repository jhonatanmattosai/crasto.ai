import re

path = r'c:\Users\jm881\OneDrive\CRASTO.AI\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

original_len = len(content)

# 1. ADD PRECONNECTS at very top of <head>
preconnects = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link rel="preconnect" href="https://cdn.tailwindcss.com">\n'
    '<link rel="dns-prefetch" href="https://code.iconify.design">\n'
    '<link rel="dns-prefetch" href="https://www.googletagmanager.com">\n'
    '<link rel="dns-prefetch" href="https://cdn.jsdelivr.net">\n'
)
content = content.replace(
    '<meta charset="utf-8" />\n',
    '<meta charset="utf-8" />\n' + preconnects
)

# 2. DEFER unicornStudio vendor script
content = content.replace(
    '<script src="static/vendor/unicornStudio_f86b9c4abf24.js"></script>',
    '<script src="static/vendor/unicornStudio_f86b9c4abf24.js" defer></script>'
)

# Fix inline UnicornStudio loader in body to wait for deferred script
old_loader = (
    '!function () { if (!window.UnicornStudio) { window.UnicornStudio = { isInitialized: !1 }; var i = document.createElement("script"); i.src = "https://cdn.jsdelivr.net/gh/hiunicornstudio/unicornstudio.js@v2.1.0-1/dist/unicornStudio.umd.js"; i.onload = function () { if (document.readyState === "loading") { document.addEventListener("DOMContentLoaded", function () { UnicornStudio.init(); window.UnicornStudio.isInitialized = !0 }) } else { UnicornStudio.init(); window.UnicornStudio.isInitialized = !0 } }; (document.head || document.body).appendChild(i) } else if (!window.UnicornStudio.isInitialized && window.UnicornStudio.init) { UnicornStudio.init(); window.UnicornStudio.isInitialized = !0 } }();'
)
new_loader = (
    '(function(){\n'
    '    function initUS(){\n'
    '        if(window.UnicornStudio&&!window.UnicornStudio.isInitialized&&window.UnicornStudio.init){\n'
    '            UnicornStudio.init();window.UnicornStudio.isInitialized=true;\n'
    '        }\n'
    '    }\n'
    '    window.addEventListener("load",initUS);\n'
    '})();'
)
content = content.replace(old_loader, new_loader)

# Fix second UnicornStudio init call
old_init2 = (
    '<script>\n'
    '                        if (window.UnicornStudio) {\n'
    '                            window.UnicornStudio.init();\n'
    '                        }\n'
    '                    </script>'
)
new_init2 = (
    '<script>\n'
    '                        window.addEventListener("load",function(){\n'
    '                            if(window.UnicornStudio&&!window.UnicornStudio.isInitialized){\n'
    '                                UnicornStudio.init();window.UnicornStudio.isInitialized=true;\n'
    '                            }\n'
    '                        });\n'
    '                    </script>'
)
content = content.replace(old_init2, new_init2)

# 3. DEFER Iconify
content = content.replace(
    '<script src="https://code.iconify.design/iconify-icon/2.1.0/iconify-icon.min.js"></script>',
    '<script src="https://code.iconify.design/iconify-icon/2.1.0/iconify-icon.min.js" defer></script>'
)

# 4. ASYNC LOAD Instrument Serif (non-critical decorative font)
old_serif = (
    '    <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap"\n'
    '        id="all-fonts-link-font-instrument-serif" rel="stylesheet" />'
)
new_serif = (
    '    <link rel="preload" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap"'
    ' as="style" onload="this.rel=\'stylesheet\'" id="all-fonts-link-font-instrument-serif">\n'
    '    <noscript><link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet"></noscript>'
)
content = content.replace(old_serif, new_serif)

# 5. ADD IMAGE ATTRIBUTES
content = content.replace(
    '<img src="static/img/crasto-logo-icon.png" alt="CRASTO.AI" class="h-6 md:h-8 w-auto">',
    '<img src="static/img/crasto-logo-icon.png" alt="CRASTO.AI" class="h-6 md:h-8 w-auto" width="32" height="32" fetchpriority="high">'
)
content = content.replace(
    '<img src="static/img/crasto-logo-icon.png" alt="Crasto.AI" class="h-8 w-auto">',
    '<img src="static/img/crasto-logo-icon.png" alt="Crasto.AI" class="h-8 w-auto" width="32" height="32" loading="lazy">'
)

# 6. CLEAN UP scroll-fix style block - remove harmful overrides
old_scroll_fix_start = '    <style data-scroll-fix="true">'
old_scroll_fix_end = '    </style>\n    <!-- Iconify for icons -->'

start_idx = content.find(old_scroll_fix_start)
end_idx = content.find(old_scroll_fix_end)

if start_idx != -1 and end_idx != -1:
    new_styles = '''    <style>
        /* Base layout */
        html, body { overflow-x: hidden; height: auto; min-height: 100%; }
        .main-content { overflow: visible; height: auto; }
        /* Prevent widow words */
        h1, h2, h3, h4 { text-wrap: balance; }
        /* Fixed header */
        #site-header { transition: background-color 0.4s ease, backdrop-filter 0.4s ease, border-color 0.4s ease, box-shadow 0.4s ease; }
        #site-header.scrolled {
            background-color: rgba(2, 4, 10, 0.75);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
            box-shadow: 0 4px 32px rgba(0, 0, 0, 0.4);
        }
    </style>
    <!-- Iconify for icons -->'''
    content = content[:start_idx] + new_styles + content[end_idx + len(old_scroll_fix_end):]

# 7. REMOVE disabled-font-classes meta (Aura artifact)
content = re.sub(
    r'\s*<meta\s+content="font-roboto,font-montserrat[^"]*"\s+name="disabled-font-classes"\s*/>\s*',
    '\n',
    content
)

# 8. REMOVE duplicate .invisible style (Aura artifact)
content = content.replace(
    '    <style>\n        .invisible {\n            visibility: hidden !important;\n        }\n    </style>\n',
    ''
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

new_len = len(content)
print(f"Original: {original_len:,} chars")
print(f"New:      {new_len:,} chars")
print(f"Saved:    {original_len - new_len:,} chars ({(original_len-new_len)/original_len*100:.1f}%)")
print()

checks = {
    'preconnect fonts.googleapis': 'rel="preconnect" href="https://fonts.googleapis.com"' in content,
    'preconnect fonts.gstatic crossorigin': 'rel="preconnect" href="https://fonts.gstatic.com" crossorigin' in content,
    'dns-prefetch iconify': 'dns-prefetch" href="https://code.iconify.design"' in content,
    'unicornStudio deferred': 'unicornStudio_f86b9c4abf24.js" defer' in content,
    'iconify deferred': 'iconify-icon.min.js" defer' in content,
    'instrument serif async': 'rel="preload"' in content and 'Instrument+Serif' in content,
    'header logo fetchpriority': 'fetchpriority="high"' in content,
    'footer logo lazy': 'loading="lazy"' in content,
    'no harmful opacity override': '.opacity-0,\n        [class*="opacity-0"] {\n            opacity: 1 !important' not in content,
    'no harmful translate override': '.translate-y-full' not in content,
    'no disabled-font-classes': 'disabled-font-classes' not in content,
    'site-header styles kept': '#site-header.scrolled' in content,
    'h1-h4 text-wrap kept': 'text-wrap: balance' in content,
}
all_ok = True
for k, v in checks.items():
    print(f"  {'OK' if v else 'FAIL'} {k}")
    if not v: all_ok = False
print()
print('ALL CHECKS PASSED' if all_ok else 'SOME CHECKS FAILED')
