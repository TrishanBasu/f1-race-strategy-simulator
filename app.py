
import streamlit as st
import pandas as pd


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="F1 Race Strategy Simulator",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# F1 RED / BLACK THEME
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at top right,
            rgba(225, 6, 0, 0.13),
            transparent 28%
        ),
        linear-gradient(
            135deg,
            #050505 0%,
            #0b0b0b 45%,
            #111111 100%
        );

    color: #f5f5f5;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}


/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #090909 0%,
        #111111 100%
    );

    border-right: 1px solid #292929;
}

section[data-testid="stSidebar"] * {
    color: #f2f2f2;
}


/* HEADER */

.hero-title {
    font-size: 3.2rem;
    font-weight: 900;
    letter-spacing: -2px;
    margin-bottom: 0;
    color: #ffffff;
}

.hero-title span {
    color: #e10600;
}

.hero-subtitle {
    color: #a7a7a7;
    font-size: 1.05rem;
    margin-top: 5px;
    margin-bottom: 25px;
}

.red-line {
    height: 4px;
    width: 100%;

    background: linear-gradient(
        90deg,
        #e10600 0%,
        #e10600 35%,
        #303030 35%,
        #303030 100%
    );

    margin: 15px 0 25px 0;
}


/* CARDS */

.f1-card {
    background: linear-gradient(
        145deg,
        #151515,
        #0d0d0d
    );

    border: 1px solid #292929;
    border-left: 4px solid #e10600;

    border-radius: 10px;

    padding: 18px 20px;

    margin-bottom: 15px;
}

.f1-card h3 {
    margin-top: 0;
    color: white;
    font-size: 1.05rem;
}

.f1-card p {
    color: #aaaaaa;
}


/* SECTION HEADERS */

.section-header {
    font-size: 1.45rem;
    font-weight: 800;

    margin-top: 30px;
    margin-bottom: 15px;

    border-left: 5px solid #e10600;

    padding-left: 12px;
}


/* METRIC CARDS */

.metric-card {
    background: #111111;

    border: 1px solid #2b2b2b;

    border-radius: 10px;

    padding: 18px;

    text-align: center;

    min-height: 115px;
}

.metric-label {
    color: #888888;

    font-size: 0.78rem;

    text-transform: uppercase;

    letter-spacing: 1px;

    font-weight: 700;
}

.metric-value {
    color: #ffffff;

    font-size: 1.65rem;

    font-weight: 900;

    margin-top: 7px;
}

.metric-red {
    color: #e10600;
}


/* WINNER */

.winner-card {
    background:
        linear-gradient(
            135deg,
            rgba(225, 6, 0, 0.18),
            rgba(10, 10, 10, 0.96)
        );

    border: 1px solid #e10600;

    border-radius: 12px;

    padding: 24px;

    margin: 20px 0;

    box-shadow:
        0 0 30px rgba(225, 6, 0, 0.08);
}

.winner-title {
    color: #e10600;

    text-transform: uppercase;

    font-size: 0.85rem;

    font-weight: 800;

    letter-spacing: 1.5px;
}


/* INFO */

.info-box {
    background: #111111;

    border: 1px solid #303030;

    border-radius: 9px;

    padding: 15px 18px;

    color: #bdbdbd;
}


/* BUTTON */

.stButton > button {
    background: #e10600 !important;

    color: white !important;

    border: none !important;

    border-radius: 7px !important;

    font-weight: 800 !important;

    min-height: 45px;

    transition: 0.2s ease;
}

.stButton > button:hover {
    background: #ff180f !important;

    box-shadow:
        0 0 18px rgba(225, 6, 0, 0.35);

    transform: translateY(-1px);
}


/* INPUTS */

div[data-baseweb="select"] > div {
    background-color: #171717;

    border-color: #353535;
}

.stNumberInput input {
    background-color: #171717 !important;

    color: white !important;

    border-color: #353535 !important;
}


/* FOOTER */

.footer {
    text-align: center;

    color: #666666;

    font-size: 0.8rem;

    padding: 30px 0 10px 0;
}


/* BADGES */

.badge {
    display: inline-block;

    padding: 5px 10px;

    border-radius: 20px;

    background: #242424;

    color: #dddddd;

    font-size: 0.75rem;

    font-weight: 700;

    margin-right: 5px;
}

.badge-red {
    background: rgba(225, 6, 0, 0.18);

    color: #ff4b45;

    border: 1px solid rgba(225, 6, 0, 0.4);
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATASET
# ============================================================

@st.cache_data
def load_dataset():

    df = pd.read_csv(
        "f1_2025_strategy_dataset.csv"
    )

    df.columns = [
        str(c).strip()
        for c in df.columns
    ]

    return df


try:

    races_df = load_dataset()

except Exception:

    st.error(
        "Could not load "
        "f1_2025_strategy_dataset.csv. "
        "Make sure the CSV is in the same "
        "GitHub repository as app.py."
    )

    st.stop()


# ============================================================
# 2025 RACE DATA
# ============================================================

# Numerical pace, pit-loss and circuit-stress values
# are simulation assumptions, not official F1 measurements.

RACE_DEFAULTS = {

    "Australia": {
        "circuit": "Albert Park",
        "laps": 57,
        "pace": 86.5,
        "pit_loss": 22.5,
        "stress": 0.95
    },

    "China": {
        "circuit": "Shanghai",
        "laps": 56,
        "pace": 96.5,
        "pit_loss": 24.0,
        "stress": 0.95
    },

    "Japan": {
        "circuit": "Suzuka",
        "laps": 53,
        "pace": 94.5,
        "pit_loss": 23.5,
        "stress": 1.25
    },

    "Bahrain": {
        "circuit": "Bahrain International Circuit",
        "laps": 57,
        "pace": 96.5,
        "pit_loss": 22.0,
        "stress": 1.30
    },

    "Saudi Arabia": {
        "circuit": "Jeddah Corniche",
        "laps": 50,
        "pace": 92.5,
        "pit_loss": 21.0,
        "stress": 0.90
    },

    "Miami": {
        "circuit": "Miami",
        "laps": 57,
        "pace": 91.5,
        "pit_loss": 22.3,
        "stress": 0.90
    },

    "Emilia-Romagna": {
        "circuit": "Imola",
        "laps": 63,
        "pace": 87.5,
        "pit_loss": 23.5,
        "stress": 1.00
    },

    "Monaco": {
        "circuit": "Monaco",
        "laps": 78,
        "pace": 80.5,
        "pit_loss": 24.5,
        "stress": 0.85
    },

    "Spain": {
        "circuit": "Barcelona-Catalunya",
        "laps": 66,
        "pace": 82.5,
        "pit_loss": 22.2,
        "stress": 1.15
    },

    "Canada": {
        "circuit": "Circuit Gilles-Villeneuve",
        "laps": 70,
        "pace": 76.5,
        "pit_loss": 19.0,
        "stress": 0.90
    },

    "Austria": {
        "circuit": "Red Bull Ring",
        "laps": 70,
        "pace": 72.0,
        "pit_loss": 20.0,
        "stress": 0.95
    },

    "Great Britain": {
        "circuit": "Silverstone",
        "laps": 52,
        "pace": 95.0,
        "pit_loss": 29.0,
        "stress": 1.20
    },

    "Belgium": {
        "circuit": "Spa-Francorchamps",
        "laps": 44,
        "pace": 110.0,
        "pit_loss": 23.5,
        "stress": 1.15
    },

    "Hungary": {
        "circuit": "Hungaroring",
        "laps": 70,
        "pace": 80.0,
        "pit_loss": 20.0,
        "stress": 1.10
    },

    "Netherlands": {
        "circuit": "Zandvoort",
        "laps": 72,
        "pace": 77.5,
        "pit_loss": 17.6,
        "stress": 1.15
    },

    "Italy": {
        "circuit": "Monza",
        "laps": 53,
        "pace": 83.0,
        "pit_loss": 24.8,
        "stress": 0.90
    },

    "Azerbaijan": {
        "circuit": "Baku City Circuit",
        "laps": 51,
        "pace": 102.0,
        "pit_loss": 21.0,
        "stress": 0.85
    },

    "Singapore": {
        "circuit": "Marina Bay",
        "laps": 62,
        "pace": 101.0,
        "pit_loss": 22.0,
        "stress": 1.20
    },

    "United States": {
        "circuit": "Circuit of the Americas",
        "laps": 56,
        "pace": 99.0,
        "pit_loss": 21.5,
        "stress": 1.00
    },

    "Mexico": {
        "circuit": "Mexico City",
        "laps": 71,
        "pace": 80.0,
        "pit_loss": 21.0,
        "stress": 0.95
    },

    "Brazil": {
        "circuit": "Interlagos",
        "laps": 71,
        "pace": 75.5,
        "pit_loss": 23.5,
        "stress": 1.05
    },

    "Las Vegas": {
        "circuit": "Las Vegas Strip",
        "laps": 50,
        "pace": 96.5,
        "pit_loss": 21.5,
        "stress": 0.85
    },

    "Qatar": {
        "circuit": "Lusail",
        "laps": 57,
        "pace": 90.0,
        "pit_loss": 30.0,
        "stress": 1.35
    },

    "Abu Dhabi": {
        "circuit": "Yas Marina",
        "laps": 58,
        "pace": 89.0,
        "pit_loss": 22.0,
        "stress": 0.95
    }
}


# ============================================================
# TYRE MODEL
# ============================================================

TYRE_MODEL = {

    "C1": {
        "display": "Hard",
        "offset": 0.42,
        "peak_start": 3,
        "peak_end": 20,
        "critical_lap": 42,
        "deg_rate": 0.032,
        "late_rate": 0.060,
        "min_laps": 24,
        "max_laps": 42
    },

    "C2": {
        "display": "Hard",
        "offset": 0.30,
        "peak_start": 3,
        "peak_end": 18,
        "critical_lap": 38,
        "deg_rate": 0.036,
        "late_rate": 0.065,
        "min_laps": 22,
        "max_laps": 38
    },

    "C3": {
        "display": "Medium",
        "offset": 0.20,
        "peak_start": 2,
        "peak_end": 14,
        "critical_lap": 32,
        "deg_rate": 0.045,
        "late_rate": 0.078,
        "min_laps": 18,
        "max_laps": 33
    },

    "C4": {
        "display": "Medium",
        "offset": 0.05,
        "peak_start": 2,
        "peak_end": 12,
        "critical_lap": 29,
        "deg_rate": 0.050,
        "late_rate": 0.082,
        "min_laps": 17,
        "max_laps": 31
    },

    "C5": {
        "display": "Soft",
        "offset": -0.22,
        "peak_start": 2,
        "peak_end": 8,
        "critical_lap": 18,
        "deg_rate": 0.082,
        "late_rate": 0.125,
        "min_laps": 9,
        "max_laps": 20
    },

    "C6": {
        "display": "Soft",
        "offset": -0.32,
        "peak_start": 2,
        "peak_end": 7,
        "critical_lap": 15,
        "deg_rate": 0.092,
        "late_rate": 0.135,
        "min_laps": 8,
        "max_laps": 18
    },

    "INT": {
        "display": "Intermediate",
        "offset": 4.50,
        "peak_start": 2,
        "peak_end": 7,
        "critical_lap": 16,
        "deg_rate": 0.075,
        "late_rate": 0.100
    }
}


# ============================================================
# CAR PERFORMANCE CLASSES
# ============================================================

CLASS_DATA = {

    "Class 1": {
        "constructors": "McLaren • Mercedes",
        "pace_delta": -0.75
    },

    "Class 2": {
        "constructors": "Red Bull • Ferrari",
        "pace_delta": -0.35
    },

    "Class 3": {
        "constructors": "Williams • Aston Martin",
        "pace_delta": 0.00
    },

    "Class 4": {
        "constructors": "Alpine • Haas",
        "pace_delta": 0.35
    },

    "Class 5": {
        "constructors": "Racing Bulls • Sauber",
        "pace_delta": 0.70
    },

    "Class 6": {
        "constructors": "Audi • Cadillac",
        "pace_delta": 1.05
    }
}


# ============================================================
# 2025 PIRELLI NOMINATIONS
# ============================================================

PIRELLI_2025 = {

    "Australia": ["C3", "C4", "C5"],
    "China": ["C2", "C3", "C4"],
    "Japan": ["C1", "C2", "C3"],
    "Bahrain": ["C1", "C2", "C3"],
    "Saudi Arabia": ["C3", "C4", "C5"],
    "Miami": ["C3", "C4", "C5"],
    "Emilia-Romagna": ["C4", "C5", "C6"],
    "Monaco": ["C4", "C5", "C6"],
    "Spain": ["C1", "C2", "C3"],
    "Canada": ["C4", "C5", "C6"],
    "Austria": ["C3", "C4", "C5"],
    "Great Britain": ["C2", "C3", "C4"],
    "Belgium": ["C1", "C3", "C4"],
    "Hungary": ["C3", "C4", "C5"],
    "Netherlands": ["C2", "C3", "C4"],
    "Italy": ["C3", "C4", "C5"],
    "Azerbaijan": ["C4", "C5", "C6"],
    "Singapore": ["C3", "C4", "C5"],
    "United States": ["C1", "C3", "C4"],
    "Mexico": ["C2", "C4", "C5"],
    "Brazil": ["C2", "C3", "C4"],
    "Las Vegas": ["C3", "C4", "C5"],
    "Qatar": ["C1", "C2", "C3"],
    "Abu Dhabi": ["C3", "C4", "C5"]
}


# ============================================================
# DISPLAY HELPERS
# ============================================================

def tyre_role(compound, country=None):

    if compound == "INT":
        return "Intermediate"

    # Pirelli nominates three dry compounds for each weekend.
    # Within that nominated set, the hardest compound is the
    # race Hard, the middle compound is Medium, and the softest
    # compound is Soft. This keeps the tyre labels correct for
    # every 2025 race weekend.
    if country in PIRELLI_2025:
        nominated = PIRELLI_2025[country]
        if compound in nominated:
            role_index = nominated.index(compound)
            return ["Hard", "Medium", "Soft"][role_index]

    return TYRE_MODEL[compound]["display"]


def tyre_name(compound, country=None):

    return tyre_role(compound, country)


def tyre_display_with_code(compound, country=None):

    if compound == "INT":
        return "Intermediate"

    return (
        f"{tyre_role(compound, country)} "
        f"({compound})"
    )


def strategy_display(strategy, country=None):

    return " → ".join(
        tyre_display_with_code(x, country)
        for x in strategy
    )


def format_time(seconds):

    minutes = int(
        seconds // 60
    )

    secs = (
        seconds
        - minutes * 60
    )

    return f"{minutes}:{secs:05.2f}"


def format_delta(seconds):

    sign = (
        "+"
        if seconds >= 0
        else "-"
    )

    return (
        f"{sign}"
        f"{abs(seconds):.2f}s"
    )


# ============================================================
# TYRE DEGRADATION
# ============================================================

def calculate_tyre_degradation(
    compound,
    tyre_age,
    circuit_stress
):

    tyre = TYRE_MODEL[compound]

    if tyre_age <= 0:
        return 0.0

    peak_start = tyre["peak_start"]

    peak_end = tyre["peak_end"]

    critical = tyre["critical_lap"]

    # -----------------------------
    # Warm-up
    # -----------------------------

    if tyre_age <= peak_start:

        raw = (
            0.018
            * tyre_age
        )

    # -----------------------------
    # Peak
    # -----------------------------

    elif tyre_age <= peak_end:

        warmup = (
            0.018
            * peak_start
        )

        extra_age = (
            tyre_age
            - peak_start
        )

        raw = (
            warmup
            + 0.012
            * extra_age
            + 0.004
            * (
                extra_age ** 1.35
            )
        )

    # -----------------------------
    # Degrading
    # -----------------------------

    elif tyre_age <= critical:

        peak_value = (
            calculate_tyre_degradation(
                compound,
                peak_end,
                1.0
            )
        )

        extra_age = (
            tyre_age
            - peak_end
        )

        peak_length = max(
            critical - peak_end,
            1
        )

        raw = (
            peak_value
            + tyre["deg_rate"]
            * (
                extra_age ** 1.28
                / (
                    peak_length ** 0.20
                )
            )
        )

    # -----------------------------
    # Critical
    # -----------------------------

    else:

        critical_value = (
            calculate_tyre_degradation(
                compound,
                critical,
                1.0
            )
        )

        extra_age = (
            tyre_age
            - critical
        )

        raw = (
            critical_value
            + tyre["late_rate"]
            * (
                extra_age ** 1.42
            )
        )

    return round(
        raw * circuit_stress,
        3
    )


# ============================================================
# TYRE PHASE
# ============================================================

def tyre_phase(
    compound,
    tyre_age
):

    tyre = TYRE_MODEL[compound]

    if tyre_age <= 0:
        return "New tyre"

    if tyre_age <= tyre["peak_start"]:
        return "Warm-up"

    if tyre_age <= tyre["peak_end"]:
        return "Peak performance"

    if tyre_age < tyre["critical_lap"]:
        return "Degrading"

    return "Critical degradation"


# ============================================================
# LAP TIME MODEL
# ============================================================

def calculate_lap_time(
    country,
    compound,
    tyre_age,
    car_class,
    previous_lap=None,
    wet=False
):

    race = RACE_DEFAULTS[country]
    tyre = TYRE_MODEL[compound]
    base = race["pace"]

    car_delta = CLASS_DATA[car_class]["pace_delta"]

    # Weekend role drives the main dry-pace gap. The same physical C-code
    # can be Hard at one race and Soft at another.
    if compound == "INT":
        tyre_delta = tyre["offset"]
    else:
        role = get_compound_role_index(country, compound)
        role_delta = {
            0: 0.20,
            1: 0.00,
            2: -0.40
        }[role]
        physical_adjustment = {
            "C1": 0.04,
            "C2": 0.02,
            "C3": 0.00,
            "C4": -0.02,
            "C5": -0.04,
            "C6": -0.06
        }.get(compound, 0.0)
        tyre_delta = role_delta + physical_adjustment

    degradation = calculate_tyre_degradation(
        compound,
        tyre_age,
        race["stress"]
    )

    if compound != "INT":
        role_deg_factor = {
            0: 0.90,
            1: 1.00,
            2: 1.25
        }[get_compound_role_index(country, compound)]
        degradation *= role_deg_factor

    # Universal role-aware degradation scaling.
    # The weekend role controls how aggressively a tyre loses performance;
    # circuit stress then amplifies the effect.
    if compound != "INT":
        role = get_compound_role_index(country, compound)
        stress_factor = 0.90 + 0.30 * race["stress"]

        role_deg_factor = {
            0: 0.82,   # Hard
            1: 1.00,   # Medium
            2: 1.48    # Soft
        }[role]
        degradation *= role_deg_factor * stress_factor / 1.20

    # Strong progressive long-stint penalty. This is deliberately smooth,
    # not a hard-coded track rule, so every circuit gets different behavior
    # from its own stress value and nominated tyre roles.
    overuse_penalty = 0.0
    if compound != "INT":
        role = get_compound_role_index(country, compound)
        stress = race["stress"]

        useful_age = {
            0: 28.0,   # Hard
            1: 21.0,   # Medium
            2: 12.5    # Soft
        }[role] + (1.0 - stress) * {
            0: 4.0,
            1: 3.0,
            2: 4.0
        }[role]

        rate = {
            0: 0.018,
            1: 0.035,
            2: 0.30
        }[role]

        if tyre_age > useful_age:
            extra = tyre_age - useful_age
            stress_factor = 0.90 + 0.30 * stress
            overuse_penalty = rate * (extra ** 1.65) * stress_factor

        # Once a Soft tyre is past its useful window, make every additional
        # lap increasingly expensive. This is what stops 20-25 lap Soft
        # stints from beating sensible Medium/Hard race strategies.
        if role == 2 and tyre_age > useful_age + 3:
            extra = tyre_age - useful_age - 3
            overuse_penalty += 0.12 * (extra ** 1.75) * (0.90 + 0.30 * stress)

    rain_delta = 0.0

    if wet:
        if compound == "INT":
            rain_delta = -17.5
        else:
            rain_delta = 10.0 + tyre_age * 0.08

    lap_time = (
        base
        + car_delta
        + tyre_delta
        + degradation
        + overuse_penalty
        + rain_delta
    )

    if previous_lap is not None:
        lap_time = (
            0.85 * lap_time
            + 0.15 * previous_lap
        )

    return lap_time


# ============================================================
# DRY STRATEGY GENERATOR
# ============================================================

def generate_dry_strategies(country):

    available = PIRELLI_2025.get(
        country,
        ["C3", "C4", "C5"]
    )

    strategies = []

    # -----------------------------
    # 1 stop
    # -----------------------------

    for a in available:

        for b in available:

            if a == b:
                continue

            strategies.append(
                {
                    "compounds": [a, b],
                    "stops": 1
                }
            )

    # -----------------------------
    # 2 stops
    # -----------------------------

    for a in available:

        for b in available:

            for c in available:

                if len({a, b, c}) < 2:
                    continue

                strategies.append(
                    {
                        "compounds": [
                            a,
                            b,
                            c
                        ],
                        "stops": 2
                    }
                )

    # -----------------------------
    # 3 stops
    # -----------------------------

    for a in available:

        for b in available:

            for c in available:

                for d in available:

                    if len({
                        a,
                        b,
                        c,
                        d
                    }) < 2:

                        continue

                    strategies.append(
                        {
                            "compounds": [
                                a,
                                b,
                                c,
                                d
                            ],
                            "stops": 3
                        }
                    )

    return strategies


# ============================================================
# STINT LENGTHS
# ============================================================

def get_compound_role_index(country, compound):
    """Return the weekend role: 0=Hard, 1=Medium, 2=Soft."""
    if compound == "INT":
        return None
    nominated = PIRELLI_2025.get(country, [])
    if compound in nominated:
        return nominated.index(compound)
    return 1


def effective_tyre_limits(country, compound):
    """Universal realistic race-life envelope based on weekend tyre role.

    C1-C6 are physical compounds. Their race role is determined by the
    weekend nomination. Soft is intentionally a short-stint tyre, Medium a
    medium/long-stint tyre, and Hard the long-stint tyre. Circuit stress
    tightens the envelope on demanding tracks.
    """
    tyre = TYRE_MODEL[compound]

    if compound == "INT":
        return (1, RACE_DEFAULTS[country]["laps"])

    role = get_compound_role_index(country, compound)
    stress = RACE_DEFAULTS[country]["stress"]
    laps = RACE_DEFAULTS[country]["laps"]

    # These are useful race windows, not absolute tyre failure limits.
    # Lower-stress circuits permit slightly longer stints.
    if role == 2:       # Soft
        useful = 12.0 + (1.0 - stress) * 5.0
        absolute = 18.0 + (1.0 - stress) * 5.0
        min_laps = max(8, tyre.get("min_laps", 8))
    elif role == 1:     # Medium
        useful = 21.0 + (1.0 - stress) * 5.0
        absolute = 31.0 + (1.0 - stress) * 6.0
        min_laps = max(12, tyre.get("min_laps", 12))
    else:               # Hard
        useful = 27.0 + (1.0 - stress) * 5.0
        absolute = 40.0 + (1.0 - stress) * 6.0
        min_laps = max(16, tyre.get("min_laps", 16))

    # Keep the limits physically sensible for the actual race distance.
    max_laps = min(laps, int(round(absolute)))
    return min_laps, max(min_laps, max_laps)


def get_stint_target_laps(country, compound):
    """Target realistic race mileage for the tyre's weekend role."""
    stress = RACE_DEFAULTS[country]["stress"]
    role = get_compound_role_index(country, compound)

    if role == 2:       # Soft
        target = 12.5 + (1.0 - stress) * 4.0
    elif role == 1:     # Medium
        target = 21.5 + (1.0 - stress) * 4.0
    else:               # Hard
        target = 28.5 + (1.0 - stress) * 4.0

    min_laps, max_laps = effective_tyre_limits(country, compound)
    return max(min_laps, min(max_laps, target))


def create_stints(total_laps, compounds, country=None):
    """Create a valid race-length split using weekend tyre roles."""
    if not compounds:
        return []
    if country is None:
        country = next(iter(RACE_DEFAULTS))

    limits = [effective_tyre_limits(country, c) for c in compounds]
    mins = [x[0] for x in limits]
    maxs = [x[1] for x in limits]

    if total_laps < sum(mins) or total_laps > sum(maxs):
        return []

    targets = [get_stint_target_laps(country, c) for c in compounds]
    total_target = sum(targets)
    lengths = [
        max(mins[i], min(maxs[i], int(round(total_laps * targets[i] / total_target))))
        for i in range(len(compounds))
    ]

    while sum(lengths) < total_laps:
        choices = [i for i in range(len(lengths)) if lengths[i] < maxs[i]]
        if not choices:
            return []
        idx = max(choices, key=lambda i: targets[i] - lengths[i])
        lengths[idx] += 1

    while sum(lengths) > total_laps:
        choices = [i for i in range(len(lengths)) if lengths[i] > mins[i]]
        if not choices:
            return []
        idx = max(choices, key=lambda i: lengths[i] - targets[i])
        lengths[idx] -= 1

    return lengths


def generate_stint_length_candidates(total_laps, compounds, country=None):
    """Generate deterministic, realistic stint allocations.

    Candidates stay close to role-based targets. This prevents the optimizer
    from exploiting equal-ish splits such as a 25-lap Soft stint.
    """
    if country is None:
        country = next(iter(RACE_DEFAULTS))

    base = create_stints(total_laps, compounds, country)
    if not base:
        return []

    candidates = {tuple(base)}
    limits = [effective_tyre_limits(country, c) for c in compounds]
    mins = [x[0] for x in limits]
    maxs = [x[1] for x in limits]

    # Only small reallocations around the realistic base allocation.
    for i in range(len(compounds)):
        for j in range(len(compounds)):
            if i == j:
                continue
            for shift in (-3, -2, 2, 3):
                trial = base.copy()
                trial[i] += shift
                trial[j] -= shift
                if all(mins[k] <= trial[k] <= maxs[k] for k in range(len(trial))):
                    candidates.add(tuple(trial))

    # For 3+ stints, allow small balancing changes.
    if len(compounds) >= 3:
        for i in range(len(compounds)):
            for j in range(len(compounds)):
                if i == j:
                    continue
                for k in range(len(compounds)):
                    if k in (i, j):
                        continue
                    trial = base.copy()
                    trial[i] += 2
                    trial[j] -= 1
                    trial[k] -= 1
                    if all(mins[x] <= trial[x] <= maxs[x] for x in range(len(trial))):
                        candidates.add(tuple(trial))

    return [list(x) for x in sorted(candidates)]


# ============================================================
# DRY STRATEGY SIMULATION
# ============================================================

def simulate_dry_strategy(
    country,
    strategy,
    car_class,
    starting_position,
    stint_lengths=None
):

    race = RACE_DEFAULTS[country]

    compounds = (
        strategy["compounds"]
    )

    if stint_lengths is None:
        stint_lengths = create_stints(
            race["laps"],
            compounds,
            country
        )

    total_time = 0.0

    previous_lap = None

    lap_records = []

    current_lap = 0

    # Small deterministic
    # starting-position effect.

    if starting_position <= 3:

        start_factor = -0.10

    elif starting_position >= 18:

        start_factor = 0.10

    else:

        start_factor = 0.0

    for stint_index, compound in enumerate(
        compounds
    ):

        stint_length = (
            stint_lengths[stint_index]
        )

        for age in range(
            1,
            stint_length + 1
        ):

            current_lap += 1

            lap_time = calculate_lap_time(
                country,
                compound,
                age,
                car_class,
                previous_lap,
                wet=False
            )

            if current_lap <= 3:

                lap_time += start_factor

            total_time += lap_time

            lap_records.append(
                {
                    "Lap": current_lap,
                    "Tyre": tyre_name(
                        compound, country
                    ),
                    "Compound": compound,
                    "Tyre Age": age,
                    "Phase": tyre_phase(
                        compound,
                        age
                    ),
                    "Lap Time (s)": round(
                        lap_time,
                        3
                    ),
                    "Condition": "Dry"
                }
            )

            previous_lap = lap_time

        # Pit stop
        if (
            stint_index
            < len(compounds) - 1
        ):

            total_time += (
                race["pit_loss"]
            )

            lap_records.append(
                {
                    "Lap":
                        f"Pit {stint_index + 1}",

                    "Tyre":
                        "PIT STOP",

                    "Compound":
                        "-",

                    "Tyre Age":
                        "-",

                    "Phase":
                        "-",

                    "Lap Time (s)":
                        round(
                            race["pit_loss"],
                            3
                        ),

                    "Condition":
                        "Pit"
                }
            )

    return {
        "total_time": total_time,
        "strategy": strategy,
        "stints": stint_lengths,
        "laps": pd.DataFrame(
            lap_records
        )
    }


# ============================================================
# DRY OPTIMIZER
# ============================================================

def optimize_dry_strategy(
    country,
    car_class,
    starting_position
):

    strategies = generate_dry_strategies(country)
    best_by_key = {}

    for strategy in strategies:
        compounds = tuple(strategy["compounds"])
        candidates = generate_stint_length_candidates(
            RACE_DEFAULTS[country]["laps"],
            strategy["compounds"],
            country
        )

        for stint_lengths in candidates:
            limits = [effective_tyre_limits(country, c) for c in strategy["compounds"]]
            valid = all(
                minimum <= length <= maximum
                for (minimum, maximum), length in zip(limits, stint_lengths)
            )
            if not valid:
                continue

            result = simulate_dry_strategy(
                country,
                strategy,
                car_class,
                starting_position,
                stint_lengths=stint_lengths
            )

            # Keep only the fastest allocation for a compound sequence.
            # This removes repeated rows that differ only by a tiny stint shift.
            key = (compounds, strategy["stops"])
            if key not in best_by_key or result["total_time"] < best_by_key[key]["total_time"]:
                best_by_key[key] = result

    results = list(best_by_key.values())
    results.sort(key=lambda x: x["total_time"])
    return results


# ============================================================
# ============================================================
# RAIN DURATION → FINAL TIME ADJUSTMENT
# ============================================================

def calculate_rain_laps(country, rain_duration_minutes):
    race = RACE_DEFAULTS[country]

    if rain_duration_minutes <= 0:
        return 0

    rain_seconds = rain_duration_minutes * 60
    return max(
        1,
        min(
            race["laps"],
            int(round(rain_seconds / race["pace"]))
        )
    )


def calculate_rain_impact(country, rain_duration_minutes):
    """
    Rain is not assigned an exact lap window.

    The normal dry-race strategy is simulated first.
    The user's rain duration is then converted into approximate
    wet laps and a deterministic time adjustment is added.

    The adjustment includes:
    - Intermediate tyre running time loss
    - pit stop onto Intermediate tyres
    - pit stop back to dry tyres
    - wet-condition transition/crossover loss
    """
    race = RACE_DEFAULTS[country]

    if rain_duration_minutes <= 0:
        return {
            "rain_laps": 0,
            "intermediate_loss": 0.0,
            "pit_loss": 0.0,
            "transition_loss": 0.0,
            "adjustment": 0.0,
        }

    rain_laps = calculate_rain_laps(
        country,
        rain_duration_minutes
    )

    # Approximate Intermediate pace disadvantage versus
    # the representative dry race pace. Circuit stress makes
    # wet running slightly more difficult at high-stress tracks.
    intermediate_penalty = (
        0.105
        + 0.015 * race["stress"]
    )

    intermediate_loss = (
        rain_laps
        * race["pace"]
        * intermediate_penalty
    )

    # A normal temporary rain period requires two tyre-change stops:
    # dry → Intermediate and Intermediate → dry.
    pit_loss = 2 * race["pit_loss"]

    # Small additional loss for the transition into/out of wet conditions.
    transition_loss = (
        min(rain_laps, 10)
        * 0.35
        * race["stress"]
    )

    adjustment = (
        intermediate_loss
        + pit_loss
        + transition_loss
    )

    return {
        "rain_laps": rain_laps,
        "intermediate_loss": intermediate_loss,
        "pit_loss": pit_loss,
        "transition_loss": transition_loss,
        "adjustment": adjustment,
    }


# HEADER
# ============================================================

st.markdown(
    '<div class="hero-title">'
    'F1 <span>RACE STRATEGY</span> SIMULATOR'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero-subtitle">
        Race strategy modelling • Tyre degradation •
        Pit-stop optimization • Rain impact
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="red-line"></div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    <h2 style="margin-bottom:5px;">
        🏎️ Race Setup
    </h2>

    <p style="color:#888;">
        Configure your simulated Grand Prix
    </p>
    """,
    unsafe_allow_html=True
)

countries = list(
    RACE_DEFAULTS.keys()
)

country = st.sidebar.selectbox(
    "🏁 2025 Grand Prix",
    countries,
    key="race_country_selector"
)

race = RACE_DEFAULTS[country]

st.sidebar.markdown(
    f"""
    <div class="f1-card">
        <b>{race['circuit']}</b><br>
        <span style="color:#888;">
            {race['laps']} laps
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

starting_position = st.sidebar.number_input(
    "Starting Position",
    min_value=1,
    max_value=20,
    value=10,
    step=1,
    key="starting_position_input"
)

class_options = list(
    CLASS_DATA.keys()
)

car_class = st.sidebar.selectbox(
    "Car Performance Class",
    class_options,
    key="car_performance_class_selector"
)

st.sidebar.markdown(
    f"""
    <div class="info-box">
        <b>{car_class}</b><br>
        <span style="color:#aaa;">
            {CLASS_DATA[car_class]['constructors']}
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

rain_option = st.sidebar.selectbox(
    "🌧️ Rain",
    [
        "No Rain",
        "Rain"
    ],
    key="rain_condition_selector"
)

rain_duration = 0

if rain_option == "Rain":
    rain_duration = st.sidebar.number_input(
        "Rain Duration (minutes)",
        min_value=5,
        max_value=180,
        value=30,
        step=5,
        key="rain_duration_input"
    )

    estimated_laps = calculate_rain_laps(
        country,
        rain_duration
    )

    st.sidebar.markdown(
        f"""
        <div class="info-box">
            <b>Estimated wet running</b><br>
            Approximately
            <b>{estimated_laps} laps</b>
        </div>
        """,
        unsafe_allow_html=True
    )

run_simulation = st.sidebar.button(
    "🏁 RUN SIMULATION",
    use_container_width=True
)


# ============================================================
# TOP METRICS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Grand Prix", country)

with col2:
    st.metric("Starting Position", f"P{starting_position}")

with col3:
    st.metric("Car Class", car_class)

with col4:
    if rain_option == "No Rain":
        condition_display = "Dry"
    else:
        condition_display = "Rain"
    st.metric("Conditions", condition_display)


# HOME SCREEN
# ============================================================

if not run_simulation:

    st.markdown(
        '<div class="section-header">'
        'How the simulator works'
        '</div>',
        unsafe_allow_html=True
    )

    info1, info2, info3 = st.columns(3)

    with info1:

        st.markdown(
            """
            <div class="f1-card">

                <h3>🏎️ Car Performance</h3>

                <p>
                Six simulated performance classes represent
                different constructor performance levels.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    with info2:

        st.markdown(
            """
            <div class="f1-card">

                <h3>🛞 Tyre Strategy</h3>

                <p>
                Hard, Medium and Soft tyres have different
                pace, warm-up, peak-performance and
                degradation characteristics.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    with info3:

        st.markdown(
            """
            <div class="f1-card">

                <h3>🌧️ Rain Strategy</h3>

                <p>
                Intermediate tyres are used during wet
                conditions and also experience tyre
                degradation.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    # --------------------------------------------------------
    # TYRE SELECTION
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-header">'
        '2025 Tyre Selection'
        '</div>',
        unsafe_allow_html=True
    )

    available = PIRELLI_2025.get(
        country,
        ["C3", "C4", "C5"]
    )

    tyre_text = " • ".join(
        tyre_display_with_code(x, country)
        for x in available
    )

    st.markdown(
        f"""
        <div class="info-box">

            <b>2025 nominated dry tyres:</b>
            &nbsp; {tyre_text}

            <br><br>

            <b>Weekend tyre roles:</b> Hard → Medium → Soft

            <br><br>

            <span class="badge badge-red">
                Intermediate available for wet conditions
            </span>

        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # SIMULATION MODEL
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-header">'
        'Simulation Model'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="f1-card">

        The simulator evaluates the race lap by lap.

        <br><br>

        <b>Tyre degradation is applied to:</b>

        <br><br>

        🟥 <b>Soft</b> — fastest initial pace,
        shorter useful life

        <br>

        🟡 <b>Medium</b> — balanced pace and durability

        <br>

        ⚪ <b>Hard</b> — slower initial pace,
        longest dry-tyre life

        <br>

        🟢 <b>Intermediate</b> — wet conditions

        <br><br>

        The model considers circuit stress, car class,
        tyre age and previous-lap pace.

        <br><br>

        The optimizer compares one-stop, two-stop and
        three-stop strategies.

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# ============================================================
# RUN SIMULATION
# ============================================================

if run_simulation:

    with st.spinner(
        "Running race strategy simulation..."
    ):

        # Always optimize the dry race first.
        # Rain is added as a final time adjustment.
        results = optimize_dry_strategy(
            country,
            car_class,
            starting_position
        )

        best = results[0]

        st.markdown(
            '<div class="section-header">'
            '🏆 Recommended Strategy'
            '</div>',
            unsafe_allow_html=True
        )

        st.success(
            "🏁 FASTEST SIMULATED DRY-RACE STRATEGY"
        )

        st.markdown(
            f"## 🏎️ "
            f"{strategy_display(best['strategy']['compounds'], country)}"
        )

        st.markdown(
            f"**Simulated dry GP time:** "
            f"`{format_time(best['total_time'])}`"
        )

        # --------------------------------------------------------
        # METRICS
        # --------------------------------------------------------

        m1, m2, m3, m4 = st.columns(4)

        with m1:
            st.metric(
                "Pit Stops",
                best["strategy"]["stops"]
            )

        with m2:
            st.metric(
                "Dry GP Time",
                format_time(best["total_time"])
            )

        with m3:
            st.metric(
                "Circuit",
                country
            )

        with m4:
            st.metric(
                "Car Class",
                car_class
            )

        # --------------------------------------------------------
        # STRATEGY COMPARISON
        # --------------------------------------------------------

        st.markdown(
            '<div class="section-header">'
            'Strategy Comparison'
            '</div>',
            unsafe_allow_html=True
        )

        comparison_rows = []

        best_time = best["total_time"]

        for i, result in enumerate(results[:10]):

            comparison_rows.append(
                {
                    "Rank":
                        i + 1,

                    "Strategy":
                        strategy_display(
                            result["strategy"]["compounds"],
                            country
                        ),

                    "Pit Stops":
                        result["strategy"]["stops"],

                    "Simulated Time":
                        format_time(
                            result["total_time"]
                        ),

                    "Gap":
                        (
                            "BEST"
                            if i == 0
                            else format_delta(
                                result["total_time"]
                                - best_time
                            )
                        )
                }
            )

        st.dataframe(
            pd.DataFrame(comparison_rows),
            use_container_width=True,
            hide_index=True
        )

        # --------------------------------------------------------
        # RECOMMENDED STINTS
        # --------------------------------------------------------

        st.markdown(
            '<div class="section-header">'
            'Recommended Stints'
            '</div>',
            unsafe_allow_html=True
        )

        stint_cols = st.columns(
            len(best["strategy"]["compounds"])
        )

        for i, compound in enumerate(
            best["strategy"]["compounds"]
        ):

            with stint_cols[i]:

                st.markdown(
                    f"### 🏁 Stint {i + 1}"
                )

                st.markdown(
                    f"## {tyre_name(compound, country)}"
                )

                st.caption(
                    f"Compound code: {compound} • "
                    f"Approx. {best['stints'][i]} laps"
                )

        # --------------------------------------------------------
        # LAP-BY-LAP SIMULATION
        # --------------------------------------------------------

        st.markdown(
            '<div class="section-header">'
            'Lap-by-Lap Simulation'
            '</div>',
            unsafe_allow_html=True
        )

        st.dataframe(
            best["laps"],
            use_container_width=True,
            hide_index=True,
            height=500
        )

        # --------------------------------------------------------
        # FINAL RAIN IMPACT
        # --------------------------------------------------------

        st.markdown(
            '<div class="section-header">'
            '🌧️ Rain Impact'
            '</div>',
            unsafe_allow_html=True
        )

        if rain_option == "No Rain" or rain_duration <= 0:

            st.info(
                "No rain adjustment applied. "
                "The GP time above is the final simulated time."
            )

        else:

            rain = calculate_rain_impact(
                country,
                rain_duration
            )

            adjusted_gp_time = (
                best["total_time"]
                + rain["adjustment"]
            )

            r1, r2, r3, r4 = st.columns(4)

            with r1:
                st.metric(
                    "Rain Duration",
                    f"{rain_duration:.0f} min"
                )

            with r2:
                st.metric(
                    "Estimated Wet Laps",
                    f"~{rain['rain_laps']}"
                )

            with r3:
                st.metric(
                    "Adjusted Rain Time",
                    f"+{format_time(rain['adjustment'])}"
                )

            with r4:
                st.metric(
                    "Adjusted GP Time",
                    format_time(adjusted_gp_time)
                )

            st.info(
                f"""
                **Rain duration:** {rain_duration:.0f} minutes

                **Estimated wet running:** approximately
                {rain["rain_laps"]} laps

                **Intermediate tyre running loss:**
                +{format_time(rain["intermediate_loss"])}

                **Two wet-condition tyre-change pit stops:**
                +{format_time(rain["pit_loss"])}

                **Wet-condition transition loss:**
                +{format_time(rain["transition_loss"])}

                **Total adjusted rain time:**
                +{format_time(rain["adjustment"])}

                ### 🏁 Final Estimated GP Time
                **{format_time(adjusted_gp_time)}**

                *Rain is modelled as a duration-based time adjustment,
                not as an exact rain window or weather forecast.*
                """
            )


# MODEL ASSUMPTIONS
# ============================================================

with st.expander(
    "ℹ️ Model assumptions & methodology"
):

    st.markdown(
        """
        ### 2025 Data

        The simulator uses the 2025 F1 calendar,
        race distances and 2025 Pirelli dry-tyre
        nominations.

        ### Tyre Display

        The technical compounds are simplified
        for viewer readability:

        | Internal compound | Viewer display |
        |---|---|
        | C1 | Hard |
        | C2 | Hard |
        | C3 | Medium |
        | C4 | Medium |
        | C5 | Soft |
        | C6 | Soft |
        | INT | Intermediate |

        ### Tyre degradation

        Degradation is applied to every tyre type:

        - Hard
        - Medium
        - Soft
        - Intermediate

        Each tyre has:

        - Warm-up phase
        - Peak-performance phase
        - Degrading phase
        - Critical degradation phase

        Circuit stress changes the degradation rate.

        ### Lap-time model

        Lap time considers:

        - Circuit baseline pace
        - Car performance class
        - Tyre compound
        - Tyre age
        - Circuit stress
        - Previous lap time

        A small previous-lap smoothing effect prevents
        unrealistic sudden lap-time changes.

        ### Car classes

        Car classes are simulated performance bands.

        They are not official FIA rankings.

        ### Pit stops

        Pit-stop losses are circuit-specific
        simulation assumptions.

        ### Rain

        Rain windows are deterministic representative
        scenarios.

        They are not weather forecasts.

        ### Important

        This is a strategy simulation rather than a
        prediction engine.

        Numerical pace, tyre degradation, circuit stress,
        car-class differences and pit-stop losses are
        simplified modelling assumptions and should not
        be interpreted as official F1 performance measurements.
        """
    )
# FOOTER
st.markdown(
    """
    <div class="footer">

        F1 Race Strategy Simulator •
        2025 Data •
        Python + Pandas + Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
