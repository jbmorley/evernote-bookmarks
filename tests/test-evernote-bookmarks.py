#!/usr/bin/env python

import os
import os.path
import shutil
import subprocess
import tempfile
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_DIR = os.path.join(ROOT_DIR, "tests")
RESOURCES_DIR = os.path.join(TESTS_DIR, "resources")

EVERNOTE_BOOKMARKS_PATH = os.path.join(ROOT_DIR, "evernote-bookmarks")


class TempDir(object):

    def __enter__(self):
        self.path = tempfile.mkdtemp()
        self.previous = os.getcwd()
        os.chdir(self.path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.previous)
        shutil.rmtree(self.path)


class TestEvernoteBookmarks(unittest.TestCase):

    def _assert_files_equal(self, path_a, path_b):
        with open(path_a, 'r') as a, open(path_b, 'r') as b:
            self.assertEqual(a.read(), b.read())

    def _run_evernote_bookmarks_and_assert_results_expected(self, identifier):
        with TempDir():
            subprocess.check_call([EVERNOTE_BOOKMARKS_PATH,
                                   os.path.join(RESOURCES_DIR, "%s.xml" % (identifier, )),
                                   "bookmarks.html"])
            self._assert_files_equal("bookmarks.html",
                                     os.path.join(RESOURCES_DIR, "%s.html" % (identifier, )))

    def test_well_formed_note(self):
        self._run_evernote_bookmarks_and_assert_results_expected("well_formed_note")

    def test_missing_source_url_a_href(self):
        self._run_evernote_bookmarks_and_assert_results_expected("missing_source_url_a_href")

    def test_missing_source_url_a_no_href(self):
        self._run_evernote_bookmarks_and_assert_results_expected("missing_source_url_a_no_href")


if __name__ == '__main__':
    unittest.main()
