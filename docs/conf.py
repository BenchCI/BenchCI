project = "BenchCI"
author = "BenchCI"
release = "0.1"

extensions = [
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "furo"
html_static_path = ["_static"]

myst_enable_extensions = [
    "colon_fence",
    "deflist",
]