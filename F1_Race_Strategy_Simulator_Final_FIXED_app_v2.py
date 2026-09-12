
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
        "offset": 0.65,
        "peak_start": 3,
        "peak_end": 18,
        "critical_lap": 40,
        "deg_rate": 0.040,
        "late_rate": 0.075
    },

    "C2": {
        "display": "Hard",
        "offset": 0.45,
        "peak_start": 3,
        "peak_end": 16,
        "critical_lap": 36,
        "deg_rate": 0.045,
        "late_rate": 0.080
    },

    "C3": {
        "display": "Medium",
        "offset": 0.25,
        "peak_start": 2,
        "peak_end": 13,
        "critical_lap": 31,
        "deg_rate": 0.050,
        "late_rate": 0.085
    },

    "C4": {
        "display": "Medium",
        "offset": 0.05,
        "peak_start": 2,
        "peak_end": 11,
        "critical_lap": 27,
        "deg_rate": 0.055,
        "late_rate": 0.090
    },

    "C5": {
        "display": "Soft",
        "offset": -0.25,
        "peak_start": 2,
        "peak_end": 8,
        "critical_lap": 19,
        "deg_rate": 0.070,
        "late_rate": 0.105
    },

    "C6": {
        "display": "Soft",
        "offset": -0.40,
        "peak_start": 2,
        "peak_end": 7,
        "critical_lap": 16,
        "deg_rate": 0.080,
        "late_rate": 0.115
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

def tyre_name(compound):

    return TYRE_MODEL[compound]["display"]


def tyre_display_with_code(compound):

    if compound == "INT":
        return "Intermediate"

    return (
        f"{TYRE_MODEL[compound]['display']} "
        f"({compound})"
    )


def strategy_display(strategy):

    return " → ".join(
        tyre_display_with_code(x)
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

    car_delta = (
        CLASS_DATA[car_class]["pace_delta"]
    )

    tyre_delta = tyre["offset"]

    degradation = (
        calculate_tyre_degradation(
            compound,
            tyre_age,
            race["stress"]
        )
    )

    rain_delta = 0.0

    # Intermediate works best in wet conditions.
    if wet:

        if compound == "INT":

            rain_delta = -17.5

        else:

            rain_delta = (
                10.0
                + tyre_age * 0.08
            )

    lap_time = (
        base
        + car_delta
        + tyre_delta
        + degradation
        + rain_delta
    )

    # Previous-lap smoothing.
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

def create_stints(
    total_laps,
    number_of_stops
):

    stint_count = (
        number_of_stops + 1
    )

    base = (
        total_laps
        // stint_count
    )

    remainder = (
        total_laps
        % stint_count
    )

    lengths = []

    for i in range(stint_count):

        length = base

        if i < remainder:

            length += 1

        lengths.append(length)

    return lengths


# ============================================================
# DRY STRATEGY SIMULATION
# ============================================================

def simulate_dry_strategy(
    country,
    strategy,
    car_class,
    starting_position
):

    race = RACE_DEFAULTS[country]

    compounds = (
        strategy["compounds"]
    )

    stint_lengths = (
        create_stints(
            race["laps"],
            len(compounds) - 1
        )
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
                        compound
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

    strategies = (
        generate_dry_strategies(
            country
        )
    )

    results = []

    for strategy in strategies:

        result = (
            simulate_dry_strategy(
                country,
                strategy,
                car_class,
                starting_position
            )
        )

        results.append(result)

    results.sort(
        key=lambda x:
        x["total_time"]
    )

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
    countries
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
    step=1
)

class_options = list(
    CLASS_DATA.keys()
)

car_class = st.sidebar.selectbox(
    "Car Performance Class",
    class_options
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
    ]
)

rain_duration = 0

if rain_option == "Rain":
    rain_duration = st.sidebar.number_input(
        "Rain Duration (minutes)",
        min_value=5,
        max_value=180,
        value=30,
        step=5
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
        sorted(
            set(
                tyre_name(x)
                for x in available
            )
        )
    )

    st.markdown(
        f"""
        <div class="info-box">

            <b>2025 nominated dry tyres:</b>
            &nbsp; {tyre_text}

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
            f"{strategy_display(best['strategy']['compounds'])}"
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
                            result["strategy"]["compounds"]
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
                    f"## {tyre_name(compound)}"
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
