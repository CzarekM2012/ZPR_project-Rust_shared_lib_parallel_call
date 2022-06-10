use libc;
use std::ffi::CStr;
use std::fs;

# [no_mangle]
pub extern fn parallelized_function(args: *const *const libc::c_char, argc: libc::c_uint) -> libc::c_int {
    let mut arguments = Vec::<String>::new();
    let mut current_pointer = args;
    unsafe {
        for _ in 0..argc {
            match CStr::from_ptr(*current_pointer).to_str() {
                Ok(val) => arguments.push(val.to_owned()),
                Err(_) => return -1 // arg had invalid UTF-8 data, contents of Err has the details, you may want to change the way this situation is handled
            }
            current_pointer = current_pointer.offset(1);
        }
    }
    /*
    Parsing specific arguments to types needed by function




    */
    count_word_occurences_in_file(&arguments[0], &arguments[1]).try_into().unwrap()
}

fn count_word_occurences_in_file(filepath: &String, word: &String) -> isize {
    let contents;
    match fs::read_to_string(filepath) {
        Ok(val) => contents = val,
        Err(err) => {
            let message = format!("Could not read from file: {}. ", filepath) + &err.to_string();
            println!("{}", message);
            return -2;
        }
    }
    contents.matches(word).count().try_into().unwrap()
}