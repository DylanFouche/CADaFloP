# CADaFloP
Prototype components for a dataflow implementation of the CARTA backend.

## Setup

### 1. Clone this repo
```bash
git clone https://github.com/DylanFouche/CADaFloP
```

### 2. Install requirements
```bash
python3 -m pip install -r requirements.txt
```

## Usage

### Running tests

#### 1. Unit tests

Execute all unit tests:
```bash
./main.py -t
```

#### 2. Performance tests

Execute performance tests:
```bash
./main.py -p
```

This tests Dask locally by default. Combine this with other command line parameters to test different scenarios. For example, to compare CARTA with Dask distributed:
```bash
./main.py -pc && ./main.py -pd
```

#### 3. All tests

Use the shell script to execute the full suite of performance and correctness tests:

```bash
./test.sh
```

This script will also take care of starting and stopping the CARTA server and dask schedulers.

### Running the project interactively

```bash
./main.py
```

Usage: main.py [-h] [-c] [-v] [-t] [-p] [-d] [-m] [-b BASE]
               [--dask_address DASK_ADDRESS] [--carta_address CARTA_ADDRESS]
               [--dask_port DASK_PORT] [--carta_port CARTA_PORT]

Optional arguments:

  -h, --help:                        Show help message and exit
  
  -c, --carta:                       Establish a connection with CARTA back-end
  
  -v, --verbose:                     Enable verbose info logging to console
  
  -t, --unit_tests:                  Run unit tests
  
  -p, --performance_tests:           Run performance tests
  
  -d, --distributed:                 Distribute Dask work over our cluster
  
  -m, --ramdisk:                     Use test images already in memory
  
  -b BASE, --base BASE:              Root directory of image data (Default: /data/cadaflop/Data/)
  
  --dask_address DASK_ADDRESS:       Host address for our Dask python server (Default: 'localhost')
  
  --carta_address CARTA_ADDRESS:     Host address for the CARTA back-end server (Default: 'localhost')
  
  --dask_port DASK_PORT:             Port for our Dask python server (Default: 3003)
  
  --carta_port CARTA_PORT:           Port for the CARTA back-end server (Default: 3002)
  
 
