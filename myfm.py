#~/usr/bin/env python

from gnuradio import gr,eng_notation
from gnuradio import audio
from gnuradio import usrp
from gnuradio import blks
from gnuradio.eng_option import eng_option
from optparse import OptionParser
import sys
import math

from gnuradio.wxgui import stdgui,fftsink
import wx
class wfm_rx_graph(stdgui.gui_flow_graph):
    def__init__(self,frame,panel,vbox,argv):
        stdgui.gui_flow_graph.__init__(self,frame,panel,vbox,argv)

        IF_freq=parseargs(argv[1:])
        adc_rate=64e6

        decim=250
        quad_rate=adc_rate/decim
        audo_decimation=9
        audio_rate=quad_rate/audio_decimation

        src=usrp.source_c(0,decim)
        src.set_rx_freq(0,IF_freq)
        src.set_pga(0,20)

        guts=blks.wfm_rcv(self,quad_rate,audio_decimation)

        audio_sink=audio.sink(int(audio_rate))

        self.connect(src,guts)
        self.connect(guts,(audio_sink,0))

        if 1:
            pre_demod,fft_win1=\
                    fftsink.make_fft_sink_c(self,panel,"Pre-Demodulation",
                            512,quad_rate)
                    self.connect(src,pre_demod)
                    vbox.Add(fft_win1,1,wx.EXPAND)
        if 1:
            post_deemph,fft_win3=\
                    fftsink.make_fft_sink_f(self,panel,"With Deemph",512,quad_rate,-60,20)
                    self.connect(gut.deemph,post_deemph)
                    vbox.Add(fft_win3,1,wx.EXPAND)

        if 1:
            post_filt,fft_win4=\
                    fftsink.make_fft_sink_f(self,panel,"PostFilter",512,audio_rate,-60,20)
                    self.connect(gnuts.audio_filter,post_filt)
                    vbox.Add(fft_win4,1,wx.EXPAND)


