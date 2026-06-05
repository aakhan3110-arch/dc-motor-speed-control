import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. MOTOR PARAMETERS & PHYSICAL CONSTANTS
# ==========================================
# Simulating a small permanent-magnet DC motor
R_armature = 2.0    # Armature resistance (Ohms)
L_armature = 0.5    # Armature inductance (Henries)
K_t = 0.1          # Torque constant (Nm/A)
K_e = 0.1          # Back-EMF constant (V/(rad/s))
J_inertia = 0.02   # Rotor moment of inertia (kg*m^2)
b_friction = 0.1   # Viscous friction coefficient (N*m*s)

# ==========================================
# 2. SIMULATION ENGINE
# ==========================================
def simulate_dc_motor(voltage_profile, time_array):
    """
    Simulates the dynamic transient response of a DC Motor using Euler Integration.
    Equations of state:
    di/dt = (V - R*i - K_e*w) / L
    dw/dt = (K_t*i - b*w) / J
    """
    dt = time_array[1] - time_array[0]
    num_steps = len(time_array)
    
    # Initialize state variables
    speed_rad_s = np.zeros(num_steps)
    current_amps = np.zeros(num_steps)
    
    current = 0.0
    omega = 0.0
    
    for t in range(1, num_steps):
        V = voltage_profile[t-1]
        
        # Derivatives
        di_dt = (V - R_armature * current - K_e * omega) / L_armature
        domega_dt = (K_t * current - b_friction * omega) / J_inertia
        
        # Euler Updates
        current += di_dt * dt
        omega += domega_dt * dt
        
        # Store states
        current_amps[t] = current
        speed_rad_s[t] = omega
        
    # Convert angular velocity (rad/s) to RPM for standard industrial display
    speed_rpm = speed_rad_s * (60 / (2 * np.pi))
    return speed_rpm, current_amps

def generate_pwm_signal(duty_cycle, frequency, duration, dt):
    """
    Generates a high-frequency square wave representing PWM voltage.
    """
    t = np.arange(0, duration, dt)
    period = 1.0 / frequency
    
    # Determine the ON threshold within a single period
    pulse_on = t % period < (duty_cycle * period)
    voltage_signal = np.where(pulse_on, 12.0, 0.0) # 12V Max Supply
    return t, voltage_signal

# ==========================================
# 3. ANALYTICAL VISUALIZATION PIPELINE
# ==========================================
def run_analysis_pipeline():
    dt = 0.001
    duration = 3.0
    time_steps = np.arange(0, duration, dt)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('DC Motor Speed Control & PWM Simulation', fontsize=16, fontweight='bold')
    
    # --- Plot 1: Steady-State Speed vs. Voltage ---
    voltages = np.arange(0, 13, 1)
    # Steady state speed equation: w = (V * K_t) / (R*b + K_e*K_t)
    steady_state_speed_rad = (voltages * K_t) / (R_armature * b_friction + K_e * K_t)
    steady_state_speed_rpm = steady_state_speed_rad * (60 / (2 * np.pi))
    
    axes[0, 0].plot(voltages, steady_state_speed_rpm, 'o-', color='crimson', linewidth=2)
    axes[0, 0].set_title('Steady-State Characteristics: Speed vs. Voltage')
    axes[0, 0].set_xlabel('Armature Voltage (V)')
    axes[0, 0].set_ylabel('Steady State Speed (RPM)')
    axes[0, 0].grid(True, linestyle='--')
    
    # --- Plot 2: Dynamic Step Response (Step Input) ---
    step_voltage = np.where(time_steps < 0.5, 0.0, 12.0) # Step from 0V to 12V at t=0.5s
    speed_step, _ = simulate_dc_motor(step_voltage, time_steps)
    
    axes[0, 1].plot(time_steps, step_voltage, 'g--', label='Input Voltage (V)')
    ax2 = axes[0, 1].twinx()
    ax2.plot(time_steps, speed_step, 'b-', label='Motor Speed (RPM)', linewidth=2)
    axes[0, 1].set_xlabel('Time (seconds)')
    axes[0, 1].set_ylabel('Voltage (V)', color='g')
    ax2.set_ylabel('Speed (RPM)', color='b')
    axes[0, 1].set_title('Transient Step Response (0V to 12V Direct DC)')
    
    # --- Plot 3 & 4: PWM Control Profiles (Low vs High Duty Cycle) ---
    pwm_profiles = [
        {"duty": 0.25, "ax_idx": (1, 0), "color": 'darkorange', "title": "PWM Control: 25% Duty Cycle (Low Speed)"},
        {"duty": 0.75, "ax_idx": (1, 1), "color": 'teal', "title": "PWM Control: 75% Duty Cycle (High Speed)"}
    ]
    
    for profile in pwm_profiles:
        ax_curr = axes[profile["ax_idx"]]
        t_pwm, v_pwm = generate_pwm_signal(duty_cycle=profile["duty"], frequency=50, duration=duration, dt=dt)
        speed_pwm, _ = simulate_dc_motor(v_pwm, t_pwm)
        
        # Plot limited window of the PWM pulse for clarity, but full speed output
        ax_curr.plot(t_pwm[:500], v_pwm[:500], color='grey', alpha=0.5, label='PWM Pulses (Truncated view)')
        ax_twin = ax_curr.twinx()
        ax_twin.plot(t_pwm, speed_pwm, color=profile["color"], linewidth=2, label=f'Speed at {int(profile["duty"]*100)}% Duty')
        
        ax_curr.set_xlabel('Time (seconds)')
        ax_curr.set_ylabel('Voltage Pulses (V)', color='grey')
        ax_twin.set_ylabel('Speed (RPM)', color=profile["color"])
        ax_curr.set_title(profile["title"])
        ax_twin.legend(loc='lower right')
        
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("[*] Launching DC Motor Mathematical Simulation Engine...")
    run_analysis_pipeline()
