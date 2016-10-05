#!/usr/bin/env python3
"""
Test getopt for export_fields scripts.
"""

import sys, ast, getopt

def main(argv):
    """Parse python command line arguments."""
    arg_dict = {}
    switches = {'origin':list,'len':list,'delta':list}
    #singles=''.join([x[0]+':' for x in switches])
    singles=''
    long_form=[x+'=' for x in switches]
    d={x[0]+':':'--'+x for x in switches}
    try:
        opts, args = getopt.getopt(argv, singles, long_form)
    except getopt.GetoptError:
        print("Bad argument")
        sys.exit(2)

    for opt, arg in opts:
        if opt[1]+':' in d: o=d[opt[1]+':'][2:]
        elif opt in d.values(): o=opt[2:]
        else: o=''
        print("opt: ", opt, ", arg: ",  arg, ", o: ", o)
        if o and arg:
            arg_dict[o]=ast.literal_eval(arg)
            
        if not o or not isinstance(arg_dict[o], switches[o]):
            print(opt, arg, " Error: bad arg")
            sys.exit(2)

    for e in arg_dict:
        print(e, arg_dict[e], type(arg_dict[e]))

if __name__ == '__main__':
    main(sys.argv[1:])
