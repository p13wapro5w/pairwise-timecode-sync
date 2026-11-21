import math

def frame_diff(a, b):
    """帧差。"""
    raise NotImplementedError("TODO: frame_diff")

def adaptive_threshold(level, noise):
    """自适应阈值。"""
    raise NotImplementedError("TODO: adaptive_threshold")

def drop_frames(minutes):
    """drop-frame 帧数。"""
    raise NotImplementedError("TODO: drop_frames")

def drift_correct(frames, ppm, hours):
    """漂移校正。"""
    raise NotImplementedError("TODO: drift_correct")

def midnight_wrap(frame, day):
    """跨天归一。"""
    raise NotImplementedError("TODO: midnight_wrap")

def sample_to_frame(samples, rate, fps):
    """采样转帧。"""
    raise NotImplementedError("TODO: sample_to_frame")

def relock(signal):
    """重新锁定。"""
    raise NotImplementedError("TODO: relock")

def offset_by_rate(offset, source_fps, target_fps):
    """帧率换算偏移。"""
    raise NotImplementedError("TODO: offset_by_rate")

def priority(ltc, vitc):
    """优先级。"""
    raise NotImplementedError("TODO: priority")

def export_format(drop_frame):
    """导出格式。"""
    raise NotImplementedError("TODO: export_format")

def tc_key(seed, index):
    """时间码键。"""
    raise NotImplementedError("TODO: tc_key")

def tc_to_frames(hours, minutes, seconds, frames, fps):
    """时间码转帧。"""
    raise NotImplementedError("TODO: tc_to_frames")

def frames_to_tc(frames, fps):
    """帧转时间码。"""
    raise NotImplementedError("TODO: frames_to_tc")

def is_drop(label):
    """drop 判定。"""
    raise NotImplementedError("TODO: is_drop")

def clamp_tc(frame, day):
    """时间码钳制。"""
    raise NotImplementedError("TODO: clamp_tc")
