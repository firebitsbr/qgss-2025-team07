def grade_ex1a(qubo_settings: dict, optimizer_settings: dict, ansatz_settings: dict, apply_postprocess: bool, assets: dict) -> None:
    """
    Grades Exercise 1a by checking:
    - Correct asset keys and data length
    - Correct QUBO settings: nt, nq, dt, max_investment
    - Correct ansatz settings
    - Postprocessing and optimizer configuration
    """

    # Check asset keys
    expected_assets = {'NVDA', 'TSLA', 'AMZN'}
    if set(assets.keys()) != expected_assets:
        print(f"❌ Incorrect asset keys. Expected: {sorted(expected_assets)}.")
        return

    # Check data length
    min_points = (4 + 1) * 30
    for asset, prices in assets.items():
        if len(prices) <= min_points:
            print(f"❌ Asset {asset} has insufficient data. Requires more than {min_points} data points.")
            return

    # QUBO settings
    if qubo_settings.get('nt') != 4:
        print("❌ Incorrect value for 'nt'. Expected: 4.")
        return

    if qubo_settings.get('nq') != 2:
        print("❌ Incorrect value for 'nq'. Expected: 2.")
        return

    if qubo_settings.get('dt') != 30:
        print("❌ Incorrect value for 'dt'. Expected: 30.")
        return

    if qubo_settings.get('max_investment') != 6:
        print("❌ Incorrect value for 'max_investment'. Expected: 6.")
        return

    # Ansatz settings
    if ansatz_settings.get('ansatz') != 'optimized_real_amplitudes':
        print("❌ Incorrect 'ansatz'. Expected: 'optimized_real_amplitudes'.")
        return

    if ansatz_settings.get('multiple_passmanager') is not False:
        print("❌ 'multiple_passmanager' must be set to False.")
        return

    # Postprocess flag
    if apply_postprocess is not True:
        print("❌ 'apply_postprocess' must be set to True.")
        return

    # Optimizer constraints
    de_settings = optimizer_settings.get('de_optimizer_settings', {})
    num_gens = de_settings.get('num_generations', 0)
    pop_size = de_settings.get('population_size', 0)
    if (num_gens + 1) * pop_size > 70:
        print("❌ Too many circuits. Ensure (num_generations + 1) * population_size ≤ 70.")
        return

    primitive_settings = optimizer_settings.get('primitive_settings', {})
    if primitive_settings.get('estimator_shots') != 25_000:
        print("❌ 'estimator_shots' must be set to 25_000.")
        return

    if primitive_settings.get('sampler_shots') != 100_000:
        print("❌ 'sampler_shots' must be set to 100_000.")
        return

    print("✅ Exercise 1a solution is correct!")


def grade_ex1b(dpo_result: dict) -> None:
    """
    Grades Exercise 1b by checking how close the minimum objective cost is
    to the known global minimum (-3.51097567).
    """

    try:
        min_cost = min(dpo_result['metadata']['all_samples_metrics']['objective_costs'])
    except (KeyError, TypeError):
        print("❌ Invalid format in 'dpo_result'. Could not find objective costs.")
        return

    global_min = -3.51097567
    tolerance = 0.1

    # Check closeness to global minimum
    if abs(min_cost - global_min) < tolerance:
        print("✅ The minimum cost is very close to the global minimum! Your implementation is correct.")
        return

    # Check for suspiciously low value
    if min_cost < global_min:
        print("❌ The minimum cost is lower than the known global minimum. There may be an issue with your implementation.")
        return

    # Report relative deviation
    relative_deviation = abs((min_cost - global_min) / global_min) * 100
    print(f"⚠️ The relative deviation from the global minimum is {relative_deviation:.2f}%. Please review your implementation.")


def grade_ex2(
    qubo_settings: dict,
    optimizer_settings: dict,
    ansatz_settings: dict,
    apply_postprocess: bool,
    assets: dict,
    num_generations_ex_1: int,
    previous_session_id: list
) -> None:
    """
    Grades Exercise 2 by verifying:
    - Warm restart from previous session
    - Correct increment in number of generations
    - Asset keys and data size
    - QUBO, ansatz, optimizer, and postprocessing settings
    """

    # Check previous_session_id
    if not isinstance(previous_session_id, list) or len(previous_session_id) != 1 or not isinstance(previous_session_id[0], str):
        print("❌ 'previous_session_id' must be a list containing a single string.")
        return

    # Check number of generations increased by 2
    expected_generations = num_generations_ex_1 + 2
    actual_generations = optimizer_settings.get('de_optimizer_settings', {}).get('num_generations')
    if actual_generations != expected_generations:
        print(f"❌ Incorrect number of generations. Expected: {expected_generations}, got: {actual_generations}.")
        return

    # Check asset keys
    expected_assets = {'NVDA', 'TSLA', 'AMZN'}
    if set(assets.keys()) != expected_assets:
        print(f"❌ Incorrect asset keys. Expected: {sorted(expected_assets)}.")
        return

    # Check asset data length
    min_points = (4 + 1) * 30
    for asset, prices in assets.items():
        if len(prices) <= min_points:
            print(f"❌ Asset {asset} has insufficient data. Requires more than {min_points} data points.")
            return

    # QUBO settings
    if qubo_settings.get('nt') != 4:
        print("❌ Incorrect 'nt'. Expected: 4.")
        return

    if qubo_settings.get('nq') != 2:
        print("❌ Incorrect 'nq'. Expected: 2.")
        return

    if qubo_settings.get('dt') != 30:
        print("❌ Incorrect 'dt'. Expected: 30.")
        return

    if qubo_settings.get('max_investment') != 6:
        print("❌ Incorrect 'max_investment'. Expected: 6.")
        return

    # Ansatz settings
    if ansatz_settings.get('ansatz') != 'optimized_real_amplitudes':
        print("❌ Incorrect 'ansatz'. Expected: 'optimized_real_amplitudes'.")
        return

    if ansatz_settings.get('multiple_passmanager') is not False:
        print("❌ 'multiple_passmanager' must be set to False.")
        return

    # Postprocessing flag
    if apply_postprocess is not True:
        print("❌ 'apply_postprocess' must be set to True.")
        return

    # Primitive shots
    primitive_settings = optimizer_settings.get('primitive_settings', {})
    if primitive_settings.get('estimator_shots') != 25_000:
        print("❌ 'estimator_shots' must be set to 25_000.")
        return

    if primitive_settings.get('sampler_shots') != 100_000:
        print("❌ 'sampler_shots' must be set to 100_000.")
        return

    print("✅ Exercise 2 solution is correct!")
