#!/bin/env python


class TypeMissingFromConfiguration(Exception):
    def __init__(self, message: str):
        self.message = message


class UnsupportedConfigurationFileType(Exception):
    def __init__(self, message: str):
        self.message = message


class RequiredKeyMissingFromConfiguration(Exception):
    def __init__(self, message: str):
        self.message = message
