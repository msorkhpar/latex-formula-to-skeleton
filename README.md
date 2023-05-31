## LaTeX Formula Skeleton Generator

This repository provides a solution for generating the skeleton of LaTeX formulas using the `latex`, `dvisvgm`, `cairosvg`, and `skimage` libraries. The process involves converting LaTeX formulas to DVI, SVG, and PNG formats, followed by skeleton extraction using the Lee algorithm.

## Requirements

To use this code, ensure you have the following dependencies installed:
- `latex` command-line tool
- `dvisvgm` command-line tool for converting DVI to SVG
- `cairosvg` for converting SVG to PNG
- `numpy` and `pandas` for data processing
- `skimage` for skeleton extraction

### Usage

1. Set up the output directory by modifying the `output_dir` variable in the `.env` file.
2. Create a CSV file named `latex_symbols.csv` with columns: `Name` and `Symbol` for each LaTeX symbol(formula) to be processed.
3. Run the code.
4. Generated files will be available under the paths provided in the `.env` file.

Please ensure that you have the necessary dependencies installed and configured properly before running the code.

Feel free to customize the code and adapt it to your specific requirements.
