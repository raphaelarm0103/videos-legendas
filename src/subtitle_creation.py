from datetime import timedelta
import srt


class SubtitleCreator:
    def create_word_srt(self, segments, srt_file):
        subtitles = []
        index = 1
        for segment in segments:
            if 'words' in segment and segment['words']:
                for word in segment['words']:
                    start = timedelta(seconds=float(word['start']))
                    end = timedelta(seconds=float(word['end']))
                    content = word['word'].strip()
                    subtitles.append(srt.Subtitle(index=index, start=start, end=end, content=content))
                    index += 1

        with open(srt_file, 'w', encoding='utf-8') as file:
            file.write(srt.compose(subtitles))
