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

# Finely tuned attraction coupling parameter
ALPHA_ATTRACT = 1.5e-21  

# ==============================================================================
# 2. BEAM ILLUMINATION MASKING
# ==============================================================================
angles_in = np.random.normal(0, sigma_angle, NUM_ELECTRONS)
x_at_slits = D1 * np.tan(angles_in)

in_slit1 = (x_at_slits >= (x_center_slit1 - W_SLIT/2.0)) & (x_at_slits <= (x_center_slit1 + W_SLIT/2.0))
in_slit2 = (x_at_slits >= (x_center_slit2 - W_SLIT/2.0)) & (x_at_slits <= (x_center_slit2 + W_SLIT/2.0))

x_curr1, angles_curr1 = x_at_slits[in_slit1], angles_in[in_slit1]
x_curr2, angles_curr2 = x_at_slits[in_slit2], angles_in[in_slit2]

# ==============================================================================
# 3. INTERACTION ENGINE (TRUE COULOMB WALL ATTRACTION PULL)
# ==============================================================================
def compute_true_wall_attraction(x_local, w_slit):
    half_w = w_slit / 2.0
    x_bounded = np.clip(x_local, -half_w * 0.95, half_w * 0.95)
    
    dist_left = half_w + x_bounded   
    dist_right = half_w - x_bounded  
    
    force_pull = (1.0 / dist_right**2) - (1.0 / dist_left**2)
    return ALPHA_ATTRACT * force_pull

# Process Slit 1 (P1 Profile)
x_local1 = x_curr1 - x_center_slit1
delta_theta1 = compute_true_wall_attraction(x_local1, W_SLIT)
angles_out1 = angles_curr1 + delta_theta1
x_screen1 = (x_curr1 + L_TUNNEL * np.tan(angles_out1)) + D2 * np.tan(angles_out1)

# Process Slit 2 (P2 Profile)
x_local2 = x_curr2 - x_center_slit2
delta_theta2 = compute_true_wall_attraction(x_local2, W_SLIT)
angles_out2 = angles_curr2 + delta_theta2
x_screen2 = (x_curr2 + L_TUNNEL * np.tan(angles_out2)) + D2 * np.tan(angles_out2)

# Combine both arrays for the total open profile (P12)
x_screen_total = np.concatenate([x_screen1, x_screen2])

# ==============================================================================
# NUMERICAL VERIFICATION (PARTICLE CONSERVATION CHECK)
# ==============================================================================
count_p1 = len(x_screen1)
count_p2 = len(x_screen2)
count_p12 = len(x_screen_total)

print("="*60)
print("             PARTICLE CONSERVATION MONITOR             ")
print("="*60)
print(f"-> Electrons passing through Slit 1 (P1):  {count_p1}")
print(f"-> Electrons passing through Slit 2 (P2):  {count_p2}")
print(f"-> Sum of independent channels (P1 + P2):  {count_p1 + count_p2}")
print(f"-> Total measured with both open (P12):    {count_p12}")
print("-"*60)
if (count_p1 + count_p2) == count_p12:
    print("VERIFICATION SUCCESS: Particle conservation is exactly 100.000%!")
else:
    print("WARNING: Discrepancy detected.")
print("="*60)

# ==============================================================================
# 4. PLOTTING WITH LOGARITHMIC SCALE
# ==============================================================================
plt.figure(figsize=(12, 7))
bin_edges = np.linspace(-35, 35, 200)

# Plot P1 
plt.hist(x_screen1 * 1e6, bins=bin_edges, color='teal', edgecolor='black', 
         alpha=0.5, label='Slit 1 Only Open (P1 Profile)')

# Plot P2
plt.hist(x_screen2 * 1e6, bins=bin_edges, color='gold', edgecolor='black', 
         alpha=0.5, label='Slit 2 Only Open (P2 Profile)')

# Plot P12 
plt.hist(x_screen_total * 1e6, bins=bin_edges, color='darkblue', 
         histtype='step', linewidth=2.5, label='Both Slits Open (P12 = P1 + P2)')

# SWITCH TO LOGARITHMIC SCALE TO REVEAL WINGS
plt.yscale('log')

plt.title("Model 2 (Log Scale): Electrostatic Image-Charge Wall Attraction", fontsize=13, fontweight='bold')
plt.xlabel("Screen Position x (μm)", fontsize=12)
plt.ylabel("Electron Count (Log Scale)", fontsize=12)
plt.legend(loc='upper right')
plt.grid(True, linestyle='--', alpha=0.4, which="both") # grid lines for log scale major/minor ticks

plt.savefig("Model2_Divergence_LogScale.png", dpi=300, bbox_inches='tight')
print("-> Saved log-scale visual to 'Model2_Divergence_LogScale.png'")
plt.show()
