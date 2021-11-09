from pathlib import Path
from typing import Dict
import sys

import amici
import numpy as np
import petab


benchmark_path = Path("Benchmark-Models-PEtab") / "Benchmark-Models"

output_path = Path('output')

epsilons = [1e-9, 1e-7, 1e-5, 1e-3, 1e-1]


def get_petab_problem(model_name: str) -> petab.Problem:
    petab_problem = petab.Problem.from_yaml(str(
        benchmark_path / model_name / (model_name + '.yaml')
    ))

    return petab_problem


def get_result_path(model_name: str, tool_name: str) -> Path:
    return output_path / model_name / tool_name / 'result'


def get_model_path(model_name: str, tool_name: str) -> Path:
    return output_path / model_name / tool_name / 'model'


def get_default_parameters_scaled(petab_problem: petab.Problem) -> Dict[str, float]:
    parameters = dict(zip(
        petab_problem.x_ids,
        petab_problem.x_nominal_scaled,
    ))
    return parameters


def get_midpoint_parameters_scaled(petab_problem: petab.Problem) -> Dict[str, float]:
    midpoint = (
        (np.array(petab_problem.lb_scaled) + np.array(petab_problem.ub_scaled))
        /2
    )
    parameters = dict(zip(
        petab_problem.x_ids,
        midpoint,
    ))
    return parameters


def setup():
    tool_name = sys.argv[1]
    model_name = sys.argv[2]

    model_output_path = get_model_path(model_name=model_name, tool_name=tool_name)
    model_output_path.mkdir(parents=True, exist_ok=True)
    model_output_dir = str(model_output_path)

    result_output_path = get_result_path(model_name=model_name, tool_name=tool_name)
    result_output_path.mkdir(parents=True, exist_ok=True)

    petab_problem = get_petab_problem(model_name)

    test_parameters = {
        'default': get_default_parameters_scaled(petab_problem),
        'midpoint': get_midpoint_parameters_scaled(petab_problem),
    }

    return (
        model_name,
        model_output_dir,
        petab_problem,
        result_output_path,
        test_parameters,
        tool_name,
    )

def setup_after_import(amici_model: amici.Model, amici_solver: amici.Solver):
    amici_solver.setSensitivityOrder(amici.SensitivityOrder.first)
    set_solver_model_options(solver=amici_solver, model=amici_model)

def set_solver_model_options(solver, model):
    # from Fabian
    solver.setMaxSteps(int(1e4))
    solver.setAbsoluteTolerance(1e-8)
    solver.setRelativeTolerance(1e-8)

    if model.getName() == 'Chen_MSB2009':
        solver.setMaxSteps(int(2e5))
        solver.setInterpolationType(
            amici.InterpolationType_polynomial
        )
        solver.setSensitivityMethod(
            amici.SensitivityMethod.adjoint
        )

    if model.getName() in ('Brannmark_JBC2010', 'Isensee_JCB2018'):
        model.setSteadyStateSensitivityMode(
            amici.SteadyStateSensitivityMode.simulationFSA
        )
