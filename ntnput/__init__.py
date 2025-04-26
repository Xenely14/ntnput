# +-------------------------------------+
# |         ~ Author : Xenely ~         |
# +=====================================+
# | GitHub: https://github.com/Xenely14 |
# | Discord: xenely                     |
# +-------------------------------------+

import typing
import ctypes
import ctypes.wintypes

# Local imports
from . import misc

# ==-------------------------------------------------------------------== #
# Global and static variables, constants                                  #
# ==-------------------------------------------------------------------== #
LEFT_DOWN = 0x02
LEFT_UP = 0x04
RIGHT_DOWN = 0x10
RIGHT_UP = 0x08

KEY_DOWN = 0x00
KEY_UP = 0x02


# ==-------------------------------------------------------------------== #
# С-structures                                                            #
# ==-------------------------------------------------------------------== #
class InjectInputMouseInfo(ctypes.Structure):
    """Structure containing information about mouse input injection."""

    _fields_ = [
        ("x_direction", ctypes.c_int),
        ("y_direction", ctypes.c_int),
        ("mouse_data", ctypes.c_uint),
        ("mouse_options", ctypes.c_int),
        ("time_offset_in_miliseconds", ctypes.c_uint),
        ("extra_info", ctypes.c_void_p)
    ]


class KeybdInput(ctypes.Structure):
    """Structure containing information about keyboard input injection."""

    _fields_ = [
        ("vk_code", ctypes.c_ushort),
        ("scan_code", ctypes.c_ushort),
        ("dw_flags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("extra_info", ctypes.c_void_p)
    ]


# ==-------------------------------------------------------------------== #
# Wrapped syscall functions                                               #
# ==-------------------------------------------------------------------== #
_NtDelayExecution = misc.syscall("NtDelayExecution", result_type=ctypes.c_ulong, arguments_types=[ctypes.c_int, ctypes.POINTER(ctypes.wintypes.LARGE_INTEGER)], module=b"ntdll.dll")
_NtUserInjectMouseInput = misc.syscall("NtUserInjectMouseInput", result_type=ctypes.c_ulong, arguments_types=[ctypes.POINTER(InjectInputMouseInfo), ctypes.c_int], module=b"win32u.dll")
_NtUserInjectKeyboardInput = misc.syscall("NtUserInjectKeyboardInput", result_type=ctypes.c_ulong, arguments_types=[ctypes.POINTER(KeybdInput), ctypes.c_int], module=b"win32u.dll")


# ==-------------------------------------------------------------------== #
# Functions                                                               #
# ==-------------------------------------------------------------------== #
def mouse_move(x: int, y: int) -> None:
    """Moves mouse relative to it's current position using wrapped syscall `NtUserInjectMouseInput` function."""

    # Moving mouse
    _NtUserInjectMouseInput(ctypes.byref(InjectInputMouseInfo(x_direction=x, y_direction=-y)), 1)


def mouse_move_to(x: int, y: int) -> None:
    """Moves mouse by absolute coorinate position using wrapped syscall `NtUserInjectMouseInput` function."""

    # Enable process DPI awareness to retrieve `indeed` screen resolution
    ctypes.windll.user32.SetProcessDPIAware()

    # Retrieving screen resolutions
    screen_width = ctypes.windll.user32.GetSystemMetrics(0)
    screen_height = ctypes.windll.user32.GetSystemMetrics(1)

    # Normalizing coordinates
    normalized_x = int((x / screen_width) * 65535)
    normalized_y = int((y / screen_height) * 65535)

    # Moving mouse
    _NtUserInjectMouseInput(ctypes.byref(InjectInputMouseInfo(x_direction=normalized_x, y_direction=normalized_y, mouse_options=0x8000)), 1)


def mouse_click(button: typing.Literal["left", "right"] = "left") -> None:
    """Clicks mouse using wrapped syscall `NtUserInjectMouseInput` function."""

    # If button literal is not allowed
    if button not in (allowed_literals := typing.get_args(mouse_click.__annotations__["button"])):
        raise Exception("Button literal is invalid, expected one of: `%s`" % ", ".join(allowed_literals))

    # Clicking mouse
    match button:

        case "left": _NtUserInjectMouseInput(ctypes.byref(InjectInputMouseInfo(mouse_options=LEFT_DOWN)), 1)
        case "right": _NtUserInjectMouseInput(ctypes.byref(InjectInputMouseInfo(mouse_options=RIGHT_DOWN)), 1)


def mouse_release(button: typing.Literal["left", "right"] = "left") -> None:
    """Releases mouse using wrapped syscall `NtUserInjectMouseInput` function."""

    # If button literal is not allowed
    if button not in (allowed_literals := typing.get_args(mouse_click.__annotations__["button"])):
        raise Exception("Button literal is invalid, expected one of: `%s`" % ", ".join(allowed_literals))

    # Releasing mouse
    match button:

        case "left": _NtUserInjectMouseInput(ctypes.byref(InjectInputMouseInfo(mouse_options=LEFT_UP)), 1)
        case "right": _NtUserInjectMouseInput(ctypes.byref(InjectInputMouseInfo(mouse_options=RIGHT_UP)), 1)


def mouse_click_and_release(button: typing.Literal["left", "right"] = "left", delay_ms: float = 0.0) -> None:
    """Clicks mouse and releases after given delay time passed in milliseconds using wrapped syscall `NtUserInjectMouseInput` function."""

    # If button literal is not allowed
    if button not in (allowed_literals := typing.get_args(mouse_click.__annotations__["button"])):
        raise Exception("Button literal is invalid, expected one of: `%s`" % ", ".join(allowed_literals))

    # Clicking and releasing mouse
    mouse_click(button), _NtDelayExecution(1, ctypes.byref(ctypes.wintypes.LARGE_INTEGER(int(-abs(delay_ms) * 10_000)))), mouse_release(button)


def keyboard_press(key_code: int) -> None:
    """Presses keyboard key using wrapped syscall `NtUserInjectKeyboardInput` function."""

    # Pressing keyboard key
    _NtUserInjectKeyboardInput(ctypes.byref(KeybdInput(vk_code=key_code, dw_flags=KEY_DOWN)), 1)


def keyboard_release(key_code: int) -> None:
    """Releases keyboard key using wrapped syscall `NtUserInjectKeyboardInput` function."""

    # Pressing keyboard key
    _NtUserInjectKeyboardInput(ctypes.byref(KeybdInput(vk_code=key_code, dw_flags=KEY_UP)), 1)


def keyboard_press_and_release(key_code: int, delay_ms: float = 0.0) -> None:
    """Presses keyboard key and releases after given delay time passed in milliseconds using wrapped syscall `NtUserInjectKeyboardInput` function."""

    # Clicking and releasing keyboard key
    keyboard_press(key_code), _NtDelayExecution(1, ctypes.byref(ctypes.wintypes.LARGE_INTEGER(int(-abs(delay_ms) * 10_000)))), keyboard_release(key_code)
