use pyo3::prelude::*;

/// Rust "Hello, World!" function callable from Python
#[pyfunction]
fn rust_hello() {
    println!("Hello from Rust!");
}

/// Rust module definition
#[pymodule]
fn rust_ext(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(rust_hello, m)?)?;
    Ok(())
}
