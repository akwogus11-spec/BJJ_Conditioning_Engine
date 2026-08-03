
from app import estimate_bjj_load, safety_result

def test_bjj_load_low():
    score, label = estimate_bjj_load(2, 0, 60)
    assert label == "Low"

def test_bjj_load_high():
    score, label = estimate_bjj_load(5, 4, 90)
    assert label == "High"

def test_red_flag_stops():
    result, reasons = safety_result(["Chest pain during exercise or at rest"], "No current pain")
    assert result == "STOP"

def test_recurring_pain_conservative():
    result, reasons = safety_result(["None of these"], "Recurring mild pain that does not stop training")
    assert result == "CONSERVATIVE"
