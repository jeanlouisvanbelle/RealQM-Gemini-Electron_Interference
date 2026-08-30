import numpy as np
import matplotlib.pyplot as plt

# ==============================================================================
# 1. ACTUAL UNL EXPERIMENTAL DIMENSIONS (Double-Slit Phase)
# ==============================================================================
NUM_ELECTRONS = 200000    # Total particles fired at the setup
D1 = 0.305                # Distance from collimator to double-slit (30.5 cm)
D2 = 0.305                # Distance from double-slit to detector screen (30.5 cm)
W_SLIT = 50e-9            # Width of EACH slit (50 nm)
D_SLIT = 280e-9           # Center-to-center slit separation (280 nm)
L_TUNNEL = 100e-9         # Thickness of the silicon-nitride membrane (100 nm)

# Centers of the two individual slits
x_center_slit1 = -D_SLIT / 2.0  # -140 nm
x_center_slit2 =  D_SLIT / 2.0  # +140 nm

# To illuminate BOTH slits uniformly, the angular spread from the collimator
# must span from the outer edge of Slit 1 to the outer edge of Slit 2
x_outer_bound = (D_SLIT / 2.0) + (W_SLIT / 2.0)
eps_max = np.arctan(x_outer_bound / D1)

# ==============================================================================
# 2. TRAJECTORY GENERATION AND SELECTION
# ==============================================================================
# Generate incoming uniform angular profiles spanning the entire double-slit region
angles_in = np.random.uniform(-eps_max, eps_max, NUM_ELECTRONS)
x_at_slits = D1 * np.tan(angles_in)

# Slit 1 Mask selection (particles that land within Slit 1 boundaries)
in_slit1 = (x_at_slits >= (x_center_slit1 - W_SLIT/2.0)) & (x_at_slits <= (x_center_slit1 + W_SLIT/2.0))
# Slit 2 Mask selection (particles that land within Slit 2 boundaries)
in_slit2 = (x_at_slits >= (x_center_slit2 - W_SLIT/2.0)) & (x_at_slits <= (x_center_slit2 + W_SLIT/2.0))

# Track positions and angles for electrons that successfully enter a slit
x_curr1, angles_curr1 = x_at_slits[in_slit1], angles_in[in_slit1]
x_curr2, angles_curr2 = x_at_slits[in_slit2], angles_in[in_slit2]

print(f"-> Electrons entering Slit 1 (P1 path): {len(x_curr1)}")
print(f"-> Electrons entering Slit 2 (P2 path): {len(x_curr2)}")

# ==============================================================================
# 3. MECHANICAL TUNNEL DRIFT & DETECTION SCREEN ARRIVAL
# ==============================================================================
# Slit 1 Propagation
x_out1 = x_curr1 + L_TUNNEL * np.tan(angles_curr1)
x_screen1 = x_out1 + D2 * np.tan(angles_curr1)

# Slit 2 Propagation
x_out2 = x_curr2 + L_TUNNEL * np.tan(angles_curr2)
x_screen2 = x_out2 + D2 * np.tan(angles_curr2)

# Combine both arrays to form the classic mechanical superposition: P12 = P1 + P2
x_screen_total = np.concatenate([x_screen1, x_screen2])

# ==============================================================================
# 4. HIGH-RESOLUTION OVERLAY PLOTTING & SAVE
# ==============================================================================
plt.figure(figsize=(11, 6))

# Plot the total overlay distribution
plt.hist(x_screen_total * 1e6, bins=120, color='indigo', edgecolor='black', 
         alpha=0.6, label='Both Slits Open (P12 Mechanical Superposition)')

# Draw the boundaries of the separate slit projections to show the microscopic shift
plt.title("Classical Mechanical Overlay Profile (UNL 50nm Slits / 280nm Sep)", fontsize=13, fontweight='bold')
plt.xlabel("Screen Position x (μm)", fontsize=12)
plt.ylabel("Electron Count", fontsize=12)
plt.legend(loc='upper right')
plt.grid(True, linestyle='--', alpha=0.5)

# Save high-res plot directly to file
plt.savefig("Double_Slit_Mechanical_Overlay.png", dpi=300, bbox_inches='tight')
print("-> Successfully generated and saved 'Double_Slit_Mechanical_Overlay.png'")
plt.show()
