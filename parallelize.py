import ctypes
import argparse
from threading import Thread
from multiprocessing import cpu_count
import numpy as np
from sys import platform

def parse_arguments():
    parser = argparse.ArgumentParser(description='Parallelize execution of multiple calls to function.')
    parser.add_argument('function_args', metavar='arg', type=str, nargs='+',
                        help='call argument for function, they will be split according to argc and \
passed to calls in order they were given')
    parser.add_argument('-c', '--argc', metavar='num', type=int, default=2,
                        help='Number of arguments taken by single call to parallelized function \
(2 by default to match default function)')
    parser.add_argument('-t', '--threads', metavar='num', type=int, default=cpu_count(),
                        help='Number of separate threads to spawn (number of CPUs in the system by default)')
    args = parser.parse_args()
    args.threads = min(cpu_count(), args.threads) # No point in spawning more threads than CPUs
    return args

def truncate_args(function_args, call_argc):
    dangling = len(function_args) % call_argc
    if(dangling != 0):
        print(f'since number of function args given ({len(function_args)}) wasn\'t divisible by argc per call \
({call_argc}), last ' + (f'{dangling} args were dropped' if dangling > 1 else 'arg was dropped'))
        function_args = function_args[0:-dangling]
    return function_args

def split_args_sets(arg_sets, threads_count):
    array = np.asarray(arg_sets)
    split = np.array_split(array, threads_count)
    return [tuple(map(tuple, arr)) for arr in split]

def call_function(args, *kwargs):
    argc, writing_area, writing_index, lib = kwargs
    C_argc = ctypes.c_int(argc)
    for function_call_args in args:
        bytes_args = tuple(map(str.encode, function_call_args))
        val = lib.parallelized_function((ctypes.c_char_p * argc)(*bytes_args), C_argc)
        writing_area[writing_index] = val
        writing_index += 1


if __name__ == '__main__':
    call_args = parse_arguments()
    # Relative paths I got after building Rust code on Windows and Ubuntu, will probably cause the program to stop with error if used on another
    shared_lib_path = 'target/release/dynamic_lib' if platform=='win32' else 'target/release/libdynamic_lib.so'
    parallelized = ctypes.CDLL(shared_lib_path)

    # Prepare arguments sets for threads
    truncated_args = truncate_args(call_args.function_args, call_args.argc)
    args_sets = []
    for i in range((len(truncated_args)//call_args.argc)):
        args_sets.append(tuple(truncated_args[i*call_args.argc : (i+1)*call_args.argc]))
    threads_sets = split_args_sets(args_sets, min(call_args.threads, len(args_sets))) # No point in spawning more threads than function calls

    # Prepare area for threads to write results in
    results = [None] * len(args_sets)
    indices = []
    start = 0
    for tup in threads_sets:
        indices.append(start)
        start += len(tup)

    # Create and run threads
    threads = []
    for i in range(len(threads_sets)):
        thread = Thread(target=call_function, args=tuple([threads_sets[i], call_args.argc, results, indices[i], parallelized]))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(results)
