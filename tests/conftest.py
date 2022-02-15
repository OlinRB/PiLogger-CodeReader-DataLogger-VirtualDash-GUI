def pytest_addoption(parser):
    parser.addoption("--port", action="store", help="device file for doing end-to-end testing")
