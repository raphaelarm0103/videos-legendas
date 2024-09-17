from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from src.utils.utils import adjust_fontsize, srt_to_seconds
import pysrt


class VideoProcessor:
    def embed_subtitles(self, video_input_path, srt_path, output_path, sync_offset=0.0):
        video = VideoFileClip(video_input_path)
        video_width, video_height = video.size
        dynamic_fontsize = adjust_fontsize(video_height)
        subs = pysrt.open(srt_path, encoding='utf-8')

        subtitles_clips = []
        for sub in subs:
            start_time = max(0, srt_to_seconds(sub.start) + sync_offset)
            end_time = srt_to_seconds(sub.end) + sync_offset
            txt_clip = TextClip(
                sub.text.upper(),
                fontsize=dynamic_fontsize,
                color='white',
                stroke_color='black',
                stroke_width=2,
                font='Impact'
            ).set_position(('center', video.h - int(video.h * 0.1))).set_start(start_time).set_duration(
                end_time - start_time)

            subtitles_clips.append(txt_clip)

        final_clip = CompositeVideoClip([video] + subtitles_clips)
        final_clip.write_videofile(output_path, codec='libx264', fps=video.fps)
