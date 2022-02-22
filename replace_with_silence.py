"""
replace_with_silence.py
replacing segments of audio with silence;
"""
import os
from pydub import AudioSegment

def replace(wav_fp, timestamps_to_silence):
	"""
	wav_fp(str): string path to the audio wav filepath;
	timestamps_to_silence(list[tuple[str, str]]): list of start, end timestamps in seconds to
		silence
		ex: [(2, 7), (12, 25)] would be silencing from seconds 2 to 7 and 12 to 25.
	"""
	audio = AudioSegment.from_wav(wav_fp)
	new_audio = AudioSegment.empty()
	timestamps_to_silence.sort()

	for idx, pair in enumerate(timestamps_to_silence):
		start_s, end_s = pair
		start_ms = start_s * 1000
		end_ms = end_s * 1000
		silence = AudioSegment.silent(duration=end_ms - start_ms)
		if idx == 0:
			new_audio += audio[:start_ms] + silence
		else:
			new_audio += audio[timestamps_to_silence[idx - 1][1] * 1000:start_ms] + silence
	new_audio += audio[timestamps_to_silence[-1][1] * 1000:]
	out_fn = f'silenced_{os.path.basename(wav_fp)}'
	out_fp = os.path.join(os.path.dirname(wav_fp), out_fn)
	assert len(new_audio) == len(audio), f'{len(new_audio)}, {len(audio)}\n{wav_fp}'
	new_audio.export(out_fp, format='wav')
	print(out_fp)

def main():
	"""
	main entrypoint;
	"""
	wav_fp = "some_wav.wav" ## insert your own wav file here;
	timestamps_to_silence = [(2, 7), (12, 25)]
	replace(wav_fp, timestamps_to_silence)

if __name__ == '__main__':
	main()
