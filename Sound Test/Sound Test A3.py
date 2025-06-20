import numpy as np
import sounddevice as sd
import pygame
import threading
import random
import time
import sys


def generate_hell_audio(duration=60, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)


    drone = 0.4 * np.sin(2 * np.pi * 90 * t) + 0.3 * np.sin(2 * np.pi * 40 * t)


    speech = np.random.uniform(-0.3, 0.3, sample_rate * 2) * np.hanning(sample_rate * 2)
    speech = speech[::-1]
    speech_layer = np.zeros_like(t)
    speech_start = sample_rate * 20
    speech_layer[speech_start:speech_start+len(speech)] = speech[:len(t) - speech_start]


    screams = np.zeros_like(t)
    for _ in range(5):
        start = random.randint(0, len(t) - sample_rate // 4)
        length = sample_rate // 6
        screams[start:start+length] += np.sin(2 * np.pi * random.randint(400, 900) * t[:length]) * np.hanning(length) * 0.7


    whisper_left = np.zeros_like(t)
    whisper_right = np.zeros_like(t)
    for _ in range(30):
        start = random.randint(0, len(t) - sample_rate // 10)
        length = sample_rate // 15
        w = np.random.uniform(-0.2, 0.2, length) * np.hanning(length)
        if random.random() > 0.5:
            whisper_left[start:start+length] += w
        else:
            whisper_right[start:start+length] += w


    pulse = (np.sin(2 * np.pi * 0.25 * t) > 0).astype(float)

    left = (drone + screams + speech_layer + whisper_left) * pulse
    right = (drone + screams + speech_layer + whisper_right) * pulse
    stereo = np.column_stack((left, right))

    stereo /= np.max(np.abs(stereo)) * 1.1
    return stereo

def play_audio(audio, sample_rate=44100):
    sd.play(audio, sample_rate)
    sd.wait()


def visual_flash_simulation(duration=60):
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
    font = pygame.font.SysFont("Arial", 60, bold=True)
    clock = pygame.time.Clock()
    start_time = time.time()

    scary_messages = [
        "I SEE YOU",
        "WHO'S BEHIND YOU?",
        "DON'T TURN AROUND",
        "YOU'RE NOT ALONE",
        "GET OUT"
    ]

    colors = [(255,255,255), (255,0,0), (0,0,0)]
    
    while time.time() - start_time < duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(random.choice(colors))

        if random.random() > 0.7:
            msg = random.choice(scary_messages)
            text = font.render(msg, True, (255, 255, 255))
            rect = text.get_rect(center=(400, 300))
            screen.blit(text, rect)

        pygame.display.flip()
        clock.tick(random.randint(5, 25))

    pygame.quit()


def start_hell_experience():
    audio = generate_hell_audio()


    vis_thread = threading.Thread(target=visual_flash_simulation)
    vis_thread.start()


    play_audio(audio)
    vis_thread.join()

if __name__ == "__main__":
    print("🧠 Beginning full audio-visual overload. You asked for this.")
    start_hell_experience()
    print("✅ Finished. You're still here.")
