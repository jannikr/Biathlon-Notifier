# print pretty dictionary
def print_dict(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            print_dict(value, indent + 1)
        else:
            for b_event in value:
                print('\t' * (indent + 1) + str(b_event))