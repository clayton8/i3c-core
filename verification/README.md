# Verification

The I3C Core is verified with rapid cocotb tests and the UVM test suite, located in `cocotb` and `uvm_i3c` directories, respectively.

## Cocotb

Tests are split into directories:
* `top` - top level, full I3C tests
* `block` - module level, unit tests, subsystems

Once setup is completed, all simulations can be launched with `make tests`.
In order to run a specific test, you can also use `TEST=<test_name> make test`.

### Debugging simulations

Launching simulation without `nox` is useful for debugging.
In the project root, first export the following variables:

```{bash}
export CALIPTRA_ROOT=$(pwd)/third_party/caliptra-rtl
export I3C_ROOT_DIR=$(pwd)
```

Then enter the `verification/cocotb/block` directory and run

```{bash}
make -C ./<block_name> clean all MODULE=<test_name>
```

## UVM

The UVM tests should be run from the project root directory.

### Running I3C agent tests

* `make tests-uvm SIMULATOR=simulator_of_your_choice` runs all I3C agent tests.
* `make i3c-verify-test-uvm SIMULATOR=simulator_of_your_choice TEST=virtual_sequence_to_run` runs a single I3C agent test.

### Running I3C core tests

* `make tests-i3c-core-uvm SIMULATOR=simulator_of_your_choice` runs all I3C core tests.
* `make i3c-core-verify-test-uvm SIMULATOR=simulator_of_your_choice TEST=virtual_sequence_to_run` runs a single I3C core test.
