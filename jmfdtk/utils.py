import sys

if 'ipykernel' in sys.modules:
    # Jupyter Notebook/Lab
    from IPython.display import Markdown

    def _display(*args):
        display(*args)

    def _display_md(mdtext):
        display(Markdown(mdtext))
else:
    def _display(*args):
        print(*args)

    def _display_md(mdtext):
        print(mdtext)
