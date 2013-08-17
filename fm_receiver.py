#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Lesson 3 - FM Rx
# Author: John Malsbury - Ettus Research
# Description: Working with the USRP!
# Generated: Sat Aug 17 10:51:11 2013
##################################################

from gnuradio import audio
from gnuradio import blks2
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio import window
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import wx

class fm_receiver(grc_wxgui.top_block_gui):

	def __init__(self):
		grc_wxgui.top_block_gui.__init__(self, title="Example bitcpf - FM Rx")
		_icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
		self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

		##################################################
		# Variables
		##################################################
		self.samp_rate = samp_rate = 8e6
		self.rx_gain = rx_gain = 15
		self.lpf_decim = lpf_decim = 20
		self.freq = freq = 106.7e6
		self.audio_samp_rate = audio_samp_rate = 96e3

		##################################################
		# Blocks
		##################################################
		_rx_gain_sizer = wx.BoxSizer(wx.VERTICAL)
		self._rx_gain_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_rx_gain_sizer,
			value=self.rx_gain,
			callback=self.set_rx_gain,
			label='rx_gain',
			converter=forms.float_converter(),
			proportion=0,
		)
		self._rx_gain_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_rx_gain_sizer,
			value=self.rx_gain,
			callback=self.set_rx_gain,
			minimum=0,
			maximum=30,
			num_steps=100,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.Add(_rx_gain_sizer)
		self.notebook_0 = self.notebook_0 = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
		self.notebook_0.AddPage(grc_wxgui.Panel(self.notebook_0), "RF")
		self.notebook_0.AddPage(grc_wxgui.Panel(self.notebook_0), "Audio")
		self.Add(self.notebook_0)
		self._freq_text_box = forms.text_box(
			parent=self.GetWin(),
			value=self.freq,
			callback=self.set_freq,
			label='freq',
			converter=forms.float_converter(),
		)
		self.Add(self._freq_text_box)
		self.wxgui_fftsink2_1 = fftsink2.fft_sink_f(
			self.notebook_0.GetPage(1).GetWin(),
			baseband_freq=0,
			y_per_div=10,
			y_divs=10,
			ref_level=0,
			ref_scale=2.0,
			sample_rate=samp_rate/lpf_decim,
			fft_size=1024,
			fft_rate=15,
			average=False,
			avg_alpha=None,
			title="FFT Plot",
			peak_hold=False,
		)
		self.notebook_0.GetPage(1).Add(self.wxgui_fftsink2_1.win)
		self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
			self.notebook_0.GetPage(0).GetWin(),
			baseband_freq=freq,
			y_per_div=10,
			y_divs=10,
			ref_level=0,
			ref_scale=2.0,
			sample_rate=samp_rate,
			fft_size=1024,
			fft_rate=15,
			average=False,
			avg_alpha=None,
			title="FFT Plot",
			peak_hold=False,
		)
		self.notebook_0.GetPage(0).Add(self.wxgui_fftsink2_0.win)
		self.uhd_usrp_source_0 = uhd.usrp_source(
			device_addr="",
			stream_args=uhd.stream_args(
				cpu_format="fc32",
				channels=range(1),
			),
		)
		self.uhd_usrp_source_0.set_samp_rate(samp_rate)
		self.uhd_usrp_source_0.set_center_freq(freq, 0)
		self.uhd_usrp_source_0.set_gain(rx_gain, 0)
		self.uhd_usrp_source_0.set_antenna("TX/RX", 0)
		self.low_pass_filter_0 = gr.fir_filter_ccf(lpf_decim, firdes.low_pass(
			1, samp_rate, 100e3, 10e3, firdes.WIN_HAMMING, 6.76))
		self.gr_wavfile_sink_0 = gr.wavfile_sink("fm_record.wav", 1, int(audio_samp_rate), 8)
		self.blks2_wfm_rcv_0 = blks2.wfm_rcv(
			quad_rate=samp_rate/lpf_decim,
			audio_decimation=1,
		)
		self.blks2_rational_resampler_xxx_0 = blks2.rational_resampler_fff(
			interpolation=96,
			decimation=int(samp_rate/lpf_decim/1000),
			taps=None,
			fractional_bw=None,
		)
		self.audio_sink_0 = audio.sink(int(audio_samp_rate), "", True)

		##################################################
		# Connections
		##################################################
		self.connect((self.low_pass_filter_0, 0), (self.blks2_wfm_rcv_0, 0))
		self.connect((self.blks2_wfm_rcv_0, 0), (self.blks2_rational_resampler_xxx_0, 0))
		self.connect((self.blks2_rational_resampler_xxx_0, 0), (self.gr_wavfile_sink_0, 0))
		self.connect((self.blks2_rational_resampler_xxx_0, 0), (self.audio_sink_0, 0))
		self.connect((self.blks2_wfm_rcv_0, 0), (self.wxgui_fftsink2_1, 0))
		self.connect((self.uhd_usrp_source_0, 0), (self.low_pass_filter_0, 0))
		self.connect((self.uhd_usrp_source_0, 0), (self.wxgui_fftsink2_0, 0))


	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
		self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
		self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 100e3, 10e3, firdes.WIN_HAMMING, 6.76))
		self.wxgui_fftsink2_1.set_sample_rate(self.samp_rate/self.lpf_decim)

	def get_rx_gain(self):
		return self.rx_gain

	def set_rx_gain(self, rx_gain):
		self.rx_gain = rx_gain
		self.uhd_usrp_source_0.set_gain(self.rx_gain, 0)
		self._rx_gain_slider.set_value(self.rx_gain)
		self._rx_gain_text_box.set_value(self.rx_gain)

	def get_lpf_decim(self):
		return self.lpf_decim

	def set_lpf_decim(self, lpf_decim):
		self.lpf_decim = lpf_decim
		self.wxgui_fftsink2_1.set_sample_rate(self.samp_rate/self.lpf_decim)

	def get_freq(self):
		return self.freq

	def set_freq(self, freq):
		self.freq = freq
		self.wxgui_fftsink2_0.set_baseband_freq(self.freq)
		self.uhd_usrp_source_0.set_center_freq(self.freq, 0)
		self._freq_text_box.set_value(self.freq)

	def get_audio_samp_rate(self):
		return self.audio_samp_rate

	def set_audio_samp_rate(self, audio_samp_rate):
		self.audio_samp_rate = audio_samp_rate

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	tb = fm_receiver()
	tb.Run(True)

