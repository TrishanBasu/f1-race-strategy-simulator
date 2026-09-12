import streamlit as st
import pandas as pd
import math
from itertools import combinations

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
# F1-STYLE CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top right, rgba(225, 6, 0, 0.13), transparent 28%),
        linear-gradient(135deg, #050505 0%, #0b0b0b 45%, #111111 100%);
    color: #f5f5f5;
}

/* Main container */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #090909 0%, #111111 100%);
    border-right: 1px solid #292929;
}

section[data-testid="stSidebar"] * {
    color: #f2f2f2;
}

/* Main title */
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

/* Red line */
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

/* Cards */
.f1-card {
    background: linear-gradient(145deg, #151515, #0d0d0d);
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

/* Section headers */
.section-header {
    font-size: 1.45rem;
    font-weight: 800;
    margin-top: 30px;
    margin-bottom: 15px;
    border-left: 5px solid #e10600;
    padding-left: 12px;
}

/* Metrics */
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

/* Strategy winner */
.winner-card {
    background:
        linear-gradient(135deg, rgba(225,6,0,0.18), rgba(10,10,10,0.96));
    border: 1px solid #e10600;
    border-radius: 12px;
    padding: 24px;
    margin: 20px 0;
    box-shadow: 0 0 30px rgba(225,6,0,0.08);
}

.winner-title {
    color: #e10600;
    text-transform: uppercase;
    font-size: 0.85rem;
    font-weight: 800;
    letter-spacing: 1.5px;
}

.winner-strategy {
    font-size: 2rem;
    font-weight: 900;
    color: white;
    margin: 7px 0;
}

.winner-time {
    color: #bdbdbd;
    font-size: 1rem;
}

/* Info */
.info-box {
    background: #111111;
    border: 1px solid #303030;
    border-radius: 9px;
    padding: 15px 18px;
    color: #bdbdbd;
}

/* Buttons */
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
    box-shadow: 0 0 18px rgba(225,6,0,0.35);
    transform: translateY(-1px);
}

/* Inputs */
div[data-baseweb="select"] > div {
    background-color: #171717;
    border-color: #353535;
}

.stNumberInput input {
    background-color: #171717 !important;
    color: white !important;
    border-color: #353535 !important;
}

/* Dataframe */
div[data-testid="stDataFrame"] {
    border: 1px solid #292929;
    border-radius: 8px;
}

/* Expander */
.streamlit-expanderHeader {
    background: #111111 !important;
    color: white !important;
    border: 1px solid #292929;
}

/* Footer */
.footer {
    text-align: center;
    color: #666666;
    font-size: 0.8rem;
    padding: 30px 0 10px 0;
}

/* Badges */
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
    background: rgba(225,6,0,0.18);
    color: #ff4b45;
    border: 1px solid rgba(225,6,0,0.4);
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATASET
# ============================================================

@st.cache_data
def load_dataset():
    df = pd.read_csv("f1_2025_strategy_dataset.csv")

    # Make column names consistent
    df.columns = [str(c).strip() for c in df.columns]

    return df


try:
    races_df = load_dataset()
except Exception as e:
    st.error(
        "Could not load f1_2025_strategy_dataset.csv. "
        "Make sure the CSV file is in the same GitHub repository as app.py."
    )
    st.stop()


# ============================================================
# RACE DATA
# ============================================================

# The numerical values below are simulation assumptions.
# They are NOT official F1 performance ratings.

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

# Internal C1-C6 values are hidden from the viewer.
#
# C1/C2 = HARD
# C3/C4 = MEDIUM
# C5/C6 = SOFT
# INT   = INTERMEDIATE

TYRE_MODEL = {
    "C1": {
        "display": "Hard",
        "compound": "Hard",
        "offset": 0.65,
        "peak_start": 3,
        "peak_end": 18,
        "critical_lap": 40,
        "deg_rate": 0.040,
        "late_rate": 0.075
    },
    "C2": {
        "display": "Hard",
        "compound": "Hard",
        "offset": 0.45,
        "peak_start": 3,
        "peak_end": 16,
        "critical_lap": 36,
        "deg_rate": 0.045,
        "late_rate": 0.080
    },
    "C3": {
        "display": "Medium",
        "compound": "Medium",
        "offset": 0.25,
        "peak_start": 2,
        "peak_end": 13,
        "critical_lap": 31,
        "deg_rate": 0.050,
        "late_rate": 0.085
    },
    "C4": {
        "display": "Medium",
        "compound": "Medium",
        "offset": 0.05,
        "peak_start": 2,
        "peak_end": 11,
        "critical_lap": 27,
        "deg_rate": 0.055,
        "late_rate": 0.090
    },
    "C5": {
        "display": "Soft",
        "compound": "Soft",
        "offset": -0.25,
        "peak_start": 2,
        "peak_end": 8,
        "critical_lap": 19,
        "deg_rate": 0.070,
        "late_rate": 0.105
    },
    "C6": {
        "display": "Soft",
        "compound": "Soft",
        "offset": -0.40,
        "peak_start": 2,
        "peak_end": 7,
        "critical_lap": 16,
        "deg_rate": 0.080,
        "late_rate": 0.115
    },
    "INT": {
        "display": "Intermediate",
        "compound": "Intermediate",
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


def tyre_short_name(compound):
    return TYRE_MODEL[compound]["display"]


def strategy_display(strategy):
    return " → ".join(tyre_name(x) for x in strategy)


def format_time(seconds):
    minutes = int(seconds // 60)
    secs = seconds - minutes * 60
    return f"{minutes}:{secs:05.2f}"


def format_delta(seconds):
    sign = "+" if seconds >= 0 else "-"
    return f"{sign}{abs(seconds):.2f}s"


# ============================================================
# TYRE DEGRADATION
# ============================================================

def calculate_tyre_degradation(compound, tyre_age, circuit_stress):
    """
    Continuous, non-decreasing degradation model.

    Applies to:
    - Hard
    - Medium
    - Soft
    - Intermediate
    """

    tyre = TYRE_MODEL[compound]

    if tyre_age <= 0:
        return 0.0

    peak_start = tyre["peak_start"]
    peak_end = tyre["peak_end"]
    critical = tyre["critical_lap"]

    # --------------------------------------------------------
    # Warm-up phase
    # --------------------------------------------------------

    if tyre_age <= peak_start:
        raw = 0.018 * tyre_age

    # --------------------------------------------------------
    # Peak performance phase
    # --------------------------------------------------------

    elif tyre_age <= peak_end:
        warmup = 0.018 * peak_start

        extra_age = tyre_age - peak_start

        raw = (
            warmup
            + 0.012 * extra_age
            + 0.004 * (extra_age ** 1.35)
        )

    # --------------------------------------------------------
    # Accelerating degradation
    # --------------------------------------------------------

    elif tyre_age <= critical:

        peak_value = calculate_tyre_degradation(
            compound,
            peak_end,
            1.0
        )

        extra_age = tyre_age - peak_end
        peak_length = max(critical - peak_end, 1)

        raw = (
            peak_value
            + tyre["deg_rate"]
            * (
                extra_age ** 1.28
                / (peak_length ** 0.20)
            )
        )

    # --------------------------------------------------------
    # Critical degradation
    # --------------------------------------------------------

    else:

        critical_value = calculate_tyre_degradation(
            compound,
            critical,
            1.0
        )

        extra_age = tyre_age - critical

        raw = (
            critical_value
            + tyre["late_rate"] * (extra_age ** 1.42)
        )

    return round(raw * circuit_stress, 3)


# ============================================================
# TYRE PHASE
# ============================================================

def tyre_phase(compound, tyre_age):

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

    # Car performance
    car_delta = CLASS_DATA[car_class]["pace_delta"]

    # Tyre compound pace
    tyre_delta = tyre["offset"]

    # Degradation
    degradation = calculate_tyre_degradation(
        compound,
        tyre_age,
        race["stress"]
    )

    # Rain performance
    rain_delta = 0.0

    if wet:

        if compound == "INT":
            # Intermediate becomes significantly faster
            # than dry tyres when the track is wet.
            rain_delta = -17.5

        else:
            # Dry tyres become progressively poor in wet conditions.
            rain_delta = 10.0 + (tyre_age * 0.08)

    # Initial lap
    lap_time = (
        base
        + car_delta
        + tyre_delta
        + degradation
        + rain_delta
    )

    # --------------------------------------------------------
    # Previous-lap smoothing
    # --------------------------------------------------------

    if previous_lap is not None:

        # Small momentum effect.
        # The previous lap influences the current lap,
        # but current conditions remain dominant.

        lap_time = (
            0.85 * lap_time
            + 0.15 * previous_lap
        )

    return lap_time


# ============================================================
# LEGAL STRATEGIES
# ============================================================

def generate_dry_strategies(country):

    available = PIRELLI_2025.get(
        country,
        ["C3", "C4", "C5"]
    )

    strategies = []

    # 1-stop
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

    # 2-stop
    for a in available:
        for b in available:
            for c in available:

                if len({a, b, c}) < 2:
                    continue

                strategies.append(
                    {
                        "compounds": [a, b, c],
                        "stops": 2
                    }
                )

    # 3-stop
    # Only a limited deterministic set is used to
    # prevent unnecessary computation.
    for a in available:
        for b in available:
            for c in available:
                for d in available:

                    if len({a, b, c, d}) < 2:
                        continue

                    strategies.append(
                        {
                            "compounds": [a, b, c, d],
                            "stops": 3
                        }
                    )

    return strategies


# ============================================================
# DETERMINE STINT LENGTHS
# ============================================================

def create_stints(total_laps, number_of_stops):

    stints = number_of_stops + 1

    # Balanced starting point
    base = total_laps // stints
    remainder = total_laps % stints

    lengths = []

    for i in range(stints):

        length = base

        if i < remainder:
            length += 1

        lengths.append(length)

    return lengths


# ============================================================
# SIMULATE DRY STRATEGY
# ============================================================

def simulate_dry_strategy(
    country,
    strategy,
    car_class,
    starting_position
):

    race = RACE_DEFAULTS[country]

    compounds = strategy["compounds"]

    stint_lengths = create_stints(
        race["laps"],
        len(compounds) - 1
    )

    total_time = 0.0

    previous_lap = None

    lap_records = []

    current_lap = 0

    # Starting position has a small strategic effect.
    # It should not overpower the actual pace model.

    start_factor = 0.0

    if starting_position <= 3:
        start_factor = -0.10

    elif starting_position >= 18:
        start_factor = 0.10

    for stint_index, compound in enumerate(compounds):

        stint_length = stint_lengths[stint_index]

        for age in range(1, stint_length + 1):

            current_lap += 1

            lap_time = calculate_lap_time(
                country=country,
                compound=compound,
                tyre_age=age,
                car_class=car_class,
                previous_lap=previous_lap,
                wet=False
            )

            # Tiny deterministic position effect
            if current_lap <= 3:
                lap_time += start_factor

            total_time += lap_time

            lap_records.append(
                {
                    "Lap": current_lap,
                    "Tyre": tyre_name(compound),
                    "Tyre Age": age,
                    "Phase": tyre_phase(compound, age),
                    "Lap Time (s)": round(lap_time, 3),
                    "Condition": "Dry"
                }
            )

            previous_lap = lap_time

        # Pit stop
        if stint_index < len(compounds) - 1:

            total_time += race["pit_loss"]

            lap_records.append(
                {
                    "Lap": f"Pit {stint_index + 1}",
                    "Tyre": "PIT STOP",
                    "Tyre Age": "-",
                    "Phase": "-",
                    "Lap Time (s)": round(
                        race["pit_loss"],
                        3
                    ),
                    "Condition": "Pit"
                }
            )

    return {
        "total_time": total_time,
        "strategy": strategy,
        "stints": stint_lengths,
        "laps": pd.DataFrame(lap_records)
    }


# ============================================================
# OPTIMIZE DRY STRATEGY
# ============================================================

def optimize_dry_strategy(
    country,
    car_class,
    starting_position
):

    strategies = generate_dry_strategies(country)

    results = []

    for strategy in strategies:

        result = simulate_dry_strategy(
            country=country,
            strategy=strategy,
            car_class=car_class,
            starting_position=starting_position
        )

        results.append(result)

    results.sort(
        key=lambda x: x["total_time"]
    )

    return results


# ============================================================
# RAIN DURATION
# ============================================================

def calculate_rain_laps(country, rain_duration_minutes):

    race = RACE_DEFAULTS[country]

    lap_seconds = race["pace"]

    rain_seconds = rain_duration_minutes * 60

    rain_laps = rain_seconds / lap_seconds

    return max(1, int(round(rain_laps)))


# ============================================================
# RAIN WINDOWS
# ============================================================

def generate_rain_windows(
    country,
    rain_duration_minutes
):

    race = RACE_DEFAULTS[country]

    total_laps = race["laps"]

    rain_laps = calculate_rain_laps(
        country,
        rain_duration_minutes
    )

    rain_laps = min(
        rain_laps,
        total_laps
    )

    max_start = total_laps - rain_laps + 1

    if max_start <= 1:
        return [
            {
                "name": "Full-race rain window",
                "start": 1,
                "end": total_laps
            }
        ]

    # Deterministic representative scenarios
    positions = [
        ("Early rain", 0.05),
        ("Early-mid rain", 0.25),
        ("Mid-race rain", 0.50),
        ("Late-mid rain", 0.70),
        ("Late rain", 0.90)
    ]

    windows = []

    for name, ratio in positions:

        start = int(
            round(
                1
                + (max_start - 1) * ratio
            )
        )

        start = max(
            1,
            min(start, max_start)
        )

        end = min(
            start + rain_laps - 1,
            total_laps
        )

        window = {
            "name": name,
            "start": start,
            "end": end
        }

        if window not in windows:
            windows.append(window)

    return windows


# ============================================================
# RAIN STRATEGY SIMULATION
# ============================================================

def simulate_rain_scenario(
    country,
    car_class,
    starting_position,
    rain_start,
    rain_end,
    dry_strategy
):

    race = RACE_DEFAULTS[country]

    dry_compounds = dry_strategy["compounds"]

    # --------------------------------------------------------
    # Find sensible dry pit structure
    # --------------------------------------------------------

    dry_stints = create_stints(
        race["laps"],
        len(dry_compounds) - 1
    )

    # --------------------------------------------------------
    # Build race lap by lap
    # --------------------------------------------------------

    total_time = 0.0
    previous_lap = None

    lap_records = []

    current_dry_index = 0
    current_dry_age = 0

    current_lap = 0

    pitted_for_rain = False
    returned_from_rain = False

    for lap in range(1, race["laps"] + 1):

        current_lap = lap

        is_wet = (
            rain_start
            <= lap
            <= rain_end
        )

        # ----------------------------------------------------
        # Enter intermediate when rain starts
        # ----------------------------------------------------

        if (
            is_wet
            and not pitted_for_rain
        ):

            if lap > 1:

                total_time += race["pit_loss"]

                lap_records.append(
                    {
                        "Lap": f"Pit → Intermediate",
                        "Tyre": "PIT STOP",
                        "Tyre Age": "-",
                        "Phase": "-",
                        "Lap Time (s)": round(
                            race["pit_loss"],
                            3
                        ),
                        "Condition": "Rain"
                    }
                )

            current_compound = "INT"
            int_age = 1

            pitted_for_rain = True

        # ----------------------------------------------------
        # Stay on intermediate
        # ----------------------------------------------------

        elif is_wet and pitted_for_rain:

            current_compound = "INT"

            int_age = (
                lap
                - rain_start
                + 1
            )

        # ----------------------------------------------------
        # Rain ended
        # ----------------------------------------------------

        elif (
            not is_wet
            and pitted_for_rain
            and not returned_from_rain
            and lap > rain_end
        ):

            total_time += race["pit_loss"]

            lap_records.append(
                {
                    "Lap": f"Pit → Dry",
                    "Tyre": "PIT STOP",
                    "Tyre Age": "-",
                    "Phase": "-",
                    "Lap Time (s)": round(
                        race["pit_loss"],
                        3
                    ),
                    "Condition": "Dry"
                }
            )

            returned_from_rain = True

            # Restart dry strategy from the compound
            # that would logically be in use at this stage.
            progress = lap / race["laps"]

            index = int(
                progress
                * len(dry_compounds)
            )

            index = min(
                index,
                len(dry_compounds) - 1
            )

            current_dry_index = index
            current_dry_age = 0

            current_compound = dry_compounds[
                current_dry_index
            ]

            current_dry_age += 1

        # ----------------------------------------------------
        # Normal dry running
        # ----------------------------------------------------

        else:

            current_compound = dry_compounds[
                min(
                    current_dry_index,
                    len(dry_compounds) - 1
                )
            ]

            current_dry_age += 1

            # Move through normal dry stints
            accumulated = 0

            for i, stint_length in enumerate(dry_stints):

                accumulated += stint_length

                if lap <= accumulated:

                    current_dry_index = i

                    current_compound = dry_compounds[i]

                    previous_stints = sum(
                        dry_stints[:i]
                    )

                    current_dry_age = (
                        lap
                        - previous_stints
                    )

                    break

        # ----------------------------------------------------
        # Calculate lap time
        # ----------------------------------------------------

        tyre_age = (
            int_age
            if current_compound == "INT"
            else current_dry_age
        )

        lap_time = calculate_lap_time(
            country=country,
            compound=current_compound,
            tyre_age=tyre_age,
            car_class=car_class,
            previous_lap=previous_lap,
            wet=is_wet
        )

        # ----------------------------------------------------
        # Dry tyres on wet track penalty
        # ----------------------------------------------------

        if is_wet and current_compound != "INT":

            lap_time += 12.0

        total_time += lap_time

        lap_records.append(
            {
                "Lap": lap,
                "Tyre": tyre_name(current_compound),
                "Tyre Age": tyre_age,
                "Phase": tyre_phase(
                    current_compound,
                    tyre_age
                ),
                "Lap Time (s)": round(
                    lap_time,
                    3
                ),
                "Condition": (
                    "Wet"
                    if is_wet
                    else "Dry"
                )
            }
        )

        previous_lap = lap_time

    return {
        "total_time": total_time,
        "rain_start": rain_start,
        "rain_end": rain_end,
        "strategy": dry_strategy,
        "laps": pd.DataFrame(lap_records)
    }


# ============================================================
# RAIN OPTIMIZATION
# ============================================================

def optimize_rain_strategy(
    country,
    car_class,
    starting_position,
    rain_duration_minutes,
    rain_percentage
):

    dry_results = optimize_dry_strategy(
        country,
        car_class,
        starting_position
    )

    # Use the strongest dry strategies as candidates.
    # This keeps the rain simulation fast.
    candidates = dry_results[:8]

    windows = generate_rain_windows(
        country,
        rain_duration_minutes
    )

    scenarios = []

    if rain_percentage == "50% Rain":

        scenarios.append(
            {
                "name": "No rain",
                "start": None,
                "end": None
            }
        )

    for window in windows:

        scenarios.append(
            {
                "name": window["name"],
                "start": window["start"],
                "end": window["end"]
            }
        )

    results = []

    for scenario in scenarios:

        if scenario["start"] is None:

            best = candidates[0]

            results.append(
                {
                    "scenario": scenario["name"],
                    "rain_start": None,
                    "rain_end": None,
                    "total_time": best["total_time"],
                    "strategy": best["strategy"],
                    "laps": best["laps"]
                }
            )

        else:

            for candidate in candidates:

                result = simulate_rain_scenario(
                    country=country,
                    car_class=car_class,
                    starting_position=starting_position,
                    rain_start=scenario["start"],
                    rain_end=scenario["end"],
                    dry_strategy=candidate["strategy"]
                )

                results.append(
                    {
                        "scenario": scenario["name"],
                        "rain_start": scenario["start"],
                        "rain_end": scenario["end"],
                        "total_time": result["total_time"],
                        "strategy": result["strategy"],
                        "laps": result["laps"]
                    }
                )

    results.sort(
        key=lambda x: x["total_time"]
    )

    return results


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="hero-title">F1 <span>RACE STRATEGY</span> SIMULATOR</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero-subtitle">
        Race strategy modelling • Tyre degradation • Pit-stop optimization • Rain scenarios
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

countries = list(RACE_DEFAULTS.keys())

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
        {race['laps']} laps •
        {race['pace']:.1f}s representative lap pace
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

class_options = list(CLASS_DATA.keys())

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
    "🌧️ Rain Scenario",
    [
        "No Rain",
        "50% Rain",
        "100% Rain"
    ]
)

rain_duration = 0

if rain_option != "No Rain":

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
            <b>Estimated rain duration</b><br>
            Approximately <b>{estimated_laps} laps</b>
        </div>
        """,
        unsafe_allow_html=True
    )


run_simulation = st.sidebar.button(
    "🏁 RUN SIMULATION",
    use_container_width=True
)


# ============================================================
# TOP INFORMATION
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Grand Prix</div>
            <div class="metric-value">{country}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Starting Position</div>
            <div class="metric-value">
                P{starting_position}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Car Class</div>
            <div class="metric-value">
                {car_class}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Conditions</div>
            <div class="metric-value metric-red">
                {rain_option.replace(" Rain", "")}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DEFAULT INFORMATION
# ============================================================

if not run_simulation:

    st.markdown(
        '<div class="section-header">How the simulator works</div>',
        unsafe_allow_html=True
    )

    info1, info2, info3 = st.columns(3)

    with info1:
        st.markdown(
            """
            <div class="f1-card">
                <h3>🏎️ Car Performance</h3>
                <p>
                Six performance classes represent different
                constructor performance levels. The class affects
                the simulated baseline lap pace.
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
                Hard, Medium and Soft tyres have different pace,
                warm-up, peak-performance and degradation
                characteristics.
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
                Intermediate tyres are introduced when rain
                occurs. Different deterministic rain windows
                are tested to compare strategic outcomes.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="section-header">2025 Tyre Selection</div>',
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

    st.markdown(
        '<div class="section-header">Simulation Model</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="f1-card">
        The simulator evaluates race pace lap by lap. Tyre age,
        circuit stress, car performance and the previous lap all
        influence the simulated lap time.

        <br><br>

        <b>Tyre degradation is applied to all tyre types:</b>

        <br><br>

        🟥 <b>Soft</b> — fastest initial pace, shorter competitive life<br>
        🟡 <b>Medium</b> — balanced pace and durability<br>
        ⚪ <b>Hard</b> — slower initial pace, longest dry-tyre life<br>
        🟢 <b>Intermediate</b> — optimized for wet conditions

        <br><br>

        The optimizer compares legal one-stop, two-stop and
        three-stop strategies and selects the fastest simulated
        outcome.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# RUN SIMULATION
# ============================================================

if run_simulation:

    with st.spinner("Running race strategy simulation..."):

        if rain_option == "No Rain":

            results = optimize_dry_strategy(
                country=country,
                car_class=car_class,
                starting_position=starting_position
            )

            best = results[0]

            st.markdown(
                '<div class="section-header">🏆 Recommended Strategy</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="winner-card">
                    <div class="winner-title">
                        FASTEST SIMULATED STRATEGY
                    </div>

                    <div class="winner-strategy">
                        {strategy_display(best["strategy"]["compounds"])}
                    </div>

                    <div class="winner-time">
                        Simulated race time:
                        <b>{format_time(best["total_time"])}</b>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Metrics
            m1, m2, m3, m4 = st.columns(4)

            with m1:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">Pit Stops</div>
                        <div class="metric-value">
                            {best["strategy"]["stops"]}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with m2:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">Race Time</div>
                        <div class="metric-value">
                            {format_time(best["total_time"])}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with m3:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">Circuit</div>
                        <div class="metric-value">
                            {country}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with m4:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">Car</div>
                        <div class="metric-value">
                            {car_class}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # Strategy comparison
            st.markdown(
                '<div class="section-header">Strategy Comparison</div>',
                unsafe_allow_html=True
            )

            comparison_rows = []

            best_time = best["total_time"]

            for i, result in enumerate(results[:10]):

                comparison_rows.append(
                    {
                        "Rank": i + 1,
                        "Strategy": strategy_display(
                            result["strategy"]["compounds"]
                        ),
                        "Pit Stops": result["strategy"]["stops"],
                        "Simulated Time": format_time(
                            result["total_time"]
                        ),
                        "Gap": (
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

            # Lap data
            st.markdown(
                '<div class="section-header">Lap-by-Lap Simulation</div>',
                unsafe_allow_html=True
            )

            lap_df = best["laps"].copy()

            st.dataframe(
                lap_df,
                use_container_width=True,
                hide_index=True,
                height=500
            )

            # Tyre explanation
            st.markdown(
                '<div class="section-header">Tyre Strategy Explanation</div>',
                unsafe_allow_html=True
            )

            compounds_used = best["strategy"]["compounds"]

            explanation_parts = []

            for compound in compounds_used:

                display = tyre_name(compound)

                if display == "Soft":
                    text = (
                        "Soft tyres provide the strongest initial pace "
                        "but their performance falls away faster."
                    )

                elif display == "Medium":
                    text = (
                        "Medium tyres provide a balanced combination "
                        "of pace and tyre life."
                    )

                elif display == "Hard":
                    text = (
                        "Hard tyres sacrifice initial pace for "
                        "greater durability."
                    )

                else:
                    text = (
                        "Intermediate tyres are designed for wet "
                        "or damp conditions."
                    )

                explanation_parts.append(
                    f"<b>{display}:</b> {text}"
                )

            st.markdown(
                "<div class='f1-card'>"
                + "<br><br>".join(explanation_parts)
                + "</div>",
                unsafe_allow_html=True
            )

        # ====================================================
        # RAIN SIMULATION
        # ====================================================

        else:

            results = optimize_rain_strategy(
                country=country,
                car_class=car_class,
                starting_position=starting_position,
                rain_duration_minutes=rain_duration,
                rain_percentage=rain_option
            )

            best = results[0]

            st.markdown(
                '<div class="section-header">🌧️ Rain Strategy Result</div>',
                unsafe_allow_html=True
            )

            if best["rain_start"] is None:

                rain_text = "No Rain"

            else:

                rain_text = (
                    f"Lap {best['rain_start']} – "
                    f"Lap {best['rain_end']}"
                )

            st.markdown(
                f"""
                <div class="winner-card">
                    <div class="winner-title">
                        BEST SIMULATED RAIN SCENARIO
                    </div>

                    <div class="winner-strategy">
                        {strategy_display(best["strategy"]["compounds"])}
                    </div>

                    <div class="winner-time">
                        Rain window:
                        <b>{rain_text}</b>
                        <br>
                        Simulated race time:
                        <b>{format_time(best["total_time"])}</b>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Rain metrics
            r1, r2, r3, r4 = st.columns(4)

            with r1:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">Rain Duration</div>
                        <div class="metric-value">
                            {rain_duration} min
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with r2:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">Rain Window</div>
                        <div class="metric-value">
                            {rain_text}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with r3:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">Strategy</div>
                        <div class="metric-value">
                            {best["strategy"]["stops"]} Stops
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with r4:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">Race Time</div>
                        <div class="metric-value">
                            {format_time(best["total_time"])}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # Scenario comparison
            st.markdown(
                '<div class="section-header">Rain Scenario Comparison</div>',
                unsafe_allow_html=True
            )

            scenario_best = {}

            for result in results:

                scenario = result["scenario"]

                if (
                    scenario not in scenario_best
                    or result["total_time"]
                    < scenario_best[scenario]["total_time"]
                ):

                    scenario_best[scenario] = result

            rain_rows = []

            ordered_scenarios = list(
                scenario_best.keys()
            )

            global_best_time = best["total_time"]

            for i, scenario in enumerate(
                ordered_scenarios
            ):

                result = scenario_best[scenario]

                if result["rain_start"] is None:

                    window = "No rain"

                else:

                    window = (
                        f"Lap {result['rain_start']}–"
                        f"{result['rain_end']}"
                    )

                rain_rows.append(
                    {
                        "Scenario": scenario,
                        "Rain Window": window,
                        "Strategy": strategy_display(
                            result["strategy"]["compounds"]
                        ),
                        "Pit Stops": result["strategy"]["stops"],
                        "Simulated Time": format_time(
                            result["total_time"]
                        ),
                        "Gap": format_delta(
                            result["total_time"]
                            - global_best_time
                        )
                    }
                )

            rain_table = pd.DataFrame(
                rain_rows
            )

            st.dataframe(
                rain_table,
                use_container_width=True,
                hide_index=True
            )

            # Lap-by-lap
            st.markdown(
                '<div class="section-header">Best Scenario — Lap Analysis</div>',
                unsafe_allow_html=True
            )

            st.dataframe(
                best["laps"],
                use_container_width=True,
                hide_index=True,
                height=500
            )

            # Rain explanation
            st.markdown(
                '<div class="section-header">Rain Strategy Logic</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="f1-card">

                <b>Rain probability setting:</b>
                {rain_option}

                <br><br>

                <b>Rain duration:</b>
                {rain_duration} minutes
                (approximately
                {calculate_rain_laps(country, rain_duration)}
                racing laps)

                <br><br>

                The simulator tests deterministic representative
                rain windows rather than generating random weather.

                <br><br>

                When the track becomes wet, the model switches to
                <b>Intermediate tyres</b>. Intermediate tyres also
                have their own tyre-age and degradation model.

                <br><br>

                This means degradation is modelled for
                <b>Hard, Medium, Soft and Intermediate</b> tyres.

                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# MODEL ASSUMPTIONS
# ============================================================

with st.expander("ℹ️ Model assumptions & methodology"):

    st.markdown(
        """
        ### Data

        The simulator uses the **2025 F1 calendar, race distances
        and 2025 Pirelli dry-tyre nominations**.

        ### Tyres

        Internally the Pirelli compounds are represented as:

        | Internal compound | Viewer name |
        |---|---|
        | C1 | Hard |
        | C2 | Hard |
        | C3 | Medium |
        | C4 | Medium |
        | C5 | Soft |
        | C6 | Soft |
        | INT | Intermediate |

        The viewer does not need to understand the C1–C6
        terminology.

        ### Tyre degradation

        Degradation is applied to **every tyre type**.

        The model includes:

        - Warm-up phase
        - Peak-performance phase
        - Accelerating degradation
        - Critical degradation
        - Circuit stress scaling

        Soft tyres reach their strongest performance window
        earlier and degrade faster.

        Medium tyres provide a balance between pace and durability.

        Hard tyres have a longer useful life but are slower initially.

        Intermediate tyres have their own degradation curve and
        are evaluated during wet conditions.

        ### Lap-time model

        Each lap considers:

        - Circuit baseline pace
        - Car performance class
        - Tyre compound
        - Tyre age
        - Circuit stress
        - Wet/dry conditions
        - Previous lap time

        A small previous-lap smoothing factor is used so that
        lap times do not change unrealistically from one lap
        to the next.

        ### Car classes

        The six classes are simulated performance bands.

        They are not intended to represent an official FIA
        ranking system.

        ### Pit stops

        Pit-stop time loss is a circuit-specific simulation
        assumption.

        ### Rain

        Rain scenarios are deterministic representative scenarios.

        They are not weather forecasts or predictions.

        ### Important

        This is a **strategy simulation and portfolio project**.
        Numerical pace, degradation, stress and pit-loss values
        are modelling assumptions rather than official F1
        performance measurements.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        F1 Race Strategy Simulator • 2025 Data •
        Python + Pandas + Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
