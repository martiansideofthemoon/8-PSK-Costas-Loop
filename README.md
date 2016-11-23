# 8 PSK Costas Loop

This is a python implementation of an 8-PSK Costas Loop made as on [OOT Module](https://gnuradio.org/redmine/projects/gnuradio/wiki/OutOfTreeModules) for [GNURadio](https://github.com/gnuradio/gnuradio). It can work as a standalone python script as well.

The project builds two GNURadio blocks, an 8-PSK threshold block to carry out phase detection along with a complete working Costas Loop (which uses the threshold code).

## Installation Instructions

* Make sure you have `cmake`, `numpy` and `gnuradio` installed.
* Clone the repository, `git clone https://github.com/martiansideofthemoon/8-PSK-Costas-Loop`.
* `cd 8-PSK-Costas-Loop/build`
* Once inside the build folder, run `cmake ../`. This should generate a Makefile in your `build` directory.
* In the same folder, run `make`.
* In the same folder, run `sudo make install`
* Run `gnuradio-companion`. If the block doesn't show up / doesn't work (this is likely), move to the next section.

## Troubleshooting

* **Block doesn't show up in GRC** - By default, `sudo make install` might have placed `costas8_sp_threshold.xml` and `costas8_costas_loop.xml` in the wrong folder. You can correct it in this way -
  * `sudo cp /usr/local/share/gnuradio/grc/blocks/costas8_costas_loop.xml /usr/share/gnuradio/grc/blocks/`
  * `sudo cp /usr/local/share/gnuradio/grc/blocks/costas8_sp_threshold.xml /usr/share/gnuradio/grc/blocks/`
