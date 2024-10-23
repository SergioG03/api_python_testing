from projen.python import PythonProject

project = PythonProject(
    author_email="gpajarero@outlook.es",
    author_name="sergiog03",
    module_name="api_python_testing",
    name="api_python_testing",
    version="0.1.0",
)

project.synth()