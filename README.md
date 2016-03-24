# Ideogram
Create a visual fingerprint of your Python project's source code!

## Installation
This project is currently under development. Soon, Ideogram will be hosted on PyPi.

## How to use it 
In order to get started creating, you must create some Ideogram objects and `generate` them. For example:
```python
import ideogram 

netwk = ideogram.Ideogram(outdir='network_viz',
                          mode='network',
                          title='Hola, mundo!',
                          font_family='sans-serif',
                          font_size='60px',
                          title_color='rgb(0,0,0)',
                          colorscheme='Spectral',
                          bgcolor='rgb(155,45,0)'
                          )
pack = ideogram.Ideogram(outdir='pack_viz',
                         mode='pack',
                         colorscheme='random',
                         bgcolor='random'
                         )
ideogram.generate('https://github.com/brmscheiner/ideogram',netwk,pack)
```
Ideogram objects are instantiated with several keyword arguments, which afford some control over the final product.

| Argument    | Usage     | Description                                                                                          |
|-------------|-----------|------------------------------------------------------------------------------------------------------|
| outdir      | mandatory | Specify the path to the directory to put the output html, js, and csv files                          |
| mode        | mandatory | What kind of Ideogram are you making? The options are 'network', 'moire', 'depth', and 'pack'        |
| title       | optional  | A string that will be displayed in the center of your visualization                                  |
| font_family | optional  | The font-family css attribute for the title                                                          |
| font_size   | optional  | The font-size css attribute for the title. '40px', '2.0em', and '200%' are all valid                 |
| title_color | optional  | The color attribute for the title text, such as 'red', 'rgb(0,0,0)' or 'rgba(0,0,0,0.5)'             |
| colorscheme | optional  | The colorbrewer colorscheme you would like to use. [Colorbrewer schemes](https://bl.ocks.org/mbostock/5577023)                         |
| bgcolor     | optional  | The color attribute for the background, such as 'red', 'rgb(0,0,0)' or 'rgba(0,0,0,0.5)'             |

After you're done building your Ideogram objects, pass them to the `generate` function along with the path to a local directory that contains some Python source code. 
```python
ideogram.generate('Desktop/code/myproject',thing1,thing2,thing3)
```
The `generate` function also accepts links to github projects.
```python
ideogram.generate('https://github.com/brmscheiner/ideogram',thing1,thing2,thing3,thing4)
```
Still here? OK, last step! To see your creation, you need to host the output files on a server. Depending on your background that might sound intimidating, but the good news is there's an easy-to-use Python module that takes care of the heavy lifting for you. If you have Python 2, it's called [SimpleHTTPServer](https://docs.python.org/2/library/simplehttpserver.html). In Python 3 it's called [http.server](https://docs.python.org/3/library/http.server.html). If you're not sure which version of Python is on your computer, just open the terminal and type `python --version`. Now, navigate to the directory where you put your Ideograms and start serving:
```bash
cd path/to/output/files
python -m http.server 8080       OR        python -m SimpleHTTPServer 8080
```
You should see a message like `Serving HTTP on 0.0.0.0 port 8080 ...`, possibly followed by some gibberish. All you have to do now is open Chrome or Firefox and navigate to [http://localhost:8080/](http://localhost:8080/). If everything went according to plan, you should see your visualization! For large projects, it could take a minute for the page to load and process the data.
## Examples 
Check out the [Ideogram gallery](http://scheinerbock.com/ideogram.html).

## Credit
This is my first Python package! Many thanks to Drew Garrido, James Porter, Diwank Tomer, and Oren Shoham for their help putting it all together. 
