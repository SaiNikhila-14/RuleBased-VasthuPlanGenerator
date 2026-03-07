import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np
import io
import time

# ─────────────────────────────────────────────
# 1. PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="VastuLeap Plan Generator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# 2. CUSTOM CSS — adaptive light / dark theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@400;500;600&display=swap');

/* ══ CSS variables — light: Slate & Coral ══ */
:root {
    --bg-page:          linear-gradient(135deg, #f0f4f8 0%, #f7f9fc 100%);
    --bg-card:          #ffffff;
    --border-card:      #dde4ed;
    --shadow-card:      rgba(71, 95, 130, 0.10);
    --text-primary:     #1e2c3a;
    --text-secondary:   #e05a4e;
    --text-muted:       #7a8fa6;
    --text-subtle:      #8fa3b8;
    --text-ideal:       #a0b4c8;
    --divider:          #e4ecf4;
    --progress-track:   #dde4ed;
    --hero-bg:          linear-gradient(120deg, #1e2c3a 0%, #2e4a6a 100%);
    --hero-title:       #f9c5c0;
    --hero-sub:         #f0a89f;
    --btn-bg:           linear-gradient(120deg, #e05a4e, #f0826a);
    --badge-high-bg:    #e8f5e9; --badge-high-fg:    #2e7d32;
    --badge-medium-bg:  #fff8e1; --badge-medium-fg:  #f57f17;
    --badge-low-bg:     #fce4ec; --badge-low-fg:     #c62828;
    --tag-ok-bg:        #e8f5e9; --tag-ok-fg:        #2e7d32;
    --tag-defect-bg:    #fce4ec; --tag-defect-fg:    #c62828;
    --tag-neutral-bg:   #e8edf5; --tag-neutral-fg:   #2e4a6a;
}

/* ══ Dark mode via Streamlit's data-theme attribute ══ */
[data-theme="dark"] {
    --bg-page:          linear-gradient(135deg, #0f0a04 0%, #1a1008 100%);
    --bg-card:          #1e1509;
    --border-card:      #3a2510;
    --shadow-card:      rgba(0,0,0,0.40);
    --text-primary:     #f5d9a8;
    --text-secondary:   #e4b87a;
    --text-muted:       #9a7a55;
    --text-subtle:      #b09070;
    --text-ideal:       #806040;
    --divider:          #3a2510;
    --progress-track:   #3a2510;
    --hero-bg:          linear-gradient(120deg, #3d2008 0%, #7a4520 100%);
    --hero-title:       #f5d9a8;
    --hero-sub:         #c9a06a;
    --btn-bg:           linear-gradient(120deg, #8b4a20, #c06030);
    --badge-high-bg:    #0d2b12; --badge-high-fg:    #81c784;
    --badge-medium-bg:  #2e2400; --badge-medium-fg:  #ffd54f;
    --badge-low-bg:     #2e0d14; --badge-low-fg:     #ef9a9a;
    --tag-ok-bg:        #0d2b12; --tag-ok-fg:        #81c784;
    --tag-defect-bg:    #2e0d14; --tag-defect-fg:    #ef9a9a;
    --tag-neutral-bg:   #071a30; --tag-neutral-fg:   #90caf9;
}

/* ══ Also honour system preference as fallback ══ */
@media (prefers-color-scheme: dark) {
    :root {
        --bg-page:          linear-gradient(135deg, #0f0a04 0%, #1a1008 100%);
        --bg-card:          #1e1509;
        --border-card:      #3a2510;
        --shadow-card:      rgba(0,0,0,0.40);
        --text-primary:     #f5d9a8;
        --text-secondary:   #e4b87a;
        --text-muted:       #9a7a55;
        --text-subtle:      #b09070;
        --text-ideal:       #806040;
        --divider:          #3a2510;
        --progress-track:   #3a2510;
        --hero-bg:          linear-gradient(120deg, #3d2008 0%, #7a4520 100%);
        --hero-title:       #f5d9a8;
        --hero-sub:         #c9a06a;
        --btn-bg:           linear-gradient(120deg, #8b4a20, #c06030);
        --badge-high-bg:    #0d2b12; --badge-high-fg:    #81c784;
        --badge-medium-bg:  #2e2400; --badge-medium-fg:  #ffd54f;
        --badge-low-bg:     #2e0d14; --badge-low-fg:     #ef9a9a;
        --tag-ok-bg:        #0d2b12; --tag-ok-fg:        #81c784;
        --tag-defect-bg:    #2e0d14; --tag-defect-fg:    #ef9a9a;
        --tag-neutral-bg:   #071a30; --tag-neutral-fg:   #90caf9;
    }
}

/* ══ Typography ══ */
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
h1, h2, h3 { font-family: 'Playfair Display', serif; }

/* ══ App background ══ */
.stApp { background: var(--bg-page); }

/* ══ Hero ══ */
.hero {
    background: var(--hero-bg);
    border-radius: 16px;
    padding: 2.2rem 2.5rem;
    margin-bottom: 1.8rem;
}
.hero h1 {
    font-size: 2.4rem;
    margin: 0 0 0.4rem 0;
    color: var(--hero-title);
    letter-spacing: -0.5px;
}
.hero p {
    font-size: 1.02rem;
    color: var(--hero-sub);
    margin: 0;
    opacity: 0.9;
}

/* ══ Cards ══ */
.card {
    background: var(--bg-card);
    border-radius: 14px;
    padding: 1.6rem;
    box-shadow: 0 2px 16px var(--shadow-card);
    border: 1px solid var(--border-card);
    margin-bottom: 1rem;
}
.card-title   { font-family:'Playfair Display',serif; font-size:1.15rem; font-weight:700; color:var(--text-primary);   margin-bottom:0.6rem; }
.score-number { font-size:2rem; font-weight:700; color:var(--text-secondary); margin:0.2rem 0; }
.score-meta   { font-size:0.82rem; color:var(--text-muted); margin-bottom:1rem; }
.room-label-heading { font-weight:600; font-size:0.9rem; color:var(--text-primary); margin-bottom:0.4rem; }
.zone-text    { font-size:0.78rem; color:var(--text-subtle); }
.ideal-text   { font-size:0.78rem; color:var(--text-ideal); }

/* ══ Score badges ══ */
.score-badge {
    display: inline-block;
    padding: 0.35rem 1rem;
    border-radius: 50px;
    font-weight: 600;
    font-size: 0.95rem;
    margin-bottom: 0.6rem;
}
.score-high   { background: var(--badge-high-bg);   color: var(--badge-high-fg); }
.score-medium { background: var(--badge-medium-bg); color: var(--badge-medium-fg); }
.score-low    { background: var(--badge-low-bg);    color: var(--badge-low-fg); }

/* ══ Progress bar ══ */
.progress-wrap {
    background: var(--progress-track);
    border-radius: 8px;
    height: 10px;
    margin: 0.4rem 0 1rem 0;
    overflow: hidden;
}
.progress-fill { height:100%; border-radius:8px; transition: width 0.6s ease; }

/* ══ Room rows ══ */
.room-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.45rem 0;
    border-bottom: 1px solid var(--divider);
    font-size: 0.92rem;
}

/* ══ Tags ══ */
.tag { padding:0.18rem 0.6rem; border-radius:20px; font-size:0.78rem; font-weight:600; white-space:nowrap; }
.tag-ok      { background: var(--tag-ok-bg);      color: var(--tag-ok-fg); }
.tag-defect  { background: var(--tag-defect-bg);  color: var(--tag-defect-fg); }
.tag-neutral { background: var(--tag-neutral-bg); color: var(--tag-neutral-fg); }

/* ══ Buttons ══ */
.stDownloadButton > button {
    background: var(--btn-bg) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    width: 100% !important;
}
.stDownloadButton > button:hover { opacity: 0.88 !important; }

.stButton > button[kind="primary"] {
    background: var(--btn-bg) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.65rem 1rem !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 3. CONSTANTS & RULES
# ─────────────────────────────────────────────
@st.cache_resource
def get_vastu_constants():
    ROOM_RULES = {
        'Kitchen':        'SE',
        'Master Bedroom': 'SW',
        'Pooja Room':     'NE',
        'Toilet':         'NW',
    }
    MIN_DIMS = {
        'Kitchen':        (10,  8),
        'Master Bedroom': (12, 14),
        'Pooja Room':     ( 6,  6),
        'Toilet':         ( 5,  7),
        'Bedroom 2':      (10, 10),
        'Bedroom 3':      (10, 10),
        'Living Room':    (15, 12),
    }
    ROOM_COLORS = {
        'compliant': '#4CAF50',
        'defect':    '#F44336',
        'neutral':   '#2196F3',
    }
    # Human-readable Vastu direction tips
    DIRECTION_TIPS = {
        'SE': 'South-East — Fire element, ideal for Kitchen',
        'SW': 'South-West — Earth element, grounding energy',
        'NE': 'North-East — Water element, pure divine energy',
        'NW': 'North-West — Air element, movement & change',
    }
    return ROOM_RULES, MIN_DIMS, ROOM_COLORS, DIRECTION_TIPS

ROOM_RULES, MIN_DIMS, ROOM_COLORS, DIRECTION_TIPS = get_vastu_constants()


# ─────────────────────────────────────────────
# 4. PLAN GENERATION
# ─────────────────────────────────────────────
@st.cache_data
def generate_plan_options(plot_width, plot_length, facing_direction, num_bhk):
    cx, cy = plot_width / 2, plot_length / 2

    plan_data_1 = {
        'Master Bedroom': (plot_width * 0.25, plot_length * 0.25, MIN_DIMS['Master Bedroom'], 'SW'),
        'Kitchen':        (plot_width * 0.75, plot_length * 0.25, MIN_DIMS['Kitchen'],        'SE'),
        'Pooja Room':     (plot_width * 0.75, plot_length * 0.75, MIN_DIMS['Pooja Room'],     'NE'),
        'Toilet':         (plot_width * 0.25, plot_length * 0.75, MIN_DIMS['Toilet'],         'NW'),
        'Bedroom 2':      (plot_width * 0.50, plot_length * 0.75, MIN_DIMS['Bedroom 2'],      'N'),
        'Living Room':    (cx,                plot_length * 0.50, MIN_DIMS['Living Room'],    'Center/E'),
    }
    if num_bhk == 3:
        plan_data_1['Bedroom 3'] = (plot_width * 0.50, plot_length * 0.25, MIN_DIMS['Bedroom 3'], 'S')

    plan_data_2 = {
        'Master Bedroom': (plot_width * 0.25, plot_length * 0.25, MIN_DIMS['Master Bedroom'], 'SW'),
        'Kitchen':        (plot_width * 0.75, plot_length * 0.75, MIN_DIMS['Kitchen'],        'NE-DEFECT'),
        'Pooja Room':     (plot_width * 0.75, plot_length * 0.25, MIN_DIMS['Pooja Room'],     'SE'),
        'Toilet':         (plot_width * 0.25, plot_length * 0.75, MIN_DIMS['Toilet'],         'NW'),
        'Bedroom 2':      (plot_width * 0.50, plot_length * 0.75, MIN_DIMS['Bedroom 2'],      'N'),
        'Living Room':    (cx,                plot_length * 0.50, MIN_DIMS['Living Room'],    'Center/E'),
    }
    if num_bhk == 3:
        plan_data_2['Bedroom 3'] = (plot_width * 0.50, plot_length * 0.25, MIN_DIMS['Bedroom 3'], 'S')

    return [
        {'title': 'Option 1: Traditional Layout',                   'data': plan_data_1},
        {'title': 'Option 2: High Flexibility (Check for Dosha)',    'data': plan_data_2},
    ]


# ─────────────────────────────────────────────
# 5. VASTU SCORE CALCULATOR
# ─────────────────────────────────────────────
def calculate_vastu_score(plan_data):
    """
    Returns (score_pct, compliant_rooms, defect_rooms, neutral_rooms).
    Only rooms that have a defined ideal zone are scored.
    """
    compliant = []
    defects   = []
    neutral   = []

    for room, (_, _, _, zone) in plan_data.items():
        if room in ROOM_RULES:
            if ROOM_RULES[room] == zone:
                compliant.append(room)
            else:
                defects.append(room)
        else:
            neutral.append(room)

    scored_total = len(compliant) + len(defects)
    score_pct = int((len(compliant) / scored_total) * 100) if scored_total else 100
    return score_pct, compliant, defects, neutral


# ─────────────────────────────────────────────
# 6. THEME DETECTION + FLOOR PLAN DRAWING
# ─────────────────────────────────────────────
def get_theme_colors():
    """
    Detects Streamlit's current theme and returns a dict of plot colours.
    Falls back to light if undetectable.
    """
    try:
        theme = st.get_option("theme.base")
    except Exception:
        theme = "light"

    if theme == "dark":
        return {
            "fig_bg":      "#0f0a04",
            "plot_face":   "#1a1008",
            "plot_edge":   "#f5d9a8",
            "compass":     "#f5d9a8",
            "compass_n":   "#e4b87a",
            "facing_txt":  "#e4b87a",
            "title_txt":   "#f5d9a8",
        }
    else:
        return {
            "fig_bg":      "#f0f4f8",
            "plot_face":   "#f7f9fc",
            "plot_edge":   "#1e2c3a",
            "compass":     "#1e2c3a",
            "compass_n":   "#e05a4e",
            "facing_txt":  "#e05a4e",
            "title_txt":   "#1e2c3a",
        }


def _room_status(room, zone):
    is_compliant = room in ROOM_RULES and ROOM_RULES[room] == zone
    is_defect    = 'DEFECT' in zone or (room in ROOM_RULES and not is_compliant)
    if is_compliant: return 'compliant'
    if is_defect:    return 'defect'
    return 'neutral'


def draw_compass(ax, x, y, size, tc):
    """Draws N/S/E/W compass rose using theme colours tc."""
    offsets = {'N': (0, 1), 'S': (0, -1), 'E': (1, 0), 'W': (-1, 0)}
    for label, (dx, dy) in offsets.items():
        color = tc["compass_n"] if label == 'N' else tc["compass"]
        lw    = 1.8 if label == 'N' else 1.0
        ax.annotate(
            '', xy=(x + dx * size, y + dy * size),
            xytext=(x, y),
            arrowprops=dict(arrowstyle='->', color=color, lw=lw)
        )
        ax.text(
            x + dx * size * 1.38, y + dy * size * 1.38,
            label,
            ha='center', va='center',
            fontsize=8,
            fontweight='bold' if label == 'N' else 'normal',
            color=color
        )
    ax.plot(x, y, 'o', color=tc["compass_n"], markersize=4)


def plot_plan(plan_data, plot_w, plot_l, title, facing):
    """Renders the floor plan. Returns (fig, png_bytes)."""
    tc  = get_theme_colors()
    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor(tc["fig_bg"])
    ax.set_facecolor(tc["fig_bg"])

    # Plot boundary
    ax.add_patch(plt.Rectangle(
        (0, 0), plot_w, plot_l,
        edgecolor=tc["plot_edge"], facecolor=tc["plot_face"],
        linewidth=2.5, zorder=1
    ))

    for room, (x_pos, y_pos, dims, zone) in plan_data.items():
        w, l   = dims
        status = _room_status(room, zone)
        color  = ROOM_COLORS[status]

        rect = plt.Rectangle(
            (x_pos - w / 2, y_pos - l / 2), w, l,
            edgecolor='white', facecolor=color,
            alpha=0.82, linewidth=1.5, zorder=2
        )
        ax.add_patch(rect)

        clean_zone = zone.replace('-DEFECT', '')
        ax.text(x_pos, y_pos + 0.8, room,
                ha='center', va='center',
                fontsize=8.5, color='white', fontweight='bold', zorder=3)
        ax.text(x_pos, y_pos - 0.8, f'({clean_zone})',
                ha='center', va='center',
                fontsize=7.5, color='white', alpha=0.9, zorder=3)

    # Compass
    compass_x = plot_w - max(plot_w * 0.12, 4)
    compass_y = max(plot_l * 0.10, 4)
    draw_compass(ax, compass_x, compass_y, size=min(plot_w, plot_l) * 0.07, tc=tc)

    # Facing label
    ax.text(
        plot_w / 2, -plot_l * 0.06,
        f'Facing: {facing}  ▲',
        ha='center', va='top',
        fontsize=9, color=tc["facing_txt"], fontstyle='italic'
    )

    ax.set_xlim(-plot_w * 0.05, plot_w * 1.05)
    ax.set_ylim(-plot_l * 0.12, plot_l * 1.08)
    ax.set_title(title, fontsize=13, fontweight='bold', color=tc["title_txt"], pad=12)
    ax.set_aspect('equal', adjustable='box')
    ax.axis('off')
    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=180, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    buf.seek(0)
    png_bytes = buf.read()

    return fig, png_bytes


# ─────────────────────────────────────────────
# 7. SESSION STATE HELPERS
# ─────────────────────────────────────────────
def generate_and_store_plans(plot_w, plot_l, facing, num_bhk):
    with st.spinner('Calculating Vastu layouts…'):
        time.sleep(0.8)
        st.session_state['plans']    = generate_plan_options(plot_w, plot_l, facing, num_bhk)
        st.session_state['inputs']   = (plot_w, plot_l, facing, num_bhk)
        st.session_state['ready']    = True
    st.toast('Layouts generated!', icon='🏠')


# ─────────────────────────────────────────────
# 8. SCORE CARD HTML HELPERS
# ─────────────────────────────────────────────
def score_class(pct):
    if pct >= 75: return 'score-high'
    if pct >= 50: return 'score-medium'
    return 'score-low'

def score_label(pct):
    if pct >= 75: return '✅ Highly Compliant'
    if pct >= 50: return '⚠️ Partially Compliant'
    return '❌ Low Compliance'

def progress_color(pct):
    if pct >= 75: return '#4CAF50'
    if pct >= 50: return '#FFC107'
    return '#F44336'

def room_tag(status):
    if status == 'compliant': return '<span class="tag tag-ok">✔ Compliant</span>'
    if status == 'defect':    return '<span class="tag tag-defect">✘ Defect</span>'
    return '<span class="tag tag-neutral">● Neutral</span>'


# ─────────────────────────────────────────────
# 9. MAIN APP
# ─────────────────────────────────────────────
def main():
    if 'ready' not in st.session_state:
        st.session_state['ready'] = False

    # Hero
    st.markdown("""
    <div class="hero">
        <h1>🏠 VastuLeap</h1>
        <p>Rule-based Vastu Shastra floor plan generator — enter your plot details and get compliant layout options instantly.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Input panel ──────────────────────────
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            plot_w = st.number_input('Plot Width (ft)', min_value=10, value=30, step=5, key='width')
        with c2:
            plot_l = st.number_input('Plot Length (ft)', min_value=10, value=40, step=5, key='length')
        with c3:
            facing = st.selectbox('Facing Direction', ['East', 'North', 'West', 'South'], key='facing')
        with c4:
            num_bhk = st.selectbox('Bedrooms (BHK)', [2, 3], key='bhk')

        st.markdown('</div>', unsafe_allow_html=True)

    st.button(
        '🔮 Generate Vastu Plans',
        use_container_width=True,
        type='primary',
        on_click=generate_and_store_plans,
        args=(plot_w, plot_l, facing, num_bhk)
    )

    # ── Vastu rules reference (collapsed) ────
    with st.expander('📖 Key Vastu Principles', expanded=False):
        cols = st.columns(4)
        for i, (room, direction) in enumerate(ROOM_RULES.items()):
            with cols[i % 4]:
                tip = DIRECTION_TIPS.get(direction, '')
                st.markdown(f"**{room}**  \n`{direction}` — {tip}")

    st.divider()

    # ── Results ──────────────────────────────
    if not st.session_state.get('ready'):
        st.info("Configure your plot above and click **Generate Vastu Plans**.")
        return

    plans = st.session_state.get('plans', [])
    inputs = st.session_state.get('inputs', (plot_w, plot_l, facing, num_bhk))
    pw, pl, fc, _ = inputs

    if not plans:
        st.error("Could not generate plans. Try different dimensions.")
        return

    st.subheader("Generated Layout Options")

    for plan in plans:
        score_pct, compliant_rooms, defect_rooms, neutral_rooms = calculate_vastu_score(plan['data'])
        fig, png_bytes = plot_plan(plan['data'], pw, pl, plan['title'], fc)

        col_fig, col_info = st.columns([1.1, 0.9])

        # ── Floor plan ───────────────────────
        with col_fig:
            st.pyplot(fig)
            plt.close(fig)

            fname = plan['title'].replace(' ', '_').replace(':', '').replace('/', '-') + '.png'
            st.download_button(
                label='⬇ Download as PNG',
                data=png_bytes,
                file_name=fname,
                mime='image/png',
                use_container_width=True
            )

        # ── Score card + room details ─────────
        with col_info:
            s_class = score_class(score_pct)
            s_label = score_label(score_pct)
            p_color = progress_color(score_pct)

            st.markdown(f"""
            <div class="card">
                <div class="card-title">Vastu Compliance Score</div>
                <span class="score-badge {s_class}">{s_label}</span>
                <div class="score-number">{score_pct}%</div>
                <div class="progress-wrap">
                    <div class="progress-fill" style="width:{score_pct}%; background:{p_color};"></div>
                </div>
                <div class="score-meta">
                    {len(compliant_rooms)} compliant &nbsp;·&nbsp; {len(defect_rooms)} defect(s) &nbsp;·&nbsp; {len(neutral_rooms)} neutral
                </div>
            """, unsafe_allow_html=True)

            # Room-by-room table
            st.markdown('<div class="room-label-heading">Room Placement Details</div>', unsafe_allow_html=True)
            for room, (_, _, _, zone) in plan['data'].items():
                status    = _room_status(room, zone)
                clean_z   = zone.replace('-DEFECT', '')
                ideal     = ROOM_RULES.get(room, '—')
                tag_html  = room_tag(status)
                ideal_txt = f'<span class="ideal-text">Ideal: {ideal}</span>' if room in ROOM_RULES else ''
                st.markdown(f"""
                <div class="room-row">
                    <span><strong>{room}</strong><br>
                    <span class="zone-text">Zone: {clean_z}</span> {ideal_txt}</span>
                    {tag_html}
                </div>
                """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div style="margin-bottom:2rem;"></div>', unsafe_allow_html=True)


if __name__ == '__main__':
    main()