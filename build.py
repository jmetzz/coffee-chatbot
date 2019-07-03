from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")
use_plugin("python.coverage")

name = "ActionServerPybuilder"
default_task = ['install_dependencies', 'analyze', 'publish']

@init
def set_properties(project):
    project.build_depends_on('tblib')
    project.build_depends_on('mockito')
    project.build_depends_on('parameterized')
    project.build_depends_on('responses')

@init
def initialize_flake8_plugin(project):
    project.build_depends_on("flake8")
    project.set_property('unittest_module_glob', 'test_*')
    project.set_property("flake8_verbose_output", True)
    project.set_property("flake8_break_build", True)
    project.set_property("flake8_max_line_length", 120)
    project.set_property("flake8_exclude_patterns", None)
    project.set_property("flake8_include_test_sources", False)
    project.set_property("flake8_include_scripts", False)


@init
def initialize_coverage_plugin(project):
    project.set_property('coverage_break_build', False)
    project.set_property('coverage_threshold_warn', 80)
    # for now, code coverage does not break the build
    # as we do Python, a scripted language, you have to aim for 100% coverage!
    project.set_property("coverage_exceptions", ['endpoint'])
