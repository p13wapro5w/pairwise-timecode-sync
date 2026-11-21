import pytest
import math
from media import timecode_sync as mod

CASES = [
    ("diff", 'm.frame_diff(10, 8) == 2'),
    ("threshold", 'm.adaptive_threshold(2, 3) == 6'),
    ("drop", 'm.drop_frames(1) == 2'),
    ("drift", 'm.drift_correct(1000, 0, 4) == 1000'),
    ("midnight", 'm.midnight_wrap(100, 24) == 4'),
    ("sample", 'm.sample_to_frame(48000, 48000, 24) == 24'),
    ("relock", 'm.relock(True) is True'),
    ("offset", 'm.offset_by_rate(24, 24, 48) == 48'),
    ("priority", 'm.priority(1, 0) == 1'),
    ("export", 'm.export_format(True) == "df"'),
    ("key", 'm.tc_key(3, 2) == "3:2"'),
    ("toframes", 'm.tc_to_frames(0, 0, 1, 2, 25) == 27'),
    ("totc", 'm.frames_to_tc(27, 25) == (0, 0, 1, 2)'),
    ("dropflag", 'm.is_drop("drop") is True'),
    ("clamp", 'm.clamp_tc(30, 24) == 24')
]

@pytest.mark.parametrize("name,expr", CASES, ids=[c[0] for c in CASES])
def test_contract(name, expr):
    assert eval(expr, {"m": mod, "approx": pytest.approx, "math": math})
