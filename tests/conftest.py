import sys, os
import pytest
import logging

logging.getLogger("jpegdata").setLevel(level=logging.WARNING)

logger = logging.getLogger(__name__)

# Add the library path for importing into the tests
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "source"))

arguments: list[str] = [
    "filename",
    "save",
    "level",
]


def pytest_addoption(parser):
    logger.debug("pytest_addoption(parser: %s)" % (type(parser)))

    for argument in arguments:
        parser.addoption(f"--{argument}", action="store", default=None)


def pytest_generate_tests(metafunc):
    logger.debug("pytest_generate_tests(metafunc: %s)" % (type(metafunc)))

    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    for argument in arguments:
        value = getattr(metafunc.config.option, argument)

        logger.debug(f" > argument: {argument}, value: {value}")

        if argument in metafunc.fixturenames:  # and not value is None:
            logger.debug(" > argument is in fixturenames")
            metafunc.parametrize(argument, [value])
        else:
            logger.debug(" > argument is not in fixturenames")


@pytest.fixture(scope="session", name="path")
def path() -> callable:
    """Create a fixture that can be used to obtain the absolute filepath of example data
    files by specifying the path relative to the /tests/data folder."""

    def fixture(path: str, exists: bool = True, extension: bool = True) -> str:
        """Assemble the absolute filepath for the specified example data file."""

        if not isinstance(path, str):
            raise TypeError("The 'path' argument must have a string value!")

        if not isinstance(exists, bool):
            raise TypeError("The 'exists' argument must have a boolean value!")

        if not isinstance(extension, bool):
            raise TypeError("The 'extension' argument must have a boolean value!")

        if extension is True and not (path.endswith(".jpeg") or path.endswith(".jpg")):
            path += ".jpeg"

        filepath = os.path.join(os.path.dirname(__file__), "data", path)

        if exists is True and not os.path.exists(filepath):
            raise ValueError(
                f"The requested example file, '{filepath}', does not exist!"
            )

        return filepath

    return fixture


@pytest.fixture(scope="session", name="data")
def data() -> callable:
    """Create a fixture that can be used to obtain the contents of example data files as
    strings or bytes by specifying the path relative to the /tests/data folder."""

    def fixture(path: str, binary: bool = False) -> str:
        """Read the specified data file, returning its contents either as a string value
        or if requested in binary mode returning the encoded bytes value."""

        if not isinstance(path, str):
            raise TypeError("The 'path' argument must have a string value!")

        if not isinstance(binary, bool):
            raise TypeError("The 'binary' argument must have a boolean value!")

        if not path.endswith(".xml"):
            path += ".xml"

        filepath = os.path.join(os.path.dirname(__file__), "data", path)

        if not os.path.exists(filepath):
            raise ValueError(
                f"The requested example file, '{filepath}', does not exist!"
            )

        # If binary mode has been specified, adjust the read mode accordingly
        mode: str = "rb" if binary else "r"

        with open(filepath, mode) as handle:
            return handle.read()

    return fixture
