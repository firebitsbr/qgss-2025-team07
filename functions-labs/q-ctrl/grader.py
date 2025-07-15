from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp

correct_message = "Congratulations! 🎉 Your answer is correct."
incorrect_message = "Sorry, your answer is incorrect. Please try again."

def grade_ex1(circuit_width: int, hidden_bitstring: str, shot_count: int, options: dict):
    if not isinstance(circuit_width, int) or circuit_width <= 0:
        return "The circuit width must be a positive integer. Please try again."

    if circuit_width > 40:
        return "The circuit width must not exceed 40 for best results. Please refer to our benchmarks for more information: https://quantum.cloud.ibm.com/docs/en/guides/q-ctrl-performance-management#benchmarks."

    if not isinstance(hidden_bitstring, str) or len(hidden_bitstring) != circuit_width:
        return f"The hidden bitstring must be a string of length {circuit_width}. Please try again."

    if not all(bit in '01' for bit in hidden_bitstring):
        return "The hidden bitstring must only contain '0' and '1'. Please try again."

    if not isinstance(shot_count, int) or shot_count <= 0:
        return "The shot count must be a positive integer. Please try again."

    if shot_count < 4096:
        return "The shot count must be at least 4096 for reliable results. Please try again."

    if circuit_width > 20 and shot_count < 10000:
        return "The shot count must be at least 10000 for larger circuits for reliable results. Please try again."

    if options.get("primitive") != "sampler":
        return "The primitive must be 'sampler'. Please try again."

    if options.get("pubs") is None or not isinstance(options.get("pubs"), list):
        return "The pubs must be a list of Sampler PUBs. Please try again."

    if len(options.get("pubs")) != 1:
        return "The pubs list should contain only one PUB. Please try again."

    pub = options.get("pubs")[0]

    if not isinstance(pub, tuple):
        return "The pub must be a tuple. Please try again."
    if len(pub) != 1:
        return "The pub tuple should contain exactly one element. Please try again."
    if not isinstance(pub[0], QuantumCircuit):
        return "The pub must contain a QuantumCircuit. Please try again."

    if options.get("backend_name") is None or not isinstance(options.get("backend_name"), str):
        return "The backend name must be a non-empty string. Please try again."

    if options.get("options") is None or not isinstance(options.get("options"), dict):
        return "The options must be a dictionary. Please try again."

    if options.get("options").get("default_shots") != shot_count:
        return f"The options dictionary must contain 'default_shots' equal to `shot_count`. Please try again."

    return correct_message


def grade_ex2(n_qubits: int, observable: SparsePauliOp, options: dict):
    if not isinstance(n_qubits, int) or n_qubits <= 0:
        return "The number of qubits must be a positive integer. Please try again."

    if not isinstance(observable, SparsePauliOp):
        return "The observable must be a SparsePauliOp. Please try again."

    pauli_strings = observable.to_list()
    if not pauli_strings:
        return "The observable must contain at least one Pauli string. Please try again."

    for pauli_string, _ in pauli_strings:
        if len(pauli_string) != n_qubits:
            return f"Each Pauli string must have length {n_qubits}. Please try again."

    groups = observable.group_commuting(qubit_wise=True)
    if len(groups) != 1:
        return "The observable must be a single commuting group. Please try again."

    if options.get("primitive") != "estimator":
        return "The primitive must be 'estimator'. Please try again."

    if options.get("pubs") is None or not isinstance(options.get("pubs"), list):
        return "The pubs must be a list of Estimator PUBs. Please try again."

    if len(options.get("pubs")) != 1:
        return "The pubs list should contain only one PUB. Please try again."

    pub = options.get("pubs")[0]

    if not isinstance(pub, tuple):
        return "The pub must be a tuple. Please try again."
    if len(pub) != 2:
        return "The pub tuple must contain exactly two elements. Please try again."
    if not isinstance(pub[0], QuantumCircuit) or not isinstance(pub[1], SparsePauliOp):
        return "The pub must contain a QuantumCircuit and a SparsePauliOp. Please try again."

    if options.get("backend_name") is None or not isinstance(options.get("backend_name"), str):
        return "The backend name must be a non-empty string. Please try again."

    return correct_message
