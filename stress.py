#!/usr/bin/python3
from random import randint, shuffle
import subprocess
import argparse
from time import sleep

parser = argparse.ArgumentParser(description = 'Stress Tester')
parser.add_argument('-v', action = 'store_true', help = 'Verbose Mode')
parser.add_argument('model', help = 'Path to model solution', type = str)
parser.add_argument('brute', help = 'Path to brute solution', type = str)
parser.add_argument('-t', help = 'Timeout to execute in seconds', default = 1, type = int)
parser.add_argument('-i', help = 'Show input', action = 'store_true', dest = 'show_input')
parser.add_argument('-o', help = 'Show output', action = 'store_true', dest = 'show_output')
parser.add_argument('-debug', help = 'Debug mode', action = 'store_true')
parser.add_argument('-s', help = 'Sleep mode', action = 'store_true')
args = parser.parse_args()

def gen():
    M = 20

    for i in range(1, M):
        for x in range(0, 2 ** i):
            yield f'{bin(x)[2:].zfill(i)}\n'

def evaluate(model, brute, input=''):
    if model != brute:
        with open('input', 'w') as f:
            print(input, file=f)

        raise RuntimeError('Model and brute output differ')

def main(model, brute, timeout):
    tc = 1

    gen_obj = gen()

    while True:
        print(f'Case {tc}:')

        gen_input = next(gen_obj)

        def run_solution(path):
            if args.show_input:
                print('Input:')
                print(gen_input, end='')

            if args.v:
                print(f'Running {path} solution...')

            try:
                p = subprocess.run([path], capture_output = True, timeout = timeout,
                                    text = True, input = gen_input, check = True)

            except subprocess.CalledProcessError as p_errors:
                print(f'Process exited with code {p_errors.returncode}')
                print(f'Following errors were found:\n\n{p_errors.stderr}')

                with open('input', 'w') as f:
                    print(gen_input, file=f)

                exit(0)

            except subprocess.TimeoutExpired:
                print(f'Executable exceeded timeout of {timeout} seconds')
                exit(0)

            if args.v:
                print('Ok, solution finished')

            if args.show_output:
                print('Output:')
                print(p.stdout)

            return p.stdout

        model_ans = run_solution(model)
        brute_ans = run_solution(brute)

        evaluate(model_ans, brute_ans, gen_input)

        print('#' * 100)        
        tc += 1

        if args.debug:
            break

        if args.s:
            sleep(1)

main(args.model, args.brute, args.t)
