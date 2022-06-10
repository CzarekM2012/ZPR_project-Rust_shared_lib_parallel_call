use libc;
use std::ffi::CStr;

# [no_mangle]
pub extern fn parallelized_function(arg: *mut libc::c_char) -> isize {
    let argument;
    unsafe { 
        match CStr::from_ptr(arg).to_str() {
            Ok(val) => argument = val.to_owned(),
            Err(_) => return -1 // arg had invalid UTF-8 data, contents of Err has the details, you may want to change the way this situation is handled
        }
    }
    argument.len().try_into().unwrap()
}
