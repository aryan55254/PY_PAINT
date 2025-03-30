import pygame
import tkinter as tk
from tkinter import filedialog

# Initialize Pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Pygame Drawing App")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Brush settings
brush_size = 5
current_color = BLACK
eraser_mode = False

# Canvas setup
screen.fill(WHITE)
pygame.display.update()

# Store drawings for undo feature
drawings = []
temp_surface = screen.copy()

# Track drawing state
drawing = False
prev_pos = None
shape_mode = None  # None, "rectangle", "circle", "line"

# Font
font = pygame.font.Font(None, 30)

def save_drawing():
    """Opens a file dialog and saves the drawing as an image."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        pygame.image.save(screen, file_path)

def draw_ui():
    """Draw UI elements on the screen (buttons, color selectors, etc.)."""
    pygame.draw.rect(screen, RED, (10, 10, 30, 30))  # Red color button
    pygame.draw.rect(screen, GREEN, (50, 10, 30, 30))  # Green color button
    pygame.draw.rect(screen, BLUE, (90, 10, 30, 30))  # Blue color button
    pygame.draw.rect(screen, BLACK, (130, 10, 30, 30))  # Black color button
    pygame.draw.rect(screen, WHITE, (170, 10, 30, 30))  # Eraser

    pygame.draw.rect(screen, (200, 200, 200), (220, 10, 80, 30))  # Undo Button
    screen.blit(font.render("Undo", True, BLACK), (230, 15))

    pygame.draw.rect(screen, (200, 200, 200), (320, 10, 80, 30))  # Clear Button
    screen.blit(font.render("Clear", True, BLACK), (330, 15))

    pygame.draw.rect(screen, (200, 200, 200), (420, 10, 80, 30))  # Save Button
    screen.blit(font.render("Save", True, BLACK), (435, 15))

    pygame.draw.rect(screen, (200, 200, 200), (520, 10, 80, 30))  # Brush Size
    screen.blit(font.render(f"Size: {brush_size}", True, BLACK), (530, 15))
# Main loop
running = True
while running:
    draw_ui()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mouse Click
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if 10 <= x <= 40 and 10 <= y <= 40:
                current_color = RED
                eraser_mode = False
            elif 50 <= x <= 80 and 10 <= y <= 40:
                current_color = GREEN
                eraser_mode = False
            elif 90 <= x <= 120 and 10 <= y <= 40:
                current_color = BLUE
                eraser_mode = False
            elif 130 <= x <= 160 and 10 <= y <= 40:
                current_color = BLACK
                eraser_mode = False
            elif 170 <= x <= 200 and 10 <= y <= 40:
                eraser_mode = True

            # Undo button
            elif 220 <= x <= 300 and 10 <= y <= 40:
                if drawings:
                    screen.blit(drawings.pop(), (0, 0))

            # Clear button
            elif 320 <= x <= 400 and 10 <= y <= 40:
                screen.fill(WHITE)
                drawings.clear()

            # Save button
            elif 420 <= x <= 500 and 10 <= y <= 40:
                save_drawing()

            # Brush size change
            elif 520 <= x <= 600 and 10 <= y <= 40:
                brush_size += 2
                if brush_size > 20:
                    brush_size = 2  # Reset after 20

            # Line tool
            elif 620 <= x <= 700 and 50 <= y <= 80:
                shape_mode = "line"

            else:
                drawing = True
                prev_pos = event.pos
                drawings.append(screen.copy())  # Save state for undo

        # Mouse Release
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            prev_pos = None

        # Mouse Motion
        if event.type == pygame.MOUSEMOTION and drawing:
            x, y = event.pos
            if shape_mode is None:
                if eraser_mode:
                    pygame.draw.circle(screen, WHITE, event.pos, brush_size)
                else:
                    pygame.draw.circle(screen, current_color, event.pos, brush_size)
            prev_pos = event.pos

        # Draw Shapes
        if event.type == pygame.MOUSEBUTTONUP and shape_mode:
            x, y = event.pos
            if shape_mode == "rectangle" and prev_pos:
                pygame.draw.rect(screen, current_color, (*prev_pos, x - prev_pos[0], y - prev_pos[1]), 2)
            elif shape_mode == "circle" and prev_pos:
                radius = ((x - prev_pos[0]) ** 2 + (y - prev_pos[1]) ** 2) ** 0.5
                pygame.draw.circle(screen, current_color, prev_pos, int(radius), 2)
            elif shape_mode == "line" and prev_pos:
                pygame.draw.line(screen, current_color, prev_pos, (x, y), brush_size)
            shape_mode = None  # Reset shape mode

pygame.quit()
