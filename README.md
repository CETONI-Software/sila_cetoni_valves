# CETONI SiLA 2 Valve SDK
## Installation
Run `pip install .` from the root directory containing the file `setup.py`

## Usage
Run `python -m sila_cetoni_valves --help` to receive a full list of available options

## Code generation
- generate
  ```console
  $ python -m sila2.code_generator new-package -n valve_service -o ./sila_cetoni/valves/sila ./sila_cetoni/valves/features/*.sila.xml
  ```
- update
  ```console
  $ python -m sila2.code_generator update -d ./sila_cetoni/valves/sila ./sila_cetoni/valves/features/*.sila.xml
  ```
