import networkx as nx

# Constants for the lab assignment
NUM_NODES = 50
SEED = 0

def print_results(results: bool):
    """
    Print the results of the grading.
    """
    if results:
        print("\nCongratulations 🎉! Your answer is correct.")
    else:
        print("Oops 😕! Your answer is incorrect")


def grade_lab_iskay_ex1a(G: nx.Graph) -> bool:
    """
    Return True if G matches the expected random 3-regular graph defined by:
        nx.random_regular_graph(3, NUM_NODES, seed=SEED)
    Checks:
      1. G has exactly NUM_NODES nodes.
      2. Every node has degree 3.
      3. The edge set matches the graph generated with the fixed seed.
    """
    # 1. Check node count
    if G.number_of_nodes() != NUM_NODES:
        return print_results(False)

    # 2. Check regularity (degree 3)
    if any(deg != 3 for _, deg in G.degree()):
        return print_results(False)

    # 3. Re-generate and compare
    try:
        expected = nx.random_regular_graph(3, NUM_NODES, seed=SEED)
    except Exception:
        return print_results(False)
    
    return print_results(set(G.edges()) == set(expected.edges()))


def grade_lab_iskay_ex1b(objective_func: dict, graph:nx.Graph) -> bool:
    """
    Returns True if `objective_func` correctly encodes the Ising MaxCut objective for graph G:
      - One entry per edge (i, j) in G, with key "(i, j)"
      - Each coefficient value is exactly 0.5
    """
    # Must be a dict with one entry per edge
    if not isinstance(objective_func, dict):
        return print_results(False)
    if len(objective_func) != graph.number_of_edges():
        return print_results(False)

    # Check each edge
    for i, j in graph.edges():
        key = f"({i}, {j})"
        # Ensure the key exists and the value is 0.5
        if objective_func.get(key) != 0.5:
            return print_results(False)
    return print_results(True)


def grade_lab_iskay_ex1c(arguments: dict) -> bool:
    """
    Returns True if `arguments` correctly prepares the optimizer inputs:
      - Contains exactly the keys: 'problem', 'problem_type', 'instance', 'backend_name', 'options'
      - 'problem' matches `expected_problem`
      - 'problem_type' is 'spin'
      - 'instance' is 'project-based/kipu/main'
      - 'backend_name' matches `expected_backend_name`
      - 'options' matches `expected_options`
    """
    # Must be a dict
    if not isinstance(arguments, dict):
        return print_results(False)

    # Check all required keys are present (and no extras)
    required_keys = {'problem', 'problem_type', 'instance', 'backend_name', 'options'}
    if set(arguments.keys()) != required_keys:
        return print_results(False)

    # 1. problem
    graph = nx.random_regular_graph(3, NUM_NODES, seed=SEED)
    # Create the objective function for MaxCut in Ising formulation
    def graph_to_ising_maxcut(G):
        # Initialize the linear and quadratic coefficients
        objective_func = {}
        for i, j in G.edges:
            objective_func[f"({i}, {j})"] = 0.5        
        return objective_func
    
    objective_func = graph_to_ising_maxcut(graph)
    if arguments['problem'] != objective_func:
        print("Problem does not match expected objective function.")
        return print_results(False)

    # 2. problem_type
    if arguments['problem_type'] != 'spin':
        print("Problem type is not 'spin'.")
        return print_results(False)

    available_backends = [
        'ibm_aachen',
        'ibm_brisbane',
        'ibm_brussels',
        'ibm_fez',
        'ibm_marrakesh',
        'ibm_sherbrooke',
        'ibm_strasbourg',
        'ibm_torino',
    ]

    # 3. backend_name
    if arguments['backend_name'] not in available_backends:
        print("Backend name does not match expected.")
        return print_results(False)

    # 4. options
    expected_options = {
        "shots": 2_500,
        "num_iterations": 10,
        "use_session": True
    }
    if arguments['options'] != expected_options:
        print("Options do not match expected.")
        return print_results(False)

    return print_results(True)


def grade_lab_iskay_ex1d(result: dict) -> bool:
    """
    """
    # Must be a dict
    if not isinstance(result, dict):
        return print_results(False)

    # Check all required keys are present (and no extras)
    required_keys = {'solution', 'solution_info', 'prob_type'}
    if set(result.keys()) != required_keys:
        return print_results(False)

    optimal_cost = -29.5

    obtained_cost = result.get('solution_info', {}).get('cost')
    if obtained_cost is None:
        print("Solution info does not contain 'cost'.")
        return print_results(False)
    elif obtained_cost != optimal_cost:
        print(f"Obtained cost {obtained_cost} does not match expected optimal cost {optimal_cost}. But it is not a failure. Try another backend or increase the number of shots.")
        return print_results(True)
    elif obtained_cost == optimal_cost:
        print(f"Obtained cost {obtained_cost} matches expected optimal cost {optimal_cost}. ")
        return print_results(True)
    

def grade_lab_iskay_ex1e(cut: int) -> bool:
    """
    """
    if not isinstance(cut, int):
        return print_results(False)

    if cut==67:
        return print_results(True)
    

def grade_lab_iskay_ex2a(idx: int) -> bool:
    """
    """
    if not isinstance(idx, int):
        return print_results(False)

    if idx==5:
        return print_results(True)
    

def grade_lab_iskay_ex2b(one_local_terms:int, two_local_terms:int, three_local_terms:int) -> bool:
    """
    """
    if not isinstance(one_local_terms, int) and not isinstance(two_local_terms, int) and not isinstance(three_local_terms, int):
        return print_results(False)

    if one_local_terms == 127 and two_local_terms == 142 and three_local_terms == 69:
        return print_results(True)
    

def grade_lab_iskay_ex2c(arguments: dict) -> bool:
    """
    Returns True if `arguments` correctly prepares the optimizer inputs:
      - Contains exactly the keys: 'problem', 'problem_type', 'instance', 'backend_name', 'options'
      - 'problem' matches `expected_problem`
      - 'problem_type' is 'spin'
      - 'instance' is 'project-based/kipu/main'
      - 'backend_name' matches `expected_backend_name`
      - 'options' matches `expected_options`
    """
    # Must be a dict
    if not isinstance(arguments, dict):
        return print_results(False)

    # Check all required keys are present (and no extras)
    required_keys = {'problem', 'problem_type', 'instance', 'backend_name', 'options'}
    if set(arguments.keys()) != required_keys:
        return print_results(False)

    # 1. problem
    with open(f'data/ibm_washington.txt', 'r') as file:
        content = file.read()

    objective_func = {}

    for list_of_fields in eval(content):
        for field in list_of_fields:
            for key,val in field.items():
                if isinstance(key, tuple):
                    objective_func[str(tuple(sorted(key)))] = val
                elif isinstance(key, int):
                    objective_func[str((key,))] = val
    
    if arguments['problem'] != objective_func:
        print("Problem does not match expected objective function.")
        return print_results(False)

    # 2. problem_type
    if arguments['problem_type'] != 'spin':
        print("Problem type is not 'spin'.")
        return print_results(False)

    available_backends = [
        'ibm_aachen',
        'ibm_brisbane',
        'ibm_brussels',
        'ibm_fez',
        'ibm_marrakesh',
        'ibm_sherbrooke',
        'ibm_strasbourg',
        'ibm_torino',
    ]

    # 3. backend_name
    if arguments['backend_name'] not in available_backends:
        print("Backend name does not match expected.")
        return print_results(False)

    # 4. options
    expected_options = {
        "shots": 10000,
        "num_iterations": 10,
        "use_session": True
    }
    if arguments['options'] != expected_options:
        print("Options do not match expected.")
        return print_results(False)

    return print_results(True)
