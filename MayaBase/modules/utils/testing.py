"""
Author:SuoLin Zhang
Created:2023
About: Testing tools to automate the testing of our code from within Maya.
"""

import MayaBase.modules

import os

import unittest


def discoverAndRun(start_dir, pattern='test_*.py'):
    """Discover and run the test cases, returning the results."""
    loader = unittest.TestLoader()
    tests = loader.discover(start_dir, pattern=pattern)
    # Use the standard text runner which prints to stdout
    runner = unittest.TextTestRunner()
    # Returns a TestResult
    result = runner.run(tests)
    return result


def getTestOutput(module, pattern='test_*.py'):
    result = discoverAndRun(os.path.dirname(module.__file__), pattern)
    print("\n>>> result.testsRun: \t%s" % (result.testsRun))
    print(">>> result.passes: \t\t%s" % (result.testsRun - len(result.errors)))
    print(">>> result.errors: \t\t%s" % (len(result.errors)))
    print(">>> result.failures: \t%s" % (len(result.failures)))
    print(">>> result.skipped: \t%s" % (len(result.skipped)))


def testAllModules():
    getTestOutput(MayaBase.modules)
