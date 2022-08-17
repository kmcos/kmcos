import ast # Library for parsing string representations of Python objects

# Class to encapsulate each module and the associated methods for storing it on
# disk.
class module_export_import:

    def __init__(self, save_filename, load_filename, module):
        self.save_filename = save_filename
        self.load_filename = load_filename
        self.module = module

    # This function is for saving all of the variables in the specified module.
    def save_params(self):

        # Get a list of all the exportable variables in the module. These
        # variables are listed in the special __var_list__ variable in the
        # module.
        module_vars = getattr(self.module, '__var_list__')

        # Loop over all variables in the module, get each value, and write it to
        # disk if it is a simple object (elementary data type or one-deep
        # container of elementary data types).
        with open(self.save_filename, 'wt') as f:
            for module_var in module_vars:
                module_var_val = getattr(self.module, module_var)
                if (type(module_var_val) == type('str')) or (type(module_var_val) == type(b'str')):
                    # We need to make sure string values get printed as string
                    # values or they won't be read properly on reload
                    f.write(module_var + " = '" + str(module_var_val) + "'\n")
                else:
                    # This a non-string elementary data type, so we write it as-is
                    f.write(module_var + ' = ' + str(module_var_val) + '\n')

    # This function is for setting variables in the specified module using
    # previously saved parameters.
    def load_params(self):

        # Loop over all variables in the file, get each value, and save it to
        # the module.
        with open(self.load_filename, 'rt') as f:
            for line in f:

                # This checks for comment and blank lines and skips them
                if line.strip().startswith('#') or len(line.strip()) == 0:
                    continue

                # NOTE: Alternatively, if we didn't care about security, we
                # could just exec each line (or the whole file) as the lines are
                # written in valid Python syntax of 'variable = value'.

                # Split on first equal sign only and strip surrounding
                # whitespace.  Stripping the whitespace is necessary or else we
                # will have a variable 'name' or 'value' that is surrounded by
                # spaces. When the 'name' is actually ' name ' (note the
                # spaces), setattr() will assign the parsed value to a module
                # variable named ' name ', not 'name'. If the value has
                # surrounding whitespace (at least leading whitespace), the ast
                # parser will give an 'unexpected indent' error.
                module_var, module_var_val = line.split('=', 1)
                module_var = module_var.strip()
                module_var_val = module_var_val.strip()

                # Convert to an actual Python object
                # Workaround for sets as literal_eval can't handle them in
                # Python 2.7
                if 'set' in module_var_val:
                    # Extract the bracketed portion which can be converted into
                    # a list
                    module_var_val = module_var_val[4:-1]

                    # Convert to a list
                    module_var_val = ast.literal_eval(module_var_val)

                    # Convert list to a set
                    module_var_val = set(module_var_val)
                else:
                    module_var_val = ast.literal_eval(module_var_val)

                # Store it in the module
                setattr(self.module, module_var, module_var_val)
