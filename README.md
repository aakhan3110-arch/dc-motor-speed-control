# DC Motor Speed Control Simulation

A mathematical physics-based simulation of a Permanent Magnet DC (PMDC) Motor. This project implements state-space differential equations via Euler integration to model and analyze the relationship between armature input voltage, dynamic transient states, and steady-state mechanical velocity using Pulse Width Modulation (PWM).

## 🚀 Features
* **Transient State Solver:** Tracks instantaneous armature current ($i$) and angular velocity ($\omega$) dynamically over time.
* **Steady-State Characterization:** Automatically computes and plots the linear relationship of Speed vs. Voltage.
* **PWM Signal Modulator:** Features a variable duty-cycle square wave generator to show how high-frequency switching translates into smooth torque/speed curves.
* **Multi-Panel Analytics Dashboard:** Interactive Matplotlib graphics detailing step responses and PWM smoothing behaviors.

---

## 🛠️ Tech Stack
* **Language:** Python 3
* **Computation Engine:** NumPy
* **Data Visualization:** Matplotlib

---

## 📐 Mathematical Framework
The simulation solves two coupled first-order ordinary differential equations (ODEs) describing the electro-mechanical system physics:

$$\frac{di}{dt} = \frac{1}{L}(V(t) - R \cdot i - K_e \cdot \omega)$$

$$\frac{d\omega}{dt} = \frac{1}{J}(K_t \cdot i - b \cdot \omega)$$

Where:
* $V$ = Armature Supply Voltage
* $R, L$ = Electrical Armature Resistance & Inductance
* $K_e, K_t$ = Back-EMF and Torque Constants
* $J, b$ = Rotor Inertia & Viscous Friction Coefficient

---

## 📋 Installation & Usage

1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR-USERNAME/dc-motor-speed-control.git](https://github.com/YOUR-USERNAME/dc-motor-speed-control.git)
   cd dc-motor-speed-control
