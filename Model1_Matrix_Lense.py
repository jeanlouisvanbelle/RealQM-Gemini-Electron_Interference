import numpy as np
import matplotlib.pyplot as plt

# ==============================================================================
# 1. ACTUAL UNL EXPERIMENTAL DIMENSIONS
# ==============================================================================
NUM_ELECTRONS = 500000    
D1 = 0.305                # 30.5 cm
D2 = 0.305                # 30.5 cm
W_SLIT = 50e-9            # 50 nm
D_SLIT = 280e-9           # 280 nm center-to-center
L_TUNNEL = 100e-9         # 100 nm thickness

x_center_slit1 = -D_SLIT / 2.0  # -140 nm
x_center_slit2 =  D_SLIT / 2.0  # +140 nm

sigma_x_slits = D_SLIT * 1.5    
sigma_angle = np.arctan(sigma_x_slits / D1)
K_RESONANCE = 1.6e8  

# ==============================================================================
# 2. TRAJECTORY GENERATION & SEPARATION
# ==============================================================================
angles_in = np.random.normal(0, sigma_angle, NUM_ELECTRONS)
x_at_slits = D1 * np.tan(angles_in)

in_slit1 = (x_at_slits >= (x_center_slit1 - W_SLIT/2.0)) & (x_at_slits <= (x_center_slit1 + W_SLIT/2.0))
in_slit2 = (x_at_slits >= (x_center_slit2 - W_SLIT/2.0)) & (x_at_slits <= (x_center_slit2 + W_SLIT/2.0))

x_curr1, angles_curr1 = x_at_slits[in_slit1], angles_in[in_slit1]
x_curr2, angles_curr2 = x_at_slits[in_slit2], angles_in[in_slit2]

# ==============================================================================
# 3. INTERACTION ENGINE (MODEL 1: MASS LENS POTENTIALS)
# ==============================================================================
def compute_mass_lens_deflection(x_local, w_slit):
    x_norm = x_local / (w_slit / 2.0)
    momentum_modulation = np.sin(K_RESONANCE * x_local)
    delta_theta = 2.2e-5 * momentum_modulation * (1.0 - x_norm**2)
    return delta_theta

# Process individual slit profiles
x_local1 = x_curr1 - x_center_slit1
delta_theta1 = compute_mass_lens_deflection(x_local1, W_SLIT)
x_screen1 = (x_curr1 + L_TUNNEL * np.tan(angles_curr1 + delta_theta1)) + D2 * np.tan(angles_curr1 + delta_theta1)

x_local2 = x_curr2 - x_center_slit2
delta_theta2 = compute_mass_lens_deflection(x_local2, W_SLIT)
x_screen2 = (x_curr2 + L_TUNNEL * np.tan(angles_curr2 + delta_theta2)) + D2 * np.tan(angles_curr2 + delta_theta2)

# ==============================================================================
# 4. HIGH-RESOLUTION MULTI-PANEL VISUALIZATION
# ==============================================================================
fig, axes = plt.subplots(1, 3, figsize=(18, 5.5), sharey=True)
bin_edges = np.linspace(-10, 10, 180)

# --- Panel A: Slit 1 Only Open ---
axes[0].hist(x_screen1 * 1e6, bins=bin_edges, color='mediumpurple', edgecolor='black', alpha=0.7)
axes[0].set_title(r"A: Slit 1 Open ($P_1$ Only)", fontsize=12, fontweight='bold')
axes[0].set_xlabel(r"Screen Position x ($\mu$m)", fontsize=11)
axes[0].set_ylabel("Electron Count", fontsize=11)
axes[0].set_xlim(-10, 10)
axes[0].grid(True, linestyle='--', alpha=0.5)

# --- Panel B: Slit 2 Only Open ---
axes[1].hist(x_screen2 * 1e6, bins=bin_edges, color='lightgreen', edgecolor='black', alpha=0.7)
axes[1].set_title(r"B: Slit 2 Open ($P_2$ Only)", fontsize=12, fontweight='bold')
axes[1].set_xlabel(r"Screen Position x ($\mu$m)", fontsize=11)
axes[1].set_xlim(-10, 10)
axes[1].grid(True, linestyle='--', alpha=0.5)

# --- Panel C: Both Slits Open (P12 Overlay) ---
x_screen_total = np.concatenate([x_screen1, x_screen2])
axes[2].hist(x_screen_total * 1e6, bins=bin_edges, color='dimgray', edgecolor='black', alpha=0.4, label='Stacked Space')
axes[2].hist(x_screen_total * 1e6, bins=bin_edges, color='black', histtype='step', linewidth=2.0, label=r"$P_{12} = P_1 + P_2$")
axes[2].set_title(r"C: Both Open ($P_{12}$ Superposition)", fontsize=12, fontweight='bold')
axes[2].set_xlabel(r"Screen Position x ($\mu$m)", fontsize=11)
axes[2].set_xlim(-10, 10)
axes[2].legend(loc='upper right')
axes[2].grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()

# Export high-res compilation
plt.savefig("Model1_Three_Panel_Resonance.png", dpi=300, bbox_inches='tight')
print("-> Successfully generated and saved 'Model1_Three_Panel_Resonance.png'")
plt.show()
