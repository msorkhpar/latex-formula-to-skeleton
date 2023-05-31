import os
import subprocess
from string import Template

import cairosvg
import pandas as pd
from dotenv import load_dotenv
from pandas import DataFrame

from image_processor import process_image

TEX_TEMPLATE = Template(r'''
\documentclass{standalone}
\usepackage{amssymb}
\usepackage{amsmath}
\usepackage{wasysym}
\begin{document}
$symbol
\end{document}
''')


def generate_png_from_latex(name, symbol: str, paths: dict[str, str], png_size):
    tex_file = os.path.join(paths['tex'], f"{name}.tex")
    dvi_file = os.path.join(paths['dvi'], f"{name}.dvi")
    svg_file = os.path.join(paths['svg'], f"{name}.svg")
    png_file = os.path.join(paths['png'], f"{name}.png")
    png_transparent = os.path.join(paths['png_t'], f"{name}.png")
    tex = tex_file[:-4]

    # Create .tex file using TEX_TEMPLATE constant
    with open(tex_file, "w") as file:
        file.write(TEX_TEMPLATE.substitute(symbol=f"${symbol.strip()}$"))

    # Compile LaTeX File
    subprocess.run(["latex", f"-output-directory={paths['dvi']}", tex], check=True)

    # Convert LaTeX to SVG using dvisvgm
    subprocess.run(["dvisvgm", "--exact", "--no-fonts", "-n", "-o", svg_file, dvi_file],
                   check=True)

    # Convert SVG to PNG using cairosvg
    cairosvg.svg2png(url=svg_file, write_to=png_file, output_width=png_size, output_height=png_size,
                     background_color="white")
    cairosvg.svg2png(url=svg_file, write_to=png_transparent, output_width=png_size, output_height=png_size)


if __name__ == '__main__':
    load_dotenv()
    csv_input_file = os.path.abspath(os.getenv("INPUT_PATH", "./latex_symbols.csv"))
    output_dir = os.getenv("INPUT_PATH", "output")
    png_size = int(os.getenv("PNG_SIZE", "1024"))
    paths = {
        "tex": os.getenv("TEX_DIR_PATH", f"{output_dir}/tex"),
        "dvi": os.getenv("DVI_DIR_PATH", f"{output_dir}/dvi"),
        "svg": os.getenv("SVG_DIR_PATH", f"{output_dir}/svg"),
        "png": os.getenv("PNG_DIR_PATH", f"{output_dir}/png"),
        "png_t": os.getenv("PNG_TRANSPARENT_DIR_PATH", f"{output_dir}/png_transparent"),
        "skeleton": os.getenv("SKELETON_DIR_PATH", f"{output_dir}/skeleton"),
    }
    [os.makedirs(path, exist_ok=True) for name, path in paths.items()]

    # Read the input csv file
    df: DataFrame = pd.read_csv(csv_input_file)
    print('''
|Index|Name|LaTeX symbol| SVG | PNG | PNG | Skeleton | Tex | DVI |  
|:--: |:--:|:--:        |:--: | :--:| :--: |:------: | :--:| :--:|''')

    for index, row in df.iterrows():
        name = row['Name']
        symbol = row['Symbol']
        image = row['Image']

        # Generate png file
        #generate_png_from_latex(name, symbol, paths, png_size)

        svg_file = os.path.join(paths['svg'], f"{name}.svg")
        png_transparent = os.path.join(paths['png_t'], f"{name}.png")
        tex_file = os.path.join(paths['tex'], f"{name}.tex")
        dvi_file = os.path.join(paths['dvi'], f"{name}.dvi")
        skeleton_file = os.path.join(paths['skeleton'], f"{name}.png")
        png_file = os.path.join(paths['png'], f"{name}.png")
        print(f"|{index+1}|{name}|{symbol}|<img src='{svg_file}' height='32' width='32'> | [link]({png_file}) | [link]({png_transparent}) | [link]({skeleton_file}) | [link]({tex_file}) | [link]({dvi_file}) | ")
        # Generate skeleton of the generated file
        #process_image(png_file, skeleton_file)
