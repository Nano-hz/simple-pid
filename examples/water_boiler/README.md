# Water Boiler Example

Simple simulation of a water boiler which can heat up water and where the heat dissipates slowly over time. Running the example will run the water boiler simulation for 10 seconds and use the PID controller to make the boiler reach a setpoint temperature. The measured temperature includes Gaussian sensor noise. The results are printed to the log every 0.5 seconds, showing the target temperature, current temperature and boiler power. After the run, control performance metrics (rise time, overshoot and steady-state error) are reported.

## Installation

It's recommended to install the dependencies (numpy and click, in addition to the simple-pid library itself) in a virtual environment.

```bash
# Linux:
python -m venv venv
. venv/bin/activate

# Windows:
python -m venv venv
venv/Scripts/activate
```

Then install the example dependencies:

```bash
python -m pip install ../..[examples]
```

## Usage

```bash
# Activate the virtual environment if you use one:
. venv/bin/activate

# Run the example with default settings:
python water_boiler.py

# Once you're done deactivate the virtual environment if you use one:
deactivate
```

All simulation parameters can be configured on the command line. Run `python water_boiler.py --help` for details, for example:

```bash
# 15 seconds simulation with a target of 80 °C, PID gains and reproducible noise:
python water_boiler.py --duration 15 --target 80 --kp 8 --ki 0.02 --kd 0.2 --noise 0.2 --seed 42
```
