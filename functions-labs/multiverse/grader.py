def grade_exercise_1(optimizer_options_ex1: dict) -> None:
    """
    Grades Exercise 1 by checking:
    - 'simulator' key exists in optimizer_options_ex1
    - Its value is set to True
    """

    if "simulator" not in optimizer_options_ex1:
        print("❌ Missing key: 'simulator'")
        return

    if optimizer_options_ex1["simulator"] is not True:
        print("❌ 'simulator' must be set to True.")
        return

    print("✅ Exercise 1 solution is correct!")

def grade_exercise_2(learners_types: list, learners_proportions: list) -> None:
    """
    Grades Exercise 2 by verifying:
    - learners_types contains 2 unique valid classifiers.
    - learners_proportions contains 2 values, both 0.5, summing to 1.0.
    """

    allowed_learners = {
        "DecisionTreeClassifier",
        "GaussianNB",
        "KNeighborsClassifier",
        "MLPClassifier",
        "LogisticRegression"
    }

    # Check learners_types
    if not isinstance(learners_types, list):
        print("❌ 'learners_types' must be a list.")
        return
    if len(learners_types) != 2:
        print("❌ 'learners_types' must contain exactly 2 elements.")
        return
    if len(set(learners_types)) != 2:
        print("❌ All learners in 'learners_types' must be unique.")
        return
    invalid = [l for l in learners_types if l not in allowed_learners]
    if invalid:
        print(f"❌ Invalid learner types detected: {invalid}")
        print(f"✅ Allowed types are: {sorted(allowed_learners)}")
        return

    # Check learners_proportions
    if not isinstance(learners_proportions, list):
        print("❌ 'learners_proportions' must be a list.")
        return
    if len(learners_proportions) != 2:
        print("❌ 'learners_proportions' must contain exactly 2 elements.")
        return
    if not all(p == 0.5 for p in learners_proportions):
        print("❌ All proportions in 'learners_proportions' must be 0.5.")
        return
    if not abs(sum(learners_proportions) - 1.0) < 1e-8:
        print("❌ The proportions must sum up to 1.0.")
        return

    # All checks passed
    print("✅ Exercise 2 solution is correct!")


def grade_exercise_3(optimizer_options_solution: dict) -> None:
    """
    Grades Exercise 3 by validating the contents of optimizer_options_solution.
    Ensures:
    - 'num_solutions' is >= 100000
    - 'simulator' is False
    - 'classical_optimizer_options["maxiter"]' is 10
    Prints detailed feedback based on correctness.
    """
    # Required keys
    expected_keys = {"num_solutions", "simulator", "classical_optimizer_options"}

    missing_keys = expected_keys - optimizer_options_solution.keys()
    if missing_keys:
        print(f"❌ Missing keys in optimizer_options_solution: {missing_keys}")
        return

    # Check num_solutions is >= 100000
    if not isinstance(optimizer_options_solution["num_solutions"], int) or optimizer_options_solution["num_solutions"] < 100000:
        print("❌ 'num_solutions' must be an integer >= 100000.")
        return

    # Check simulator is False
    if optimizer_options_solution["simulator"] is not False:
        print("❌ 'simulator' must be set to False to use quantum optimization.")
        return

    # Check classical_optimizer_options["maxiter"] is 10
    classical_opts = optimizer_options_solution.get("classical_optimizer_options", {})
    if not isinstance(classical_opts, dict) or classical_opts.get("maxiter") != 10:
        print("❌ 'classical_optimizer_options[\"maxiter\"]' must be set to 10.")
        return

    # All checks passed
    print("✅ Exercise 3 solution is correct!")



