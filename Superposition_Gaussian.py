import numpy as np
import matplotlib.pyplot as plt

# ==============================================================================
# 1. ACTUAL UNL EXPERIMENTAL DIMENSIONS (Gaussian Beam Setup)
# ==============================================================================
NUM_ELECTRONS = 500000    # Increased count to ensure good statistics after masking
D1 = 0.305                # Distance from collimator to double-slit (30.5 cm)
D2 = 0.305                # Distance from double-slit to detector screen (30.5 cm)
W_SLIT = 50e-9            # Width of EACH slit (50 nm)
D_SLIT = 280e-9           # Center-to-center slit separation (280 nm)
L_TUNNEL = 100e-9         # Thickness of the silicon-nitride membrane (100 nm)

# Centers of the two individual slits
x_center_slit1 = -D_SLIT / 2.0  # -140 nm
x_center_slit2 =  D_SLIT / 2.0  # +140 nm

# Define a wide Gaussian beam spread at the slit layer
# We choose a sigma such that the beam spans smoothly across both slits
sigma_x_slits = D_SLIT * 1.5    # Spatial spread at the slits
sigma_angle = np.arctan(sigma_x_slits / D1)  # Angular spread from the gun

print(f"-> Angular beam sigma: {sigma_angle:.6e} rad")

# ==============================================================================
# 2. GAUSSIAN TRAJECTORY INITIALIZATION & MASKING
# ==============================================================================
# Sample initial firing angles from a normal (Gaussian) distribution
angles_in = np.random.normal(0, sigma_angle, NUM_ELECTRONS)
x_at_slits = D1 * np.tan(angles_in)

# Slit 1 Mask: check if the electron enters the 50 nm window of Slit 1
in_slit1 = (x_at_slits >= (x_center_slit1 - W_SLIT/2.0)) & (x_at_slits <= (x_center_slit1 + W_SLIT/2.0))
# Slit 2 Mask: check if the electron enters the 50 nm window of Slit 2
in_slit2 = (x_at_slits >= (x_center_slit2 - W_SLIT/2.0)) & (x_at_slits <= (x_center_slit2 + W_SLIT/2.0))

# Track successful paths
x_curr1, angles_curr1 = x_at_slits[in_slit1], angles_in[in_slit1]
x_curr2, angles_curr2 = x_at_slits[in_slit2], angles_in[in_slit2]

num_passed = len(x_curr1) + len(x_curr2)
print(f"-> Electrons passing through Slit 1: {len(x_curr1)}")
print(f"-> Electrons passing through Slit 2: {len(x_curr2)}")
print(f"-> Total throughput: {num_passed} / {NUM_ELECTRONS} ({num_passed/NUM_ELECTRONS*100:.2f}%)")
print(f"-> Blocked/Bounced electrons: {NUM_ELECTRONS - num_passed}")

# ==============================================================================
# 3. PROPAGATION TO DETECTOR SCREEN
# ==============================================================================
# Slit 1 paths arriving at screen
x_screen1 = (x_curr1 + L_TUNNEL * np.tan(angles_curr1)) + D2 * np.tan(angles_curr1)

# Slit 2 paths arriving at screen
x_screen2 = (x_curr2 + L_TUNNEL * np.tan(angles_curr2)) + D2 * np.tan(angles_curr2)

# Combine both for the P12 overlay pattern
x_screen_total = np.concatenate([x_screen1, x_screen2])

# ==============================================================================
# 4. PLOTTING THE GAUSSIAN OVERLAY & SAVE
# ==============================================================================
plt.figure(figsize=(11, 6))

# Plot the combined distribution on the screen
plt.hist(x_screen_total * 1e6, bins=120, color='rebeccapurple', edgecolor='black', 
         alpha=0.7, label='Both Slits Open (P12 Mechanical Superposition)')

plt.title("Double-Slit Mechanical Overlay with Wide Gaussian Beam Profile", fontsize=13, fontweight='bold')
plt.xlabel("Screen Position x (μm)", fontsize=12)
plt.ylabel("Electron Count", fontsize=12)
plt.legend(loc='upper right')
plt.grid(True, linestyle='--', alpha=0.5)

# Save high-res plot directly to file
plt.savefig("Double_Slit_Gaussian_Overlay.png", dpi=300, bbox_inches='tight')
print("-> Saved plot to 'Double_Slit_Gaussian_Overlay.png'")
plt.show()
