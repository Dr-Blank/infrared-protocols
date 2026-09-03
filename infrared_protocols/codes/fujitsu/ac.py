"""Fixed-code button codes for Fujitsu General air conditioners.

Each value is the message type byte of a 7-byte util message the remote emits
verbatim, unlike the state frames built by ``FujitsuAcCommand``. The signature and the
checksum are the same for every one, so they are not stored here;
``FujitsuAcFixedCommand`` adds them. A full message is ``14 63 00 10 10`` + the type
byte + its one's complement, e.g. economy ``0x09`` is transmitted as
``14 63 00 10 10 09 F6``.

The air conditioner keeps the state for all of these. A remote sends the same bytes
every time and nothing in the message says what the result was, so these are one-shot
actions rather than settings that can be read back.
"""

from enum import IntEnum

from ...commands import Command
from ...commands.fujitsu_ac import FujitsuAcFixedCommand


class FujitsuAcButton(IntEnum):
    """Fujitsu General AC fixed-code button; value is the message type byte."""

    POWER_OFF = 0x02
    """Stop the unit. The only way to turn it off, as a state frame cannot."""

    TEST_RUN = 0x03
    """Installer test run, which forces the unit to run regardless of the room
    temperature. Meant for commissioning and not for normal use."""

    ECONOMY = 0x09
    """Toggle economy mode, which caps the unit's power draw."""

    POWERFUL = 0x39
    """Toggle the powerful, or turbo, boost."""

    # The remote's WLAN button steps a menu on its own display, one level per press.
    # L1 enables or disables the adapter and L2 starts a connection by one of two
    # methods. Fujitsu General's documentation gives the button sequences but never
    # says which connection method is which, so these are named after what the remote
    # displays rather than after WPS or access-point mode. L3 exists as well, for
    # initializing the adapter, but has not been captured.
    WLAN_ENABLE = 0x52
    """L1 "on": enable the wireless LAN adapter."""

    WLAN_DISABLE = 0x53
    """L1 "oF": disable the wireless LAN adapter."""

    WLAN_CONNECT_METHOD_1 = 0x54
    """L2 "1n": start a connection using the adapter's first method."""

    WLAN_CONNECT_METHOD_2 = 0x55
    """L2 "2n": start a connection using the adapter's second method."""

    STEP_VERTICAL_LOUVRE = 0x6C
    """Move the vertical louvre to its next position. The unit holds the position, so
    the remote only ever says "next"."""

    STEP_HORIZONTAL_LOUVRE = 0x79
    """Move the horizontal louvre to its next position."""

    def to_command(self) -> Command:
        """Build a Fujitsu General AC fixed-code command for this button."""
        return FujitsuAcFixedCommand(command=self.value)
