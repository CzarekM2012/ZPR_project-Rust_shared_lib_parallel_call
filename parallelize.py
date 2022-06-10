import ctypes

parallelized = ctypes.CDLL('target/release/dynamic_lib')

string = ctypes.c_char_p(b"1wse4df123")
print(parallelized.parallelized_function(string))
print(string.value)
