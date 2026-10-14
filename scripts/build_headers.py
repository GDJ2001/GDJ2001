"""Build the desktop and mobile SVG header with a shared animated IDE scene."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DEFS = '''<defs>
  <linearGradient id="background" x2="1" y2="1"><stop stop-color="#081321"/><stop offset="1" stop-color="#101e35"/></linearGradient>
  <linearGradient id="accent"><stop stop-color="#62edcf"/><stop offset="1" stop-color="#79adff"/></linearGradient>
  <linearGradient id="glass" x2="0.8" y2="1"><stop stop-color="#233a54"/><stop offset="1" stop-color="#122339"/></linearGradient>
  <radialGradient id="glow"><stop stop-color="#327d96" stop-opacity=".25"/><stop offset="1" stop-color="#327d96" stop-opacity="0"/></radialGradient>
  <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".8" fill="#81a5ca" opacity=".11"/></pattern>
  <filter id="shadow" x="-30%" y="-35%" width="170%" height="190%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#020911" flood-opacity=".65"/></filter>
  <clipPath id="line1"><rect class="reveal line1" x="75" y="88" width="240" height="17"/></clipPath>
  <clipPath id="line2"><rect class="reveal line2" x="75" y="111" width="240" height="17"/></clipPath>
  <clipPath id="line3"><rect class="reveal line3" x="75" y="134" width="240" height="17"/></clipPath>
  <clipPath id="line4"><rect class="reveal line4" x="75" y="157" width="240" height="17"/></clipPath>
</defs>
<style>
  .reveal{animation-duration:12s;animation-iteration-count:infinite;animation-timing-function:steps(25,end)}
  .line1{animation-name:type1}.line2{animation-name:type2}.line3{animation-name:type3}.line4{animation-name:type4}
  @keyframes type1{0%,3%{width:0}18%,94%{width:240px}100%{width:0}}
  @keyframes type2{0%,15%{width:0}30%,94%{width:240px}100%{width:0}}
  @keyframes type3{0%,27%{width:0}42%,94%{width:240px}100%{width:0}}
  @keyframes type4{0%,39%{width:0}54%,94%{width:240px}100%{width:0}}
  .progress{animation:build 12s ease-in-out infinite;transform-origin:0 0}
  @keyframes build{0%,43%{width:0}68%,94%{width:207px}100%{width:0}}
  .success{animation:success 12s ease-in-out infinite}
  @keyframes success{0%,62%{opacity:0;transform:translateY(4px)}70%,94%{opacity:1;transform:translateY(0)}100%{opacity:0}}
  .building{opacity:0;animation:building 12s ease-in-out infinite}
  @keyframes building{0%,5%{opacity:0}10%,58%{opacity:1}65%,100%{opacity:0}}
  .preview{animation:float 6s ease-in-out infinite}
  @keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
  .bars{animation:bars 12s ease-in-out infinite;transform-origin:282px 207px}
  @keyframes bars{0%,50%{transform:scaleY(.15);opacity:.35}70%,94%{transform:scaleY(1);opacity:1}100%{transform:scaleY(.15);opacity:.35}}
  .flow{stroke-dasharray:5 11;animation:flow 2s linear infinite}
  @keyframes flow{to{stroke-dashoffset:-32}}
  .status{animation:pulse 3s ease-in-out infinite}
  @keyframes pulse{50%{opacity:.5}}
  @media(prefers-reduced-motion:reduce){.reveal,.progress,.success,.building,.preview,.bars,.flow,.status{animation:none}.building{opacity:0}}
</style>'''

SCENE = '''
  <g fill="none" stroke="#345d76" stroke-width="1.4">
    <path d="M299 190v47q0 18-18 18h-33"/>
    <path class="flow" d="M299 190v47q0 18-18 18h-33" stroke="#62edcf"/>
  </g>
  <g filter="url(#shadow)">
    <rect x="0" y="6" width="344" height="213" rx="13" fill="#0b1526" stroke="#39536e"/>
    <path d="M13 6h318q13 0 13 13v22H0V19Q0 6 13 6" fill="#1b2b40"/>
    <circle cx="17" cy="24" r="3.5" fill="#f18e98"/>
    <circle cx="30" cy="24" r="3.5" fill="#f2cb82"/>
    <circle cx="43" cy="24" r="3.5" fill="#69dab5"/>
    <text x="178" y="28" text-anchor="middle" fill="#a4bdd5" font-family="Consolas,monospace" font-size="10">workspace / app.ts</text>
    <path d="M0 41h344M55 41v177" stroke="#283d55"/>
    <g fill="#506b87"><rect x="14" y="61" width="25" height="4" rx="2"/><rect x="20" y="77" width="21" height="4" rx="2"/><rect x="20" y="93" width="16" height="4" rx="2"/><rect x="20" y="109" width="23" height="4" rx="2"/><rect x="14" y="139" width="25" height="4" rx="2"/><rect x="20" y="155" width="19" height="4" rx="2"/></g>
    <path d="m10 61-3 2 3 2m0 74-3 2 3 2" stroke="#8ba9c5" fill="none"/>
    <rect x="55" y="41" width="87" height="28" fill="#162b40"/>
    <rect x="55" y="41" width="87" height="2" fill="#62edcf"/>
    <text x="69" y="59" fill="#79adff" font-family="Consolas,monospace" font-size="10">TS</text>
    <text x="89" y="59" fill="#d5e2ef" font-family="Consolas,monospace" font-size="10">app.ts</text>
    <text x="159" y="59" fill="#708ba5" font-family="Consolas,monospace" font-size="10">api.ts</text>
    <g font-family="Consolas,monospace" font-size="10" fill="#49617a"><text x="62" y="101">1</text><text x="62" y="124">2</text><text x="62" y="147">3</text><text x="62" y="170">4</text><text x="62" y="193">5</text></g>
    <g font-family="Consolas,monospace" font-size="11.5" fill="#d5e2ef">
      <text x="79" y="101" clip-path="url(#line1)"><tspan fill="#bba6ff">async function</tspan> <tspan fill="#79adff">build</tspan>() {</text>
      <text x="79" y="124" clip-path="url(#line2)">  <tspan fill="#bba6ff">const</tspan> app = <tspan fill="#79adff">createApp</tspan>();</text>
      <text x="79" y="147" clip-path="url(#line3)">  <tspan fill="#bba6ff">await</tspan> app.<tspan fill="#62edcf">connect</tspan>();</text>
      <text x="79" y="170" clip-path="url(#line4)">  <tspan fill="#bba6ff">return</tspan> app.<tspan fill="#62edcf">start</tspan>();</text>
      <text x="79" y="193">}</text>
    </g>
    <circle cx="326" cy="56" r="3" fill="#62edcf" class="status"/>
  </g>
  <g class="preview">
    <g filter="url(#shadow)">
      <rect x="245" y="121" width="119" height="114" rx="12" fill="url(#glass)" stroke="#547996"/>
      <path d="M245 148h119" stroke="#47627b"/>
      <circle cx="258" cy="135" r="3" fill="#62edcf"/>
      <text x="270" y="139" fill="#d5e2ef" font-family="Segoe UI,Arial,sans-serif" font-size="9" letter-spacing="1">LIVE PREVIEW</text>
      <rect x="257" y="159" width="45" height="5" rx="2.5" fill="#91afc9"/>
      <rect x="257" y="171" width="30" height="3" rx="1.5" fill="#54718b"/>
      <path d="M257 208h95" stroke="#54718b"/>
      <g class="bars"><rect x="263" y="189" width="12" height="18" rx="3" fill="#7aa9ff"/><rect x="284" y="178" width="12" height="29" rx="3" fill="#8f9bff"/><rect x="305" y="184" width="12" height="23" rx="3" fill="#73ccd9"/><rect x="326" y="169" width="12" height="38" rx="3" fill="#62edcf"/></g>
      <rect x="257" y="220" width="47" height="3" rx="1.5" fill="#54718b"/>
      <rect x="310" y="220" width="25" height="3" rx="1.5" fill="#54718b"/>
    </g>
  </g>
  <g filter="url(#shadow)">
    <rect x="-12" y="234" width="250" height="67" rx="10" fill="#0a1925" stroke="#34536c"/>
    <text x="3" y="255" font-family="Consolas,monospace" font-size="11" fill="#d5e2ef"><tspan fill="#62edcf">$</tspan> npm run build</text>
    <rect x="4" y="263" width="207" height="3" rx="1.5" fill="#263a54"/>
    <rect class="progress" x="4" y="263" width="207" height="3" rx="1.5" fill="url(#accent)"/>
    <text class="building" x="4" y="285" font-family="Consolas,monospace" font-size="10" fill="#8da9c0">compiling application...</text>
    <g class="success"><path d="m5 281 3 3 6-7" stroke="#62edcf" stroke-width="1.5" fill="none" stroke-linecap="round"/><text x="22" y="285" font-family="Consolas,monospace" font-size="10" fill="#62edcf">build complete · ready to ship</text></g>
  </g>
'''


def build(mobile=False):
    width, height = (480, 620) if mobile else (960, 420)
    if mobile:
        intro = '''<path d="M30 35h28" stroke="#62edcf" stroke-width="3"/>
        <text x="70" y="40" fill="#9db6cc" font-size="11" letter-spacing="2">FULL-STACK DEVELOPER</text>
        <text x="30" y="104" fill="#f0f6fc" font-size="38" font-weight="700" letter-spacing="-1.2">Geethika Dilshan</text>
        <text x="30" y="148" fill="url(#accent)" font-size="38" font-weight="700" letter-spacing="-1.2">Jayarathna</text>
        <text x="30" y="187" fill="#d5e2ef" font-size="19">Thoughtful interfaces.</text>
        <text x="30" y="214" fill="#d5e2ef" font-size="19">Dependable systems.</text>'''
        footer = '''<path d="M30 550h420" stroke="#283d55"/>
        <circle cx="35" cy="574" r="4" fill="#62edcf" class="status"/>
        <text x="48" y="579" fill="#b5c6d8" font-size="12">OPEN TO DEVELOPER OPPORTUNITIES</text>
        <text x="30" y="604" fill="#8da9c0" font-size="11">SRI LANKA · GDJ2001</text>'''
        transform = 'translate(62 246) scale(.96)'
    else:
        intro = '''<path d="M40 41h34" stroke="#62edcf" stroke-width="3"/>
        <text x="87" y="46" fill="#9db6cc" font-size="12" letter-spacing="2.4">FULL-STACK DEVELOPER</text>
        <text x="40" y="132" fill="#f0f6fc" font-size="48" font-weight="700" letter-spacing="-1.8">Geethika Dilshan</text>
        <text x="40" y="190" fill="url(#accent)" font-size="48" font-weight="700" letter-spacing="-1.8">Jayarathna</text>
        <text x="42" y="247" fill="#d5e2ef" font-size="22">Thoughtful interfaces.</text>
        <text x="42" y="279" fill="#d5e2ef" font-size="22">Dependable systems.</text>
        <text x="42" y="319" fill="#7f9bb7" font-size="12" letter-spacing="2">WEB / BACKEND / AI</text>'''
        footer = '''<path d="M40 357H920" stroke="#283d55"/>
        <circle cx="45" cy="390" r="4" fill="#62edcf" class="status"/>
        <text x="58" y="395" fill="#b5c6d8" font-size="12">OPEN TO DEVELOPER OPPORTUNITIES</text>
        <text x="920" y="395" text-anchor="end" fill="#8da9c0" font-size="12">SRI LANKA · GDJ2001</text>'''
        transform = 'translate(553 38)'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">Geethika Dilshan Jayarathna — Full-stack developer</title>
  <desc id="desc">Software engineering illustration: code is typed in an editor, an application preview comes to life, and a terminal completes a build. Thoughtful interfaces. Dependable systems. Sri Lanka.</desc>
  {DEFS}
  <rect width="{width}" height="{height}" rx="20" fill="url(#background)"/>
  <rect width="{width}" height="{height}" rx="20" fill="url(#dots)"/>
  <ellipse cx="{width * .8}" cy="{height * .4}" rx="300" ry="240" fill="url(#glow)"/>
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="19" fill="none" stroke="#2a4058"/>
  <g font-family="Segoe UI,Arial,sans-serif">{intro}{footer}</g>
  <g transform="{transform}">{SCENE}</g>
</svg>\n'''


if __name__ == '__main__':
    for mobile in (False, True):
        name = 'header-mobile.svg' if mobile else 'header.svg'
        (ROOT / 'assets' / name).write_text(build(mobile), encoding='utf-8')
    print('Built desktop and mobile headers with the animated editor scene.')
