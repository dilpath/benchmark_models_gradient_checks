# Gradient checks for PEtab benchmark models
Gradient checks for the collection of PEtab benchmark models. The gradients checked are performed using AMICI for simulation, via interfaces in AMICI and pyPESTO.

# Usage
1. Link to the benchmark models. Either:
    - clone the models inside this repository with:
    ```bash
    git clone https://github.com/Benchmarking-Initiative/Benchmark-Models-PEtab.git
    ```
    - change paths to match a pre-existing copy of the models
        - `_helpers.py`: `benchmark_path`
        - `run.sh`: `benchmark_dir`
2. Setup a Python environment with:
    - AMICI
    - pyPESTO
    - libpetab-python
3. Submit the SLURM jobs with `bash run.sh`
4. Plot results with `python3 plot.py`

# TODO
- tee output to log file named by tool/model/vector
- parallelize across test vectors
- use job array
