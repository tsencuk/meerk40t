"""
Moshi Device Plugin

Registers the needed classes for ruida device (or would if the ruida device could be controlled).
"""
from meerk40t.ruida.control import RuidaControl
from meerk40t.ruida.device import RuidaDevice
from meerk40t.ruida.emulator import RuidaEmulator
from meerk40t.ruida.loader import RDLoader


def plugin(kernel, lifecycle=None):
    if lifecycle == "plugins":
        from .gui import gui

        return [gui.plugin]
    if lifecycle == "register":
        kernel.register("provider/device/ruida", RuidaDevice)

        _ = kernel.translation
        kernel.register("load/RDLoader", RDLoader)
        kernel.register("emulator/ruida", RuidaEmulator)

        @kernel.console_option(
            "verbose",
            "v",
            type=bool,
            action="store_true",
            help=_("do not watch server channels"),
        )
        @kernel.console_option(
            "quit",
            "q",
            type=bool,
            action="store_true",
            help=_("shutdown current ruidaserver"),
        )
        @kernel.console_command(
            "ruidacontrol",
            help=_("activate the ruidaserver."),
            hidden=True,
        )
        def ruidaserver(
            command, channel, _, verbose=False, quit=False, **kwargs
        ):
            """
            The ruidaserver emulation methods provide a simulation of a ruida device.
            this interprets ruida devices in order to be compatible with software that
            controls that type of device. This would then be sent to the device in a
            somewhat agnostic fashion. Commands like Ruida ACS's pause and stop require
            that the meerk40t device has a "pause" command and stop requires it has an
            "estop". You cannot stop a file output for example. Most of the other commands
            are device-agnostic, including the data sent.

            Laser is optional and only useful for a man-in-the-middle decoding

            ruidacontrol gives the ruida device control over the active device.
            ruidadesign accepts the ruida signals but turns them only into cutcode to be run locally.
            ruidabounce sends data to the ruidaemulator but sends data to the set bounce server.
            """
            root = kernel.root
            ruidacontrol = root.device.lookup("ruidacontrol")
            if ruidacontrol is None:
                if quit:
                    return
                ruidacontrol = RuidaControl(root, channel, _, verbose)
                root.device.register("ruidacontrol", ruidacontrol)
            if quit:
                ruidacontrol.quit()
                root.device.unregister("ruidacontrol")

    if lifecycle == "preboot":
        suffix = "ruida"
        for d in kernel.derivable(suffix):
            kernel.root(f"service device start -p {d} {suffix}\n")
