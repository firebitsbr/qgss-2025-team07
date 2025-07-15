def grade_ex1(use_case, physical_parameters):
    if use_case != 'cfd':
        return "Please choose the correct use case"

    if physical_parameters != {"a": 1.0, "b": 1.0}:
        return "Please choose the correct physical parameters"
    
    return 'Congratulations 🎉! Your answer is correct.'
    

def grade_ex2(use_case, physical_parameters, nb_qubits, depth, nb_shots, initialization, mode):
    if use_case != 'cfd':
        return "Please choose the correct use case"

    if physical_parameters != {"a": 0.5, "b": 0.25}:
        return "Please choose the correct physical parameters" 
    
    if nb_qubits !={"u": {"t": 2, "x":1}}:
        return "Please choose the correct qubit number" 
    
    if depth !={"u": 3}:
        return "Please choose the correct depth" 
    
    if nb_shots !=[500, 2500, 5000, 10000]:
        return "Please provide the correct list of shots"

    if initialization != "RANDOM":
        return "Please choose the correct initialization"

    if mode !="session":
        return "Please choose session mode to submit your quantum task"

    return 'Congratulations 🎉! Your answer is correct.'


def grade_ex3(use_case, physical_parameters, nb_qubits, depth, nb_shots, max_iters, initialization, mode):
    if use_case != "cfd":
        return "Please choose the correct use case"

    if physical_parameters != {"a": 0.5, "b": 0.25}:
        return "Please choose the correct physical parameters"

    if nb_qubits !={"u": {"t": 2, "x":1}}:
        return "Please choose the correct qubit number"

    if depth !={"u": 3}:
        return "Please choose the correct depth"

    if nb_shots !=[500, 2500, 5000, 10000]:
        return "Please provide the correct list of shots"

    if max_iters != [100, 20, 2, 1]:
        "Please provide the correct list of max_iters"

    if initialization != "RANDOM":
        return "Please choose the correct initialization"

    if mode !="session":
        return "Please choose session mode to submit your quantum task"
