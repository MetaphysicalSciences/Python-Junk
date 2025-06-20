import numpy as np
import sounddevice as sd
import random

def beefed_up_psych_audio(duration=60, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)


    drone = 0.3 * np.sin(2 * np.pi * 130 * t) + 0.2 * np.sin(2 * np.pi * 80 * t)


    whisper = np.zeros((len(t), 2))
    for _ in range(30):
        start = random.randint(0, len(t) - sample_rate // 10)
        length = random.randint(sample_rate // 20, sample_rate // 5)
        w_noise = np.random.uniform(-0.2, 0.2, length) * np.hanning(length)
        if random.random() < 0.5:
            whisper[start:start+length, 0] += w_noise  
        else:
            whisper[start:start+length, 1] += w_noise  


    speech_len = sample_rate * 2
    fake_speech = np.random.uniform(-0.3, 0.3, speech_len) * np.hanning(speech_len)
    fake_speech_rev = fake_speech[::-1]

    speech_track = np.zeros(len(t))
    speech_start = random.randint(sample_rate * 10, sample_rate * 20)
    speech_track[speech_start:speech_start+speech_len] += fake_speech_rev[:len(t) - speech_start]


    pulse = 0.7 * (np.sin(2 * np.pi * 0.25 * t) > 0).astype(float)

    # Combine everything
    final_left = (drone + whisper[:, 0] + speech_track) * pulse
    final_right = (drone + whisper[:, 1] + speech_track) * pulse
    stereo = np.column_stack((final_left, final_right))


    max_val = np.max(np.abs(stereo))
    if max_val > 0:
        stereo /= max_val * 1.1

    return stereo

def play_in_memory(audio, sample_rate=44100):
    print("▶ Playing beefed-up psychological audio. Focus. No interruptions. Close Your eyes be in a dark roomfor best effect and if you get headphones even better")
    sd.play(audio, sample_rate)
    sd.wait()
    print("⏹ Done. You good?")

if __name__ == "__main__":
    audio = beefed_up_psych_audio()
    play_in_memory(audio)
