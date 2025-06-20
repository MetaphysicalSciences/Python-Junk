import numpy as np
import sounddevice as sd
import pygame
import threading
import random
import time
import sys

def generate_audio(duration=60, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)

    drone = 0.5 * np.sin(2 * np.pi * 90 * t) + 0.4 * np.sin(2 * np.pi * 40 * t)
    speech = np.random.uniform(-0.4, 0.4, sample_rate * 2) * np.hanning(sample_rate * 2)
    speech = speech[::-1]
    speech_layer = np.zeros_like(t)
    speech_start = sample_rate * 20
    speech_layer[speech_start:speech_start+len(speech)] = speech[:len(t) - speech_start]

    screams = np.zeros_like(t)
    for _ in range(10):
        start = random.randint(0, len(t) - sample_rate // 6)
        length = sample_rate // 5
        freq = random.randint(400, 1200)
        screams[start:start+length] += np.sin(2 * np.pi * freq * t[:length]) * np.hanning(length) * 0.9

    whisper_left = np.zeros_like(t)
    whisper_right = np.zeros_like(t)
    for _ in range(50):
        start = random.randint(0, len(t) - sample_rate // 12)
        length = sample_rate // 10
        w = np.random.uniform(-0.3, 0.3, length) * np.hanning(length)
        if random.random() > 0.5:
            whisper_left[start:start+length] += w
        else:
            whisper_right[start:start+length] += w

    pulse = (np.sin(2 * np.pi * 0.3 * t) > 0).astype(float)

    left = (drone + screams + speech_layer + whisper_left) * pulse
    right = (drone + screams + speech_layer + whisper_right) * pulse
    stereo = np.column_stack((left, right))

    max_val = np.max(np.abs(stereo))
    if max_val > 0:
        stereo /= max_val * 1.1
    return stereo

def play_audio(audio, sample_rate=44100):
    sd.play(audio, sample_rate)
    sd.wait()

def visual_sim(duration=60):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.SysFont("Arial", 60, bold=True)
    clock = pygame.time.Clock()
    start_time = time.time()

    messages = [
        "I SEE YOU",
        "WHO'S THERE?",
        "DON'T LOOK BACK",
        "RUN",
        "STAY QUIET"
    ]

    colors = [(255,255,255), (255,0,0), (0,0,0)]

    while time.time() - start_time < duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(random.choice(colors))

        if random.random() > 0.6:
            msg = random.choice(messages)
            text = font.render(msg, True, (255, 255, 255))
            rect = text.get_rect(center=(400, 300))
            screen.blit(text, rect)

        pygame.display.flip()
        clock.tick(random.randint(10, 40))

    pygame.quit()

def run():
    audio = generate_audio()
    vis_thread = threading.Thread(target=visual_sim)
    vis_thread.start()
    play_audio(audio)
    vis_thread.join()

if __name__ == "__main__":
    run()
