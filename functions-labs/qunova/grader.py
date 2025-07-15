from qiskit import QuantumCircuit
from qiskit.quantum_info.operators.base_operator import BaseOperator

correct_message = "Congratulations! 🎉 Your answer is correct."
incorrect_message = "Sorry, your answer is incorrect. Please try again."

def grade_ex1a(ex1a_answer: dict):
    if ex1a_answer.get("basis") != "ccpvdz":
        return "Wrong basis. Please try again."
    if ex1a_answer.get("active_orbitals") != list(range(2,14,1)):
        return "Wrong active orbitals. Please try again."
    if ex1a_answer.get("frozen_orbitals") != list(range(2)):
        return "Wrong frozen orbitals. Please try again."
    return correct_message

def grade_ex1b(ex1b_answer: dict):
    if ex1b_answer.get("hivqe_energy") > -78.0396545776652 or ex1b_answer.get("hivqe_energy") < -78.0788722041575:
        return "Wrong hivqe energy. Please try again."
    return correct_message

def grade_ex2a(ex2_answer: dict):
    if type(ex2_answer.get("max_states_list")) is not list:
        return "max_states_list is not a list. Please try again."
    max_states_list = ex2_answer.get("max_states_list")
    if not any(2000 <= x < 5000 for x in max_states_list) or max(max_states_list) < 5000:
        return "max_states_list does not include any number strictly between 2000 and 5000. Please try again."
    if ex2_answer.get("basis") != "ccpvdz":
        return "Wrong basis. Please try again."
    if ex2_answer.get("active_orbitals") != list(range(2,14,1)):
        return "Wrong active orbitals. Please try again."
    if ex2_answer.get("frozen_orbitals") != list(range(2)):
        return "Wrong frozen orbitals. Please try again."
    return correct_message

def grade_ex2b(ex2_answer: dict):
    if ex2_answer.get("max_states") < 3000:
        return "Too small max_states. Please try again."
    if ex2_answer.get("hivqe_energy") > (-78.0788722041575 + 0.0016):
        return "hivqe energy would not be accurate enough. Please try again."
    return correct_message

def grade_ex3(ex3_answer: float):
    print(f"Note: Maximum energy difference is: {ex3_answer*1000} mHa")
    if ex3_answer > 0.0016:
        return "At least one of the energy difference is greater than 1.6 mHa. Please try again."
    return correct_message