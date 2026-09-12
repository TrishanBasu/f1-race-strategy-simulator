import streamlit as st
import pandas as pd
import itertools


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="F1 Race Strategy Simulator",
    page_icon="🏎️",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv("f1_2025_strategy_dataset.csv")

    return df


races_df = load_data()


# ============================================================
# TYRE MODEL
# ============================================================

# pace_offset:
# lower = faster
#
# peak_start / peak_end:
# period where tyre gives relatively stable performance
#
# degradation_start:
# point where noticeable degradation begins
#
# critical_lap:
# tyre becomes heavily degraded

TYRE_MODEL = {

    "C1": {
        "category": "Hard",
        "pace_offset": 0.50,
        "peak_start": 3,
        "peak_end": 18,
        "degradation_start": 19,
        "critical_lap": 38
    },

    "C2": {
        "category": "Hard",
        "pace_offset": 0.35,
        "peak_start": 3,
        "peak_end": 16,
        "degradation_start": 17,
        "critical_lap": 34
    },

    "C3": {
        "category": "Medium",
        "pace_offset": 0.20,
        "peak_start": 2,
        "peak_end": 13,
        "degradation_start": 14,
        "critical_lap": 30
    },

    "C4": {
        "category": "Medium",
        "pace_offset": 0.00,
        "peak_start": 2,
        "peak_end": 11,
        "degradation_start": 12,
        "critical_lap": 25
    },

    "C5": {
        "category": "Soft",
        "pace_offset": -0.25,
        "peak_start": 2,
        "peak_end": 8,
        "degradation_start": 9,
        "critical_lap": 18
    },

    "C6": {
        "category": "Soft",
        "pace_offset": -0.40,
        "peak_start": 2,
        "peak_end": 7,
        "degradation_start": 8,
        "critical_lap": 15
    },

    "INT": {
        "category": "Intermediate",
        "pace_offset": 4.50,
        "peak_start": 2,
        "peak_end": 12,
        "degradation_start": 13,
        "critical_lap": 28
    }
}


# ============================================================
# CAR PERFORMANCE CLASSES
# ============================================================

# Class 1 = fastest
# Class 6 = slowest

CLASS_PACE = {

    "Class 1": 0.00,
    "Class 2": 0.35,
    "Class 3": 0.75,
    "Class 4": 1.20,
    "Class 5": 1.75,
    "Class 6": 2.35
}


# ============================================================
# TYRE PHASE
# ============================================================

def tyre_phase(compound, tyre_age):

    tyre = TYRE_MODEL[compound]

    if tyre_age <= tyre["peak_start"]:

        return "Warm-up"

    elif tyre_age <= tyre["peak_end"]:

        return "Peak"

    elif tyre_age < tyre["critical_lap"]:

        return "Degrading"

    else:

        return "Critical"


# ============================================================
# TYRE DEGRADATION
# ============================================================

def calculate_tyre_degradation(
    compound,
    tyre_age,
    circuit_stress
):

    tyre = TYRE_MODEL[compound]

    stress = circuit_stress


    # --------------------------------------------------------
    # WARM-UP
    # --------------------------------------------------------

    if tyre_age <= tyre["peak_start"]:

        degradation = (
            0.02
            * tyre_age
            * stress
        )


    # --------------------------------------------------------
    # PEAK
    # --------------------------------------------------------

    elif tyre_age <= tyre["peak_end"]:

        age_in_peak = (
            tyre_age
            - tyre["peak_start"]
        )

        degradation = (
            0.04
            + 0.015 * age_in_peak
        ) * stress


    # --------------------------------------------------------
    # DEGRADATION
    # --------------------------------------------------------

    elif tyre_age < tyre["critical_lap"]:

        degradation_age = (
            tyre_age
            - tyre["peak_end"]
        )

        degradation = (
            0.10
            + 0.045
            * (degradation_age ** 1.35)
        ) * stress


    # --------------------------------------------------------
    # CRITICAL
    # --------------------------------------------------------

    else:

        degradation_age = (
            tyre_age
            - tyre["critical_lap"]
        )

        base_degradation = (

            0.10

            + 0.045
            * (
                (
                    tyre["critical_lap"]
                    - tyre["peak_end"]
                )
                ** 1.35
            )
        )

        degradation = (

            base_degradation

            + 0.12
            * (degradation_age ** 1.6)

        ) * stress


    return degradation


# ============================================================
# LAP TIME CALCULATION
# ============================================================

def calculate_lap_time(

    base_pace,
    compound,
    tyre_age,
    circuit_stress,
    car_class,
    previous_lap_time=None,
    wet=False,
    crossover=False

):

    tyre = TYRE_MODEL[compound]


    # --------------------------------------------------------
    # INTERMEDIATE
    # --------------------------------------------------------

    if compound == "INT":

        current_time = (

            base_pace

            + CLASS_PACE[car_class]

            + tyre["pace_offset"]

            + calculate_tyre_degradation(
                "INT",
                min(tyre_age, 40),
                circuit_stress
            )

        )

        if wet:

            current_time -= 18.0

        elif crossover:

            current_time -= 8.0


    # --------------------------------------------------------
    # SLICK TYRES
    # --------------------------------------------------------

    else:

        current_time = (

            base_pace

            + CLASS_PACE[car_class]

            + tyre["pace_offset"]

            + calculate_tyre_degradation(
                compound,
                tyre_age,
                circuit_stress
            )

        )


        # Slicks become significantly slower
        # when rain is established.

        if wet:

            current_time += 18.0


        # Crossover conditions

        elif crossover:

            current_time += 7.0


    # --------------------------------------------------------
    # PREVIOUS LAP EFFECT
    # --------------------------------------------------------

    if previous_lap_time is not None:

        current_time = (

            0.85 * current_time

            + 0.15 * previous_lap_time

        )


    return current_time


# ============================================================
# FORMAT TIME
# ============================================================

def format_time(seconds):

    minutes = int(
        seconds // 60
    )

    remaining = (
        seconds
        - minutes * 60
    )

    return (
        f"{minutes}:"
        f"{remaining:06.3f}"
    )


# ============================================================
# COMPOUND DISPLAY
# ============================================================

def compound_display(compound):

    if compound == "INT":

        return "Intermediate"

    return compound


# ============================================================
# AVAILABLE DRY TYRES
# ============================================================

def get_available_slicks(race):

    return [

        race["hard_compound"],

        race["medium_compound"],

        race["soft_compound"]

    ]


# ============================================================
# BUILD DRY STRATEGIES
# ============================================================

def generate_dry_strategies(race):

    total_laps = int(
        race["total_laps"]
    )

    slicks = get_available_slicks(
        race
    )

    strategies = []


    # --------------------------------------------------------
    # 1 STOP
    # --------------------------------------------------------

    for compounds in itertools.product(
        slicks,
        repeat=2
    ):

        if compounds[0] == compounds[1]:

            continue


        for pit_lap in range(
            10,
            total_laps - 10
        ):

            strategies.append({

                "compounds": list(compounds),

                "pit_laps": [pit_lap]

            })


    # --------------------------------------------------------
    # 2 STOPS
    # --------------------------------------------------------

    for compounds in itertools.product(
        slicks,
        repeat=3
    ):

        if (
            compounds[0] == compounds[1]
            or
            compounds[1] == compounds[2]
        ):

            continue


        for pit1 in range(
            10,
            total_laps - 20,
            4
        ):

            for pit2 in range(
                pit1 + 10,
                total_laps - 8,
                4
            ):

                strategies.append({

                    "compounds": list(compounds),

                    "pit_laps": [
                        pit1,
                        pit2
                    ]

                })


    return strategies


# ============================================================
# SIMULATE DRY STRATEGY
# ============================================================

def simulate_dry_strategy(

    race,
    car_class,
    compounds,
    pit_laps

):

    total_laps = int(
        race["total_laps"]
    )

    base_pace = float(
        race["base_race_pace_seconds"]
    )

    pit_loss = float(
        race["pit_stop_seconds"]
    )

    stress = float(
        race["pirelli_stress_factor"]
    )


    total_time = 0.0

    previous_lap = None

    current_stint = 0

    tyre_age = 0

    lap_data = []


    for lap in range(
        1,
        total_laps + 1
    ):


        # ----------------------------------------------------
        # PIT STOP
        # ----------------------------------------------------

        if lap in pit_laps:

            total_time += pit_loss

            current_stint += 1

            tyre_age = 0


        tyre_age += 1


        compound = compounds[
            min(
                current_stint,
                len(compounds) - 1
            )
        ]


        # ----------------------------------------------------
        # LAP TIME
        # ----------------------------------------------------

        lap_time = calculate_lap_time(

            base_pace,

            compound,

            tyre_age,

            stress,

            car_class,

            previous_lap_time=previous_lap

        )


        total_time += lap_time


        previous_lap = lap_time


        lap_data.append({

            "Lap": lap,

            "Tyre": compound_display(
                compound
            ),

            "Tyre Age": tyre_age,

            "Phase": tyre_phase(
                compound,
                tyre_age
            ),

            "Lap Time (s)": round(
                lap_time,
                3
            )

        })


    return {

        "total_time": total_time,

        "compounds": compounds,

        "pit_laps": pit_laps,

        "lap_data": lap_data

    }


# ============================================================
# OPTIMIZE DRY STRATEGY
# ============================================================

def optimize_dry_strategy(
    race,
    car_class
):

    strategies = generate_dry_strategies(
        race
    )

    best_result = None


    for strategy in strategies:

        result = simulate_dry_strategy(

            race,

            car_class,

            strategy["compounds"],

            strategy["pit_laps"]

        )


        if (
            best_result is None
            or
            result["total_time"]
            < best_result["total_time"]
        ):

            best_result = result


    return best_result


# ============================================================
# RAIN DURATION → LAPS
# ============================================================

def calculate_rain_laps(

    race,
    duration_minutes

):

    base_lap_time = float(
        race["base_race_pace_seconds"]
    )

    duration_seconds = (
        duration_minutes * 60
    )

    laps = (
        duration_seconds
        / base_lap_time
    )

    return max(
        1,
        round(laps)
    )


# ============================================================
# GENERATE RAIN WINDOWS
# ============================================================

def generate_rain_windows(

    race,
    duration_minutes

):

    total_laps = int(
        race["total_laps"]
    )

    rain_laps = calculate_rain_laps(

        race,

        duration_minutes

    )


    if rain_laps >= total_laps:

        return [
            (1, total_laps)
        ]


    max_start = (
        total_laps
        - rain_laps
        + 1
    )


    # Deterministic.
    # No random numbers.

    fractions = [

        0.00,

        0.25,

        0.50,

        0.75,

        1.00

    ]


    starts = []


    for fraction in fractions:

        start = round(

            1

            + (
                max_start - 1
            )
            * fraction

        )


        if start not in starts:

            starts.append(start)


    windows = []


    for start in starts:

        end = min(

            total_laps,

            start
            + rain_laps
            - 1

        )

        windows.append(
            (start, end)
        )


    return windows


# ============================================================
# SIMULATE RAIN SCENARIO
# ============================================================

def simulate_rain_scenario(

    race,

    car_class,

    rain_start,

    rain_end

):

    total_laps = int(
        race["total_laps"]
    )

    base_pace = float(
        race["base_race_pace_seconds"]
    )

    pit_loss = float(
        race["pit_stop_seconds"]
    )

    stress = float(
        race["pirelli_stress_factor"]
    )


    slicks = get_available_slicks(
        race
    )


    # --------------------------------------------------------
    # Find best slick for dry sections
    # --------------------------------------------------------

    best_slick = None

    best_dry_time = None


    for compound in slicks:

        previous = None

        tyre_age = 0

        dry_time = 0.0


        for lap in range(
            1,
            total_laps + 1
        ):

            if (
                rain_start
                <= lap
                <= rain_end
            ):

                continue


            tyre_age += 1


            lap_time = calculate_lap_time(

                base_pace,

                compound,

                tyre_age,

                stress,

                car_class,

                previous_lap_time=previous

            )


            dry_time += lap_time

            previous = lap_time


        if (
            best_dry_time is None
            or dry_time < best_dry_time
        ):

            best_dry_time = dry_time

            best_slick = compound


    # --------------------------------------------------------
    # Final lap-by-lap rain simulation
    # --------------------------------------------------------

    total_time = 0.0

    previous = None

    slick_age = 0

    intermediate_age = 0

    current_tyre = best_slick

    lap_data = []


    # Pit into Intermediate
    # immediately before rain.

    rain_entry_pit = max(
        1,
        rain_start - 1
    )


    # Return to slick
    # immediately after rain.

    rain_exit_pit = min(
        total_laps - 1,
        rain_end + 1
    )


    for lap in range(
        1,
        total_laps + 1
    ):


        # ----------------------------------------------------
        # ENTER INTERMEDIATE
        # ----------------------------------------------------

        if (
            lap == rain_entry_pit
            and rain_start > 1
        ):

            total_time += pit_loss

            current_tyre = "INT"

            intermediate_age = 0


        # ----------------------------------------------------
        # RETURN TO SLICK
        # ----------------------------------------------------

        if (
            lap == rain_exit_pit
            and rain_end < total_laps
        ):

            total_time += pit_loss

            current_tyre = best_slick

            slick_age = 0


        # ----------------------------------------------------
        # RAIN
        # ----------------------------------------------------

        raining = (

            rain_start
            <= lap
            <= rain_end

        )


        if current_tyre == "INT":

            intermediate_age += 1

            tyre_age = intermediate_age


            lap_time = calculate_lap_time(

                base_pace,

                "INT",

                tyre_age,

                stress,

                car_class,

                previous_lap_time=previous,

                wet=raining,

                crossover=False

            )


            phase = tyre_phase(
                "INT",
                tyre_age
            )


        else:

            slick_age += 1

            tyre_age = slick_age


            lap_time = calculate_lap_time(

                base_pace,

                current_tyre,

                tyre_age,

                stress,

                car_class,

                previous_lap_time=previous,

                wet=raining,

                crossover=(
                    abs(lap - rain_start) <= 1
                    or
                    abs(lap - rain_end) <= 1
                )

            )


            phase = tyre_phase(

                current_tyre,

                tyre_age

            )


        total_time += lap_time

        previous = lap_time


        lap_data.append({

            "Lap": lap,

            "Tyre": compound_display(
                current_tyre
            ),

            "Tyre Age": tyre_age,

            "Phase": phase,

            "Lap Time (s)": round(
                lap_time,
                3
            ),

            "Rain": "Yes"
            if raining
            else "No"

        })


    return {

        "total_time": total_time,

        "dry_compound": best_slick,

        "pit_laps": [
            rain_entry_pit,
            rain_exit_pit
        ],

        "lap_data": lap_data

    }


# ============================================================
# MAIN UI
# ============================================================

st.title(
    "🏎️ F1 Race Strategy Simulator"
)

st.write(
    "A deterministic race-strategy simulator "
    "using 2025 F1 circuit data, tyre degradation, "
    "pit-stop loss, car performance classes and "
    "possible rain windows."
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header(
    "Race Setup"
)


country = st.sidebar.selectbox(

    "2025 Grand Prix",

    races_df["country"].tolist()

)


starting_position = st.sidebar.number_input(

    "Starting Position",

    min_value=1,

    max_value=20,

    value=8

)


car_class = st.sidebar.selectbox(

    "Car Class",

    list(CLASS_PACE.keys()),

    index=1

)


rain_probability = st.sidebar.selectbox(

    "Rain Probability",

    [

        "No Rain",

        "50% Rain",

        "100% Rain"

    ]

)


rain_duration = 0


if rain_probability != "No Rain":

    rain_duration = st.sidebar.number_input(

        "Rain Duration (minutes)",

        min_value=1,

        max_value=180,

        value=30

    )


calculate = st.sidebar.button(

    "🏁 Calculate Strategy",

    type="primary",

    use_container_width=True

)


# ============================================================
# SELECTED RACE
# ============================================================

race = races_df[
    races_df["country"] == country
].iloc[0]


# ============================================================
# RACE INFORMATION
# ============================================================

st.subheader(
    "Race Information"
)


col1, col2, col3, col4 = st.columns(4)


col1.metric(

    "Circuit",

    race["circuit"]

)


col2.metric(

    "Race Laps",

    int(race["total_laps"])

)


col3.metric(

    "Representative Dry Pace",

    f'{race["base_race_pace_seconds"]:.1f}s'

)


col4.metric(

    "Pit Stop Loss",

    f'{race["pit_stop_seconds"]:.1f}s'

)


st.info(

    f'**2025 Pirelli selection:** '
    f'{race["hard_compound"]} / '
    f'{race["medium_compound"]} / '
    f'{race["soft_compound"]}'

)


# ============================================================
# WAIT FOR CALCULATION
# ============================================================

if not calculate:

    st.markdown(
        """
        ### How to use

        **1.** Select a 2025 Grand Prix.

        **2.** Enter your starting position.

        **3.** Select your car performance class.

        **4.** Select the rain probability.

        **5.** If rain is possible, enter its duration.

        **6.** Click **Calculate Strategy**.

        The simulator then evaluates possible tyre strategies
        and selects the lowest simulated race time.
        """
    )

    st.stop()


# ============================================================
# DRY STRATEGY
# ============================================================

dry_result = optimize_dry_strategy(

    race,

    car_class

)


st.subheader(
    "🏆 Recommended Dry Strategy"
)


col1, col2, col3, col4 = st.columns(4)


col1.metric(

    "Strategy",

    " → ".join(

        compound_display(x)

        for x in dry_result["compounds"]

    )

)


col2.metric(

    "Pit Lap(s)",

    ", ".join(

        str(x)

        for x in dry_result["pit_laps"]

    )

)


col3.metric(

    "Simulated Race Time",

    format_time(
        dry_result["total_time"]
    )

)


col4.metric(

    "Starting Position",

    f"P{starting_position}"

)


# ============================================================
# STRATEGY EXPLANATION
# ============================================================

if starting_position <= 3:

    position_text = (
        "Because the starting position is near the front, "
        "a strategy that protects track position is valuable."
    )

elif starting_position <= 10:

    position_text = (
        "The starting position is in the competitive midfield/top "
        "group, so the model balances tyre life and pace."
    )

else:

    position_text = (
        "Starting further down the grid makes aggressive tyre "
        "strategies more valuable."
    )


st.write(

    f"**Strategy reasoning:** "
    f"The simulator selected the strategy with the lowest "
    f"calculated race time after accounting for tyre degradation, "
    f"circuit stress and pit-stop loss. {position_text}"

)


# ============================================================
# RAIN
# ============================================================

if rain_probability == "No Rain":

    st.success(

        "☀️ No Rain selected — "
        "the simulator uses the dry strategy only."

    )


else:

    rain_laps = calculate_rain_laps(

        race,

        rain_duration

    )


    st.subheader(
        "🌧️ Possible Rain Scenarios"
    )


    st.write(

        f"Rain probability: **{rain_probability}**  \n"
        f"Entered rain duration: **{rain_duration} minutes**  \n"
        f"Estimated rain duration: **~{rain_laps} racing laps**"

    )


    # --------------------------------------------------------
    # 50% RAIN — NO RAIN BRANCH
    # --------------------------------------------------------

    if rain_probability == "50% Rain":

        st.markdown(
            "### ☀️ Scenario — Rain Does Not Occur"
        )


        st.info(

            f"Because this is a 50% rain probability, "
            f"the race can remain completely dry.\n\n"
            f"**Strategy:** "
            f'{" → ".join(compound_display(x) for x in dry_result["compounds"])}\n\n'
            f"**Pit:** "
            f'{", ".join(str(x) for x in dry_result["pit_laps"])}'

        )


    # --------------------------------------------------------
    # RAIN WINDOWS
    # --------------------------------------------------------

    windows = generate_rain_windows(

        race,

        rain_duration

    )


    st.markdown(
        "### 🌧️ Rain Timing Scenarios"
    )


    for index, (
        rain_start,
        rain_end
    ) in enumerate(windows):


        result = simulate_rain_scenario(

            race,

            car_class,

            rain_start,

            rain_end

        )


        with st.container(border=True):

            st.markdown(

                f"### Scenario {index + 1}"

            )


            col1, col2, col3 = st.columns(3)


            col1.metric(

                "Rain Window",

                f"Lap {rain_start} → {rain_end}"

            )


            col2.metric(

                "Dry Tyre",

                result["dry_compound"]

            )


            col3.metric(

                "Simulated Time",

                format_time(
                    result["total_time"]
                )

            )


            st.write(

                f"**Strategy:** "
                f"{result['dry_compound']} → "
                f"Intermediate → "
                f"{result['dry_compound']}"

            )


            st.write(

                f"**Pit window:** "
                f"Lap {result['pit_laps'][0]} "
                f"and Lap {result['pit_laps'][1]}"

            )


            st.caption(

                "This is a deterministic scenario. "
                "The simulator does not randomly choose "
                "when the rain starts."

            )


# ============================================================
# LAP-BY-LAP DATA
# ============================================================

with st.expander(
    "📊 View Dry Strategy Lap-by-Lap Data"
):

    lap_df = pd.DataFrame(
        dry_result["lap_data"]
    )


    st.dataframe(

        lap_df,

        use_container_width=True,

        hide_index=True

    )


# ============================================================
# TYRE INFORMATION
# ============================================================

with st.expander(
    "🛞 Tyre Model"
):

    tyre_table = pd.DataFrame({

        "Compound": [
            "C1",
            "C2",
            "C3",
            "C4",
            "C5",
            "C6",
            "Intermediate"
        ],

        "Category": [
            "Hard",
            "Hard",
            "Medium",
            "Medium",
            "Soft",
            "Soft",
            "Wet"
        ],

        "Peak End": [
            TYRE_MODEL["C1"]["peak_end"],
            TYRE_MODEL["C2"]["peak_end"],
            TYRE_MODEL["C3"]["peak_end"],
            TYRE_MODEL["C4"]["peak_end"],
            TYRE_MODEL["C5"]["peak_end"],
            TYRE_MODEL["C6"]["peak_end"],
            TYRE_MODEL["INT"]["peak_end"]
        ],

        "Critical Lap": [
            TYRE_MODEL["C1"]["critical_lap"],
            TYRE_MODEL["C2"]["critical_lap"],
            TYRE_MODEL["C3"]["critical_lap"],
            TYRE_MODEL["C4"]["critical_lap"],
            TYRE_MODEL["C5"]["critical_lap"],
            TYRE_MODEL["C6"]["critical_lap"],
            TYRE_MODEL["INT"]["critical_lap"]
        ]

    })


    st.dataframe(

        tyre_table,

        use_container_width=True,

        hide_index=True

    )


# ============================================================
# MODEL NOTES
# ============================================================

with st.expander(
    "ℹ️ Model Assumptions"
):

    st.markdown(
        """
        ### Tyres

        All tyres experience degradation.

        **C1/C2:** long-life hard compounds.

        **C3/C4:** balanced medium compounds.

        **C5/C6:** fast soft compounds with an earlier
        degradation window.

        **Intermediate:** used for wet conditions and also
        experiences degradation with tyre age.

        ### Previous Lap

        Each lap uses a small contribution from the previous
        lap time. This prevents every lap from being calculated
        as a completely independent number.

        ### Rain

        Rain is deterministic.

        **0%:** no rain.

        **50%:** rain may happen or may not happen.

        **100%:** rain definitely happens.

        The model does not randomly choose the rain start.

        Instead it evaluates representative early, middle
        and late rain windows.

        ### Wet Tyre

        Only the **Intermediate** is used in this simplified
        project. Full Wet is intentionally excluded.

        ### Car Classes

        Cars inside the same class are treated as having equal
        performance.

        ### Important

        Race pace, pit-stop loss, circuit-stress numbers,
        car-class differences and tyre degradation curves
        are simulation assumptions for this educational project.
        They are not official F1 telemetry.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "F1 Race Strategy Simulator • 2025 Dataset • "
    "Deterministic Mathematical Simulation"
)
