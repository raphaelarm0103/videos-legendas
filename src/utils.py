from datetime import timedelta


def adjust_fontsize(video_height, scale_factor=0.05):
    return int(video_height * scale_factor)


def srt_to_seconds(time):
    return time.hours * 3600 + time.minutes * 60 + time.seconds + time.milliseconds / 1000
