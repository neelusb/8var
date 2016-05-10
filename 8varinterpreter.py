#!/usr/bin/env python

import eightvar
import sys
import os

def prompt(inp):
    if not inp.startswith('8v'):
        inp = '8v1.1v.' + inp + 'fin'
    retval = eightvar.prnt(inp)
    if retval:
        return retval

def passToEV(inp):
    if inp.startswith('#!'):
        while inp[0] != '\n':
            inp = inp[1:]
        inp = inp[1:]
    eightvar.prnt(inp)

def minify(inp):
    out = ''
    if inp.startswith("#!"):
        bangout = ''
        while not inp.startswith('##'):
            bangout = bangout + inp[0]
            inp = inp[1:]
        inp = inp[2:]
        out = out + bangout + '##'
        bangout = ''
    while len(inp) > 0:
        if inp.startswith('\ '):
            out = out + '\ '
            inp = inp[2:]
        elif inp.startswith(' '):
            inp = inp[1:]
        elif inp.startswith('\n'):
            inp = inp[1:]
        else:
            out = out + inp[0]
            inp = inp[1:]
    return out    

if len(sys.argv) == 1:
    prm = ''
    inp = ''
    print '8var 1.1.6 (v1.1.6 May 9, 2016 21:41:12 UTC)'
    print '8var interpreter from https://www.github.com/neelusb/8var'
    print ''
    while prm[-4:] != 'exit' and prm[-3:] != 'fin':
        try:
            prm = raw_input('>>> ')
            if prm.startswith('in') and prm[2] != 't' and prm[2:4] != 'cl':
                prmx = raw_input('')
                if prm.startswith('instr'):
                    prm = prm[2:] + "'" + prmx + "'"
                else:
                    prm = prm[2:] + prmx
            if prm.startswith('flt') or prm.startswith('float') or prm.startswith('str') or prm.startswith('bool') or prm.startswith('out') or prm.startswith('uout') or prm.startswith('in') or prm.startswith('dly'):
                if not prm.startswith('out'):
                    inp = inp + prm
                    retval = prompt(inp)
                    if retval:
                        print retval
                else:
                    retval = prompt(inp + prm)
                    if retval:
                        print retval
            else:
                sys.stdout.write("\n")
        except (KeyboardInterrupt, EOFError):
            print "\nUse 'fin' or 'exit' to exit."
                
elif len(sys.argv) > 4:
    sys.exit('Too many arguments and/or invalid arguments received.')

elif len(sys.argv) == 3:
    script, flag, toeightvar = sys.argv
    if flag == '-c':
        eightvar.prnt(toeightvar)
    elif flag == 'minify':
        script, flag, inpfile = sys.argv
        out = ''
        inp = open(inpfile, "r").read()
        outfile = ''
        
        if '.' in inpfile:
            procfile = inpfile[::-1]
            outfileext = ''
            while procfile[0] != '.':
                outfileext = outfileext + procfile[0]
                procfile = procfile[1:]
            procfile = procfile[1:]
            outfileext = outfileext[::-1]
            outfileext = '.min.' + outfileext
            while len(procfile) > 0:
                outfile = outfile + procfile[0]
                procfile = procfile[1:]
            outfile = outfile[::-1]
            outfile = outfile + outfileext
        else:
            outfileext = 'min.8v'
            while len(procfile) > 0:
                outfile = outfile + procfile[0]
                procfile = procfile[1:]
            outfile = outfile[::-1]
            outfile = outfile + outfileext
        out = minify(inp)
        open(outfile, "w").write(out)
        print 'Minified file ' + inpfile + ' and saved to file ' + outfile + '.'
    else:
        sys.exit('Too many arguments and/or invalid arguments received.') 

elif len(sys.argv) == 4:
    script, flag, inpfile, outfile = sys.argv
    if flag == 'minify':
        out = ''
        inp = open(inpfile, "r").read()

        out = minify(inp)
        open(outfile, "w").write(out)
        print 'Minified file ' + inpfile + ' and saved to file ' + outfile + '.'
    else:
        sys.exit('Too many arguments and/or invalid arguments received.') 
        
else:
    script, fname = sys.argv
    if not os.path.isfile(fname):
        sys.exit('File ' + fname + ' not found. Please check the path and try again.')
    else:
        passToEV(open(fname, "r").read())
