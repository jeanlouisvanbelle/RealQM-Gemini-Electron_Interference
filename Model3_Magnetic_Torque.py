import numpy as np
import matplotlib.pyplot as plt

# ==============================================================================
# 1. ACTUAL UNL EXPERIMENTAL DIMENSIONS & COUPLING CONSTANTS
# ==============================================================================
NUM_ELECTRONS = 500000    
D1 = 0.305                # Collimator to double-slit (30.5 cm)
D2 = 0.305                # Double-slit to detector screen (30.5 cm)
W_SLIT = 50e-9            # Width of EACH slit (50 nm)
D_SLIT = 280e-9           # Center-to-center slit separation (280 nm)
L_TUNNEL = 100e-9         # Membrane thickness (100 nm)

x_center_slit1 = -D_SLIT / 2.0  # -140 nm
x_center_slit2 =  D_SLIT / 2.0  # +140 nm

sigma_x_slits = D_SLIT * 1.5    
sigma_angle = np.arctan(sigma_x_slits / D1)
ALPHA_MAG = 2.85e-6  

# ==============================================================================
# 2. TRAJECTORY INITIALIZATION & SEPARATION
# ==============================================================================
angles_in = np.random.normal(0, sigma_angle, NUM_ELECTRONS)
x_at_slits = D1 * np.tan(angles_in)

in_slit1 = (x_at_slits >= (x_center_slit1 - W_SLIT/2.0)) & (x_at_slits <= (x_center_slit1 + W_SLIT/2.0))
in_slit2 = (x_at_slits >= (x_center_slit2 - W_SLIT/2.0)) & (x_at_slits <= (x_center_slit2 + W_SLIT/2.0))

x_curr1, angles_curr1 = x_at_slits[in_slit1], angles_in[in_slit1]
x_curr2, angles_curr2 = x_at_slits[in_slit2], angles_in[in_slit2]

phases1 = np.random.uniform(0, 2 * np.pi, len(x_curr1))
phases2 = np.random.uniform(0, 2 * np.pi, len(x_curr2))

# ==============================================================================
# 3. INTERACTION ENGINE (MODEL 3 TORQUE)
# ==============================================================================
def compute_magnetic_deflection(x_local, phase, w_slit):
    x_norm = x_local / (w_slit / 2.0)
    gradient_profile = x_norm / (1.001 - np.abs(x_norm))**0.5
    force_torque = gradient_profile * np.sin(phase)
    return ALPHA_MAG * force_torque

# Process Slit 1 independently (P1 Distribution)
x_local1 = x_curr1 - x_center_slit1
delta_theta1 = compute_magnetic_deflection(x_local1, phases1, W_SLIT)
angles_out1 = angles_curr1 + delta_theta1
x_screen1 = (x_curr1 + L_TUNNEL * np.tan(angles_out1)) + D2 * np.tan(angles_out1)

# Process Slit 2 independently (P2 Distribution)
x_local2 = x_curr2 - x_center_slit2
delta_theta2 = compute_magnetic_deflection(x_local2, phases2, W_SLIT)
angles_out2 = angles_curr2 + delta_theta2
x_screen2 = (x_curr2 + L_TUNNEL * np.tan(angles_out2)) + D2 * np.tan(angles_out2)

# ==============================================================================
# 4. PLOTTING THE INDEPENDENT COMPONENT CHANNELS
# ==============================================================================
plt.figure(figsize=(12, 7))

# Set uniform bin boundaries across all profiles for precise comparison
bin_edges = np.linspace(-25, 25, 150)

# Plot P1 (Slit 1 Only Open)
plt.hist(x_screen1 * 1e6, bins=bin_edges, color='dodgerblue', edgecolor='black', 
         alpha=0.5, label='Slit 1 Only Open (P1 Profile)')

# Plot P2 (Slit 2 Only Open)
plt.hist(x_screen2 * 1e6, bins=bin_edges, color='orange', edgecolor='black', 
         alpha=0.5, label='Slit 2 Only Open (P2 Profile)')

# Plot P12 (Both Slits Open - Combined Stack)
plt.hist(np.concatenate([x_screen1, x_screen2]), bins=bin_edges, color='crimson', 
         histtype='step', linewidth=2.5, label='Both Slits Open (P12 = P1 + P2)')

plt.title("Model 3 Components: Single-Slit Profiles (P1, P2) vs. Double-Slit Overlay (P12)", fontsize=13, fontweight='bold')
plt.xlabel("Screen Position x (μm)", fontsize=12)
plt.ylabel("Electron Count", fontsize=12)
plt.legend(loc='upper right')
plt.grid(True, linestyle='--', alpha=0.5)

# Export the multi-channel visualization
plt.savefig("Model3_Single_vs_Double_Overlay.png", dpi=300, bbox_inches='tight')
print("-> Saved component analysis to 'Model3_Single_vs_Double_Overlay.png'")
plt.show()

