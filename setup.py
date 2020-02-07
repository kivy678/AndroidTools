from distutils.core import setup, Extension
import os

LibPath = os.path.dirname(os.path.realpath(__file__))

module = Extension(
    "[moduleName]",
    define_macros=[("MAJOR_VERSION", "1"), ("MINOR_VERSION", "0")],
    # include_dirs = [LibPath],
    # library_dirs = [],
    # libraries = [],
    sources=[".cpp"],
    language="c++",
    extra_compile_args=["-std=c++11", "-w", "-Wall", "-O2"],
)

setup(
    name="AndroidTools",
    version="0.1",
    description="Android Tool KIT",
    author="Kivy",
    author_email="kivy678@gmail.com",
    url="",
    # ext_modules=[module]
)
