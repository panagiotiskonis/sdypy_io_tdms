# SDyPy TDMS I/O

This package provides read and write functions for National Instruments `.tdms`
files in a way that is compliant with the SDyPy format for timeseries.

## Installation

Available from PyPI:

```bash
pip install sdypy-io-tdms
```

## Using the package

Reading and writing is provided by `read_tdms` and `write_tdms`. Both functions
return or accept SEP-005 compliant data validated through the `Sep005Data` model
from [`sdypy-sep005`](https://github.com/OWI-Lab/sdypy-sep005-compliance).

```python
from sdypy_io_tdms import read_tdms, write_tdms

signals = read_tdms("path/to/file.tdms")

write_tdms(signals, "path/to/output.tdms")
```

`read_tdms` returns a list of validated `Sep005Data` models. `write_tdms`
accepts `Sep005Data` instances or dictionaries and converts dict entries before
writing.

## Contributing

Contributions are welcome and greatly appreciated!

### Workflow

A bug fix or enhancement is delivered using a pull request. A good pull request
should cover one bug fix or enhancement feature. This keeps the change set easier
to review and less likely to need major rework or rejection.

The workflow that developers typically use is as follows.

1. Fork the [sdypy_io_tdms](https://github.com/OWI-Lab/sdypy_io_tdms)
   repository into your account.

2. Clone the source onto your development machine:

   ```bash
   git clone https://github.com/OWI-Lab/sdypy_io_tdms.git
   cd sdypy_io_tdms
   ```

3. Install [uv](https://docs.astral.sh/uv/) and sync the project dependencies:

   ```bash
   uv sync
   ```

   This creates a virtual environment and installs the default dependency groups
   (`ci` and `test`) defined in `pyproject.toml`.

4. Create a branch for local development:

   ```bash
   git checkout -b name-of-your-bugfix-or-feature
   ```

5. Develop your fix or enhancement:

   - Make a fix or enhancement (for example, modify a class, method, function,
     or module).
   - Update an existing unit test or create a new unit test module to verify
     the change works as expected.
   - Run the test suite:

     ```bash
     uv run pytest
     ```

6. Update the docs for anything but trivial bug fixes, then build them to verify
   the result:

   ```bash
   uv sync --group docs
   cd docs
   uv run make clean
   uv run make html
   ```

7. Commit and push changes to your fork:

   ```bash
   git add .
   git commit -m "A detailed description of the changes."
   git push origin name-of-your-bugfix-or-feature
   ```

   A pull request should preferably only have one commit upon the current
   `main` HEAD (via rebases and squash).

8. Submit a pull request through GitHub.

9. Check that automated continuous integration steps all pass. Fix any problems
   if necessary and update the pull request.

## Acknowledgements

This package was developed in the framework of the
[Interreg Smart Circular Bridge project](https://vb.nweurope.eu/projects/project-search/smart-circular-bridge-scb-for-pedestrians-and-cyclists-in-a-circular-built-environment/).
