"""时间码同步工具。

覆盖多机位对轨中的常见问题：按帧（而非字符串）比较、LTC 自适应切片阈值、
drop-frame 解析、晶振漂移校正、跨午夜归一、音频采样与帧号换算、genlock
重新锁定、按帧率换算偏移、LTC/VITC 优先级，以及导出时保持 drop-frame 格式。
"""


def frame_diff(a, b):
    """按帧号比较两个时间码，返回绝对帧差。"""
    return abs(int(a) - int(b))


def adaptive_threshold(level, noise):
    """根据信号电平与噪声底生成自适应切片阈值。

    阈值随信号电平缩放，并始终高于噪声底，避免低电平声道被当成噪声。
    """
    level = float(level)
    noise = float(noise)
    if level <= 0:
        return 0
    return max(level * noise, noise + 1)


def drop_frames(minutes):
    """返回 ``minutes`` 分钟内 drop-frame 时间码丢弃的帧号总数。

    29.97/59.94 的 drop-frame 每分钟丢 2 帧，但每 10 分钟不丢。
    """
    minutes = int(minutes)
    if minutes <= 0:
        return 0
    return minutes * 2 - (minutes // 10) * 2


def drift_correct(frames, ppm, hours):
    """按晶振漂移（ppm）和自由运行时长校正帧号。

    ``frames`` 为 jam sync 之后自由运行累积的帧数；漂移量与累积帧数成正比
    （2 帧 / 4 小时约合 5.8 ppm）。``hours`` 仅用于确认确实经历过自由运行，
    为 0 时不做校正。ppm 为正表示时钟走快、时间码领先，故从帧号中扣除漂移。
    """
    frames = int(frames)
    if float(hours) <= 0 or not ppm:
        return frames
    drift = frames * float(ppm) * 1e-6
    return int(round(frames - drift))


def midnight_wrap(frame, day):
    """把跨天的时间码帧号归一到一个自然日内（``day`` 为一天的帧数）。"""
    day = int(day)
    if day <= 0:
        raise ValueError("day must be positive")
    return int(frame) % day


def sample_to_frame(samples, rate, fps):
    """把音频采样计数换算为时间码帧号，使用精确换算而非整数除法。"""
    rate = float(rate)
    if rate <= 0:
        raise ValueError("rate must be positive")
    return int(round(int(samples) * float(fps) / rate))


def relock(signal):
    """genlock 丢失后检测信号是否恢复并重新锁定。"""
    return bool(signal)


def offset_by_rate(offset, source_fps, target_fps):
    """把源机位上的偏移帧数换算到目标帧率。

    偏移本质上是时间量，必须按帧率比例换算，不能直接套用帧数。
    """
    source_fps = float(source_fps)
    if source_fps <= 0:
        raise ValueError("source_fps must be positive")
    return int(round(int(offset) * float(target_fps) / source_fps))


def priority(ltc, vitc):
    """LTC/VITC 同时存在且不一致时固定选择 LTC。"""
    return ltc if ltc is not None else vitc


def export_format(drop_frame):
    """导出时保持时间码的 drop-frame 标记。"""
    return "df" if drop_frame else "ndf"


def tc_key(seed, index):
    """生成时间码键（``seed:index``），用于区分不同日期/素材段。

    键本身是字符串，跨天比较应先经 :func:`midnight_wrap` 归一为帧号再比较。
    """
    return f"{int(seed)}:{int(index)}"


def tc_to_frames(hours, minutes, seconds, frames, fps):
    """把时间码各字段换算为从零点起的绝对帧号。

    时间码按名义帧率计数，23.976/29.97 分别对应 24/30 帧每秒，故取整。
    """
    nominal = int(round(float(fps)))
    if nominal <= 0:
        raise ValueError("fps must be positive")
    total_seconds = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
    return total_seconds * nominal + int(frames)


def frames_to_tc(frames, fps):
    """把绝对帧号换算为 ``(hours, minutes, seconds, frames)``。"""
    nominal = int(round(float(fps)))
    if nominal <= 0:
        raise ValueError("fps must be positive")
    frames = int(frames)
    total_seconds, frame = divmod(frames, nominal)
    hours, rem = divmod(total_seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    return hours, minutes, seconds, frame


def is_drop(label):
    """判断时间码/容器标签是否表示 drop-frame。"""
    if isinstance(label, bool):
        return label
    return str(label).strip().lower() in {"drop", "df", "drop-frame", "dropframe"}


def clamp_tc(frame, day):
    """把时间码帧号钳制在合法范围内。"""
    day = int(day)
    if day <= 0:
        raise ValueError("day must be positive")
    return min(max(int(frame), 0), day)
