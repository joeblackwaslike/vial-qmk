"""Build QMK documentation locally
"""
import shutil
from pathlib import Path
from subprocess import DEVNULL

from milc import cli

DOCS_PATH = Path('docs/')
BUILD_PATH = Path('.build/docs/')


@cli.subcommand('Build QMK documentation.', hidden=not cli.config.user.developer)
def generate_docs(cli):
    """Invoke the docs generation process

    TODO(unclaimed):
        * [ ] Add a real build step... something static docs
    """

    if BUILD_PATH.exists():
        shutil.rmtree(BUILD_PATH)

    shutil.copytree(DOCS_PATH, BUILD_PATH)

    # When not verbose we want to hide all output
    args = {
        'capture_output': not cli.config.general.verbose,
        'check': True,
        'stdin': DEVNULL,
    }


    cli.log.info('Generating internal docs...')

    # Generate internal docs
    cli.run(['doxygen', 'Doxyfile'], **args)
    cli.run(['moxygen', '-q', '-a', '-g', '-o', BUILD_PATH / 'internals_%s.md', 'doxygen/xml'], **args)

    cli.log.info('Successfully generated internal docs to %s.', BUILD_PATH)
