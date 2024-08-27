from pathlib import Path
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py


class BuildPy(build_py):
    def run(self):
        super().run()
        name = "jsx.pth"
        input_file = Path("src") / name
        output_file = Path(self.build_lib) / name
        self.copy_file(str(input_file), str(output_file), preserve_mode=False)


setup(
    name="python-jsx",
    version="0.0.1",
    description="JSX syntax in Python",
    author="eminalparslan",
    author_email="eminalparslan@gmail.com",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    cmdclass={"build_py": BuildPy},
)
