
import streamlit as st
import pandas as pd
from dataclasses import dataclass
from typing import List, Dict, Tuple

st.set_page_config(
    page_title="BJJ Physical Training Engine v2",
    page_icon="🥋",
    layout="wide",
)

# ============================================================
# Evidence metadata
# ============================================================
EVIDENCE = {
    "bjj_demands": {
        "title": "Physical demands of Brazilian jiu-jitsu",
        "summary": (
            "BJJ is an intermittent grappling sport requiring repeated high-intensity efforts, "
            "whole-body strength, isometric endurance, grip capacity, and sufficient aerobic fitness "
            "to recover between intense actions and rounds."
        ),
        "source": "Andreato et al. (2017), systematic review",
        "url": "https://pubmed.ncbi.nlm.nih.gov/28194734/",
    },
    "resistance_training": {
        "title": "Resistance-training prescription",
        "summary": (
            "Progressive resistance training improves strength, power, muscle mass, and physical function. "
            "The engine uses multiple sets, controlled proximity to failure, full range of motion where tolerated, "
            "and progressive overload."
        ),
        "source": "ACSM Position Stand (2026)",
        "url": "https://pubmed.ncbi.nlm.nih.gov/41843416/",
    },
    "concurrent_training": {
        "title": "Concurrent strength and endurance training",
        "summary": (
            "Strength and endurance can be developed concurrently, but total fatigue and session placement matter. "
            "The engine reduces conditioning when mat load is high and avoids hard lower-body work immediately "
            "before the hardest sparring day."
        ),
        "source": "Huiberts et al. (2024), systematic review and meta-analysis",
        "url": "https://pubmed.ncbi.nlm.nih.gov/37847373/",
    },
    "session_rpe": {
        "title": "Training-load monitoring",
        "summary": (
            "Session-RPE is a practical method for estimating internal training load in combat sports. "
            "This prototype uses BJJ frequency, session duration, and hard-sparring frequency as a simple proxy."
        ),
        "source": "Slimani et al. (2017), review",
        "url": "https://pubmed.ncbi.nlm.nih.gov/28933715/",
    },
}

# ============================================================
# Exercise database
# ============================================================
EXERCISES = [
    {
        "name": "Medicine-Ball Chest Pass",
        "slot": "power_upper",
        "level": "beginner",
        "equipment": ["Full gym", "Basic gym"],
        "fatigue": 1,
        "duration_min": 6,
        "why": "Trains rapid upper-body force production with low fatigue before the main strength work.",
        "evidence": "resistance_training",
        "alternatives": ["Explosive Push-Up", "Band-Resisted Press"],
    },
    {
        "name": "Box Jump",
        "slot": "power_lower",
        "level": "beginner",
        "equipment": ["Full gym", "Basic gym", "Home/minimal"],
        "fatigue": 1,
        "duration_min": 6,
        "why": "Develops lower-body explosive intent with low repetition volume and limited metabolic fatigue.",
        "evidence": "resistance_training",
        "alternatives": ["Broad Jump", "Kettlebell Swing"],
    },
    {
        "name": "Goblet Squat",
        "slot": "knee_dominant",
        "level": "beginner",
        "equipment": ["Full gym", "Basic gym", "Home/minimal"],
        "fatigue": 2,
        "duration_min": 10,
        "why": "A technically accessible squat pattern for developing lower-body strength with controlled loading.",
        "evidence": "resistance_training",
        "alternatives": ["Leg Press", "Split Squat"],
    },
    {
        "name": "Leg Press",
        "slot": "knee_dominant",
        "level": "beginner",
        "equipment": ["Full gym", "Basic gym"],
        "fatigue": 2,
        "duration_min": 10,
        "why": "Provides stable knee- and hip-extensor strength work with low balance and coordination demand.",
        "evidence": "resistance_training",
        "alternatives": ["Goblet Squat", "Split Squat"],
    },
    {
        "name": "Rear-Foot-Elevated Split Squat",
        "slot": "knee_dominant",
        "level": "intermediate",
        "equipment": ["Full gym", "Basic gym", "Home/minimal"],
        "fatigue": 3,
        "duration_min": 11,
        "why": "Develops unilateral lower-body strength, but volume is restricted because soreness can interfere with mat training.",
        "evidence": "resistance_training",
        "alternatives": ["Reverse Lunge", "Step-Up"],
    },
    {
        "name": "Trap-Bar Deadlift",
        "slot": "hip_dominant",
        "level": "intermediate",
        "equipment": ["Full gym"],
        "fatigue": 2,
        "duration_min": 11,
        "why": "Builds whole-body force and hip-extensor strength with a relatively simple setup.",
        "evidence": "resistance_training",
        "alternatives": ["Romanian Deadlift", "Hip Thrust"],
    },
    {
        "name": "Romanian Deadlift",
        "slot": "hip_dominant",
        "level": "intermediate",
        "equipment": ["Full gym", "Basic gym"],
        "fatigue": 2,
        "duration_min": 11,
        "why": "Develops posterior-chain and hip-extensor strength relevant to posture, bridging, and force transfer.",
        "evidence": "resistance_training",
        "alternatives": ["Hip Thrust", "Dumbbell Romanian Deadlift"],
    },
    {
        "name": "Hip Thrust",
        "slot": "hip_dominant",
        "level": "beginner",
        "equipment": ["Full gym", "Basic gym"],
        "fatigue": 2,
        "duration_min": 10,
        "why": "Trains hip extension with a stable setup and low technical complexity.",
        "evidence": "resistance_training",
        "alternatives": ["Glute Bridge", "Romanian Deadlift"],
    },
    {
        "name": "Chest-Supported Row",
        "slot": "pull",
        "level": "beginner",
        "equipment": ["Full gym", "Basic gym"],
        "fatigue": 1,
        "duration_min": 9,
        "why": "Builds pulling strength while limiting unnecessary lower-back fatigue.",
        "evidence": "bjj_demands",
        "alternatives": ["Cable Row", "One-Arm Dumbbell Row"],
    },
    {
        "name": "Pull-Up / Assisted Pull-Up",
        "slot": "pull",
        "level": "intermediate",
        "equipment": ["Full gym", "Basic gym", "Home/minimal"],
        "fatigue": 2,
        "duration_min": 9,
        "why": "Develops relative pulling strength that supports opponent control and body repositioning.",
        "evidence": "bjj_demands",
        "alternatives": ["Lat Pulldown", "Band Pulldown"],
    },
    {
        "name": "Dumbbell Bench Press",
        "slot": "push",
        "level": "beginner",
        "equipment": ["Full gym", "Basic gym"],
        "fatigue": 2,
        "duration_min": 9,
        "why": "Provides general upper-body pushing strength with independent arm loading.",
        "evidence": "resistance_training",
        "alternatives": ["Push-Up", "Machine Chest Press"],
    },
    {
        "name": "Push-Up",
        "slot": "push",
        "level": "beginner",
        "equipment": ["Full gym", "Basic gym", "Home/minimal"],
        "fatigue": 1,
        "duration_min": 8,
        "why": "A simple and scalable upper-body pushing exercise with minimal equipment.",
        "evidence": "resistance_training",
        "alternatives": ["Incline Push-Up", "Dumbbell Bench Press"],
    },
    {
        "name": "Pallof Press",
        "slot": "trunk",
        "level": "beginner",
        "equipment": ["Full gym", "Basic gym", "Home/minimal"],
        "fatigue": 1,
        "duration_min": 6,
        "why": "Trains the trunk to resist unwanted rotation while maintaining posture under external force.",
        "evidence": "bjj_demands",
        "alternatives": ["Side Plank", "Dead Bug"],
    },
    {
        "name": "Farmer Carry",
        "slot": "grip",
        "level": "beginner",
        "equipment": ["Full gym", "Basic gym", "Home/minimal"],
        "fatigue": 2,
        "duration_min": 7,
        "why": "Combines grip, trunk stiffness, and locomotion without attempting to imitate a BJJ technique.",
        "evidence": "bjj_demands",
        "alternatives": ["Suitcase Carry", "Timed Dumbbell Hold"],
    },
    {
        "name": "Towel Hang",
        "slot": "grip",
        "level": "intermediate",
        "equipment": ["Full gym", "Basic gym", "Home/minimal"],
        "fatigue": 2,
        "duration_min": 6,
        "why": "Provides scalable isometric grip-endurance work relevant to prolonged gripping demands.",
        "evidence": "bjj_demands",
        "alternatives": ["Gi Hang", "Timed Bar Hang"],
    },
]

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

RED_FLAGS = [
    "None of these",
    "Chest pain during exercise or at rest",
    "Unexplained fainting or severe dizziness",
    "New numbness, weakness, or loss of coordination",
    "Suspected concussion or persistent symptoms after a recent head impact",
    "Recent fracture, dislocation, or surgery without medical clearance",
    "Severe pain at rest or obvious joint deformity/instability",
    "A clinician has told me not to exercise",
]

# ============================================================
# Rule engine
# ============================================================
def estimate_bjj_load(sessions: int, hard_sessions: int, duration: int) -> Tuple[int, str]:
    duration_factor = 1 if duration <= 60 else 2 if duration <= 90 else 3
    score = sessions * duration_factor + hard_sessions * 2
    label = "Low" if score <= 6 else "Moderate" if score <= 11 else "High"
    return score, label


def safety_result(red_flags: List[str], pain_status: str) -> Tuple[str, List[str]]:
    reasons = [x for x in red_flags if x != "None of these"]
    if reasons:
        return "STOP", reasons
    if pain_status == "Pain limits normal BJJ training or daily activities":
        return "STOP", ["Pain currently limits normal training or daily activities."]
    if pain_status == "Recurring mild pain that does not stop training":
        return "CONSERVATIVE", ["Recurring mild pain was reported."]
    return "CLEAR", []


def choose_exercise(slot: str, equipment: str, beginner: bool, max_fatigue: int, used: set):
    for exercise in EXERCISES:
        if exercise["slot"] != slot:
            continue
        if equipment not in exercise["equipment"]:
            continue
        if beginner and exercise["level"] == "intermediate":
            continue
        if exercise["fatigue"] > max_fatigue:
            continue
        if exercise["name"] in used:
            continue
        return exercise
    return None


def prescription(goal: str, slot: str, base_sets: int):
    if slot.startswith("power"):
        return 2, "3–5", "Fast and technically clean; stop before fatigue", "90–180 s"
    if slot in {"trunk", "grip"}:
        return 2, "20–40 s", "Controlled; stop before grip or trunk position collapses", "60–90 s"
    if goal == "Maximum strength":
        return base_sets, "4–6", "2–3 RIR", "2–3 min"
    if goal == "Muscle gain":
        return base_sets, "6–12", "2–3 RIR", "90–150 s"
    return base_sets, "6–10", "2–4 RIR", "90–150 s"


def build_strength_session(name: str, profile: Dict, load_label: str, conservative: bool):
    beginner = profile["strength_experience"] == "No regular resistance training"
    max_fatigue = 1 if conservative else 2 if load_label == "High" else 3
    base_sets = 2 if beginner or load_label == "High" or profile["recovery"] == "Poor" else 3

    # Alternate the emphasis of A and B.
    slots = (
        ["power_lower", "knee_dominant", "pull", "hip_dominant", "push", "trunk", "grip"]
        if name == "Strength A"
        else ["power_upper", "hip_dominant", "push", "knee_dominant", "pull", "trunk", "grip"]
    )

    rows, used = [], set()
    total_minutes = 8  # warm-up allowance

    for slot in slots:
        ex = choose_exercise(slot, profile["equipment"], beginner, max_fatigue, used)
        if ex is None:
            continue
        sets, reps, intensity, rest = prescription(profile["goal"], slot, base_sets)
        row = {
            "Session": name,
            "Exercise": ex["name"],
            "Sets": sets,
            "Reps / duration": reps,
            "Intensity": intensity,
            "Rest": rest,
            "Why this exercise": ex["why"],
            "Alternatives": " / ".join(ex["alternatives"]),
            "Evidence": EVIDENCE[ex["evidence"]]["source"],
            "_duration": ex["duration_min"],
        }
        rows.append(row)
        used.add(ex["name"])
        total_minutes += ex["duration_min"]

    # Keep the session within the user's available time by removing lowest-priority end slots.
    while rows and total_minutes > profile["session_minutes"]:
        removed = rows.pop()
        total_minutes -= removed["_duration"]

    for row in rows:
        row.pop("_duration", None)
    return rows


def build_conditioning(profile: Dict, load_label: str):
    if load_label == "High" or profile["recovery"] == "Poor":
        return [{
            "Session": "Conditioning",
            "Exercise": "Easy aerobic work",
            "Sets": 1,
            "Reps / duration": "25–40 min",
            "Intensity": "Conversational pace / RPE 3–4",
            "Rest": "Continuous",
            "Why this exercise": "BJJ load or recovery burden is already high, so another hard interval session is avoided.",
            "Alternatives": "Bike / rower / incline walk",
            "Evidence": EVIDENCE["concurrent_training"]["source"],
        }]

    if profile["goal"] == "Late-round conditioning":
        modality = {
            "Bike": "Stationary-bike intervals",
            "Rowing machine": "Rowing intervals",
            "Running": "Running intervals",
            "No preference": "Bike or rowing intervals",
        }[profile["conditioning"]]
        return [{
            "Session": "Conditioning",
            "Exercise": modality,
            "Sets": 5,
            "Reps / duration": "2 min hard / 2 min easy",
            "Intensity": "RPE 8; hard but not maximal",
            "Rest": "2 min easy movement",
            "Why this exercise": "Provides a measurable repeated-effort stimulus without copying technical BJJ movements.",
            "Alternatives": "4 × 3 min / 6 × 90 s",
            "Evidence": EVIDENCE["bjj_demands"]["source"],
        }]

    duration = "35–50 min" if profile["goal"] == "Aerobic base" else "30–40 min"
    return [{
        "Session": "Conditioning",
        "Exercise": "Easy aerobic work",
        "Sets": 1,
        "Reps / duration": duration,
        "Intensity": "Conversational pace / RPE 3–4",
        "Rest": "Continuous",
        "Why this exercise": "Adds aerobic development without duplicating the high-intensity stress already present in sparring.",
        "Alternatives": "Bike / rower / incline walk",
        "Evidence": EVIDENCE["concurrent_training"]["source"],
    }]


def nearest_available_day(target_index: int, available: List[str], occupied: set):
    for distance in range(0, 7):
        for candidate in [target_index - distance, target_index + distance]:
            day = DAYS[candidate % 7]
            if day in available and day not in occupied:
                return day
    return None


def place_sessions(profile: Dict, physical_names: List[str]):
    bjj_days = profile["bjj_days"]
    hard_days = set(profile["hard_bjj_days"])
    available = profile["physical_days"]
    occupied = set()
    schedule_rows = []

    # Add BJJ rows first.
    for day in DAYS:
        if day in bjj_days:
            session_type = "Hard BJJ sparring" if day in hard_days else "BJJ training"
            schedule_rows.append({"Day": day, "Session": session_type, "Placement rationale": "User-selected mat training day."})

    # Score possible physical-training days.
    def day_score(day):
        idx = DAYS.index(day)
        prev_day = DAYS[(idx - 1) % 7]
        next_day = DAYS[(idx + 1) % 7]
        score = 0
        if day in bjj_days:
            score -= 5
        if next_day in hard_days:
            score -= 4
        if prev_day in hard_days:
            score -= 2
        if day in available:
            score += 3
        return score

    ranked_days = sorted(available, key=day_score, reverse=True)

    for session_name in physical_names:
        chosen = next((d for d in ranked_days if d not in occupied), None)
        if chosen is None:
            break
        occupied.add(chosen)
        idx = DAYS.index(chosen)
        next_day = DAYS[(idx + 1) % 7]
        rationale = "Selected from the user's available days."
        if next_day in hard_days:
            rationale += " Warning: hard sparring follows the next day; keep volume conservative."
        elif chosen not in bjj_days:
            rationale += " Avoids same-day overlap with BJJ."
        schedule_rows.append({"Day": chosen, "Session": session_name, "Placement rationale": rationale})

    order = {day: i for i, day in enumerate(DAYS)}
    return pd.DataFrame(sorted(schedule_rows, key=lambda x: order[x["Day"]]))


def four_week_progression(conservative: bool, competition: str):
    if conservative:
        rows = [
            ["Week 1", "Use tolerable loads and keep 3–4 RIR", "No increase in symptoms"],
            ["Week 2", "Add one repetition only when clearly comfortable", "Symptoms remain stable during and after training"],
            ["Week 3", "Maintain or use the smallest possible load increase", "BJJ quality remains stable"],
            ["Week 4", "Reduce sets by 25–35%", "Finish the week fresher"],
        ]
    else:
        rows = [
            ["Week 1", "Establish loads at the prescribed RIR", "Stable technique"],
            ["Week 2", "Add one repetition per set where possible", "Target RIR maintained"],
            ["Week 3", "Add 2.5–5% load after reaching the top of the rep range", "No meaningful drop in BJJ quality"],
            ["Week 4", "Maintain or reduce volume by 20–30% according to fatigue", "Finish the week fresher"],
        ]

    if competition == "Within 2 weeks":
        rows[-2][1] = "Maintain intensity but reduce total sets by about one third"
        rows[-1][1] = "Very low volume; avoid unfamiliar exercises"
    return pd.DataFrame(rows, columns=["Week", "Progression rule", "Checkpoint"])


def feedback_adjustment(session_rpe: int, pain: int, sleep: str, bjj_quality: str, completed: str):
    actions = []
    if pain >= 7:
        return [
            "Stop automatic progression.",
            "Do not use the app to decide whether continued training is safe.",
            "Seek assessment from an appropriate healthcare professional.",
        ]
    if pain >= 4:
        actions += [
            "Reduce the next session's load by approximately 10%.",
            "Replace the exercise that provoked symptoms with the listed alternative.",
            "Do not progress load until symptoms return to baseline.",
        ]
    if session_rpe >= 9 and sleep == "Poor":
        actions.append("Reduce the next physical session's total sets by about 20%.")
    if bjj_quality == "Clearly worse":
        actions.append("Remove the conditioning session or reduce one set from each main strength exercise.")
    if completed == "Completed easily" and session_rpe <= 7 and pain <= 2:
        actions.append("Progress using the next planned repetition or load increase.")
    elif completed == "Could not complete":
        actions.append("Keep or reduce the current load; do not add weight next time.")
    if not actions:
        actions.append("Maintain the current plan for another week.")
    return actions

# ============================================================
# UI
# ============================================================
st.title("🥋 BJJ Physical Training Engine — v2")
st.caption(
    "Multiple-choice, rule-based prototype for apparently healthy adult BJJ practitioners. "
    "It does not diagnose, rehabilitate injuries, or provide return-to-sport clearance."
)

if "step" not in st.session_state:
    st.session_state.step = 1
if "answers" not in st.session_state:
    st.session_state.answers = {}

steps = ["Safety", "BJJ profile", "Goal", "Schedule", "Recovery", "Program", "Feedback"]
st.progress((st.session_state.step - 1) / (len(steps) - 1))
st.write(f"**Step {st.session_state.step} of {len(steps)} — {steps[st.session_state.step - 1]}**")

def next_step():
    st.session_state.step += 1

def previous_step():
    st.session_state.step = max(1, st.session_state.step - 1)

if st.session_state.step == 1:
    red_flags = st.multiselect("Select every statement that applies:", RED_FLAGS, default=["None of these"])
    pain_status = st.radio(
        "Current pain status:",
        [
            "No current pain",
            "Minor stable discomfort that does not affect training",
            "Recurring mild pain that does not stop training",
            "Pain limits normal BJJ training or daily activities",
        ],
    )
    st.warning("A red flag or activity-limiting pain stops automatic program generation.")
    if st.button("Continue", type="primary"):
        st.session_state.answers.update(red_flags=red_flags, pain_status=pain_status)
        next_step()
        st.rerun()

elif st.session_state.step == 2:
    c1, c2 = st.columns(2)
    with c1:
        bjj_experience = st.selectbox("BJJ experience", ["Under 1 year", "1–3 years", "3–6 years", "Over 6 years"])
        bjj_sessions = st.select_slider("BJJ sessions per week", [1, 2, 3, 4, 5, 6, 7], value=3)
        hard_sessions = st.select_slider("Hard-sparring sessions per week", [0, 1, 2, 3, 4, 5, 6, 7], value=2)
    with c2:
        bjj_duration = st.selectbox("Typical BJJ-session duration", [45, 60, 75, 90, 120], index=3)
        strength_experience = st.selectbox(
            "Resistance-training experience",
            ["No regular resistance training", "Less than 1 year", "1–3 years", "More than 3 years"],
        )
    b1, b2 = st.columns(2)
    if b1.button("Back"):
        previous_step(); st.rerun()
    if b2.button("Continue", type="primary"):
        st.session_state.answers.update(
            bjj_experience=bjj_experience,
            bjj_sessions=bjj_sessions,
            hard_sessions=min(hard_sessions, bjj_sessions),
            bjj_duration=bjj_duration,
            strength_experience=strength_experience,
        )
        next_step(); st.rerun()

elif st.session_state.step == 3:
    goal = st.radio(
        "Primary goal for this four-week block:",
        ["General BJJ strength", "Maximum strength", "Late-round conditioning", "Aerobic base", "Muscle gain"],
    )
    competition = st.radio(
        "Competition timing:",
        ["No competition planned", "More than 8 weeks away", "In 3–8 weeks", "Within 2 weeks"],
    )
    conditioning = st.selectbox("Preferred conditioning modality", ["Bike", "Rowing machine", "Running", "No preference"])
    b1, b2 = st.columns(2)
    if b1.button("Back"):
        previous_step(); st.rerun()
    if b2.button("Continue", type="primary"):
        st.session_state.answers.update(goal=goal, competition=competition, conditioning=conditioning)
        next_step(); st.rerun()

elif st.session_state.step == 4:
    st.subheader("Weekly schedule")
    bjj_days = st.multiselect("BJJ training days", DAYS, default=["Tuesday", "Thursday", "Sunday"])
    hard_bjj_days = st.multiselect("Hard-sparring days", bjj_days, default=[d for d in ["Thursday", "Sunday"] if d in bjj_days])
    physical_days = st.multiselect(
        "Days available for physical training",
        DAYS,
        default=["Monday", "Wednesday", "Friday", "Saturday"],
    )
    physical_sessions = st.select_slider("Physical-training sessions per week", [1, 2, 3], value=2)
    session_minutes = st.selectbox("Available time per physical session", [30, 45, 60, 75], index=2)
    equipment = st.radio("Training environment", ["Full gym", "Basic gym", "Home/minimal"])
    b1, b2 = st.columns(2)
    if b1.button("Back"):
        previous_step(); st.rerun()
    if b2.button("Continue", type="primary"):
        if len(physical_days) < physical_sessions:
            st.error("Select at least as many available physical-training days as planned sessions.")
        elif not bjj_days:
            st.error("Select at least one BJJ training day.")
        else:
            st.session_state.answers.update(
                bjj_days=bjj_days,
                hard_bjj_days=hard_bjj_days,
                physical_days=physical_days,
                physical_sessions=physical_sessions,
                session_minutes=session_minutes,
                equipment=equipment,
            )
            next_step(); st.rerun()

elif st.session_state.step == 5:
    recovery = st.radio("Recovery over the last two weeks:", ["Good", "Average", "Poor"])
    b1, b2 = st.columns(2)
    if b1.button("Back"):
        previous_step(); st.rerun()
    if b2.button("Generate program", type="primary"):
        st.session_state.answers.update(recovery=recovery)
        next_step(); st.rerun()

elif st.session_state.step == 6:
    p = st.session_state.answers
    safety, reasons = safety_result(p["red_flags"], p["pain_status"])

    if safety == "STOP":
        st.error("Automatic program generation stopped.")
        st.write(
            "Your answers are outside this prototype's scope. Do not use this app to decide whether it is safe to train. "
            "Seek assessment from an appropriate physician or qualified healthcare professional."
        )
        for reason in reasons:
            st.write(f"- {reason}")
    else:
        conservative = safety == "CONSERVATIVE"
        load_score, load_label = estimate_bjj_load(p["bjj_sessions"], p["hard_sessions"], p["bjj_duration"])

        physical_names = ["Strength A"]
        if p["physical_sessions"] >= 2:
            physical_names.append("Strength B")
        if p["physical_sessions"] >= 3:
            physical_names.append("Conditioning")

        rows = build_strength_session("Strength A", p, load_label, conservative)
        if p["physical_sessions"] >= 2:
            rows += build_strength_session("Strength B", p, load_label, conservative)
        if p["physical_sessions"] >= 3:
            rows += build_conditioning(p, load_label)

        program = pd.DataFrame(rows)
        weekly_schedule = place_sessions(p, physical_names)

        st.success("Program generated")
        if conservative:
            st.warning(
                "Recurring pain was reported. This is not a rehabilitation program. "
                "Exercise fatigue and progression were reduced; professional assessment remains advisable."
            )

        st.subheader("Profile summary")
        st.dataframe(pd.DataFrame([{
            "BJJ experience": p["bjj_experience"],
            "BJJ sessions/week": p["bjj_sessions"],
            "Hard sparring/week": p["hard_sessions"],
            "Estimated BJJ load": f"{load_label} ({load_score})",
            "Primary goal": p["goal"],
            "Physical sessions/week": p["physical_sessions"],
            "Recovery": p["recovery"],
        }]), use_container_width=True, hide_index=True)

        st.subheader("Suggested weekly placement")
        st.dataframe(weekly_schedule, use_container_width=True, hide_index=True)

        st.subheader("Physical-training sessions")
        st.dataframe(program, use_container_width=True, hide_index=True)

        st.subheader("Four-week progression")
        st.dataframe(four_week_progression(conservative, p["competition"]), use_container_width=True, hide_index=True)

        st.subheader("Core placement rules")
        st.write("- Avoid hard lower-body work immediately before the hardest sparring session.")
        st.write("- Keep at least one low-load or rest day each week.")
        st.write("- Stop strength sets when technique breaks down; do not chase failure.")
        st.write("- When BJJ load rises unexpectedly, reduce physical-training volume before reducing technical practice.")
        if p["competition"] == "Within 2 weeks":
            st.write("- Competition is close: reduce total sets and avoid unfamiliar exercises.")

        st.subheader("Evidence used by the engine")
        for item in EVIDENCE.values():
            with st.expander(item["title"]):
                st.write(item["summary"])
                st.markdown(f"**Source:** [{item['source']}]({item['url']})")

        st.download_button(
            "Download physical program as CSV",
            program.to_csv(index=False).encode("utf-8-sig"),
            "bjj_physical_program.csv",
            "text/csv",
        )
        st.download_button(
            "Download weekly schedule as CSV",
            weekly_schedule.to_csv(index=False).encode("utf-8-sig"),
            "bjj_weekly_schedule.csv",
            "text/csv",
        )

    c1, c2 = st.columns(2)
    if c1.button("Back"):
        previous_step(); st.rerun()
    if c2.button("Continue to weekly feedback", type="primary", disabled=(safety == "STOP")):
        next_step(); st.rerun()

else:
    st.subheader("Weekly feedback and automatic adjustment")
    session_rpe = st.slider("Average physical-session RPE", 1, 10, 7)
    pain = st.slider("Highest pain during or after physical training", 0, 10, 0)
    sleep = st.radio("Sleep this week", ["Good", "Average", "Poor"])
    bjj_quality = st.radio("BJJ performance compared with normal", ["Better", "Similar", "Clearly worse"])
    completed = st.radio("Program completion", ["Completed easily", "Completed as planned", "Could not complete"])

    if st.button("Calculate next-week adjustment", type="primary"):
        actions = feedback_adjustment(session_rpe, pain, sleep, bjj_quality, completed)
        st.subheader("Recommended adjustment")
        for action in actions:
            st.write(f"- {action}")
        st.info(
            "This feedback rule is deliberately conservative. It adjusts volume and progression, "
            "but it does not diagnose pain or decide medical clearance."
        )

    st.divider()
    if st.button("Start over"):
        st.session_state.step = 1
        st.session_state.answers = {}
        st.rerun()

st.sidebar.header("Prototype boundaries")
st.sidebar.write(
    "Included: apparently healthy adults, 1–3 physical sessions per week, four-week planning, "
    "multiple-choice intake, schedule placement, exercise rationale, and simple weekly adaptation."
)
st.sidebar.write(
    "Excluded: diagnosis, rehabilitation, return-to-sport clearance, rapid weight cutting, minors, pregnancy, "
    "medication advice, and individualized clinical exercise prescription."
)
