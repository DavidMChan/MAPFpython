# Override print function to allow verbosity control

def printv(*args, **kwargs):
    """custom print function"""
    # If verbosity is unspecified, assume high verbosity level (to behave like regular print)
    verbosity=int(kwargs['verbosity']) if 'verbosity' in kwargs.keys() else 0
    if GLOBAL_ARGS.verbose>=verbosity:
        print(args)
