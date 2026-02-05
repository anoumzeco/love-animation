import pygame
import math
import random
import sys

pygame.init()

# ---------------- CONFIG ----------------
WIDTH, HEIGHT = 1000, 700
BG_COLOR = (26, 26, 46)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("VERY IMPORTANT QUESTION")
clock = pygame.time.Clock()

font_big = pygame.font.SysFont(None, 42)
font_small = pygame.font.SysFont(None, 30)
font_love = pygame.font.SysFont(None, 64)

COLORS = [
    (255, 94, 135),
    (255, 133, 162),
    (255, 179, 198),
    (255, 215, 228),
    (199, 206, 234),
    (167, 154, 255),
]

# ---------------- PARTICLES ----------------
class Particle:
    def __init__(self, x, y, ptype="mouse"):
        self.x = x
        self.y = y
        self.type = ptype
        self.life = random.randint(60, 140)
        self.max_life = self.life
        self.color = random.choice(COLORS)
        self.size = random.uniform(1.2, 3.5)
        self.angle = random.random() * math.tau
        self.speed = random.uniform(0.05, 0.3)

        if ptype == "firework":
            self.vx = math.cos(self.angle) * random.uniform(2, 4)
            self.vy = math.sin(self.angle) * random.uniform(2, 4)
            self.gravity = 0.05

    def update(self):
        if self.type == "firework":
            self.vy += self.gravity
            self.x += self.vx
            self.y += self.vy
        else:
            self.x += math.cos(self.angle) * self.speed
            self.y += math.sin(self.angle) * self.speed
        self.life -= 1

    def draw(self):
        alpha = max(0, int(255 * self.life / self.max_life))
        if alpha <= 0:
            return
        s = max(1, int(self.size))
        surf = pygame.Surface((s * 2, s * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.color, alpha), (s, s), s)
        screen.blit(surf, (self.x - s, self.y - s))

    def alive(self):
        return self.life > 0

# ---------------- HEART ----------------
def heart_point(t):
    x = 16 * math.sin(t) ** 3
    y = (
        13 * math.cos(t)
        - 5 * math.cos(2 * t)
        - 2 * math.cos(3 * t)
        - math.cos(4 * t)
    )
    scale = min(WIDTH, HEIGHT) * 0.4
    cx, cy = WIDTH // 2, HEIGHT // 2
    return (
        cx + x * scale / 16,
        cy - y * scale / 16,
    )

def spawn_heart_particles(particles, n):
    for _ in range(n):
        t = random.random() * math.tau
        x, y = heart_point(t)
        particles.append(Particle(x, y, "heart"))

# ---------------- BUTTON ----------------
class Button:
    def __init__(self, text, x, y):
        self.text = text
        self.rect = pygame.Rect(x, y, 160, 60)

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        label = font_small.render(self.text, True, (255, 255, 255))
        screen.blit(
            label,
            (
                self.rect.centerx - label.get_width() // 2,
                self.rect.centery - label.get_height() // 2,
            ),
        )

    def hover(self, mx, my):
        return self.rect.collidepoint(mx, my)

# ---------------- MAIN ----------------
def main():
    particles = []
    show_heart = False

    yes_btn = Button("TIAGO", WIDTH // 2 - 200, HEIGHT // 2 + 120)
    no_btn = Button("JÚLIA", WIDTH // 2 + 40, HEIGHT // 2 + 120)

    running = True
    while running:
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEMOTION:
                for _ in range(4):
                    particles.append(
                        Particle(
                            mx + random.uniform(-10, 10),
                            my + random.uniform(-10, 10),
                        )
                    )

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for _ in range(140):
                    particles.append(Particle(mx, my, "firework"))

                if not show_heart and yes_btn.hover(mx, my):
                    show_heart = True
                    particles.clear()
                    spawn_heart_particles(particles, 900)

        # NO button runs away
        if not show_heart and no_btn.hover(mx, my):
            no_btn.rect.x += random.randint(-120, 120)
            no_btn.rect.y += random.randint(-80, 80)
            no_btn.rect.clamp_ip(screen.get_rect())

        screen.fill(BG_COLOR)

        for i in range(len(particles) - 1, -1, -1):
            p = particles[i]
            p.update()
            if not p.alive():
                particles.pop(i)
            else:
                p.draw()

        if show_heart:
            # LOVE TEXT
            love_text = font_love.render("I LOVE YOU", True, (255, 255, 255))
            screen.blit(
                love_text,
                (
                    WIDTH // 2 - love_text.get_width() // 2,
                    HEIGHT // 2 - 300,
                ),
            )

            heart_count = sum(1 for p in particles if p.type == "heart")
            if heart_count < 900:
                spawn_heart_particles(particles, 6)
        else:
            # Question text
            lines = [
                "GOSTAS MAIS DO TIAGO OU DA JÚLIA ?",
            ]
            for i, line in enumerate(lines):
                txt = font_big.render(line, True, (255, 255, 255))
                screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, 150 + i * 45))

            yes_btn.draw()
            no_btn.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
