from _helpers import (
    epsilons,
    setup,
    setup_after_import,
)


(
    model_name,
    model_output_dir,
    petab_problem,
    result_output_path,
    test_parameters,
    tool_name,
) = setup()

print(tool_name)
print(model_name)

if tool_name == 'amici':
    import amici.petab_import
    import amici.petab_objective
    amici_model = amici.petab_import.import_petab_problem(
        petab_problem=petab_problem,
        model_output_dir=model_output_dir,
        model_name=model_name,
    )
    amici_solver = amici_model.getSolver()
elif tool_name == 'pypesto':
    import pypesto.petab
    pypesto_importer = pypesto.petab.PetabImporter(
        petab_problem=petab_problem,
        output_folder=model_output_dir,
        model_name=model_name,
    )
    amici_objective = pypesto_importer.create_objective()
    amici_model = amici_objective.amici_model
    amici_solver = amici_objective.amici_solver
    
setup_after_import(
    amici_model=amici_model,
    amici_solver=amici_solver,
)

for test_id, parameters in test_parameters.items():
    if tool_name == 'amici':
        df = amici.petab_objective.check_grad_multi_eps(
            petab_problem=petab_problem,
            amici_model=amici_model,
            amici_solver=amici_solver,
            problem_parameters=parameters,
            detailed=True,
            scaled_parameters=True,
            multi_eps=epsilons,
            ignore_missing_parameters=True,
        )
    elif tool_name == 'pypesto':
        df = amici_objective.check_grad_multi_eps(
            x=list(parameters.values()),
            detailed=True,
            multi_eps=epsilons,
        )
    df.to_csv(str(result_output_path / f'{test_id}.tsv'), sep='\t')
