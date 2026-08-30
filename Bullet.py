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

# Derived angular boundaries based on the 2-sigma rule (95.45% throughput)
# w = 2 * d1 * tan(eps_upper) -> eps_upper = arctan(w / (2 * d1))
eps_upper = np.arctan(W_SLIT / (2 * D1))
sigma_eps = eps_upper / 2.0  # 2-sigma profile

print(f"-> Angle Upper Boundary (2-sigma): {eps_upper:.6e} rad")
print(f"-> Calculated Angular Sigma:       {sigma_eps:.6e} rad")

# ==============================================================================
# 2. TRAJECTORY INITIALIZATION
# ==============================================================================
# Sample initial angles from a Gaussian distribution
angles_in = np.random.normal(0, sigma_eps, NUM_ELECTRONS)

# Sample initial spatial positions across the slit using a spatial Gaussian profile
# We scale sigma so that nearly all particles fall inside the physical slit width
sigma_x = W_SLIT / 4.0  
x_in = np.random.normal(0, sigma_x, NUM_ELECTRONS)

# Filter out particles that physically miss the front entrance of the slit
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

# Mechanical check: Did any electron hit the parallel tunnel walls?
# Wall boundaries are at +/- (W_SLIT / 2)
hit_wall = (np.abs(x_out) > (W_SLIT / 2.0))
num_collisions = np.sum(hit_wall)

print(f"-> Electrons colliding with walls: {num_collisions} ({num_collisions/num_passed*100:.4f}%)")

# For the tiny fraction that hits the walls, an elastic collision reverses the angle's sign
# but retains its exact absolute magnitude: theta = -epsilon
angles_out = angles_curr.copy()
angles_out[hit_wall] = -angles_curr[hit_wall]

# ==============================================================================
# 4. PROPAGATION TO DETECTOR SCREEN & VISUALIZATION
# ==============================================================================
# Final coordinate on the detector screen
x_screen = x_out + D2 * np.tan(angles_out)

# Plotting the smooth, 'bullet-like' arrival profile predicted by Feynman
plt.figure(figsize=(10, 6))
counts, bins, _ = plt.hist(x_screen * 1e3, bins=100, color='royalblue', edgecolor='black', alpha=0.7)
plt.title("Pure Ballistic Mechanical Baseline (Single Slit)", fontsize=14, fontweight='bold')
plt.xlabel("Screen Position x (mm)", fontsize=12)
plt.ylabel("Electron Count", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()
