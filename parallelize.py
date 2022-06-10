import ctypes

parallelized = ctypes.CDLL('target/release/dynamic_lib')

args = (ctypes.c_char_p * 2)(*[b'data/4', b'Semantics'])
argc = ctypes.c_int(len(args))
print(parallelized.parallelized_function(args, argc))
