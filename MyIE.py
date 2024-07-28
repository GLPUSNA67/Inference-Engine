import re
print("5/26 9:55 PM")
print("6/23 10:11 PM")
print("MyIE is located in C:\PythonProjects\IE\MyIE.py")
# C: \PythonProjects\IE\MyIE.py


class InferenceEngine:
    def __init__(self):
        self.knowledge_base = {}
        self.rules = []
        self.inferred = []
        self.conflict_resolution_strategy = None

    def add_fact(self, key, value=None, trigger_update=True):
        print(f"* Entering add_fact: {key} = {value}")
        if value is None:
            if key not in self.knowledge_base:
                self.knowledge_base[key] = True
                print(f"Fact added/updated: {key} = True")
                if trigger_update:
                    self.forward_chain()
        else:
            if key not in self.knowledge_base or self.knowledge_base[key] != value:
                self.knowledge_base[key] = value
                print(f"Fact added/updated: {key} = {value}")
                if trigger_update:
                    self.forward_chain()

    def add_rule(self, rule):
        print(f"* Entering add_rule: {rule.conditions} -> {rule.conclusion}")
        self.rules.append(rule)
        print(f"Rule added: {rule.conditions} -> {rule.conclusion}")

    def set_conflict_resolution_strategy(self, strategy):
        self.conflict_resolution_strategy = strategy

    def forward_chain(self):
        print("* Entering forward_chain")
        new_inferences = True

        while new_inferences:
            new_inferences = False
            applicable_rules = []

            print("* Entering forward_chain loop")
            for rule in self.rules:
                print(
                    f"* Evaluating rule: {rule.conditions} -> {rule.conclusion}")
                bindings = rule.is_applicable(self.knowledge_base)
                if bindings:
                    applicable_rules.append((rule, bindings))
                    print(f"* Rule is applicable with bindings: {bindings}")

            if self.conflict_resolution_strategy:
                applicable_rules = self.conflict_resolution_strategy(
                    applicable_rules)

            for rule, bindings in applicable_rules:
                for binding in bindings:
                    new_fact_key, new_fact_value = rule.apply(
                        binding, self.knowledge_base)
                    if new_fact_key and (new_fact_key not in self.knowledge_base or self.knowledge_base[new_fact_key] != new_fact_value):
                        self.add_fact(new_fact_key, new_fact_value,
                                      trigger_update=False)
                        self.inferred.append((new_fact_key, new_fact_value))
                        new_inferences = True
                        print(
                            f"* New fact inferred: {new_fact_key} = {new_fact_value}")

    def print_facts(self):
        print("* Entering print_facts")
        print("70 Known Facts:")
        for key, value in self.knowledge_base.items():
            print(f"{key} = {value}")

    def print_inferred(self):
        print("* Entering print_inferred")
        print("76 Inferred Facts:")
        for key, value in self.inferred:
            print(f"{key} = {value}")

    def bind_variables(self, pattern, bindings):
        print(
            f"81 * Entering bind_variables: {pattern} with bindings {bindings}")
        pattern_key, pattern_value = pattern
        for var, value in bindings.items():
            pattern_key = pattern_key.replace(var, value)
            pattern_value = pattern_value.replace(var, value)
        return pattern_key, pattern_value


class Rule:
    def __init__(self, conditions, conclusion):
        self.conditions = conditions
        self.conclusion = conclusion

    def is_applicable(self, knowledge_base):
        print(f"* Entering is_applicable: {self.conditions}")
        bindings_list = []
        for condition_key, condition_value in self.conditions:
            print(
                f"* Checking condition '{condition_key} = {condition_value}' against knowledge base")
            bindings = self.match(
                condition_key, condition_value, knowledge_base)
            if bindings is not None:
                bindings_list.append(bindings)
                print(
                    f"* Condition '{condition_key} = {condition_value}' is matched with bindings {bindings}")
            else:
                print(
                    f"* Condition '{condition_key} = {condition_value}' is not matched")
                return None
        return [self.merge_bindings(bindings_list)]

    def apply(self, bindings, knowledge_base):
        print(f"* Entering apply: {self.conclusion} with bindings {bindings}")
        new_fact_key, new_fact_value_expr = self.conclusion
        print(f"* Original expression: {new_fact_value_expr}")
        for var, value in bindings.items():
            new_fact_key = new_fact_key.replace(var, value)
            new_fact_value_expr = new_fact_value_expr.replace(var, value)

        # Replace variable references with actual values from knowledge base
        for var in re.findall(r'\$(\w+)', new_fact_value_expr):
            if var in knowledge_base:
                print(f"* Replacing ${var} with {knowledge_base[var]}")
                new_fact_value_expr = new_fact_value_expr.replace(
                    f'${var}', str(knowledge_base[var]))
            else:
                raise ValueError(f"Variable {var} not found in knowledge base")

        print(
            f"* Evaluating expression for new fact value: {new_fact_value_expr}")
        try:
            # Check if the expression is numeric
            if any(op in new_fact_value_expr for op in ('+', '-', '*', '/', '(', ')')):
                new_fact_value = eval(new_fact_value_expr)
            else:
                new_fact_value = new_fact_value_expr
        except Exception as e:
            print(
                f"* Error evaluating expression: {new_fact_value_expr} with error: {e}")
            return None, None

        print(
            f"* Applying rule: {self.conditions} -> {self.conclusion} with bindings {bindings} resulting in new fact {new_fact_key} = {new_fact_value}")
        return new_fact_key, new_fact_value

    def match(self, pattern_key, pattern_value, knowledge_base):
        print(f"* Entering match: {pattern_key} = {pattern_value}")
        if pattern_key in knowledge_base:
            fact_value = knowledge_base[pattern_key]
            if isinstance(fact_value, list):
                for item in fact_value:
                    if pattern_value == str(item):
                        print(
                            f"* Exact match for pattern '{pattern_key} = {pattern_value}' with list item '{item}' in fact '{pattern_key}'")
                        return {}
            elif pattern_value == str(fact_value):
                print(
                    f"* Exact match for pattern '{pattern_key} = {pattern_value}' with fact '{pattern_key} = {fact_value}'")
                return {}
            pattern_vars = re.findall(r'\$(\w+)', pattern_value)
            fact_parts = str(fact_value).split()
            pattern_parts = pattern_value.split()
            if len(pattern_parts) != len(fact_parts):
                return None
            bindings = {}
            match = True
            for p, f in zip(pattern_parts, fact_parts):
                if p.startswith('$'):
                    bindings[p] = f
                elif p != f:
                    match = False
                    break
            if match:
                print(
                    f"* Matching pattern '{pattern_key} = {pattern_value}' with fact '{pattern_key} = {fact_value}' resulting in bindings {bindings}")
                return bindings
        print(
            f"* No match for pattern '{pattern_key} = {pattern_value}' in knowledge base")
        return None

    def merge_bindings(self, bindings_list):
        print(f"* Entering merge_bindings")
        merged = {}
        for bindings in bindings_list:
            merged.update(bindings)
        return merged


def conflict_resolution(applicable_rules):
    print(f"* Entering conflict_resolution")
    # Example conflict resolution: prioritize rules with more specific conditions
    applicable_rules.sort(key=lambda x: len(x[0].conditions), reverse=True)
    return applicable_rules


# Example usage
if __name__ == "__main__":
    print("* Starting example usage")
    engine = InferenceEngine()

    # Adding rules first
    engine.add_rule(Rule([("mass", "$mass"), ("m_mass", "$m_mass"),
                    ("units", "grams")], ("moles", "$mass / $m_mass")))
    engine.add_rule(Rule(
        [("Weather", "Sunny"), ("Days", "Weekend")], ("Activity", "Go to the beach")))
    engine.add_rule(Rule([("Activity", "Go to the beach")],
                    ("Action", "Wear sunscreen")))
    engine.add_rule(Rule([("Action", "Wear sunscreen")],
                    ("Result", "Avoid sunburn")))
    engine.add_rule(Rule([("substances", "element")], ("State", "solid")))

    # Adding initial facts
    engine.add_fact("moles", 1.0)
    engine.add_fact("units", "grams")
    engine.add_fact("m_mass", 12)
    engine.add_fact("mass", 18)
    engine.add_fact("Weather", ["Sunny", "Cloudy"])
    engine.add_fact("Days", "Weekend")
    engine.add_fact(
        "substance", ["element", "compound", "diatomic", "polyatomic"])
    engine.add_fact(
        "element", ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne"])
    # Print known and inferred facts
    engine.print_facts()
    engine.print_inferred()

    # Changing mass to trigger recalculation
    engine.add_fact("mass", 18, trigger_update=True)

    # Print known and inferred facts
    engine.print_facts()
    engine.print_inferred()

    """ Try adding some facts about a Monster Sudoku puzzle.
       Start with identifying cells by name and current value
       or string of remaining numbers.
    """
    engine.add_fact("R1C1", "468AD")
    engine.add_fact("R1C2", "B")
    engine.add_fact("R1C3", "2")
    engine.add_fact("R1C4", "1")
    engine.add_fact("R1C5", "48CEF")
    engine.add_fact("R1C6", "8AC")
    engine.add_fact("R1C7", "48AE")
    engine.add_fact("R1C8", "3")
    engine.add_fact("R1C9", "68AE")
    engine.add_fact("R1C10", "6A")
    engine.add_fact("R1C11", "9")
    engine.add_fact("R1C12", "456F")
    engine.add_fact("R1C13", "568F")
    engine.add_fact("R1C14", "B")
    engine.add_fact("R1C15", "0")
    engine.add_fact("R1C16", "7")
    engine.add_fact("R2C1", "F")
    engine.add_fact("R2C2", "39AE")
    engine.add_fact("R2C3", "5")
    engine.add_fact("R2C4", "378AE")
    engine.add_fact("R2C5", "D")
    engine.add_fact("R2C6", "0289A")
    engine.add_fact("R2C7", "289AE")
    engine.add_fact("R2C8", "027A")
    engine.add_fact("R2C9", "23678AE")
    engine.add_fact("R2C10", "0367A")
    engine.add_fact("R2C11", "4")
    engine.add_fact("R2C12", "378AE")
    engine.add_fact("R2C13", "B")
    engine.add_fact("R2C14", "C")
    engine.add_fact("R2C15", "1369")
    engine.add_fact("R2C16", "12689")
    """ The following updates a cell value after it is inferred. """
    engine.add_fact("R1C1", "D", trigger_update=True)

    engine.print_facts()
    engine.print_inferred()

    # Backward chaining example
    # goal_key, goal_value = "moles", 1.5
    # if engine.backward_chain(goal_key, goal_value):
    #     print(f"The goal '{goal_key} = {goal_value}' is achieved.")
    # else:
    #     print(f"The goal '{goal_key} = {goal_value}' cannot be achieved.")

    # Print facts after backward chaining
    # engine.print_facts()

    # print("226 moles are ", engine.moles)
    # Backward chaining example
    # goal = "Avoid sunburn"
    # if engine.backward_chain(goal):
    #     print(f"The goal '{goal}' is achieved.")
    # else:
    #     print(f"The goal '{goal}' cannot be achieved.")

    # Print facts after backward chaining
    # engine.print_facts()

    # print("23 entered forward_chain")
    # print("31 entered for rule in self.rules:")
    # print("35 applicable_rules ", applicable_rules)
    # print("37 entered if self.conflict_resolution_strategy:")
    # print("42 entered for rule, bindings in applicable_rules:")
    # print("42 entered for binding in bindings:")
    # print("47 entered if new_fact and new_fact not in self.knowledge_base:")
