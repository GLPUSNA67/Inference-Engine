# 9/7/24
from tkinter import *
import tkinter as tk
import re
print("MyIE is located in C:\PythonProjects\IE\MyIE.py")
# C: \PythonProjects\IE\MyIE.py
root = Tk()
screen_height = root.winfo_screenheight()
puzzle_height = int(screen_height * 7 / 8)
puzzle_width = int(puzzle_height * 1.3)
root.geometry(f"{puzzle_width}x{puzzle_height}")
print("33 puzzle_width screen_height", puzzle_width, screen_height)
root.geometry(f"{puzzle_width}x{puzzle_height}")
main_frame = Frame(root)
main_frame.grid(row=0, column=0, columnspan=10)
main_frame.config(highlightbackground="red", highlightthickness=2)
main_canvas = Canvas(main_frame)
main_canvas.grid(row=0, column=0, columnspan=10)
lbl_Title = Label(main_canvas, text="IE Interface")
lbl_Title.grid(row=0, sticky='n')
# lbl_Title.config(font=titlefont)
F1_frame = Frame(main_canvas)
F1_frame.grid(row=2, column=0, sticky="nw")
F1_frame.config(highlightbackground="blue", highlightthickness=2)
F2_frame = Frame(main_canvas)
F2_frame.grid(row=2, column=4, sticky="nw")
F2_frame.config(highlightbackground="red", highlightthickness=2)
btn_R1C1 = tk.Button(F1_frame, wraplength=48, justify=LEFT, text="startingString", command='update_R1C1',
                     width=6, height=5)
btn_R1C1.grid(row=1, column=0, sticky='w')
# btn_R1C1.config(font=labelfont)


def update_R1C1():
    print("31 update cell")
    engine = InferenceEngine()


class InferenceEngine:
    def __init__(self):
        self.knowledge_base = {}
        self.rules = []
        self.inferred = []
        self.conflict_resolution_strategy = None

    def add_fact(self, key, value=None, trigger_update=True):
        print(f"16 Entering add_fact: {key} = {value}")
        if value is None:
            if key not in self.knowledge_base:
                self.knowledge_base[key] = True
                print(f"20 Fact added/updated: {key} = True")
                if trigger_update:
                    self.forward_chain()
        else:
            if key not in self.knowledge_base or self.knowledge_base[key] != value:
                self.knowledge_base[key] = value
                print(f"26 Fact added/updated: {key} = {value}")
                if trigger_update:
                    self.forward_chain()

    def add_rule(self, rule):
        print(f"31 Entering add_rule: {rule.conditions} -> {rule.conclusion}")
        self.rules.append(rule)
        print(f"Rule added: {rule.conditions} -> {rule.conclusion}")

    def set_conflict_resolution_strategy(self, strategy):
        self.conflict_resolution_strategy = strategy

    def forward_chain(self):
        print("39 Entering forward_chain")
        new_inferences = True

        while new_inferences:
            new_inferences = False
            applicable_rules = []

            print("46 Entering forward_chain loop")
            for rule in self.rules:
                print(
                    f"49 Evaluating rule: {rule.conditions} -> {rule.conclusion}")
                bindings = rule.is_applicable(self.knowledge_base)
                if bindings:
                    applicable_rules.append((rule, bindings))
                    print(f"53 Rule is applicable with bindings: {bindings}")

            if self.conflict_resolution_strategy:
                applicable_rules = self.conflict_resolution_strategy(
                    applicable_rules)

            for rule, bindings in applicable_rules:
                # print("60 rule, bindings ", rule) --> prints object reference
                for binding in bindings:
                    print("62 rule, bindings ", binding)
                    new_fact_key, new_fact_value = rule.apply(
                        binding, self.knowledge_base)
                    if new_fact_key and (new_fact_key not in self.knowledge_base or self.knowledge_base[new_fact_key] != new_fact_value):
                        self.add_fact(new_fact_key, new_fact_value,
                                      trigger_update=False)
                        self.inferred.append((new_fact_key, new_fact_value))
                        new_inferences = True
                        print(
                            f"71 New fact inferred: {new_fact_key} = {new_fact_value}")

    def print_facts(self):
        print("72 Entering print_facts")
        print("73 Known Facts:")
        for key, value in self.knowledge_base.items():
            print(f"{key} = {value}")

    def print_inferred(self):
        print("78 Entering print_inferred")
        print("79 Inferred Facts:")
        for key, value in self.inferred:
            print(f"{key} = {value}")

    def bind_variables(self, pattern, bindings):
        print(
            f"88 * Entering bind_variables: {pattern} with bindings {bindings}")
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
        print(f"99 Entering is_applicable: {self.conditions}")
        bindings_list = []
        for condition_key, condition_value in self.conditions:
            print(
                f"103 Checking condition '{condition_key} = {condition_value}' against knowledge base")
            bindings = self.match(
                condition_key, condition_value, knowledge_base)
            if bindings is not None:
                bindings_list.append(bindings)
                print(
                    f"109 Condition '{condition_key} = {condition_value}' is matched with bindings {bindings}")
            else:
                print(
                    f"112 Condition '{condition_key} = {condition_value}' is not matched")
                return None
        return [self.merge_bindings(bindings_list)]

    def apply(self, bindings, knowledge_base):
        print(
            f"117 Entering apply: {self.conclusion} with bindings {bindings}")
        new_fact_key, new_fact_value_expr = self.conclusion
        print(f"119 Original expression: {new_fact_value_expr}")
        for var, value in bindings.items():
            new_fact_key = new_fact_key.replace(var, value)
            new_fact_value_expr = new_fact_value_expr.replace(var, value)

        # Replace variable references with actual values from knowledge base
        for var in re.findall(r'\$(\w+)', new_fact_value_expr):
            if var in knowledge_base:
                print(f"127 Replacing ${var} with {knowledge_base[var]}")
                new_fact_value_expr = new_fact_value_expr.replace(
                    f'129 ${var}', str(knowledge_base[var]))
            else:
                raise ValueError(f"Variable {var} not found in knowledge base")

        print(
            f"134 Evaluating expression for new fact value: {new_fact_value_expr}")
        try:
            # Check if the expression is numeric
            if any(op in new_fact_value_expr for op in ('+', '-', '*', '/', '(', ')')):
                new_fact_value = eval(new_fact_value_expr)
                print("142 new_fact_value is ", new_fact_value)
            else:
                new_fact_value = new_fact_value_expr
                print("145 new_fact_value is ", new_fact_value)
        except Exception as e:
            print(
                f"148 Error evaluating expression: {new_fact_value_expr} with error: {e}")
            return None, None

        print(
            f"147 Applying rule: {self.conditions} -> {self.conclusion} with bindings {bindings} resulting in new fact {new_fact_key} = {new_fact_value}")
        return new_fact_key, new_fact_value

    def match(self, pattern_key, pattern_value, knowledge_base):
        print(f"151 Entering match: {pattern_key} = {pattern_value}")
        if pattern_key in knowledge_base:
            fact_value = knowledge_base[pattern_key]
            if isinstance(fact_value, list):
                print("160 fact_value is ", fact_value)
                for item in fact_value:
                    print("162 item is ", item)
                    if pattern_value == str(item):
                        print(
                            f"165 Exact match for pattern '{pattern_key} = {pattern_value}' with list item '{item}' in fact '{pattern_key}'")
                        return {}
            elif pattern_value == str(fact_value):
                print(
                    f"169 Exact match for pattern '{pattern_key} = {pattern_value}' with fact '{pattern_key} = {fact_value}'")
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
                    f"179 Matching pattern '{pattern_key} = {pattern_value}' with fact '{pattern_key} = {fact_value}' resulting in bindings {bindings}")
                return bindings
        print(
            f"182 No match for pattern '{pattern_key} = {pattern_value}' in knowledge base")
        return None

    def merge_bindings(self, bindings_list):
        print(f"186 Entering merge_bindings")
        merged = {}
        for bindings in bindings_list:
            merged.update(bindings)
            print("197 merged is ", merged)
        return merged


def conflict_resolution(applicable_rules):
    print(f"194 Entering conflict_resolution")
    # Example conflict resolution: prioritize rules with more specific conditions
    applicable_rules.sort(key=lambda x: len(x[0].conditions), reverse=True)
    return applicable_rules


# Example usage
if __name__ == "__main__":
    print("202 Starting example usage")

    engine = InferenceEngine()

    engine.add_fact("left_bank_missionaries", 3)
    engine.add_fact("left_bank_cannibals", 3)
    engine.add_fact("right_bank_missionaries", 0)
    engine.add_fact("right_bank_cannibals", 0)
    engine.add_fact("boat_location", "left_bank")
    engine.add_fact("boat_occupancy", [1, 2])
    engine.add_fact("constraint_violated", False)
    engine.add_rule(
        Rule([("left_bank_missionaries", [1, 2, 3]), ("left_bank_cannibals", [1, 2, 3]), ("boat_location", "left_bank")], ("move_to_right_bank", ["missionaries", "cannibals"])))
    engine.add_rule(
        Rule([("right_bank_missionaries", [1, 2, 3]), ("right_bank_cannibals", [1, 2, 3]), ("boat_location", "right_bank")], ("move_to_left_bank", ["missionaries", "cannibals"])))
    engine.add_rule(
        Rule("left_bank_cannibals" > "left_bank_missionaries", ("constraint_violated", True)))

    engine.print_facts()
    engine.print_inferred()

    # Print known and inferred facts
    engine.print_facts()
    engine.print_inferred()

    root.mainloop()

    # Print facts after backward chaining
    # engine.print_facts()
