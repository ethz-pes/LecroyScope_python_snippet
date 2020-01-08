import LecroyScope


if __name__ == "__main__":
    """
    Test code for the LecroyScope class.
    """

    # create the object
    data = dict()
    ip = "xxx.xx.xx.x"
    obj = LecroyScope.LecroyScope(data)

    # connect to the device
    obj.open()

    # configure the scope
    channel = {"C1": dict(), "C2": dict()}
    channel["C1"]["div"] = 1000.0
    channel["C1"]["attenuation"] = 1000.0
    channel["C1"]["offset"] = -2000.0
    channel["C1"]["skew"] = 0.0
    channel["C1"]["invert"] = False
    channel["C1"]["bandwidth"] = "Full"
    channel["C1"]["coupling"] = "DC1M"
    channel["C1"]["filter"] = "None"
    channel["C1"]["comment"] = "V HV OUT"
    channel["C2"]["div"] = 20.0
    channel["C2"]["attenuation"] = 50.0
    channel["C2"]["offset"] = -20.0
    channel["C2"]["skew"] = 0.0
    channel["C2"]["invert"] = False
    channel["C2"]["bandwidth"] = "Full"
    channel["C2"]["coupling"] = "DC1M"
    channel["C2"]["filter"] = "None"
    channel["C2"]["comment"] = "I HV OUT"

    time = dict()
    time["div"] = 100e-9
    time["offset"] = 200e-9
    time["offset_origin"] = 0.0
    time["sample"] = 1e6

    trigger = dict()
    trigger["channel"] = "C2"
    trigger["edge"] = "Positive"
    trigger["coupling"] = "DC"
    trigger["window"] = 0.0
    trigger["level"] = 10.0

    config = {"channel": channel, "time": time, "trigger": trigger}
    obj.set_config(config)

    # force auto calibration
    obj.cal()

    # activate the buzzer
    obj.buzz()

    # trigger single shot mode
    obj.single()

    # trigger stop
    obj.stop()

    # trigger normal mode
    obj.normal()

    # force trigger event
    obj.force()

    # automatic trigger
    obj.auto()

    # automatic trigger mode
    obj.auto()

    # get the trigger status
    trig_status = obj.get_status()

    # take a screeshot (png)
    data_tmp = obj.screenshot()

    # download the waveform data from the scope (dict)
    skip = 10
    data_tmp = obj.waveform(skip)

   # reset the device
    obj.reset_config()

    # disconnect from the device
    obj.close()
