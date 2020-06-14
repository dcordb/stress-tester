from random import randint, shuffle
import subprocess
import argparse

parser = argparse.ArgumentParser(description = 'Stress Tester')
parser.add_argument('-v', action = 'store_true', help = 'Verbose Mode')
parser.add_argument('exec', help = 'Path to executable file', type = str)
parser.add_argument('-t', help = 'Timeout to execute in seconds', default = 1, type = int)
args = parser.parse_args()

def gen():
    n = randint(1, 5)
    a = [ randint(1, 10) for _ in range(n) ]

    s = (
        f'{n}\n' + 
        " ".join(map(str, a)) + '\n'
    )

    return s

def evaluate(input, output):
    pass

def main(exec_path, timeout):
    #executable name and timeout (in seconds)

    tc = 1

    while True:
        print(f'Case {tc}:')

        gen_input = gen()

        try:
            p = subprocess.run([exec_path], capture_output = True, timeout = timeout,
                                text = True, input = gen_input, check = True)

        except subprocess.CalledProcessError as p_errors:
            print(f'Process exited with code {p_errors.returncode}')
            print(f'Following errors were found:\n\n{p_errors.stderr}')

            with open('input', 'w') as f:
                print(gen_input, file=f)

            break

        except subprocess.TimeoutExpired:
            print(f'Executable exceeded timeout of {timeout} seconds')
            break

        if args.v:
            print('Input:')
            print(gen_input, end='')

            print('Output:')
            print(p.stdout)

        evaluate(gen_input, p.stdout)

        print('Ok')
        
        tc += 1

main(args.exec, args.t)
