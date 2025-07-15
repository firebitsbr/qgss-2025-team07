from qiskit import QuantumCircuit
from qiskit.quantum_info.operators.base_operator import BaseOperator
from qiskit.quantum_info import SparsePauliOp, Operator
import numpy as np
import networkx as nx
import qiskit

correct_message = "Congratulations! 🎉 Your answer is correct."
incorrect_message = "Sorry, your answer is incorrect. Please try again."


def kicked_ising_1D(num_qubits: int, theta_x: float, theta_zz: float, s: int) -> QuantumCircuit:
    """
    Parameters:
        num_qubits (int): number of qubits on chain. 
        theta_x (float): Angle for RX gates.
        theta_zz (float): Angle for RZZ gates.
        s (int): Number of steps.
    
    Returns:
        QuantumCircuit: The resulting quantum circuit.
    """
    graph = nx.path_graph(num_qubits)
    qc = QuantumCircuit(num_qubits)

    # Precompute edge layers (alternating non-overlapping pairs)
    edges = list(graph.edges())
    even_edges = [(u, v) for (u, v) in edges if u % 2 == 0]
    odd_edges  = [(u, v) for (u, v) in edges if u % 2 == 1]

    for step in range(s):
        # RX on all qubits
        for q in range(num_qubits):
            qc.rx(theta_x, q)
        
        # Apply even and odd layers separately
        for edge_layer in [even_edges, odd_edges]:
            for u, v in edge_layer:
                qc.rzz(theta_zz, u, v)

        if step < s-1:
            qc.barrier()
    
    return qc


def grade_ex2(pubs_ex2:list, backend_name_ex2:str, options_ex2:dict):
    
    
    # check types:
    if not isinstance(pubs_ex2,list) or not isinstance(backend_name_ex2, str) or not isinstance(options_ex2,dict):
        return "Type error in input parameters"
    
    
    circ = QuantumCircuit(4)
    circ.ry(0.927*2, 0)   
    circ.cx(0, 1)
    circ.cx(1, 2)
    circ.cx(2, 3)
    
    avg_magnetization = SparsePauliOp.from_sparse_list(
        [("Z", [q], 1 / 4) for q in range(4)], num_qubits=4)
    
    all_z = SparsePauliOp.from_sparse_list(
        [("Z"*4, range(4),1)], 4)
    
    obs_list =  [avg_magnetization, all_z]

    # test backend name
    if backend_name_ex2 !='fake_fez':
        return "Bad backend name. " +backend_name_ex2

    # test options
    if "default_precision" not in options_ex2 or "max_execution_time" not in options_ex2 or len(options_ex2)!=2:
        return "Options should have two entries 'default_precision' and 'max_execution_time'" 

    if options_ex2['default_precision']!=0.1 or options_ex2["max_execution_time"]!=900:
        return "Value in options field is wrong. Try again"
        
    # checks pubs
    if len(pubs_ex2)!=1:
        return "pubs format is [(QuantumCircuit, [obs1,obs2,...]), [parameters], precision]\n For this exercise, use pubs=[(QuantumCircuit, [obs1,obs2,...])]" 

    pair = pubs_ex2[0]
    
    if not (isinstance(pair, tuple)) or not len(pair) == 2:
        return "pubs format is [(QuantumCircuit, [obs1,obs2,...]), [parameters], precision]\n For this exercise, use pubs=[(QuantumCircuit, [obs1,obs2,...])]" 

    circ_ex2 = pair[0]
    obs_list_ex2 = pair[1]
    
    if not (isinstance(circ_ex2, QuantumCircuit)):
        return "pubs format is [(QuantumCircuit, [obs1,obs2,...]), [parameters], precision]\n For this exercise, use pubs=[(QuantumCircuit, [obs1,obs2,...])]" 


    # check circuit
    if not Operator(circ).equiv(Operator(circ_ex2)):
        return "Different circuit specified."

    # check observable list
    if not isinstance(obs_list_ex2, list):
        return "pubs[0][1] is not a list of observables"

    if len (obs_list_ex2)!=2:
        return "pubs[0][1] is not a list of the two observables specified"

    if obs_list_ex2[0]==obs_list_ex2[1]:
        return "pubs[0][1] is not a list of the two observables specified"
    
    
    for en, obs in enumerate(obs_list_ex2):
        if not (isinstance(obs, SparsePauliOp)):
            return  (f"observable {en} is not a SparsePauliOp")
        if obs not in obs_list:
            return (f"observable {en} is not one of the two observables specified")

    return correct_message


            
            
def grade_ex3(options_ex3:dict):
    
    
    # check types:
    if not isinstance(options_ex3,dict):
        return "Type error in input parameter"
    

    # test options
    if "default_precision" not in options_ex3 or "estimate_time_only" not in options_ex3 or len(options_ex3)!=2:
        return "Options should have two entries 'default_precision' and 'estimate_time_only'" 

    if options_ex3['default_precision']!=0.02 or options_ex3["estimate_time_only"]!="analytical":
        return "Value in options field is wrong. Try again"    

    return correct_message

        


def grade_ex_4_1(circuit: QuantumCircuit):
    
    if not isinstance(circuit, QuantumCircuit):
        return "Circuit should be a QuantumCircuit object. Please try again."
    
    if circuit.num_qubits != 5:
        return "Circuit should have 5 qubits (n_qubits_ex4 = 5). Please try again."
    
    expected_2q_layers = 20
    actual_2q_layers = circuit.depth(filter_function=lambda instr: len(instr.qubits) == 2)
    
    if actual_2q_layers != expected_2q_layers:
        return f"Circuit should have {expected_2q_layers} two-qubit gate layers (10 steps × 2 layers per step). Found {actual_2q_layers}. Please try again."
    
    expected_barriers = 9
    actual_barriers = sum(1 for instr in circuit.data if instr.operation.name == 'barrier')
    
    if actual_barriers != expected_barriers:
        return f"Circuit should have {expected_barriers} barriers (one between each of the 10 steps). Found {actual_barriers}. Please try again."
    
    expected_theta_x = np.pi/6
    expected_theta_zz = np.pi/3
    
    for instr in circuit.data:
        if instr.operation.name == 'rx':
            if not np.isclose(instr.operation.params[0], expected_theta_x):
                return f"RX gate angles should be π/6 (theta_x_ex4). Found {instr.operation.params[0]}. Please try again."
        elif instr.operation.name == 'rzz':
            if not np.isclose(instr.operation.params[0], expected_theta_zz):
                return f"RZZ gate angles should be π/3 (theta_zz_ex4). Found {instr.operation.params[0]}. Please try again."
    
    return correct_message




def grade_ex_4_2(precision_ex4, pubs_ex4, backend_name_ex4, options_ex4):
    
    # Expected values for Exercise 4.2
    n_qubits_ex4 = 5
    n_steps_ex4 = 10
    theta_x_ex4 = np.pi/6
    theta_zz_ex4 = np.pi/3
    
    circ_ex4 = kicked_ising_1D(n_qubits_ex4, theta_x_ex4, theta_zz_ex4, n_steps_ex4)
    observable_ex4 = qiskit.quantum_info.SparsePauliOp.from_sparse_list([("Z"*n_qubits_ex4, range(n_qubits_ex4),1)], n_qubits_ex4) # Global Z measurement
    
    # Check precision
    if not isinstance(precision_ex4, (int, float)):
        return "Precision should be a number (int or float). Please try again."
    
    if precision_ex4 <= 0.03:
        return "Precision should be greater than 0.03. Please try again."
    
    # Check backend name
    if not isinstance(backend_name_ex4, str):
        return "Backend name should be a string. Please try again."
    
    if "ibm" not in backend_name_ex4.lower():
        return "Backend name should contain 'ibm'. Please try again."
    
    # Check pubs format
    if not isinstance(pubs_ex4, list):
        return "Pubs should be a list. Please try again."
    
    if len(pubs_ex4) != 1:
        return "Pubs should contain exactly one publication tuple. Please try again."
    
    pub = pubs_ex4[0]
    if not isinstance(pub, tuple) or len(pub) != 4:
        return "Each pub should be a tuple with 4 elements: (circuit, observables, params, precision). Please try again."
    
    circuit, observables, params, precision = pub
    
    if not isinstance(circuit, QuantumCircuit):
        return "First element of pub should be a QuantumCircuit (use circ_ex4). Please try again."
    
    # Check if the circuit matches the expected circ_ex4
    if not Operator(circuit).equiv(Operator(circ_ex4)):
        return "Circuit should be circ_ex4 created with kicked_ising_1D. Please try again."
    
    if not isinstance(observables, list) or len(observables) != 1:
        return "Second element of pub should be a list with one observable. Please try again."
    
    if not isinstance(observables[0], SparsePauliOp):
        return "Observable should be a SparsePauliOp (use observable_ex4). Please try again."
    
    # Check if the observable matches the expected observable_ex4
    if not observables[0].equiv(observable_ex4):
        return "Observable should be the global Z measurement (observable_ex4). Please try again."
    
    if params != []:
        return "Third element of pub should be an empty list []. Please try again."
    
    if precision != precision_ex4:
        return "Fourth element of pub should match your precision_ex4 parameter. Please try again."
    
    # Check options
    if not isinstance(options_ex4, dict):
        return "Options should be a dictionary. Please try again."
    
    required_keys = ["estimate_time_only", "max_execution_time", "execution_mode"]
    
    for key in required_keys:
        if key not in options_ex4:
            return f"Options missing required key '{key}'. Please try again."
    
    if len(options_ex4) != len(required_keys):
        return f"Options should contain exactly {len(required_keys)} keys: {required_keys}. Please try again."
    
    # Check estimate_time_only
    if options_ex4["estimate_time_only"] != "empirical":
        return "Option 'estimate_time_only' should be 'empirical'. Please try again."
    
    # Check max_execution_time (up to 8 minutes = 480 seconds)
    if not isinstance(options_ex4["max_execution_time"], (int, float)) or options_ex4["max_execution_time"] > 480:
        return "Option 'max_execution_time' should be a number ≤ 480 seconds (8 minutes). Please try again."
    
    # Check execution_mode (can be "batch" or "session")
    if options_ex4["execution_mode"] not in ["batch", "session"]:
        return "Option 'execution_mode' should be either 'batch' or 'session'. Please try again."
    
    return correct_message




def grade_ex_4_3(precision_ex4, pubs_ex4, backend_name_ex4, options_ex4):
    
    # Expected values for Exercise 4.2
    n_qubits_ex4 = 5
    n_steps_ex4 = 10
    theta_x_ex4 = np.pi/6
    theta_zz_ex4 = np.pi/3
    
    circ_ex4 = kicked_ising_1D(n_qubits_ex4, theta_x_ex4, theta_zz_ex4, n_steps_ex4)
    observable_ex4 = qiskit.quantum_info.SparsePauliOp.from_sparse_list([("Z"*n_qubits_ex4, range(n_qubits_ex4),1)], n_qubits_ex4) # Global Z measurement
    
    # Check precision
    if not isinstance(precision_ex4, (int, float)):
        return "Precision should be a number (int or float). Please try again."
    
    if precision_ex4 <= 0.03:
        return "Precision should be at least 0.03. Please try again."
    
    # Check backend name
    if not isinstance(backend_name_ex4, str):
        return "Backend name should be a string. Please try again."
    
    if "ibm" not in backend_name_ex4.lower():
        return "Backend name should contain 'ibm'. Please try again."
    
    # Check pubs format
    if not isinstance(pubs_ex4, list):
        return "Pubs should be a list. Please try again."
    
    if len(pubs_ex4) != 1:
        return "Pubs should contain exactly one publication tuple. Please try again."
    
    pub = pubs_ex4[0]
    if not isinstance(pub, tuple) or len(pub) != 4:
        return "Each pub should be a tuple with 4 elements: (circuit, observables, params, precision). Please try again."
    
    circuit, observables, params, precision = pub
    
    if not isinstance(circuit, QuantumCircuit):
        return "First element of pub should be a QuantumCircuit (use circ_ex4). Please try again."
    
    # Check if the circuit matches the expected circ_ex4
    if not Operator(circuit).equiv(Operator(circ_ex4)):
        return "Circuit should be circ_ex4 created with kicked_ising_1D. Please try again."
    
    if not isinstance(observables, list) or len(observables) != 1:
        return "Second element of pub should be a list with one observable. Please try again."
    
    if not isinstance(observables[0], SparsePauliOp):
        return "Observable should be a SparsePauliOp (use observable_ex4). Please try again."
    
    # Check if the observable matches the expected observable_ex4
    if not observables[0].equiv(observable_ex4):
        return "Observable should be the global Z measurement (observable_ex4). Please try again."
    
    if params != []:
        return "Third element of pub should be an empty list []. Please try again."
    
    if precision != precision_ex4:
        return "Fourth element of pub should match your precision_ex4 parameter. Please try again."
    
    # Check options
    if not isinstance(options_ex4, dict):
        return "Options should be a dictionary. Please try again."
    
    required_keys = ["max_execution_time", "execution_mode"]
    
    for key in required_keys:
        if key not in options_ex4:
            return f"Options missing required key '{key}'. Please try again."
    
    if len(options_ex4) != len(required_keys):
        return f"Options should contain exactly {len(required_keys)} keys: {required_keys}. Please try again."
    
    # Check max_execution_time (up to 8 minutes = 480 seconds)
    if not isinstance(options_ex4["max_execution_time"], (int, float)) or options_ex4["max_execution_time"] > 480:
        return "Option 'max_execution_time' should be a number ≤ 480 seconds (8 minutes). Please try again."
    
    # Check execution_mode (can be "batch" or "session")
    if options_ex4["execution_mode"] not in ["batch", "session"]:
        return "Option 'execution_mode' should be either 'batch' or 'session'. Please try again."
    
    return correct_message


    