"""Regenerate the HTML pages in ../docs. Run: python3 tools/build.py"""
import re
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / 'docs'
SITE = 'https://suzzetteharriott.com'
EMAIL = 'contact@suzzetteharriott.com'
NAME = 'Dr. Suzzette A. Harriott'

NAV = [
    ('/', 'Home'),
    ('/about/', 'About'),
    ('/counselling/', 'Therapeutic Conflictology'),
    ('/reset/', 'RESET'),
]


def header(current):
    links = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ''
        links.append(f'<a href="{href}"{cur}>{label}</a>')
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/" aria-label="{NAME} home">
      <svg class="brand-mark" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="28" fill="none" stroke="#2c4a5e" stroke-width="2.5"/><path d="M22 38 a10 10 0 0 1 20 0z" fill="#c9a36a"/><line x1="12" y1="38" x2="52" y2="38" stroke="#2c4a5e" stroke-width="2.5" stroke-linecap="round"/><line x1="24" y1="44" x2="40" y2="44" stroke="#c9a36a" stroke-width="2.5" stroke-linecap="round"/><line x1="28" y1="49.5" x2="36" y2="49.5" stroke="#c9a36a" stroke-width="2.5" stroke-linecap="round"/></svg>
      <span class="brand-text"><span class="brand-name">Dr. Suzzette Harriott</span>
      <span class="brand-sub">PhD &middot; Therapeutic Conflictology</span></span>
    </a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav class="nav" id="site-nav" aria-label="Main">
      {"".join(links)}
      <a class="btn" href="/contact/">Contact</a>
    </nav>
  </div>
</header>'''


FOOTER = f'''<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <p class="footer-name">Dr. Suzzette A. Harriott, PhD</p>
        <p class="footer-slogan">Where conflict becomes clarity.</p>
        <p>Therapeutic Conflictology and RESET. In person in Kingston, Jamaica, and by secure video worldwide.</p>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
      <div>
        <h3>Explore</h3>
        <ul>
          <li><a href="/about/">About</a></li>
          <li><a href="/counselling/">Therapeutic Conflictology</a></li>
          <li><a href="/reset/">RESET</a></li>
          <li><a href="/contact/">Contact</a></li>
        </ul>
      </div>
      <div>
        <h3>Legal</h3>
        <ul>
          <li><a href="/privacy-policy/">Privacy Policy</a></li>
          <li><a href="/terms-of-service/">Terms of Service</a></li>
          <li><a href="/cookie-policy/">Cookie Policy</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span data-year>2026</span> Suzzette Harriott &amp; Associates. All rights reserved.</span>
      <span>Looking for Compass college readiness? Visit <a href="https://cescarib.com">cescarib.com</a></span>
    </div>
  </div>
</footer>
<script>
  (function () {{
    var t = document.querySelector('.menu-toggle');
    var n = document.getElementById('site-nav');
    if (t && n) {{
      t.addEventListener('click', function () {{
        var open = n.classList.toggle('open');
        t.setAttribute('aria-expanded', open ? 'true' : 'false');
      }});
    }}
    var y = document.querySelector('[data-year]');
    if (y) y.textContent = new Date().getFullYear();
  }})();
</script>'''


def page(path, title, description, current, body, extra_head=''):
    full_title = f'{title} | Dr. Suzzette Harriott' if title else 'Dr. Suzzette Harriott, PhD | Where conflict becomes clarity'
    url = SITE + path
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/img/og.jpg?v=2">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Dr. Suzzette Harriott, PhD. Where conflict becomes clarity.">
<meta property="og:site_name" content="Dr. Suzzette Harriott">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg?v=2" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png?v=2" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v=2">
<meta name="theme-color" content="#1f2e3a">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v=7">
{extra_head}</head>
<body>
{header(current)}
<main id="main">
{body}
</main>
{FOOTER}
</body>
</html>
'''
    target = OUT / path.strip('/') / 'index.html' if path != '/' else OUT / 'index.html'
    if path.endswith('.html'):
        target = OUT / path.strip('/')
    # Relative links, so pages work both on the preview address and on the real domain.
    depth = len(target.relative_to(OUT).parts) - 1
    prefix = '../' * depth if depth else './'
    if not path.endswith('404.html'):
        html = re.sub(r'(href|src|poster)="/(?!/)', lambda m: f'{m.group(1)}="{prefix}', html)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html)


def ticks(items):
    return '<ul class="ticks">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'


CTA = '''<section class="section bg-navy center">
  <div class="wrap narrow">
    <h2>A conversation is the right first step.</h2>
    <p class="lead">No commitment beyond a careful listen. Bring what is on your mind, even if you cannot name it yet.</p>
    <div class="btn-row" style="justify-content:center">
      <a class="btn btn-light" href="/contact/">Start the conversation</a>
    </div>
  </div>
</section>'''

# ---------------------------------------------------------------- Home
page('/', '', 'Where conflict becomes clarity. Therapeutic Conflictology with Dr. Suzzette A. Harriott, PhD, in person in Kingston, Jamaica, and by secure video worldwide.', '/', f'''
<section class="hero">
  <video class="hero-media" autoplay muted loop playsinline poster="/img/hero-poster.jpg" aria-hidden="true">
    <source src="/media/ocean.mp4" type="video/mp4">
  </video>
  <div class="wrap">
    <p class="eyebrow">Where conflict becomes clarity</p>
    <h1>Clarity for what<br>you are carrying.</h1>
    <p class="lead">Therapeutic Conflictology for people navigating conflict, transition and the quiet pressure of holding everything together. In person in Kingston, or by secure video wherever you are.</p>
    <div class="btn-row">
      <a class="btn btn-light" href="/contact/">Start the conversation</a>
      <a class="btn btn-ghost" href="/counselling/">How the work helps</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="center narrow" style="margin:0 auto 3rem">
      <p class="eyebrow">Two ways to work together</p>
      <h2>Considered care, rooted in the Caribbean.</h2>
      <p class="lead">Most of what weighs on us is conflict of some kind: with the people we love, with the roles we carry, or within ourselves. The work here is to understand that conflict and find a steadier way forward.</p>
    </div>
    <div class="grid grid-2">
      <article class="card">
        <div class="photo"><img src="/img/tc-hero.jpg" alt="A woman looking out over the sea at sunset" loading="lazy"></div>
        <div class="card-body">
          <p class="eyebrow">One-to-one</p>
          <h3>Therapeutic Conflictology</h3>
          <p>Conflict-informed, CBT-informed support for individuals, couples, parents and families. Clarity, emotional steadiness and practical next steps through transition and conflict.</p>
          <a class="btn" href="/counselling/">Explore Therapeutic Conflictology</a>
        </div>
      </article>
      <article class="card">
        <div class="photo"><img src="/img/reset-circle.jpg" alt="A group of adults embracing in a supportive circle" loading="lazy"></div>
        <div class="card-body">
          <p class="eyebrow">Small-group immersion</p>
          <h3>RESET</h3>
          <p>Cohort-based experiential training in emotional intelligence, relationships and intentional living, with Caribbean-informed facilitation. A separate programme; no other service is required.</p>
          <a class="btn" href="/reset/">Explore RESET</a>
        </div>
      </article>
    </div>
  </div>
</section>

<section class="section bg-sand">
  <div class="wrap">
    <div class="split">
      <div>
        <p class="eyebrow">Who comes here</p>
        <h2>You may be doing well on paper and still feel out of step inside.</h2>
        <p>Illustrative, not exhaustive. If your situation is not listed, you are still welcome.</p>
      </div>
      <div>
        {ticks([
            'A life transition, relocation, divorce, grief or burnout, and you want grounded support',
            'Anxiety, low mood or repeating patterns, and you want tools that fit real life',
            'Parenting stress, family conflict, or feeling overwhelmed while holding everyone else together',
            'Tension at work or in leadership that is following you home',
            'A strained relationship with food, eating or how you see your body',
            'You feel capable on paper but misaligned inside, and want clarity without being rushed',
        ])}
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="grid grid-3">
      <article class="card">
        <div class="photo"><img src="/img/individuals.jpg" alt="A woman reflecting at a table with a notebook" loading="lazy"></div>
        <div class="card-body"><h3>Individuals</h3><p>Clarity, alignment and the inner conflict beneath the stress.</p></div>
      </article>
      <article class="card">
        <div class="photo"><img src="/img/families.jpg" alt="Parents and their daughter sitting together and smiling" loading="lazy"></div>
        <div class="card-body"><h3>Couples &amp; families</h3><p>Steadier communication, healthier boundaries and shared decisions.</p></div>
      </article>
      <article class="card">
        <div class="photo"><img src="/img/tc-reflection.jpg" alt="A man sitting thoughtfully in a calm room" loading="lazy"></div>
        <div class="card-body"><h3>Professionals</h3><p>Support for the pressure you carry at work and the tension it brings home.</p></div>
      </article>
    </div>
  </div>
</section>

<section class="section bg-sand center">
  <div class="wrap narrow">
    <p class="eyebrow">About</p>
    <h2>Dr. Suzzette A. Harriott, PhD</h2>
    <p>A therapeutic conflictologist whose work brings together psychology, conflict resolution and human resources. Her doctorate is in Conflict Analysis and Resolution, and her practice is grounded in clarity, dignity and practical guidance.</p>
    <p>Based in Kingston, Jamaica, she works with clients across the Caribbean, the United States, the United Kingdom and beyond.</p>
    <div class="btn-row" style="justify-content:center"><a class="btn btn-outline" href="/about/">More about Dr. Harriott</a></div>
  </div>
</section>

{CTA}
''', extra_head='')

# ---------------------------------------------------------------- About
page('/about/', 'About', 'About Dr. Suzzette A. Harriott, PhD: therapeutic conflictologist based in Kingston, Jamaica, working with clients across the Caribbean and beyond.', '/about/', f'''
<section class="section bg-sand">
  <div class="wrap">
    <div class="split">
      <div>
        <p class="eyebrow">About the practice</p>
        <h1>A practice for people in transition.</h1>
        <p class="lead">I work with people navigating conflict: within families, within relationships, at work, and within themselves. The aim is to bring clarity, healing and direction, wherever a person stands today.</p>
      </div>
      <div class="photo"><img src="/img/portrait.jpg" alt="Dr. Suzzette A. Harriott"></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="center narrow" style="margin:0 auto 3rem"><h2>What guides this practice.</h2></div>
    <div class="grid grid-3">
      <div class="step"><p class="eyebrow">Mission</p><h3>To meet people where they are.</h3><p>Every person arrives carrying something different. The work begins with understanding what that is, without rushing to a label.</p></div>
      <div class="step"><p class="eyebrow">Vision</p><h3>A region of considered care.</h3><p>A Caribbean where psychological support is accessible, dignified and globally credible, and where seeking help carries the same weight as seeing a doctor.</p></div>
      <div class="step"><p class="eyebrow">Values</p><h3>Honesty, depth, alignment.</h3><p>Considered care over rushed advice. Rigour over surface coaching. Cultural rootedness over imported frameworks. The client&rsquo;s own voice over my interpretation of it. Always.</p></div>
    </div>
  </div>
</section>

<section class="section bg-sand">
  <div class="wrap narrow">
    <p class="eyebrow">Biography</p>
    <h2>Dr. Suzzette A. Harriott, PhD</h2>
    <p>Dr. Suzzette A. Harriott is a therapeutic conflictologist whose work brings together psychology, human resources and conflict resolution.</p>
    <p>Her academic foundation includes undergraduate training in psychology, graduate training in human resource management, and a PhD in Conflict Analysis and Resolution. This gives her work a rare blend of behavioural insight, organisational understanding and practical strategy.</p>
    <p>Her Therapeutic Conflictology work focuses on intrapersonal conflict, interpersonal conflict, relationship coaching, confidence building and practical support through transition. She also designs and facilitates RESET, an experiential growth programme for adults.</p>
    <p>Recognised by Marquis Who&rsquo;s Who for her contributions to conflict resolution, Dr. Harriott&rsquo;s practice is grounded in clarity, dignity and practical guidance for individuals, couples and families navigating important decisions.</p>
    <p>Based in Kingston, Jamaica, her practice serves clients across the Caribbean, the United States, the United Kingdom and beyond.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="center narrow" style="margin:0 auto 3rem"><h2>Two ways to work together.</h2></div>
    <div class="grid grid-2">
      <div class="step"><h3>Therapeutic Conflictology</h3><p>Conflict-informed support for emotional overwhelm, family tension, workplace stress, career uncertainty and major life transitions.</p><a class="btn btn-outline" href="/counselling/">Explore</a></div>
      <div class="step"><h3>RESET</h3><p>A small-group experiential immersion for adults ready for intentional growth. Separate from one-to-one work.</p><a class="btn btn-outline" href="/reset/">Explore</a></div>
    </div>
  </div>
</section>

{CTA}
''')

# ---------------------------------------------------------------- Therapeutic Conflictology
page('/counselling/', 'Therapeutic Conflictology', 'Therapeutic Conflictology with Dr. Suzzette A. Harriott: short-term, goal-oriented, conflict-informed support. In person in Kingston, Jamaica, and by secure video worldwide.', '/counselling/', f'''
<section class="hero short">
  <img class="hero-media" src="/img/tc-hero.jpg" alt="" aria-hidden="true">
  <div class="wrap">
    <p class="eyebrow">In person in Kingston &middot; Secure video worldwide</p>
    <h1>Therapeutic Conflictology</h1>
    <p class="lead">Conflict-informed support for individuals, couples, families and professionals navigating emotional stress, family tension, career decisions and major life transitions.</p>
    <div class="btn-row"><a class="btn btn-light" href="mailto:{EMAIL}?subject=Therapeutic%20Conflictology%20enquiry">Start the conversation</a></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div>
        <p class="eyebrow">What it is</p>
        <h2>Understanding the conflict beneath the problem.</h2>
        <p>Therapeutic Conflictology helps you understand the conflict beneath what you are facing and create a practical path forward. It is supportive, strategic and grounded in emotional insight and conflict resolution.</p>
        <p class="note">This is not traditional therapy. Therapeutic Conflictology provides conflict-informed support to help you gain clarity, strengthen emotional resilience and move forward with practical next steps.</p>
      </div>
      <div class="photo"><img src="/img/tc-reflection.jpg" alt="A man sitting thoughtfully in a calm room" loading="lazy"></div>
    </div>
  </div>
</section>

<section class="section bg-sand">
  <div class="wrap">
    <div class="center narrow" style="margin:0 auto 3rem">
      <p class="eyebrow">Common entry points</p>
      <h2>What brings people here</h2>
      <p>Illustrative, not exhaustive. If your situation is not listed, you are still welcome.</p>
    </div>
    <div class="grid grid-3">
      <div class="step"><h3>Emotional &amp; family stress</h3>{ticks(['Emotional overwhelm', 'Family tension', 'Parent-child conflict', 'Boundaries and difficult conversations', 'Grief, transition and decision-making', 'Food, eating and body image'])}</div>
      <div class="step"><h3>Work &amp; life direction</h3>{ticks(['Career uncertainty', 'Workplace conflict', 'Life transitions and relocation', 'Burnout', 'Feeling stuck without a neat label'])}</div>
      <div class="step"><h3>Parents &amp; professionals</h3>{ticks(['Parenting through high-conflict or transitional seasons', 'Supporting a child while managing your own emotional load', 'Co-parenting and family communication', 'Leadership, community or workplace tension', 'Building steadiness before the next decision'])}</div>
    </div>
  </div>
</section>

<section class="section" id="mindful-eating">
  <div class="wrap">
    <div class="illustration"><img src="/img/shared-meal.jpg" alt="Friends laughing together over a Caribbean meal outdoors" loading="lazy" width="1600" height="686"></div>
    <div class="split">
      <div>
        <p class="eyebrow">A focus within this work</p>
        <h2>Mindful Eating &amp; Body Image</h2>
        <p>For many people, food and body image carry far more than nutrition. They hold family history, culture, stress, comfort and the expectations of others. When that relationship becomes strained, it can quietly shape how you feel, how you show up and how you see yourself.</p>
        <p>This work offers a calm, judgement-free space to understand what sits beneath your patterns around food and your body, and to build a kinder, steadier way of living with both. Sessions are one-to-one and follow the same practical, goal-oriented approach as all Therapeutic Conflictology work.</p>
      </div>
      <div>
        <h3>This may help if you are</h3>
        {ticks(['Eating in response to stress, emotion or exhaustion rather than hunger', 'Feeling caught in cycles of restriction, guilt or all-or-nothing rules', 'Carrying criticism of your body that colours how you see yourself', 'Navigating family or cultural messages about food, weight and appearance', 'Wanting a calmer, more trusting relationship with food and your body'])}
        <p class="note" style="margin-top:1.5rem">Where physical health needs attention, this work sits alongside care from your doctor and, where helpful, a registered dietitian. If you are unwell or need urgent medical care, please contact your doctor or local emergency services first.</p>
      </div>
    </div>
    <div class="btn-row"><a class="btn" href="mailto:{EMAIL}?subject=Mindful%20Eating%20%26%20Body%20Image">Ask about Mindful Eating &amp; Body Image</a></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div>
        <p class="eyebrow">My approach</p>
        <h2>Practical, focused, and yours.</h2>
        <p>Sessions are goal-oriented and practical, often four to twelve meetings, focused on steadier emotional footing, clearer decisions and tools you can use between sessions.</p>
        <p>The work draws on doctoral training in conflict analysis. Many clients are Caribbean or diaspora, navigating family expectations, migration and demanding careers while feeling privately depleted.</p>
        <p>Support here focuses on you: emotional steadiness, co-parenting, burnout and grief while you lead at home and at work. Clinical mental health care for children is referred appropriately.</p>
      </div>
      <div>
        <h3>What you leave with</h3>
        {ticks(['A clearer read on what is driving the stress, beneath the surface argument or symptom', 'Practical language and tools for boundaries and difficult conversations', 'A mapped next step you can act on between sessions', 'Greater steadiness when family or work pressure builds', 'Confidence to make decisions during transition, relocation or career change'])}
      </div>
    </div>
  </div>
</section>

<section class="section bg-navy">
  <div class="wrap">
    <div class="center narrow" style="margin:0 auto 3rem"><p class="eyebrow" style="color:var(--sand)">Client experiences</p><h2>Real shifts, real clarity.</h2></div>
    <div class="grid grid-3">
      <figure class="testimonial"><blockquote>&ldquo;Dr. Harriott helped me see the patterns I could not see myself. I finally understand why the same cycles kept repeating, and what to do differently.&rdquo;</blockquote><figcaption>Family dynamics</figcaption></figure>
      <figure class="testimonial"><blockquote>&ldquo;The most thoughtful guidance I have received. She does not tell you what to do; she helps you find your own answer.&rdquo;</blockquote><figcaption>Career and identity</figcaption></figure>
      <figure class="testimonial"><blockquote>&ldquo;Practical and immediate. I left with tools, a new perspective, and a path I could actually follow.&rdquo;</blockquote><figcaption>Workplace conflict</figcaption></figure>
    </div>
  </div>
</section>

<section class="section bg-sand">
  <div class="wrap">
    <div class="center narrow" style="margin:0 auto 3rem"><p class="eyebrow">How it works</p><h2>Three simple stages.</h2></div>
    <div class="grid grid-3">
      <div class="step"><span class="step-num">1</span><h3>Initial conversation</h3><p>We clarify what you want to change, what conflict may be underneath it, and whether this work is the right fit, including referrals when needed.</p></div>
      <div class="step"><span class="step-num">2</span><h3>Focused work</h3><p>Short-term, goal-oriented sessions: understanding patterns, strengthening resilience and mapping practical next steps.</p></div>
      <div class="step"><span class="step-num">3</span><h3>Tools you keep</h3><p>You leave with strategies you can use between sessions. Clarity and movement, not endless talk without direction.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="center narrow" style="margin:0 auto 3rem"><p class="eyebrow">How we meet</p><h2>In person or by video.</h2></div>
    <div class="grid grid-2">
      <div class="step"><h3>In person</h3><p>Suite 66, Winchester Business Centre, 15 Hope Road, Kingston 10. A calm, private space for focused work.</p></div>
      <div class="step"><h3>By secure video</h3><p>Confidential sessions across the Caribbean, North America, Europe and beyond, with the same quality of care from your chosen space.</p></div>
    </div>
    <p class="note" style="margin-top:2rem">This practice is not a crisis service. If you are in danger or need emergency psychiatric care, please contact your local emergency services or go to the nearest hospital.</p>
  </div>
</section>

{CTA}
''')

# ---------------------------------------------------------------- RESET
page('/reset/', 'RESET', 'RESET: a cohort-based experiential immersion in emotional intelligence, relationships and intentional living, facilitated by Dr. Suzzette A. Harriott.', '/reset/', f'''
<section class="hero">
  <img class="hero-media" src="/img/reset-circle.jpg" alt="" aria-hidden="true" style="object-position:center 35%">
  <div class="wrap">
    <p class="eyebrow">Experiential growth training</p>
    <h1>RESET</h1>
    <p class="lead">A cohort-based immersion that builds emotional intelligence, strengthens relationships and helps you align daily life with what matters most, through lived experience rather than lectures.</p>
    <p class="lead" style="font-family:var(--heading);font-style:italic;font-size:1.6rem">Step out of autopilot. Step into intention.</p>
    <div class="btn-row"><a class="btn btn-light" href="mailto:{EMAIL}?subject=RESET%20enquiry">Enquire about RESET</a></div>
  </div>
</section>

<nav class="pill-nav" aria-label="RESET sections">
  <div class="wrap"><ul>
    <li><a href="#overview">Overview</a></li>
    <li><a href="#arc">The arc</a></li>
    <li><a href="#outcomes">Outcomes</a></li>
    <li><a href="#format">Format</a></li>
    <li><a href="#enquire">Enquire</a></li>
  </ul></div>
</nav>

<section class="section" id="overview">
  <div class="wrap">
    <div class="split">
      <div>
        <h2>Training that happens in the room</h2>
        <p>RESET is an experience-based programme for adults ready to examine how they think, feel, relate and choose, especially when life looks fine on paper but feels strained underneath.</p>
        <p>It is not one-to-one counselling, clinical treatment or open-ended coaching. It is structured, facilitated group work: guided exercises, honest dialogue and practical tools grounded in psychological insight and conflict-resolution practice.</p>
        <p>Participants are encouraged to reach their own conclusions. Lasting change tends to stick when you discover your truth in community, not when someone hands you a script.</p>
        <p class="note">RESET stands apart from one-to-one Therapeutic Conflictology. No other service is required to attend.</p>
      </div>
      <div class="photo"><img src="/img/reset-room.jpg" alt="Adults sitting together in a facilitated group session" loading="lazy"></div>
    </div>
  </div>
</section>

<section class="section bg-sand center">
  <div class="wrap narrow">
    <h2>Ask yourself honestly</h2>
    {ticks(['Is there an area of your life you quietly wish was better?', 'Do you want more energy, intention or purpose, not just more productivity?', 'Is something holding you back from living at your full capacity?'])}
    <p style="margin-top:1.5rem">If one of these landed, the next cohort may be worth a conversation.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split reverse">
      <div>
        <h2>When the outside looks fine</h2>
        <p class="lead">You may not be in crisis. Still, something feels out of sync.</p>
        {ticks(['You feel off, but cannot name why', 'Your mind runs constantly without settling', 'You have outgrown a role, relationship or version of yourself', 'You are tired in a way sleep does not fix', 'You perform well while feeling disconnected inside'])}
      </div>
      <div class="photo"><img src="/img/reset-quiet.jpg" alt="Stacked stones on a calm, sunlit surface" loading="lazy"></div>
    </div>
  </div>
</section>

<section class="section bg-sand">
  <div class="wrap">
    <div class="center narrow" style="margin:0 auto 3rem"><h2>How the room is held</h2><p>Facilitation draws on conflict-resolution training and adult-learning design, with Caribbean cultural fluency.</p></div>
    <div class="grid grid-2">
      <div class="step"><h3>Experiential first</h3><p>You learn by doing: reflecting, practising and receiving feedback in real time with others in the room.</p></div>
      <div class="step"><h3>Your conclusions matter</h3><p>Facilitators guide the process; you own the insights. The aim is self-discovery that translates into behaviour at home and at work.</p></div>
      <div class="step"><h3>Dignity in the room</h3><p>No humiliation, no performance for approval. Direct honesty with respect, especially for Caribbean professionals navigating high expectations.</p></div>
      <div class="step"><h3>Integration after</h3><p>The goal is not a weekend high. You leave with language, tools and commitments you can apply when ordinary life resumes.</p></div>
    </div>
  </div>
</section>

<section class="section" id="arc">
  <div class="wrap">
    <div class="center narrow" style="margin:0 auto 3rem"><h2>Five movements through the work</h2><p>Each cohort moves through a sequenced arc. The names are simple; the inner work is not.</p></div>
    <div class="arc">
      <div class="step"><span class="step-num">1</span><h3>PAUSE</h3><p>Create distance from noise, urgency and roles that no longer fit.</p></div>
      <div class="step"><span class="step-num">2</span><h3>UNPACK</h3><p>Name the expectations, stories and burdens you have been carrying.</p></div>
      <div class="step"><span class="step-num">3</span><h3>UNDERSTAND</h3><p>Connect patterns to feelings, choices and relationships.</p></div>
      <div class="step"><span class="step-num">4</span><h3>RELEASE</h3><p>Loosen what is outdated: habits, narratives or obligations that are not yours.</p></div>
      <div class="step"><span class="step-num">5</span><h3>REALIGN</h3><p>Choose direction, boundaries and next steps that match your values.</p></div>
    </div>
    <p class="quote center" style="margin-top:3.5rem">Insight rarely arrives from thinking harder. It arrives when you make room to feel, name and choose.</p>
  </div>
</section>

<section class="section bg-navy" id="outcomes">
  <div class="wrap">
    <div class="split">
      <div>
        <h2>What graduates often report</h2>
        <p>Outcomes vary by person. The list reflects common themes, not guarantees.</p>
      </div>
      <div>
        {ticks(['Stronger self-esteem and personal agency', 'Greater emotional maturity and healing of old wounds', 'Tools to work through relationship friction', 'Clarity about purpose and what you want next', 'Deliberate habits in place of destructive ones', 'Better dynamics with family, friends and colleagues', 'More authentic, heartfelt communication', 'Core values named, and lived toward', 'Sharper professional focus', 'Fuller presence as a parent or caregiver', 'Recovered joy, creativity and satisfaction in daily life'])}
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="photo"><img src="/img/reset-adults.jpg" alt="Adults of different ages in a group conversation" loading="lazy"></div>
      <div>
        <h2>Who tends to thrive here</h2>
        <p class="lead">RESET is for people willing to be honest in a group, not for spectators.</p>
        {ticks(['Professionals and leaders carrying invisible pressure', 'Adults in transition: relocation, divorce, career change, empty nest', 'Those rebuilding confidence after burnout or betrayal', 'Anyone who senses misalignment but resists vague self-help', 'People ready to stop managing image and start living intentionally'])}
      </div>
    </div>
  </div>
</section>

<section class="section bg-sand" id="format">
  <div class="wrap">
    <div class="split">
      <div>
        <h2>Inside the immersion</h2>
        <p>RESET runs as a small, curated cohort, periodically, in a destination setting that supports focus and depth.</p>
        <p>Days combine facilitated processes, paired and group work, reflection and skill-building. You hear perspectives you would not get alone.</p>
        <p>Enrolment is intentionally limited so the room stays safe, confidential and engaged.</p>
        <p class="quote">This is not a casual weekend. It is a deliberate investment in who you are becoming.</p>
      </div>
      <div>
        <h3>Fit and safety</h3>
        <p>The work can be emotionally demanding. It suits adults who are stable enough to take part in guided exploration, not those in acute crisis.</p>
        <p>If you are having thoughts of self-harm, are in a psychiatric emergency, or need urgent clinical care, please contact licensed professionals or local emergency services first.</p>
        <p>One-to-one Therapeutic Conflictology remains available separately for ongoing support.</p>
      </div>
    </div>
  </div>
</section>

<section class="section bg-navy center" id="enquire">
  <div class="wrap narrow">
    <h2>Curious if RESET is your next step?</h2>
    <p class="lead">A brief conversation helps us understand your goals and whether the upcoming cohort is the right match.</p>
    <div class="btn-row" style="justify-content:center"><a class="btn btn-light" href="mailto:{EMAIL}?subject=RESET%20enquiry">Enquire about RESET</a></div>
  </div>
</section>
''')

# ---------------------------------------------------------------- Contact
page('/contact/', 'Contact', 'Contact Dr. Suzzette A. Harriott by email at contact@suzzetteharriott.com about Therapeutic Conflictology, Mindful Eating & Body Image or RESET.', '/contact/', f'''
<section class="section bg-sand">
  <div class="wrap narrow">
    <p class="eyebrow">Contact</p>
    <h1>Start the conversation.</h1>
    <p class="lead">Send a short email about what brought you here. I reply within one to two business days.</p>
    <p class="email-big"><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    <div class="btn-row"><a class="btn" href="mailto:{EMAIL}?subject=Enquiry">Email Dr. Harriott</a></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split" style="align-items:start">
      <ul class="contact-list">
        <li><strong>Email</strong><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><strong>Location</strong>Kingston, Jamaica, and secure video worldwide</li>
        <li><strong>Availability</strong>By appointment only</li>
      </ul>
      <div>
        <h3>What to include</h3>
        {ticks(['Your name and the best way to reach you', 'Which service you are asking about: Therapeutic Conflictology, Mindful Eating &amp; Body Image, couples or family sessions, or RESET', 'A sentence or two about what you are hoping for'])}
        <p class="note" style="margin-top:1.5rem">Please keep your first email brief and leave out sensitive personal or health details. We can talk about those privately once we connect.</p>
        <p class="note">This is not a crisis service. If you are in danger or need urgent care, please contact your local emergency services or go to the nearest hospital.</p>
      </div>
    </div>
  </div>
</section>
''')

# ---------------------------------------------------------------- Legal
LEGAL_CONTACT = f'''<h2>Contact</h2>
<p>Dr. Suzzette A. Harriott, PhD<br>Suzzette Harriott &amp; Associates<br>Kingston, Jamaica<br><a href="mailto:{EMAIL}">{EMAIL}</a></p>'''

def legal(path, title, desc, body):
    page(path, title, desc, '', f'''
<section class="section">
  <div class="wrap narrow legal">
    <h1>{title}</h1>
    <p><em>Last updated: November 2026</em></p>
    {body}
    {LEGAL_CONTACT}
  </div>
</section>''')

legal('/privacy-policy/', 'Privacy Policy', 'How suzzetteharriott.com handles personal information.', f'''
<p>This website, suzzetteharriott.com, is operated by Dr. Suzzette A. Harriott, PhD, practising as Suzzette Harriott &amp; Associates (&ldquo;Dr. Harriott&rdquo;, &ldquo;we&rdquo;, &ldquo;us&rdquo;). Dr. Harriott respects your privacy. This policy explains what information this website handles and how. Personal data is handled in line with Jamaica&rsquo;s Data Protection Act, 2020.</p>
<h2>What this website collects</h2>
<p>This website does not have accounts, logins, contact forms or a database. It does not collect personal information from visitors. To get in touch, you email Dr. Harriott directly.</p>
<p>If you email Dr. Harriott, she receives the information you choose to include, such as your name, email address, phone number and message.</p>
<h2>How we use your information</h2>
<ul>
<li>To reply to your enquiry</li>
<li>To arrange and provide the services you request, such as Therapeutic Conflictology sessions or RESET enrolment</li>
</ul>
<p>We do not sell, rent or share your personal information for marketing.</p>
<h2>Confidentiality</h2>
<p>Information shared with Dr. Harriott in the course of services is treated as confidential, within the limits explained to you at the start of our work together. Please avoid sending sensitive personal or health details in your first email.</p>
<h2>Technical services</h2>
<p>This website is served by a hosting provider, which processes basic technical information (such as IP address and browser type) to deliver pages securely. Fonts are loaded from Google Fonts, which receives your IP address when a page loads. We do not use analytics or advertising tools.</p>
<h2>Your rights</h2>
<p>You may ask to see, correct or delete personal information Dr. Harriott holds about you by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Changes</h2>
<p>We may update this policy from time to time. The current version will always appear on this page.</p>
''')

legal('/terms-of-service/', 'Terms of Service', 'Terms for using suzzetteharriott.com.', '''
<p>This website, suzzetteharriott.com, is operated by Dr. Suzzette A. Harriott, PhD, practising as Suzzette Harriott &amp; Associates. By using this website you agree to these terms.</p>
<h2>Information only</h2>
<p>Content on this website is general information about the services of Dr. Suzzette A. Harriott, PhD. It is not professional advice for your situation and does not create a client relationship. Services begin only after an initial conversation and mutual agreement.</p>
<h2>Not an emergency service</h2>
<p>This website and its email address are not monitored for emergencies. If you are in danger or need urgent care, contact your local emergency services or go to the nearest hospital.</p>
<h2>Intellectual property</h2>
<p>All content on this website, including text, design, images, programme names and frameworks such as RESET, belongs to Dr. Suzzette A. Harriott, PhD (Suzzette Harriott &amp; Associates) unless stated otherwise, and may not be copied or redistributed without written permission.</p>
<h2>Links to other websites</h2>
<p>We are not responsible for the content or policies of websites we link to.</p>
<h2>Limitation of liability</h2>
<p>We work to keep this website accurate, but we are not liable for any loss arising from use of the website or reliance on its content.</p>
<h2>Governing law</h2>
<p>These terms are governed by the laws of Jamaica.</p>
<h2>Changes</h2>
<p>We may update these terms from time to time. Continued use of the website means you accept the current version.</p>
''')

legal('/cookie-policy/', 'Cookie Policy', 'Cookie use on suzzetteharriott.com.', '''
<p>This policy covers suzzetteharriott.com, the website of Dr. Suzzette A. Harriott, PhD. Cookies are small files a website can store on your device.</p>
<h2>Our use of cookies</h2>
<p>This website does not set any cookies. We do not use analytics, advertising or tracking tools.</p>
<h2>Third parties</h2>
<p>Fonts are loaded from Google Fonts. Google states that it does not set cookies when serving fonts, but it does receive your IP address. You can block third-party content through your browser settings if you prefer.</p>
<h2>Changes</h2>
<p>If this changes, we will update this page before any cookies are introduced.</p>
''')

# ---------------------------------------------------------------- 404
page('/404.html', 'Page not found', 'Page not found.', '', '''
<script>
  // Old Wix addresses: send Compass and special-education visitors to cescarib.com.
  (function () {
    var p = location.pathname.toLowerCase();
    var map = [
      ['/special-education', 'https://cescarib.com/compass-care'],
      ['/college-consulting/', 'https://cescarib.com' + location.pathname],
      ['/college-consulting', 'https://cescarib.com/college-consulting'],
      ['/pre-college', 'https://cescarib.com/college-consulting'],
      ['/programs', 'https://cescarib.com/college-consulting/programs'],
      ['/outcomes', 'https://cescarib.com/college-consulting/outcomes'],
      ['/iseey-foundation', 'https://cescarib.com/college-consulting/foundation'],
      ['/compass', 'https://cescarib.com/login'],
      ['/client-portal', 'https://cescarib.com/login'],
      ['/get-started', 'https://cescarib.com/login'],
      ['/join', 'https://cescarib.com/login'],
      ['/dashboard', 'https://cescarib.com/login'],
      ['/parent-dashboard', 'https://cescarib.com/login'],
      ['/school', 'https://cescarib.com/login'],
      ['/admin', 'https://cescarib.com/login'],
      ['/careers', 'https://cescarib.com/'],
      ['/therapeutic-conflictology', '/counselling/'],
      ['/book', '/contact/']
    ];
    for (var i = 0; i < map.length; i++) {
      if (p === map[i][0] || p.indexOf(map[i][0] + '/') === 0 || (map[i][0].slice(-1) === '/' && p.indexOf(map[i][0]) === 0)) {
        location.replace(map[i][1]);
        return;
      }
    }
  })();
</script>
<section class="section center">
  <div class="wrap narrow">
    <p class="eyebrow">404</p>
    <h1>This page has moved.</h1>
    <p class="lead">The site has been reorganised. Looking for Compass college readiness? It now lives at <a href="https://cescarib.com">cescarib.com</a>.</p>
    <div class="btn-row" style="justify-content:center">
      <a class="btn" href="/">Go to the home page</a>
      <a class="btn btn-outline" href="/contact/">Contact</a>
    </div>
  </div>
</section>''')

print('built')
