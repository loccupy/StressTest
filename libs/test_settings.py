from gurux_serial import GXSerial
from gurux_net import GXNet
from libs.GXSettings import GXSettings
from libs.GXDLMSReader import GXDLMSReader


def initialization(com, address, baud, password, ip):
    # args: the command line arguments
    settings = GXSettings()

    # Serial connection if ip is not specified
    if ip is None:
        settings.getParameters("COM", com, password=password, authentication="High", serverAddress=address,
                               logicalAddress=1, clientAddress=48, baudRate=baud)
    # For TCP connection
    else:
        ip = ip.split(':')
        if len(ip) == 1:
            ip.append('6603')

        settings.getParameters(ip[0], ip[1], password=password,
                               authentication="High", serverAddress=address, logicalAddress=1, clientAddress=48,
                               baudRate=baud)

    if not isinstance(settings.media, (GXSerial, GXNet)):
        raise Exception("Unknown media type.")

    reader = GXDLMSReader(settings.client, settings.media, settings.trace, settings.invocationCounter)

    return reader, settings
