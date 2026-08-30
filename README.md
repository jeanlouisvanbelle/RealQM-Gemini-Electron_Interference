# RealQM-Gemini-Electron_Interference

Simulation code for the 2012 UNL electron interference experiment. 

**Repository URL:** [https://github.com/jeanlouisvanbelle/RealQM-Gemini-Electron_Interference](https://github.com/jeanlouisvanbelle/RealQM-Gemini-Electron_Interference)

---

## 1. Project Objective & Philosophy

This project establishes a firm, trajectory-based **deterministic alternative** to the conventional "multi-path" Copenhagen interpretation of Quantum Mechanics (QM). 

Mainstream QM relies on abstract, zero-dimensional point particles traveling along a mystical superposition of unobservable paths, mathematically managed by calculating complex "probability amplitudes." In contrast, the **Structural Realist (RealQM)** approach models the electron as an extended, localized electromagnetic field configuration (a toroidal *Zitterbewegung* soliton). 

By treating both the electron and the macroscopic slit boundaries as real field entities, this simulation demonstrates that classical-like trajectory sorting alone accounts for quantum phenomena, demonstrating that **particle statistics are strictly additive ($P_{12} = P_1 + P_2$)** without requiring mystical non-local wave collapse.

---

## 2. The Failure of Feynman's "Bullet Model"

In his famous *Lectures on Physics* (Vol. III, Chapter 1), Richard Feynman introduced a thought experiment comparing electrons to "bullets" or macroscopic "billiard balls." He assumed that a single particle passing through a single open slit would produce a smooth, featureless ballistic projection screen distribution. 

However, modern high-precision data—specifically from the **2012 University of Nebraska-Lincoln (UNL)** experiment—completely disproves this premise. The UNL data reveals structured diffraction fringes and multi-peak profiles **even when only a single slit is open**. 

Our initial mechanical simulation confirmed Feynman's expectations: a pure ballistic approach produces a flat block or a singular featureless Gaussian curve, proving mathematically that a pure "billiard-ball" mechanical baseline cannot replicate physical reality. The electron must actively interact with the slit.

---

## 3. Electromagnetic Interaction Models

To uncover the true mechanism behind single-slit diffraction and double-slit overlays, the repository implements three distinct electrodynamic models matching the physical dimensions of the UNL apparatus (50 nm slits, 280 nm separation, 100 nm tunnel length).

### Model 2: Electrostatic Image-Charge Wall Attraction
* **The Mechanics:** Treats the negative electron charge ($e$) as inducing a positive image charge in the mobile conduction electron sea of the gold-plated slit walls. 
* **The Result:** This sets up a pure attractive force pulling electrons outward toward the nearest plate. It acts as a *diverging lens*, pushing the single-slit profiles away from the axis and broadening the central gap. It proves electrostatic attraction alone cannot form a central diffraction peak.

### Model 3: Toroidal Dipole Gradient Torque
* **The Mechanics:** Explores the electron's real Bohr magneton magnetic moment interacting with localized magnetic field gradients near the gold boundaries based on its internal *Zitterbewegung* phase $\phi \in [0, 2\pi)$.
* **The Result:** The gradient sorts particles by phase, acting as an *anisotropic convergence lens*. It successfully funnels trajectories inward to bridge the central geometric gap, but it remains a smooth focusing curve lacking discrete secondary fringes.

### Model 1: The Effective Mass Matrix Lens (The Optimal RealQM Engine)
* **The Mechanics:** Based directly on **Annex I**, because the electron has a finite spatial extension, cutting across the sharp field gradients of the slit dynamically deforms its toroidal geometry. This varies its localized internal rotational frequency, resulting in a coordinate-dependent **transverse effective mass matrix** $\mathbf{M}^{-1}(x)$.
* **The Result:** The slit acts as a periodic refractive index matrix (a geometric phase-sorting GRIN lens). Trajectories are deterministically funneled into sharp, highly discrete **caustic resonance combs**. As verified in the three-panel plot, it beautifully reproduces the primary central peaks, symmetric secondary/n-ary lobes, and distinct dark fringes observed in real-life quantum diffraction while maintaining strict particle conservation ($P_{12} = P_1 + P_2$).

---

## 4. Repository Contents

* `Bullet_Uniform.py` / `Bullet_Gaussian.py`: Pure ballistic baseline simulations verifying the limitations of classical particle assumptions.
* `Model2_Image_Charge.py`: Electrostatic wall attraction (diverging lens) simulation engine.
* `Model3_Magnetic_Torque.py`: Magnetic gradient torque phase-sorting simulation engine.
* `Model1_Matrix_Lense.py`: Complete effective mass matrix lens simulation generating the multi-panel caustic resonance combs.
