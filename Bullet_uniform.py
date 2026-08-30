import numpy as np
import matplotlib.pyplot as plt

# ==============================================================================
# 1. FIXED PHYSICAL AND GEOMETRIC PARAMETERS (UNL / RealQM Baseline)
# ==============================================================================
NUM_ELECTRONS = 200000
ENERGY_KEV = 0.6          # 600 eV from the UNL experiment
D1 = 0.165                # Distance from gun/collimator to slit (16.5 cm)
D2 = 0.305                # Distance from slit to detector screen (30.5 cm)
W_SLIT = 2e-6             # Slit width (2 micrometers)
L_TUNNEL = 100e-9         # Thickness of the slit material (100 nm)

# Angular boundaries: any particle within this range hits the slit opening
eps_upper = np.arctan(W_SLIT / (2 * D1))

print(f"-> Angle Upper Boundary (Uniform Spread): +/- {eps_upper:.6e} rad")

# ==============================================================================
# 2. UNIFORM TRAJECTORY INITIALIZATION
# ==============================================================================
# Sample initial firing angles from a perfectly uniform distribution
angles_in = np.random.uniform(-eps_upper, eps_upper, NUM_ELECTRONS)

# Explicit geometric coupling: position at the slit entrance is strictly locked to the angle
x_in = D1 * np.tan(angles_in)

# Because we bound the angles directly by eps_upper, 100% of these enter the tunnel slit
passed_entrance = np.abs(x_in) <= (W_SLIT / 2.0)
x_curr = x_in[passed_entrance]
angles_curr = angles_in[passed_entrance]
num_passed = len(x_curr)

print(f"-> Electrons entering the tunnel: {num_passed} / {NUM_ELECTRONS}")

# ==============================================================================
# 3. THE BALLISTIC TUNNEL PROPAGATION
# ==============================================================================
# Calculate the total lateral drift inside the 100 nm long mechanical tunnel
lateral_drift = L_TUNNEL * np.tan(angles_curr)
x_out = x_curr + lateral_drift

# Mechanical check: Did any electron drift far enough to hit the parallel tunnel walls?
hit_wall = (np.abs(x_out) > (W_SLIT / 2.0))
num_collisions = np.sum(hit_wall)

print(f"-> Electrons colliding with walls: {num_collisions} ({num_collisions/num_passed*100:.4f}%)")

# Elastic bounce logic (reverses horizontal vector component)
angles_out = angles_curr.copy()
angles_out[hit_wall] = -angles_curr[hit_wall]

# ==============================================================================
# 4. PROPAGATION TO DETECTOR SCREEN, VISUALIZATION & FILE EXPORT
# ==============================================================================
# Final coordinate on the detector screen
x_screen = x_out + D2 * np.tan(angles_out)

# Plotting the perfectly flat, rectangular block baseline distribution
plt.figure(figsize=(10, 6))
counts, bins, _ = plt.hist(x_screen * 1e3, bins=100, color='mediumseagreen', edgecolor='black', alpha=0.7)
plt.title("Pure Ballistic Mechanical Baseline (Uniform Single Slit)", fontsize=14, fontweight='bold')
plt.xlabel("Screen Position x (mm)", fontsize=12)
plt.ylabel("Electron Count", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)

# Save the visualization directly to file before showing it
plt.savefig("Ballistic_Uniform_Baseline.png", dpi=300, bbox_inches='tight')
print("-> Output saved successfully to 'Ballistic_Uniform_Baseline.png'")
plt.show()
