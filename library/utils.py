def simplify_function_name(selection: object) -> str:
    name = selection.__name__

    if name == "tournament_selection":
        return "ts"
    elif name == "fitness_proportionate_selection":
        return "fps"
    elif name == "boltzmann_selection":
        return "bs"
    elif name == "block_single_point_xo":
        return "bspxo"
    elif name == "row_single_point_xo":
        return "rspxo"
    elif name == "row_partially_mapped_xo":
        return "rpmxo"
    elif name == "row_uniform_xo":
        return "uxo"
    elif name == "block_swap_mutation":
        return "bsm"
    elif name == "row_swap_mutation":
        return "rsm"
    elif name == "row_random_mutation":
        return "rrm"
    elif name == "row_inversion_mutation":
        return "rim"
    else:
        return "ERROR"
