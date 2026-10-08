#!/usr/bin/env python3
"""Profil README görsellerini üretir (assets/*.svg).

Metinleri değiştirmek için bu dosyadaki PROFILE / PROJECTS sözlüklerini
düzenleyip `python3 scripts/build_svgs.py` çalıştırman yeterli.
Avatarı hero.svg içine gömmek için: python3 scripts/build_svgs.py --avatar avatar.png
"""
import base64, html, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"

# ---------- Tasarım belirteçleri ----------
BG = "#0b1018"
BG2 = "#0f1622"
LINE = "#1f2a3a"
TEXT = "#e6edf3"
MUTED = "#8b98a9"
CYAN = "#38bdf8"
VIOLET = "#a78bfa"
PINK = "#f472b6"
GREEN = "#4ade80"
SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Inter', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', 'JetBrains Mono', Consolas, 'DejaVu Sans Mono', monospace"

PROFILE = {
    "handle": "@begumhandan",
    "name": "Begüm Handan Demir",
    "role": "Yazılım Mühendisliği · Samsun Üniversitesi · 4. sınıf",
    "tags": ["AI & LLM Güvenliği", "Full-Stack", "Mobil", "Otonom Sistemler"],
    "monogram": "BH",
}

TERMINAL = [
    ("cmd", "whoami"),
    ("out", "Begüm Handan Demir — yazılım mühendisi adayı, AI + full-stack"),
    ("cmd", "cat now.txt"),
    ("out", "Context-Shield AI  ████████████████████  [gizli]"),
    ("cmd", "ls experience/"),
    ("hl",  "MilSOFT/   ROBUST/   Tanyeli-SİHA/   TÜBİTAK-2209A/"),
    ("cmd", "echo $FOCUS"),
    ("out", "LLM güvenliği · görüntü işleme (YOLO) · React / React Native"),
]

# accent: kart rengi; link: README'de tıklanınca gidilecek repo
PROJECTS = [
    # redacted: kartta yalnızca isim görünür; açıklama SVG kaynağına hiç yazılmaz
    {"slug": "context-shield", "repo": "context-shield-ai", "title": "Context-Shield AI",
     "desc": [], "chips": [], "status": "[REDACTED]", "accent": CYAN, "private": True, "redacted": True},
    {"slug": "health-agent", "repo": "NAIM-BEGUM-Health-Agent", "title": "B.E.G.U.M. Health Agent",
     "desc": ["Şikayetleri analiz edip hastayı doğru", "tıbbi bölüme yönlendiren mobil asistan."],
     "chips": ["React Native", "Expo", "Serper API"], "status": "NAIM Challenge · v1.7", "accent": PINK},
    {"slug": "smartviz", "repo": "SmartVizAI", "title": "SmartVizAI",
     "desc": ["CSV/Excel yükle, veriyi tanısın ve en uygun", "grafikleri otomatik önersin. Tamamen client-side."],
     "chips": ["React", "Vite", "Vega-Lite"], "status": "veri görselleştirme", "accent": VIOLET},
    {"slug": "academic-ai", "repo": "Academic-AI-Suite", "title": "Academic AI Suite",
     "desc": ["Akademik yazımı yöneten AI editör: çeviri,", "özetleme, kaynakça ve üslup kontrolü."],
     "chips": ["React", "TypeScript", "Gemini"], "status": "prototip", "accent": CYAN},
    {"slug": "dentist", "repo": "DentistAppointmentSystem", "title": "Diş Kliniği Randevu Sistemi",
     "desc": ["Hasta, doktor ve sekreter panelli; çakışma", "kontrollü randevu ve klinik yönetimi."],
     "chips": ["Spring Boot", "MongoDB", "React"], "status": "full-stack · JWT", "accent": GREEN},
    {"slug": "prediabet", "repo": "Prediabet", "title": "Prediabet",
     "desc": ["Prediyabet riski için takip uygulaması: risk", "testi, adımsayar, kalori ve şeker takibi."],
     "chips": ["React Native", "Expo", "TypeScript"], "status": "mobil · APK yayında", "accent": VIOLET},
]

e = lambda s: html.escape(s, quote=True)

STYLE_BASE = f"""
  .sans {{ font-family: {SANS}; }}
  .mono {{ font-family: {MONO}; }}
  .orb  {{ animation: drift 14s ease-in-out infinite alternate; transform-box: fill-box; transform-origin: center; }}
  .orb2 {{ animation-duration: 18s; animation-direction: alternate-reverse; }}
  @keyframes drift {{ from {{ transform: translate(-30px, -10px) scale(1); }} to {{ transform: translate(40px, 14px) scale(1.15); }} }}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
"""


def frame(w, h, inner, extra_style="", defs="", orbs=True, r=18):
    orb_svg = ""
    if orbs:
        orb_svg = f"""
  <g clip-path="url(#clip)">
    <circle class="orb" cx="{w*0.82:.0f}" cy="{h*0.15:.0f}" r="{h*0.55:.0f}" fill="url(#gViolet)"/>
    <circle class="orb orb2" cx="{w*0.12:.0f}" cy="{h*0.95:.0f}" r="{h*0.5:.0f}" fill="url(#gCyan)"/>
  </g>"""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">
<style>{STYLE_BASE}{extra_style}</style>
<defs>
  <linearGradient id="border" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{CYAN}" stop-opacity=".55"/>
    <stop offset=".5" stop-color="{VIOLET}" stop-opacity=".25"/>
    <stop offset="1" stop-color="{PINK}" stop-opacity=".45"/>
  </linearGradient>
  <radialGradient id="gViolet"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".28"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
  <radialGradient id="gCyan"><stop offset="0" stop-color="{CYAN}" stop-opacity=".22"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
  <clipPath id="clip"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{r}"/></clipPath>
  {defs}
</defs>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{r}" fill="{BG}"/>
{orb_svg}
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{r}" fill="none" stroke="url(#border)" stroke-width="1.5"/>
{inner}
</svg>
"""


def chip(x, y, label, color, size=12, pad=12):
    w = int(len(label) * size * 0.62 + pad * 2)
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{size+14}" rx="{(size+14)/2}" fill="{color}" fill-opacity=".08" stroke="{color}" stroke-opacity=".45"/>'
            f'<text x="{x + w/2}" y="{y + size + 3}" text-anchor="middle" class="sans" font-size="{size}" font-weight="600" fill="{TEXT}">{e(label)}</text>'), w


def hero(avatar_uri=None):
    w, h = 840, 250
    cx, cy, rr = 120, 125, 64
    avatar = ""
    if avatar_uri:
        avatar = f'<image href="{avatar_uri}" x="{cx-rr}" y="{cy-rr}" width="{rr*2}" height="{rr*2}" clip-path="url(#av)" preserveAspectRatio="xMidYMid slice"/>'
    chips, x = [], 220
    for i, t in enumerate(PROFILE["tags"]):
        c, cw = chip(x, 170, t, [CYAN, VIOLET, PINK, GREEN][i % 4], 12)
        chips.append(c); x += cw + 10
    inner = f"""
  <circle cx="{cx}" cy="{cy}" r="{rr+7}" fill="none" stroke="url(#ring)" stroke-width="2.5" class="spin"/>
  <circle cx="{cx}" cy="{cy}" r="{rr}" fill="{BG2}"/>
  <text x="{cx}" y="{cy+13}" text-anchor="middle" class="sans" font-size="38" font-weight="800" fill="url(#ring)">{PROFILE['monogram']}</text>
  {avatar}<!--AVATAR-->
  <circle cx="{cx+46}" cy="{cy+46}" r="9" fill="{GREEN}" stroke="{BG}" stroke-width="4"/>
  <text x="220" y="78" class="mono" font-size="14" fill="{CYAN}">{e(PROFILE['handle'])}</text>
  <text x="218" y="124" class="sans" font-size="40" font-weight="800" fill="{TEXT}" letter-spacing="-.5">{e(PROFILE['name'])}</text>
  <text x="220" y="152" class="sans" font-size="15" fill="{MUTED}">{e(PROFILE['role'])}</text>
  {''.join(chips)}
"""
    defs = f"""<linearGradient id="ring" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
  <clipPath id="av"><circle cx="{cx}" cy="{cy}" r="{rr}"/></clipPath>"""
    style = f".spin {{ animation: spin 12s linear infinite; transform-origin: {cx}px {cy}px; }} @keyframes spin {{ to {{ transform: rotate(360deg); }} }}"
    return frame(w, h, inner, style, defs)


def terminal():
    w = 840
    lh, top = 27, 74
    h = top + lh * len(TERMINAL) + 34
    rows, styles = [], []
    t = 0.3
    for i, (kind, text) in enumerate(TERMINAL):
        y = top + i * lh
        if kind == "cmd":
            body = (f'<tspan fill="{GREEN}">begum@shield</tspan><tspan fill="{MUTED}">:</tspan>'
                    f'<tspan fill="{CYAN}">~</tspan><tspan fill="{MUTED}">$ </tspan><tspan fill="{TEXT}">{e(text)}</tspan>')
            t += 0.55
        else:
            col = VIOLET if kind == "hl" else "#c3cfdd"
            body = f'<tspan fill="{col}">{e(text)}</tspan>'
            t += 0.25
        rows.append(f'<text x="34" y="{y}" class="mono ln l{i}" font-size="14.5" xml:space="preserve">{body}</text>')
        styles.append(f".l{i} {{ animation-delay: {t:.2f}s; }}")
    cy = top + len(TERMINAL) * lh
    t += 0.4
    rows.append(f'<text x="34" y="{cy}" class="mono ln l{len(TERMINAL)}" font-size="14.5"><tspan fill="{GREEN}">begum@shield</tspan><tspan fill="{MUTED}">:</tspan><tspan fill="{CYAN}">~</tspan><tspan fill="{MUTED}">$ </tspan></text>'
                f'<rect class="cursor ln l{len(TERMINAL)}" x="158" y="{cy-13}" width="9" height="17" fill="{CYAN}"/>')
    styles.append(f".l{len(TERMINAL)} {{ animation-delay: {t:.2f}s; }}")
    style = (".ln { opacity: 0; animation: show .35s ease-out forwards; }"
             "@keyframes show { from { opacity: 0; transform: translateX(-6px); } to { opacity: 1; transform: none; } }"
             ".cursor { animation: show .3s forwards, blink 1.1s steps(1) infinite; }"
             "@keyframes blink { 50% { fill-opacity: 0; } }"
             "@media (prefers-reduced-motion: reduce) { .ln { opacity: 1; } }" + "".join(styles))
    inner = f"""
  <rect x="1" y="1" width="{w-2}" height="40" rx="18" fill="{BG2}" clip-path="url(#clip)"/>
  <rect x="1" y="30" width="{w-2}" height="11" fill="{BG2}" clip-path="url(#clip)"/>
  <line x1="1" y1="41" x2="{w-1}" y2="41" stroke="{LINE}"/>
  <circle cx="26" cy="21" r="6" fill="#ff5f57"/><circle cx="46" cy="21" r="6" fill="#febc2e"/><circle cx="66" cy="21" r="6" fill="#28c840"/>
  <text x="{w/2}" y="26" text-anchor="middle" class="mono" font-size="12.5" fill="{MUTED}">begum@shield: ~ — zsh</text>
  {''.join(rows)}
"""
    return frame(w, h, inner, style, orbs=True)


def section(title, cmd, right=""):
    w, h = 840, 58
    inner = f"""
  <text x="26" y="36" class="mono" font-size="15" font-weight="700" fill="{CYAN}" letter-spacing="2">{e(title)}</text>
  <text x="{26 + len(title)*11.5 + 22:.0f}" y="36" class="mono" font-size="13.5" fill="{MUTED}">{e(cmd)}</text>
  <text x="{w-26}" y="36" text-anchor="end" class="mono" font-size="13" fill="{MUTED}">{e(right)}</text>
"""
    return frame(w, h, inner, orbs=False, r=14)


def card(p):
    w, h = 412, 196
    a = p["accent"]
    chips, x = [], 22
    for c in p["chips"]:
        s, cw = chip(x, 128, c, a, 11, 10)
        chips.append(s); x += cw + 8
    desc = "".join(f'<text x="22" y="{86 + i*21}" class="sans" font-size="13.5" fill="#b7c3d1">{e(line)}</text>' for i, line in enumerate(p["desc"]))
    if p.get("redacted"):
        bars = [(22, 74, 300), (22, 95, 220), (22, 130, 64), (94, 130, 92), (194, 130, 74)]
        desc = "".join(f'<rect x="{x}" y="{y}" width="{bw}" height="{16 if y < 120 else 22}" rx="{3 if y < 120 else 11}" fill="#1c2636"/>' for x, y, bw in bars)
        desc += f'<rect x="22" y="74" width="300" height="16" rx="3" fill="url(#scan)" class="scan"/>'
    inner = f"""
  <circle cx="26" cy="27" r="4" fill="{a}"/>
  <text x="38" y="31" class="mono" font-size="12" fill="{MUTED}">{e(p['repo'])}</text>
  <text x="{w-22}" y="31" text-anchor="end" class="mono" font-size="{11 if p.get('private') else 15}" fill="{MUTED}">{'🔒 private' if p.get('private') else '↗'}</text>
  <text x="22" y="60" class="sans" font-size="20" font-weight="700" fill="{TEXT}">{e(p['title'])}</text>
  {desc}
  {''.join(chips)}
  <line x1="22" y1="168" x2="{w-22}" y2="168" stroke="{LINE}"/>
  <text x="22" y="186" class="mono" font-size="11.5" fill="{a}">● <tspan fill="{MUTED}">{e(p['status'])}</tspan></text>
"""
    defs = (f'<linearGradient id="scan" x1="0" x2="1"><stop offset="0" stop-color="{a}" stop-opacity="0"/><stop offset=".5" stop-color="{a}" stop-opacity=".25"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></linearGradient>' if p.get("redacted") else "")
    defs += f'<radialGradient id="glow"><stop offset="0" stop-color="{a}" stop-opacity=".22"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></radialGradient>'
    style = ".scan { animation: scan 3.2s ease-in-out infinite; } @keyframes scan { 0%,100% { opacity: .2; } 50% { opacity: 1; } }" if p.get("redacted") else ""
    body = frame(w, h, inner, style, defs=defs, orbs=False, r=16)
    # kartın köşesine kendi renginde hafif bir ışık
    return body.replace(f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="16" fill="none"',
                        f'<g clip-path="url(#clip)"><circle class="orb" cx="{w-40}" cy="20" r="120" fill="url(#glow)"/></g>\n<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="16" fill="none"', 1)


def main():
    avatar_uri = None
    if "--avatar" in sys.argv:
        data = Path(sys.argv[sys.argv.index("--avatar") + 1]).read_bytes()
        mime = "image/png" if data[:4] == b"\x89PNG" else "image/jpeg"
        avatar_uri = f"data:{mime};base64," + base64.b64encode(data).decode()
    OUT.mkdir(exist_ok=True); (OUT / "cards").mkdir(exist_ok=True)
    (OUT / "hero.svg").write_text(hero(avatar_uri), encoding="utf-8")
    (OUT / "terminal.svg").write_text(terminal(), encoding="utf-8")
    (OUT / "sec-projects.svg").write_text(section("PROJECTS.LIST", "./projects.sh --featured", "6 öne çıkan"), encoding="utf-8")
    (OUT / "sec-stack.svg").write_text(section("TECH.STACK", "cat stack.yml"), encoding="utf-8")
    (OUT / "sec-signal.svg").write_text(section("PROFILE.SIGNAL", "gh stats --live"), encoding="utf-8")
    (OUT / "sec-activity.svg").write_text(section("CONTRIBUTION.LOG", "git log --graph", "her gün güncellenir"), encoding="utf-8")
    (OUT / "sec-contact.svg").write_text(section("CONTACT", "ping begum"), encoding="utf-8")
    for p in PROJECTS:
        (OUT / "cards" / f"{p['slug']}.svg").write_text(card(p), encoding="utf-8")
    print("ok", "avatar gömüldü" if avatar_uri else "avatar yok (monogram)")


if __name__ == "__main__":
    main()
