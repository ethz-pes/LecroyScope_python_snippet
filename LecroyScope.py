import vxi11
import numpy


class LecroyScope():
    """
    This Python class remote controls the Lecroy WaveSurfer 24MXs over ethernet:
        - connect to the device
        - set up the channels
        - control the trigger
        - download a screenshot
        - download the waveform data

    This class:
        - uses the "VXI-11" ethernet instrument control protocol
        - was tested on "MS Windows" but should run with Linux
        - should also be easy to adapt to other Lecroy scopes
        - was tested with Python 2.7 but should run with Python 3.x

    This class is meant as a lightweight code to be used as a "code snippet" and not as a full package.
	Be careful, the Lecroy instruction are messy and incoherent between the scope models.
    """

    def __init__(self, ip):
        """
        Constructor of the LecroyScope class.
        """

        self.ip = ip
        self.channel_name = ["C1", "C2", "C3", "C4"]

        self.scope = None
        self.time = None
        self.channel = None

    def open(self):
        """
        Make the connection to the device. Reset the device.
        """

        self.scope = vxi11.Instrument(self.ip)
        self.reset_config()

    def close(self):
        """
        Close the connection to the device.
        """

        self.scope = None
        self.time = None
        self.channel = None

    def set_config(self, config):
        """
        Configure the channels, the timebase, and the trigger.
        """

        # save the config
        self.time = config["time"]
        self.channel = config["channel"]
        self.trigger = config["trigger"]

        # reset old config
        self.reset_config()

        # set the timebase and the time offset
        self.scope.write('VBS "app.Acquisition.Horizontal.HorScale = ""%e"' % (self.time["div"]))
        self.scope.write('VBS "app.Acquisition.Horizontal.HorOffsetOrigin = ""%e"' % (self.time["offset_origin"]))
        self.scope.write('VBS "app.Acquisition.Horizontal.HorOffset = ""%e"' % (self.time["offset"]))

        # set the sample storage
        self.scope.write('VBS "app.Acquisition.Horizontal.MaxSamples = ""%e"' % (self.time["sample"]))
        self.scope.write('VBS "app.Acquisition.Horizontal.ReferenceClock = ""INT"')
        self.scope.write('VBS "app.Acquisition.Horizontal.SampleClock = ""INT"')

        # set the channels
        for name_tmp in self.channel:
            # check channel name
            assert name_tmp in self.channel_name, "invalid channel"
            data_tmp = self.channel[name_tmp]

            # view settings
            self.scope.write('VBS "app.Acquisition.%s.View = True' % (name_tmp))
            self.scope.write('VBS "app.Acquisition.%s.InterpolateType = ""Linear"' % (name_tmp))

            # bandwidth limitation
            assert data_tmp["bandwidth"] in ["Full", "20MHz"]
            self.scope.write('VBS "app.Acquisition.%s.BandwidthLimit = ""%s"' % (name_tmp, data_tmp["bandwidth"]))

            # channel coupling type
            assert data_tmp["coupling"] in ["AC1M", "DC1M", "DC50", "Gnd"]
            self.scope.write('VBS "app.Acquisition.%s.Coupling = ""%s"' % (name_tmp, data_tmp["coupling"]))

            # digital bit averaging
            assert data_tmp["filter"] in ["0.5bits", "1.5bits", "1bits", "2.5bits", "2bits", "3bits", "None"]
            self.scope.write('VBS "app.Acquisition.%s.EnhanceResType = ""%s"' % (name_tmp, data_tmp["filter"]))

            # set scale, skew, offset, and invert
            self.scope.write('VBS "app.Acquisition.%s.Invert = %s' % (name_tmp, str(data_tmp["invert"])))
            self.scope.write('VBS "app.Acquisition.%s.Deskew = ""%e"' % (name_tmp, data_tmp["skew"]))
            self.scope.write('VBS "app.Acquisition.%s.ProbeAttenuation = ""%e"' % (name_tmp, data_tmp["attenuation"]))
            self.scope.write('VBS "app.Acquisition.%s.VerScale = ""%e"' % (name_tmp, data_tmp["div"]))
            self.scope.write('VBS "app.Acquisition.%s.VerOffset = ""%e"' % (name_tmp, data_tmp["offset"]))

        # check trigger channel name
        name_tmp = self.trigger["channel"]
        assert name_tmp in self.channel_name, "invalid channel"

        # set trigger source
        self.scope.write('VBS "app.Acquisition.Trigger.Source = ""%s"' % (name_tmp))
        self.scope.write('VBS "app.Acquisition.Trigger.Type = ""edge"')

        # set trigger slope
        assert self.trigger["edge"] in ["Either", "Negative", "Positive", "Window"]
        self.scope.write('VBS "app.Acquisition.Trigger.%s.Slope = ""%s"' % (name_tmp, self.trigger["edge"]))

        # set trigger coupling
        assert self.trigger["coupling"] in ["AC", "DC", "HFREJ", "LFREJ"]
        self.scope.write('VBS "app.Acquisition.Trigger.%s.Coupling = ""%s"' % (name_tmp, self.trigger["coupling"]))

        # set trigger level
        self.scope.write('VBS "app.Acquisition.Trigger.%s.Level = ""%e"' % (name_tmp, self.trigger["level"]))
        self.scope.write('VBS "app.Acquisition.Trigger.%s.WindowSize = ""%e"' % (name_tmp, self.trigger["window"]))

        # force a first trigger event
        self.force()

    def reset_config(self):
        """
        Reset the configuration of the scope, remove the traces.
        """

        self.scope.write("*RST")
        self.scope.write("*CLS")
        self.scope.write("CLSW")
        self.scope.write("COMB AUTO")
        self.scope.write("CRMS OFF")
        self.scope.write("CRS OFF")
        self.scope.write("DISP ON")
        self.scope.write("GRID SINGLE")
        self.scope.write("OFCT VOLTS")
        self.scope.write("PACL")
        self.scope.write("ACAL OFF")
        self.scope.write("CFMT DEF9, WORD, BIN")
        self.scope.write("CHDR SHORT")

        for name_tmp in self.channel_name:
            self.scope.write("%s:TRA OFF" % name_tmp)

        self.force()

    def cal(self):
        """
        Force the auto calibration of the scope.
        """

        self.scope.write("*CAL?")
        msg = self.scope.read()
        if msg != '*CAL 0':
            raise ValueError("invalid cal")

    def buzz(self):
        """
        Activate the buzzer.
        """

        self.scope.write('BUZZ BEEP')

    def single(self):
        """
        Trigger single shot mode.
        """

        self.scope.write("TRMD SINGLE")

    def stop(self):
        """
        Trigger stop.
        """

        self.scope.write("TRMD STOP")

    def normal(self):
        """
        Trigger normal mode.
        """

        self.scope.write("TRMD NORM")

    def force(self):
        """
        Force trigger event.
        """

        self.scope.write("TRMD SINGLE")
        self.scope.write("FRTR")

    def auto(self):
        """
        Automatic trigger mode.
        """

        self.scope.write("TRMD AUTO")

    def get_status(self):
        """
        Get the trigger status.
        """

        self.scope.write("TRMD?")
        trig_status = {'TRMD STOP': "stop", 'TRMD SINGLE': 'single', 'TRMD NORM': 'normal', 'TRMD AUTO': 'auto'}
        msg = self.scope.read()
        if msg not in trig_status:
            raise ValueError("invalid status")
        return trig_status[msg]

    def screenshot(self):
        """
        Take a screenshot, return the PNG binary file content.
        """

        self.scope.write("HCSU DEV, PNG, FORMAT,PORTRAIT, BCKG, WHITE, DEST, REMOTE, PORT, NET, AREA,GRIDAREAONLY")
        self.scope.write("SCDP")
        return self.scope.read_raw()

    def waveform(self, skip):
        """
        Download the waveform data, skip some points if required, return a dict.
        """

        # get the trigger status
        scope_status = self.get_status()

        # init the cata
        data_out = dict()
        data_out["time"] = self.time
        data_out["channel"] = self.channel
        data_out["trigger"] = self.trigger
        data_out["data"] = dict()
        data_out["skip"] = skip

        # only download the data if the scope trigger is not running
        if (scope_status == "stop") and (self.time is not None) and (self.channel is not None):
            # get the text template of the data
            self.scope.write("TMPL?")
            data_out["template"] = self.scope.read()

            # get the data
            data_out["data"] = self._get_waveform_sub(skip)
            data_out["ok"] = True
        else:
            data_out["data"] = None
            data_out["ok"] = False

        # return the data
        return data_out

    def _get_waveform_sub(self, skip):
        """
        Get the waveform, skip some points if specified, scale the data.
        """

        # setup how many points to skip in the data
        self.scope.write("WFSU SP, %i, NP, 0, FP, 0, SN, 0" % skip)

        # for each channel get the data
        data_out = dict()
        for name_tmp in self.channel:
            # init the dict
            data_out_sub = dict()

            # get the header the describe the waveform
            self.scope.write("%s:INSP? 'WAVEDESC'" % name_tmp)
            data_out_sub["header"] = self.scope.read()

            # get the waw data
            self.scope.write('%s:WF?' % name_tmp)
            msg = self.scope.read_raw()
            data_out_sub["msg"] = msg

            # parse and scale the data
            (nb, t, v) = self._extract_bin(msg)
            data_out_sub["nb"] = nb
            data_out_sub["v"] = v
            data_out_sub["t"] = t

            # assign the data
            data_out[name_tmp] = data_out_sub

        # return the data
        return data_out

    def _extract_bin(self, msg):
        """
        Extract and scale the data from the binary format.
        """

        # find the header
        start = msg.find('WAVEDESC')
        msg = msg[start:]

        # extract the number of elements in the binary data
        nb_byte_1 = numpy.fromstring(msg[60:64], dtype=numpy.uint32)
        nb_byte_2 = numpy.fromstring(msg[64:68], dtype=numpy.uint32)
        n_start = numpy.fromstring(msg[124:128], dtype=numpy.uint32)
        n_first = numpy.fromstring(msg[132:136], dtype=numpy.uint32)
        n_end = numpy.fromstring(msg[128:132], dtype=numpy.uint32)
        n_sparse = numpy.fromstring(msg[136:140], dtype=numpy.uint32)

        # check the number of elements
        assert nb_byte_2 == 0, "invalid array"
        assert n_start == 0, "invalid array"
        assert n_first == 0, "invalid array"
        assert (nb_byte_1 % 2) == 0, "invalid array"
        assert (nb_byte_1 / 2) == numpy.floor(n_end / n_sparse) + 1, "invalid array"

        # extract the scaling and offset information
        nb = int(nb_byte_1 / 2)
        v_gain = numpy.fromstring(msg[156:160], dtype=numpy.float32)
        v_offset = numpy.fromstring(msg[160:164], dtype=numpy.float32)
        t_gain = numpy.fromstring(msg[176:180], dtype=numpy.float32)
        t_offset = numpy.fromstring(msg[180:188], dtype=numpy.float64)

        # extract the waveform data, scale, and offset
        v = numpy.fromstring(msg[346:], dtype=numpy.int16, count=nb).astype(numpy.float)
        v *= v_gain
        v -= v_offset

        # extract the time data, scale, and offset
        t = numpy.arange(nb, dtype=numpy.float)
        t *= (t_gain * n_sparse)
        t += t_offset

        # return the data
        return (nb, t, v)
