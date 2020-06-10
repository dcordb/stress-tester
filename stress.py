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

def main(exec_path, time):
    #executable name and timeout (in seconds)

    tc = 1

    while True:
        print(f'Case {tc}:')

        gen_input = gen()

        if args.v:
            print(gen_input, end='')

        try:
            p = subprocess.run([exec_path], capture_output = True, timeout = time,
                                text = True, input = gen_input, check = True)

        except subprocess.CalledProcessError as p_errors:
            print(p_errors.stderr)
            break

        except subprocess.TimeoutExpired:
            print(f'Executable exceeded timeout of {time} seconds')
            break

        evaluate(gen_input, p.stdout)

        print('Ok')
        
        tc += 1

main(args.exec, args.t)
