import numpy as np
import sounddevice as sd
import random

def break_the_mind(duration=140, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)


    base1 = np.sin(2 * np.pi * 96 * t)
    base2 = np.sin(2 * np.pi * 97.3 * t)
    drone = 0.3 * (base1 + base2)


    ring = np.sin(2 * np.pi * 8200 * t) * 0.05


    whisper_env = np.random.uniform(-1, 1, len(t)) * np.hanning(len(t))
    whisper_rev = whisper_env[::-1] * 0.2


    silence_mask = np.ones_like(t)
    for _ in range(15):
        start = random.randint(sample_rate * 5, len(t) - sample_rate // 4)
        end = start + random.randint(sample_rate // 20, sample_rate // 8)
        silence_mask[start:end] = 0


    left = (drone + ring + whisper_rev) * silence_mask
    right = (np.roll(drone, 100) + ring + np.roll(whisper_rev, -200)) * silence_mask


    audio = np.column_stack((left, right))


    audio /= np.max(np.abs(audio)) * 1.1
    return audio

if __name__ == "__main__":
    print("⚠️ Beginning audio... sit still, dark room, eyes closed.")
    audio = break_the_mind()
    sd.play(audio, 44100)
    sd.wait()
    print("✅ Done. If you felt nothing… you're not human.")
