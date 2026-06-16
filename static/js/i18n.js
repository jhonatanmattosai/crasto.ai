const I18N = {
  defaultLang: 'pt',
  supportedLangs: {
    'pt': 'PT',
    'en': 'EN',
    'es': 'ES',
    'ja': 'JP',
    'zh-cn': 'CN',
    'zh-hk': 'HK',
    'de': 'DE'
  },
  translations: {},
  
  async init() {
    console.log("i18n: Inicializando sistema de tradução...");
    
    // Bind dropdown toggles
    this.bindEvents();

    let lang = localStorage.getItem('crasto_lang');
    if (!lang || !this.supportedLangs[lang]) {
      const browserLang = navigator.language.toLowerCase();
      if (this.supportedLangs[browserLang]) {
        lang = browserLang;
      } else if (browserLang.startsWith('es')) {
        lang = 'es';
      } else if (browserLang.startsWith('en')) {
        lang = 'en';
      } else if (browserLang.startsWith('de')) {
        lang = 'de';
      } else if (browserLang.startsWith('ja')) {
        lang = 'ja';
      } else if (browserLang === 'zh-cn' || browserLang === 'zh-hans') {
        lang = 'zh-cn';
      } else if (browserLang.startsWith('zh')) {
        lang = 'zh-hk';
      } else {
        lang = this.defaultLang;
      }
    }
    
    await this.applyLang(lang);
  },

  bindEvents() {
    document.querySelectorAll("[data-lang]").forEach((el) => {
      el.addEventListener("click", async (e) => {
        e.preventDefault();
        const lang = el.getAttribute("data-lang");
        await this.applyLang(lang);
        
        // Fechar menu
        const menu = document.getElementById("lang-menu");
        if (menu) {
          menu.classList.add("opacity-0", "invisible", "translate-y-2");
        }
        const btn = document.getElementById("lang-btn");
        if (btn) {
          btn.classList.remove("bg-white", "text-black");
        }
      });
    });
  },

  async fetchTranslations(lang) {
    if (this.translations[lang]) return this.translations[lang];
    
    try {
      const response = await fetch(`static/locales/${lang}.json?v=${new Date().getTime()}`); // Cache busting
      if (!response.ok) throw new Error('Translation not found');
      const data = await response.json();
      this.translations[lang] = data;
      return data;
    } catch (e) {
      console.error(`Failed to load translation for ${lang}`, e);
      return null;
    }
  },

  async applyLang(lang) {
    if (!this.supportedLangs[lang]) lang = this.defaultLang;
    
    // Fetch target language, fallback to PT if fail
    let t = await this.fetchTranslations(lang);
    if (!t) t = await this.fetchTranslations(this.defaultLang);
    
    // Fetch PT as fallback for missing keys
    let fallback = lang !== this.defaultLang ? await this.fetchTranslations(this.defaultLang) : t;

    if (!t) return;

    // Apply translations
    document.querySelectorAll("[data-i18n]").forEach((el) => {
      const key = el.getAttribute("data-i18n");
      if (t[key] !== undefined) {
        el.innerHTML = t[key];
      } else if (fallback && fallback[key] !== undefined) {
        el.innerHTML = fallback[key];
      }
    });

    // Update Language Label in Header
    const label = document.getElementById("lang-label");
    if (label) {
      label.textContent = this.supportedLangs[lang] || "PT";
    }

    // Update active state in dropdown
    document.querySelectorAll("[data-lang]").forEach((el) => {
      const isSelected = el.getAttribute("data-lang") === lang;
      el.style.background = isSelected ? "rgba(255,255,255,0.08)" : "";
    });

    // Update HTML lang attribute for SEO
    document.documentElement.lang = lang === 'pt' ? 'pt-BR' : lang;

    // Save preference
    try {
      localStorage.setItem("crasto_lang", lang);
    } catch (e) {
      console.error("Local storage error", e);
    }
  }
};

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", () => I18N.init());
} else {
  I18N.init();
}
