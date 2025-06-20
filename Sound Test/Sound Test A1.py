import numpy as np
import sounddevice as sd
import soundfile as sf

def generate_high_freq_psycho_audio(duration=60, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)


    base_freq_left = 4000
    base_freq_right = 4008

    left_tone = 0.25 * np.sin(2 * np.pi * base_freq_left * t)
    right_tone = 0.25 * np.sin(2 * np.pi * base_freq_right * t)


    ring_mod_freq = 6700
    modulator = np.sin(2 * np.pi * ring_mod_freq * t)
    ring_mod = 0.15 * modulator * np.sin(2 * np.pi * 1300 * t)


    flutter = 0.5 * (1 + np.sin(2 * np.pi * 0.5 * t))


    left_channel = (left_tone + ring_mod) * flutter
    right_channel = (right_tone + ring_mod) * flutter


    stereo_audio = np.column_stack((left_channel, right_channel))


    max_val = np.max(np.abs(stereo_audio))
    if max_val > 0:
        stereo_audio = stereo_audio / max_val * 0.8

    return stereo_audio

def save_audio(audio, filename="high_freq_psycho_audio.wav", sample_rate=44100):
    sf.write(filename, audio, sample_rate)
    print(f"[✔] Audio saved as {filename}")

def play_audio(audio, sample_rate=44100):
    print("🔊 Playing audio... Use good speakers (NO headphones)")
    sd.play(audio, sample_rate)
    sd.wait()
    print("⏹ Playback finished.")

if __name__ == "__main__":
    audio = generate_high_freq_psycho_audio()
    save_audio(audio)
    play_audio(audio)
