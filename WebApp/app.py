from flask import Flask, request, session, redirect, url_for, render_template_string
import random
import json

app = Flask(__name__)
app.secret_key = 'change-this-to-a-secret-key'

GAME_HTML = '''
<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Jeu interactif</title>
  <style>
    :root {
      --bg: #081c2f;
      --surface: #102a48;
      --surface-soft: rgba(24, 58, 94, 0.95);
      --accent: #42a5f5;
      --accent-strong: #1d4ed8;
      --text: #f8fafc;
      --text-muted: #d1d5db;
      --success: #22c55e;
      --danger: #f87171;
    }
    * { box-sizing: border-box; }
    body { margin: 0; min-height: 100vh; font-family: Inter, system-ui, sans-serif; color: var(--text); background: radial-gradient(circle at top, #183156 0%, var(--bg) 45%), linear-gradient(180deg, rgba(255,255,255,0.06), transparent 30%); }
    body::before { content: ''; position: fixed; inset: 0; background: url('data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="800" height="800" viewBox="0 0 800 800"%3E%3Ccircle cx="120" cy="120" r="55" fill="rgba(66,165,245,0.2)"/%3E%3Ccircle cx="720" cy="90" r="30" fill="rgba(255,255,255,0.08)"/%3E%3Ccircle cx="580" cy="680" r="90" fill="rgba(16,42,72,0.4)"/%3E%3C/svg%3E') no-repeat center/cover; pointer-events: none; }
    .page { max-width: 1040px; margin: 0 auto; padding: 32px 24px; }
    header { display: grid; gap: 16px; margin-bottom: 28px; }
    .hero { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 20px; align-items: center; }
    .hero h1 { margin: 0; font-size: clamp(2rem, 3vw, 3.2rem); line-height: 1.05; letter-spacing: -0.03em; }
    .hero p { max-width: 640px; color: var(--text-muted); margin: 0; }
    .grid { display: grid; gap: 20px; grid-template-columns: repeat(auto-fit,minmax(260px,1fr)); }
    .card { background: rgba(15, 33, 58, 0.95); border: 1px solid rgba(255,255,255,0.08); border-radius: 24px; padding: 28px; box-shadow: 0 28px 90px rgba(0,0,0,0.22); }
    .card h2 { margin: 0 0 14px; font-size: 1.25rem; color: var(--accent); }
    .card p, label { color: var(--text-muted); }
    .status { margin: 18px 0; padding: 16px 18px; border-radius: 18px; background: rgba(66,165,245,0.12); border: 1px solid rgba(66,165,245,0.18); }
    .status.success { background: rgba(34,197,94,0.14); border-color: rgba(34,197,94,0.25); color: var(--success); }
    .status.error { background: rgba(248,113,113,0.14); border-color: rgba(248,113,113,0.25); color: var(--danger); }
    .controls { display: grid; gap: 16px; }
    .controls label { display: block; font-size: 0.95rem; margin-bottom: 6px; }
    input[type=number] { width: 100%; border: 1px solid rgba(255,255,255,0.12); border-radius: 14px; background: rgba(255,255,255,0.04); color: var(--text); padding: 14px 16px; font-size: 1rem; }
    input[type=number]::placeholder { color: rgba(255,255,255,0.45); }
    .buttons { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 8px; }
    button { min-width: 140px; border: none; border-radius: 14px; padding: 14px 18px; font-size: 0.95rem; font-weight: 600; color: var(--text); cursor: pointer; transition: transform .18s ease, background .2s ease; }
    button:hover { transform: translateY(-1px); }
    .primary { background: linear-gradient(135deg, var(--accent), var(--accent-strong)); box-shadow: 0 18px 30px rgba(34, 113, 224, 0.22); }
    .secondary { background: rgba(255,255,255,0.08); color: var(--text-muted); }
    .stats { display: grid; gap: 14px; grid-template-columns: repeat(3,minmax(0,1fr)); }
    .stat { padding: 18px 20px; border-radius: 18px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); }
    .stat strong { display: block; margin-top: 10px; font-size: 1.5rem; color: white; }
    .stat span { color: var(--text-muted); font-size: 0.9rem; }
    .chart-card { position: relative; overflow: hidden; }
    .chart-title { display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-bottom: 18px; }
    canvas { width: 100%; height: 300px; display: block; border-radius: 20px; background: rgba(255,255,255,0.04); }
    .badge { display: inline-flex; align-items: center; gap: 8px; padding: 8px 12px; border-radius: 999px; font-size: 0.88rem; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.1); }
    .badge span { display: inline-flex; width: 10px; height: 10px; border-radius: 999px; }
    .badge--hint span { background: #60a5fa; }
    .badge--guess span { background: #fbbf24; }
    .footer-note { color: var(--text-muted); font-size: 0.92rem; margin-top: 14px; }
  </style>
</head>
<body>
  <main class="page">
    <header>
      <div class="hero">
        <div>
          <h1>Jeu de devinette interactif</h1>
          <p>Plonge dans un jeu visuel où chaque essai te rapproche du nombre mystère. Suis ton score, ton historique et ton rythme comme dans un vrai jeu moderne.</p>
        </div>
      </div>
      <div class="stats">
        <div class="stat">
          <span>Essais restants</span>
          <strong>{{ remaining }}</strong>
        </div>
        <div class="stat">
          <span>Essais utilisés</span>
          <strong>{{ attempts }}</strong>
        </div>
        <div class="stat">
          <span>Historique</span>
          <strong>{{ history if history != 'aucun' else '—' }}</strong>
        </div>
      </div>
    </header>

    <section class="card">
      <h2>Devine le nombre entre 1 et 100</h2>

      {% if status %}
        <div class="status {{ 'success' if status == 'gagné' else 'error' if status == 'perdu' else '' }}">
          {{ message }}
        </div>
        {% if last_feedback %}
          <div class="status">
            {{ last_feedback }}
          </div>
        {% endif %}
      {% endif %}

      <form method="post" action="{{ url_for('guess') }}" class="controls">
        <label for="guess">Ton dernier essai</label>
        <input id="guess" name="guess" type="number" min="1" max="100" placeholder="Entrez un nombre" required autofocus>
        <div class="buttons">
          <button class="primary" type="submit">Valider</button>
          <button class="secondary" type="submit" formaction="{{ url_for('reset') }}">Recommencer</button>
        </div>
      </form>

      <div class="footer-note">Utilise les informations du graphique pour ajuster tes prochains choix.</div>
    </section>

    <section class="card chart-card">
      <div class="chart-title">
        <div>
          <h2>Proximité des essais</h2>
          <p class="footer-note">Chaque barre montre à quel point ta réponse était proche du nombre mystère en pourcentage.</p>
        </div>
      </div>
      <canvas id="historyChart" width="720" height="320"></canvas>
    </section>
  </main>

  <script>
    const historyData = {{ history_data | safe }};
    const guessLabels = {{ guess_labels | safe }};
    const attempts = {{ attempts }};
    const maxAttempts = {{ max_attempts }};
    const lastFeedback = '{{ last_feedback }}';

    function drawChart() {
      const canvas = document.getElementById('historyChart');
      const ctx = canvas.getContext('2d');
      const width = canvas.width;
      const height = canvas.height;
      ctx.clearRect(0, 0, width, height);

      const padding = 40;
      const chartWidth = width - padding * 2;
      const chartHeight = height - padding * 2;
      const barWidth = Math.max(26, chartWidth / maxAttempts - 12);

      // grille de fond
      ctx.strokeStyle = 'rgba(255,255,255,0.12)';
      ctx.lineWidth = 1;
      for (let i = 0; i <= 5; i++) {
        const y = padding + chartHeight * i / 5;
        ctx.beginPath();
        ctx.moveTo(padding, y);
        ctx.lineTo(width - padding, y);
        ctx.stroke();
      }

      // axe x avec les valeurs devinées
      ctx.fillStyle = 'rgba(255,255,255,0.7)';
      ctx.font = '13px Inter, sans-serif';
      ctx.textAlign = 'center';
      guessLabels.forEach((guess, index) => {
        const x = padding + (index + 0.5) * (chartWidth / maxAttempts);
        ctx.fillText(guess || '-', x, height - padding + 20);
      });

      // barres de proximité en pourcentage
      const maxValue = 100;
      historyData.forEach((value, index) => {
        const x = padding + index * (chartWidth / maxAttempts) + ((chartWidth / maxAttempts) - barWidth) / 2;
        const y = padding + chartHeight * (1 - value / maxValue);
        const h = chartHeight * value / maxValue;
        const color = value > 70 ? 'rgba(34,197,94,0.9)' : value > 40 ? 'rgba(248,209,60,0.9)' : 'rgba(248,113,113,0.9)';
        ctx.fillStyle = color;
        ctx.fillRect(x, y, barWidth, h);
        ctx.fillStyle = 'rgba(255,255,255,0.9)';
        ctx.font = '11px Inter, sans-serif';
        ctx.fillText(value + '%', x + barWidth / 2, y - 10);
      });

      // bordure du chart
      ctx.strokeStyle = 'rgba(255,255,255,0.14)';
      ctx.lineWidth = 2;
      ctx.strokeRect(padding, padding, chartWidth, chartHeight);
    }

    function drawGoalLine() {
      const canvas = document.getElementById('historyChart');
      const ctx = canvas.getContext('2d');
      const width = canvas.width;
      const padding = 40;
      const chartHeight = canvas.height - padding * 2;
      ctx.save();
      ctx.fillStyle = 'rgba(255,255,255,0.6)';
      ctx.font = '12px Inter, sans-serif';
      ctx.textAlign = 'right';
      ctx.fillText('Proximité', width - padding, padding - 12);
      ctx.restore();
    }

    function init() {
      drawChart();
    }

    window.addEventListener('load', init);
  </script>
</body>
</html>
'''


def compute_closeness(guess, target):
    distance = abs(guess - target)
    return max(0, min(100, 100 - round(distance / 99 * 100)))


def start_game():
    session['target'] = random.randint(1, 100)
    session['attempts'] = 0
    session['history'] = []
    session['status'] = ''
    session['message'] = 'Bonne chance !'
    session['last_feedback'] = ''
    session['max_attempts'] = 3


@app.route('/')
def index():
    if 'target' not in session:
        start_game()

    remaining = max(0, session.get('max_attempts', 3) - session.get('attempts', 0))
    history = session.get('history', [])
    history_data = [compute_closeness(item, session['target']) for item in history]
    return render_template_string(
        GAME_HTML,
        remaining=remaining,
        attempts=session.get('attempts', 0),
        max_attempts=session.get('max_attempts', 3),
        history=', '.join(str(x) for x in history) if history else 'aucun',
        history_data=json.dumps(history_data),
        guess_labels=json.dumps(history),
        last_feedback=session.get('last_feedback', ''),
        status=session.get('status', ''),
        message=session.get('message', '')
    )


@app.route('/guess', methods=['POST'])
def guess():
    if 'target' not in session:
        start_game()

    if session.get('status') == 'gagné' or session.get('status') == 'perdu':
        return redirect(url_for('index'))

    try:
        guess_value = int(request.form['guess'])
    except (ValueError, KeyError):
        session['message'] = 'Veuillez entrer un nombre valide entre 1 et 100.'
        return redirect(url_for('index'))

    if not 1 <= guess_value <= 100:
        session['message'] = 'Le nombre doit être entre 1 et 100.'
        return redirect(url_for('index'))

    session['attempts'] += 1
    session['history'].append(guess_value)

    target = session['target']
    remaining = 10 - session['attempts']

    if guess_value == target:
        session['status'] = 'gagné'
        session['message'] = f'Bravo ! Tu as trouvé le nombre {target} en {session["attempts"]} essais.'
        session['last_feedback'] = 'Excellent ! Exactement la bonne valeur.'
    elif session['attempts'] >= session.get('max_attempts', 3):
        session['status'] = 'perdu'
        session['message'] = f'Dommage, tu as utilisé tous tes essais. Le nombre était {target}.'
        session['last_feedback'] = 'Fin du jeu. Recommence pour tenter ta chance à nouveau.'
    else:
        difference = guess_value - target
        closeness = compute_closeness(guess_value, target)
        if difference < 0:
            direction = 'plus grand'
        else:
            direction = 'plus petit'
        session['message'] = f'La bonne réponse est {direction} que {guess_value}. Proximité : {closeness}%.'
        session['last_feedback'] = f'Indice : la réponse est {direction}, {closeness}% de proximité.'

    return redirect(url_for('index'))


@app.route('/reset', methods=['POST'])
def reset():
    start_game()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
