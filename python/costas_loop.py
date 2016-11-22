#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2016 <+YOU OR YOUR COMPANY+>.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# -

import numpy as np
import time
import math
from gnuradio import gr
import costas8
from gnuradio import blocks
from gnuradio import filter

class costas_loop(gr.sync_block):
  """
  docstring for block costas_loop
  """
  def __init__(self, samp_rate, iter):
    gr.sync_block.__init__(self,
      name="costas_loop",
      in_sig=[np.complex64],
      out_sig=[np.complex64])
    self.samp_rate = samp_rate;
    self.iter = iter;
    self.call = 0
    self.samples = 0
    self.start_time = time.time()

    self.costas8_sp_threshold_1 = costas8.sp_threshold()
    self.costas8_sp_threshold_0 = costas8.sp_threshold()
    self.k_factor = -5/samp_rate
    self.prev_in_iir = 0
    self.prev_out_iir = 0
    self.prev_in_vco = 0
    self.feedback = 0

  def work(self, input_items, output_items):
    in0 = input_items[0]
    out = output_items[0]
    self.call += 1
    self.samples += in0.shape[0]
    for i in range(0, in0.shape[0]):
      # Output of costas loop
      on_first_mul = in0[i]*self.feedback
      out[i] = on_first_mul
      real = on_first_mul.real
      imag = on_first_mul.imag
      # Using threshold block
      a = self.costas8_sp_threshold_0.execute(imag)
      b = self.costas8_sp_threshold_1.execute(real)
      # IIR Filter
      in_iir = np.arcsin(imag*b - real*a)
      out_iir = 1.0001*in_iir - self.prev_in_iir + self.prev_out_iir
      self.prev_in_iir = in_iir
      self.prev_out_iir = out_iir
      # VCO Block
      in_vco = out_iir + self.prev_in_vco
      self.prev_in_vco = in_vco
      real_part = np.cos(self.k_factor*in_vco)
      imag_part = np.sin(self.k_factor*in_vco)
      out_vco = real_part + 1j*imag_part
      self.feedback = out_vco
    print self.samples
    return len(output_items[0])
