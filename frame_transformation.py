import math

# 1. Input Parameters
points = [[2.0, 0.0, -0.2], [3.5, 1.0, -0.3], [1.5, -0.8, -0.1]]

# Translation offsets (meters)
tx, ty, tz = 0.5, 0.0, 0.2

# Rotation angle in degrees
theta_deg = -15
# Convert degrees to radians for math functions
theta_rad = math.radians(theta_deg)

cos_t = math.cos(theta_rad)
sin_t = math.sin(theta_rad)

# 2. Transformation Calculations & Output
print("--- Transformed Obstacles (Base Frame) ---")

for i, point in enumerate(points, 1):
    x_c, y_c, z_c = point

    # Apply Y-axis rotation
    x_rot = x_c * cos_t + z_c * sin_t
    y_rot = y_c
    z_rot = -x_c * sin_t + z_c * cos_t

    # Apply translation
    x_base = x_rot + tx
    y_base = y_rot + ty
    z_base = z_rot + tz

    # Print results rounded to 2 decimal places
    print(
        f"Obstacle {i}: [{x_base:.2f}, {y_base:.2f}, {z_base:.2f}]"
    )