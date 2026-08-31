# Water Boiler Example

Simple simulation of a water boiler which can heat up water and where the heat dissipates slowly over time. Running the example will run the water boiler simulation for 10 seconds and use the PID controller to make the boiler reach a setpoint temperature. The results are printed to the log every second, showing the target temperature, current temperature and boiler power.

## Installation

It's recommended to install the simple-pid library in a virtual environment.

```bash
# Linux:
python -m venv venv
. venv/bin/activate

# Windows:
python -m venv venv
venv/Scripts/activate
```

Then install the simple-pid library:

```bash
python -m pip install ../..
```

## Usage

```bash
# Activate the virtual environment if you use one:
. venv/bin/activate

# Run the example:
python water_boiler.py

# Once you're done deactivate the virtual environment if you use one:
deactivate
```
