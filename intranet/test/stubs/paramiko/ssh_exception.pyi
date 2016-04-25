# Stubs for paramiko.ssh_exception (Python 3.5)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any
import socket

class SSHException(Exception): ...
class AuthenticationException(SSHException): ...
class PasswordRequiredException(AuthenticationException): ...

class BadAuthenticationType(AuthenticationException):
    allowed_types = ... # type: Any
    args = ... # type: Any
    def __init__(self, explanation, types): ...

class PartialAuthentication(AuthenticationException):
    allowed_types = ... # type: Any
    args = ... # type: Any
    def __init__(self, types): ...

class ChannelException(SSHException):
    code = ... # type: Any
    args = ... # type: Any
    def __init__(self, code, text): ...

class BadHostKeyException(SSHException):
    hostname = ... # type: Any
    key = ... # type: Any
    expected_key = ... # type: Any
    args = ... # type: Any
    def __init__(self, hostname, got_key, expected_key): ...

class ProxyCommandFailure(SSHException):
    error = ... # type: Any
    args = ... # type: Any
    def __init__(self, command, error): ...

class NoValidConnectionsError(socket.error):
    errors = ... # type: Any
    def __init__(self, errors): ...