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
# 

import numpy as np
import math
from gnuradio import gr

class sp_threshold(gr.sync_block):
    """
    docstring for block sp_threshold
    """
    def __init__(self):
        gr.sync_block.__init__(self,
            name="sp_threshold",
            in_sig=[np.float32],
            out_sig=[np.float32])


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        range1 = in0 <= math.cos(7*math.pi/8)
        range2 = np.logical_and(in0 > math.cos(7*math.pi/8), in0 <= math.cos(5*math.pi/8))
        range3 = np.logical_and(in0 > math.cos(5*math.pi/8), in0 <= math.cos(3*math.pi/8))
        range4 = np.logical_and(in0 > math.cos(3*math.pi/8), in0 <= math.cos(math.pi/8))
        range5 = in0 > math.cos(math.pi/8)
        out[range1] = -1
        out[range2] = -1/(2**0.5)
        out[range3] = 0
        out[range4] = 1/(2**0.5)
        out[range5] = 1
        return len(output_items[0])

