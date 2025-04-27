# ntnput
The Minimalistic Python library for Windows using wraps of undocumented `Nt` functions to interact with mouse and keyboard stealthy.

# Details
This library uses syscall wraps of undocumented `NtUserInjectMouseInput` and `NtUserInjectKeyboardInput` functions from `win32u.dll` module.
It's makes keyboard and mouse interaction safe and stealth due to the bypass of Windows triggers.</br>

**NtNput** also works faster than analogues because of usage of builtin `ctypes` library allowing to interact directly with C and machine code.
You can use this library if your process blocks usage of `mouse_event`, `SendInput` or etc. WinAPI functions.</br>

## Installation
1. You can install library using pip:
```
pip install ntnput
```
2. You can download this repo, put it's folder into your project and import it using the folder name:

![Local installation example](imgs/local_usage.png)

## Usage
Library provides several functions to interact with mouse:
1. `mouse_move(x, y)` - moves mouse from current position
2. `mouse_move_to(x, y)` - moves mouse to absolute x, y position
3. `mouse_click(button <default "left">)` - clicks mouse
4. `mouse_release(button <default "left">)` - releases mouse
5. `mouse_click_and_release(button <default "left">, delay_ms <default 0.0>)` - clicks mouse, sleeps, releases

And several functions to interact with keyboard:
1. `keyboard_press(key_code)` - presses keyboard button
2. `keyboard_release(key_code)` - releases keyboard button
3. `keyboard_press_and_release(key_code, delay_ms <default 0.0>)` - presses keyboard button, sleeps, releases

You can use official [Microsoft documentation](https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes) to find keyboard key codes definitions.
