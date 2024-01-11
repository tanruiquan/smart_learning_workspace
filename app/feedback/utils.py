import torch

def generate_trace(model):
    # Trace the model
    traced = torch.fx.symbolic_trace(model)

    ref_modules = dict(traced.named_modules())
    modules = []
    for n in traced.graph.nodes:
        # print(n, n.op)
        if n.op == "call_module":
            modules.append(ref_modules[n.target])
    return modules

def compare_trace(modules1, modules2):
    res = []
    if len(modules1)  != len(modules2):
        res.append("size mismatch")
        
    for m1, m2 in zip(modules1, modules2):
        if type(m1) != type(m2):
            res.append(f"mismatch for modules: {m1} and {m2}")
            print(f"mismatch for modules: {m1} and {m2}")
            continue
        attributes1 = vars(m1)
        attributes2 = vars(m2)
        print(attributes1, attributes2)
        for attribute_key in attributes1:
            print(attribute_key)
            if not attribute_key.startswith("_"):
                a1 = attributes1[attribute_key]
                a2 = attributes2[attribute_key]
                if a1 != a2:
                    res.append(f"mismatch for modules: {m1} for attribute {attribute_key}")
                    print(f"mismatch for modules: {m1} for attribute {attribute_key}")
                else:
                    res.append(f"match for modules: {m1} for attribute {attribute_key}")
                    print(f"match for modules: {m1} for attribute {attribute_key}")
    return res