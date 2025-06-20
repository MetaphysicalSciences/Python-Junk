import numpy as np
import sounddevice as sd

sample_rate = 44100
bpm = 120
bar_length_sec = 60 / bpm * 4  # 4 beats per bar

def sine_wave(freq, duration, amplitude=1.0):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    return amplitude * np.sin(2 * np.pi * freq * t)

def saw_wave(freq, duration, amplitude=1.0):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    return amplitude * 2 * (t * freq - np.floor(t * freq + 0.5))

def kick_drum(duration):
    length = int(sample_rate * duration)
    t = np.linspace(0, duration, length, False)
    sine_part = np.sin(2 * np.pi * 60 * t) * np.exp(-30 * t)
    noise_part = (np.random.rand(length) * 2 - 1) * np.exp(-60 * t) * 0.1
    return sine_part + noise_part

def snare_drum(duration):
    length = int(sample_rate * duration)
    noise = np.random.rand(length) * 2 - 1
    envelope = np.exp(-40 * np.linspace(0, duration, length))
    return noise * envelope * 0.2

def hi_hat_closed(duration):
    length = int(sample_rate * duration)
    noise = np.random.rand(length) * 2 - 1
    envelope = np.exp(-150 * np.linspace(0, duration, length))
    filtered = np.convolve(noise, np.ones(10)/10, mode='same')
    return filtered * envelope * 0.08

def hi_hat_open(duration):
    length = int(sample_rate * duration)
    noise = np.random.rand(length) * 2 - 1
    envelope = np.exp(-20 * np.linspace(0, duration, length))
    filtered = np.convolve(noise, np.ones(30)/30, mode='same')
    return filtered * envelope * 0.08

def bass_note(freq, duration):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    base = 0.4 * np.sin(2 * np.pi * freq * t)
    mod = 5 * np.sin(2 * np.pi * 2 * t)
    return base * (1 + 0.2 * np.sin(2 * np.pi * mod * t))

def arpeggio_note(freq, duration):
    return saw_wave(freq, duration, 0.15)

def build_bar():
    bar_len = int(sample_rate * bar_length_sec)
    bar = np.zeros(bar_len)

    kick_len = 0.15
    kick = kick_drum(kick_len)
    for beat in [0, 2]:
        start = int((beat * (bar_length_sec / 4)) * sample_rate)
        bar[start:start+len(kick)] += kick

    snare_len = 0.12
    snare = snare_drum(snare_len)
    for beat in [1, 3]:
        start = int((beat * (bar_length_sec / 4)) * sample_rate)
        bar[start:start+len(snare)] += snare

    hh_len = 0.05
    hh_closed = hi_hat_closed(hh_len)
    for eighth in range(8):
        if eighth % 2 == 1:
            start = int((eighth * (bar_length_sec / 8)) * sample_rate)
            bar[start:start+len(hh_closed)] += hh_closed

    hh_open = hi_hat_open(0.2)
    start = int((7 * (bar_length_sec / 8)) * sample_rate)
    bar[start:start+len(hh_open)] += hh_open

    return bar

def build_bassline():
    notes_semitones = [0, 0, 3, 5, 7, 5, 3, 0]
    base_freq = 55
    note_duration = bar_length_sec / len(notes_semitones)
    length = int(sample_rate * bar_length_sec)
    bass = np.zeros(length)

    for i, semitones in enumerate(notes_semitones):
        freq = base_freq * 2 ** (semitones / 12)
        start = int(i * note_duration * sample_rate)
        note = bass_note(freq, note_duration)
        bass[start:start+len(note)] += note[:length - start]

    return bass

def build_arpeggio():
    notes_semitones = [0, 4, 7, 12]
    base_freq = 220
    note_duration = bar_length_sec / len(notes_semitones)
    length = int(sample_rate * bar_length_sec)
    arp = np.zeros(length)

    for i, semitones in enumerate(notes_semitones):
        freq = base_freq * 2 ** (semitones / 12)
        start = int(i * note_duration * sample_rate)
        note = arpeggio_note(freq, note_duration)
        arp[start:start+len(note)] += note[:length - start]

    return arp

def normalize(signal):
    max_val = np.max(np.abs(signal))
    if max_val == 0:
        return signal
    return signal / (max_val * 1.1)

def make_loop():
    bar = build_bar()
    bass = build_bassline()
    arp = build_arpeggio()

    mix = bar + bass + arp

    mix = normalize(mix)
    stereo = np.column_stack((mix, mix))
    return stereo

if __name__ == "__main__":
    loop_audio = make_loop()
    print("Playing seamless bass groove loop. Ctrl+C to stop.")
    try:
        while True:
            sd.play(loop_audio, sample_rate)
            sd.wait()
    except KeyboardInterrupt:
        print("\nPlayback stopped.")
