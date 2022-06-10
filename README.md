# ZPR-parallel_execution


## Description

App allowing to parallelize executions of a function from shared library by splitting them between multiple threads.

Example function is implemented in file lib.rs in Rust language. In order to increase versatility, it receives arguments as strings and parses them to appropriate type. Consecutive calls of function need to be independent of each other for results to be the same, as if all calls were made in single thread.

Splitting arguments into groups, spawning threads and merging results is done in a Python script.

## Usage

In order to recompile shared library containing example function after modyfying it, run:
```
cargo build --release
```
Help for Python script can be displayed, by running:
```
python parallelize.py -h
```