import nox


@nox.session
def black(session):
    session.install("-r", "requirements-dev.txt")
    session.run("black", ".")


@nox.session
def mypy(session):
    session.install("-r", "requirements-dev.txt")
    session.run("mypy", "routes_api_service")


@nox.session
def unit_tests(session):
    session.install("-r", "requirements.txt")
    session.install("-r", "requirements-dev.txt")
    session.run("pytest", "tests/unit")


@nox.session
def integration_tests(session):
    session.install("-r", "requirements.txt")
    session.install("-r", "requirements-dev.txt")
    session.run("pytest", "tests/integration_tests")


@nox.session
def perf_test(session):
    session.install("-r", "requirements.txt")
    session.install("-r", "requirements-dev.txt")
    session.install(".")  # for some reason python can't find the project
    session.run("python", "tests/perf_test/perf_test.py")
