# Ideogram
Create a visual fingerprint of your Python project's source code!

## Installation
This project is currently under development. Soon, Ideogram will be hosted on PyPi.

## How to use it 
In order to get started creating Ideograms, you must create some Chart objects and `generate` them. For example:
```python
net = ideogram.Chart(outdir='skynet',
                     mode='network',
                     title='I am Skynet.',
                     font_family='sans-serif',
                     font_size='46px',
                     title_color=(255,255,255),
                     colorscheme=[(0,0,0),(220,431,23),(122,20,102),(255,255,255)],
                     bgcolor=(0,0,0)
                     )
moire = ideogram.Chart(outdir='output-moire',
                       mode='network',
                       colorscheme=[(0,0,0),(220,431,23),(122,20,102),(255,255,255)],
                       bgcolor=(0,0,0)
                       )
ideogram.generate('ideogram',[net,moire])
```
Chart objects are instantiated with up to 8 arguments, most of which control some aspect of the final product.

| Argument    | Usage     | Description                                                                                        |
|-------------|-----------|----------------------------------------------------------------------------------------------------|
| outdir      | mandatory | Specify the path to the directory to dump the output html, js, and csv files.                      |
| mode        | mandatory | What kind of Ideogram are you making? The options are 'network', 'moire', and 'pack'.              |
| title       | optional  | The title of your Ideogram.                                                                        |
| font_family | optional  | The font-family css attribute for the title.                                                       |
| font_size   | optional  | The font-size css attribute for the title. '40px', '2.0em', and '200%' are all valid.              |
| title_color | optional  | The color attribute for the title text, such as 'red', 'rgb(0,0,0)' or 'rgba(0,0,0,0.5)'.          |
| colorscheme | optional  |                                                                                                    |
| bgcolor     | optional  | The color attribute for the Ideogram background, such as 'red', 'rgb(0,0,0)' or 'rgba(0,0,0,0.5)'. |

After Creating any number of Chart objects, pass them to the `generate` function along with the project directory that contains your source code. 
```python
ideogram.generate('path/to/project',[Chart1,Chart2,Chart3,...])
```
To see your creation, you will need to host the visualization files on a server. Probably the easiest way is to use [SimpleHTTPServer](https://docs.python.org/2/library/simplehttpserver.html) (Python 2.x) or [http.server](https://docs.python.org/3/library/http.server.html) (Python 3.x). Open the terminal and type `python --version` if you're not sure which version of Python is on your computer. We only need the basic functionality of these modules: 
```bash
cd path/to/output/files
python -m http.server 8080       OR        python -m SimpleHTTPServer 8080
```
Now, open Chrome or Firefox and navigate to [http://localhost:8080/](http://localhost:8080/). If the server is working properly, you should be able to see your visualization! For large projects, it could take a minute for the page to load.
## Examples 
Check out the [Ideogram gallery](http://scheinerbock.com/ideogram.html).

## Credit
Many thanks to Drew Garrido, Diwank Tomer, and Oren Shoham for their valuable insight. 
