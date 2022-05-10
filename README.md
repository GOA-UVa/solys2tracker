# solys2tracker

![Version 0.2.1-alpha.7](https://img.shields.io/badge/version-0.2.1--alpha.7-informational)

Desktop app for automating the Solys2 letting it track the Moon and the Sun.

## Notice of Non-Affiliation and Disclaimer

We are not affiliated, associated, authorized, endorsed by, or in any way officially
connected with the SOLYS2 or with Kipp & Zonen, or any of its subsidiaries, or its
affiliates.

The official Kipp & Zonen website can be found at [kippzonen.com](https://kippzonen.com).

The names SOLYS2 and Kipp & Zonen as well as related names, marks, emblems and images are
registered trademarks of their respective owners.

## Features

### Tracking

One of the main features is the tracking of a body, wether it is the Sun or the Moon.

In order to do that one must go to the selected body tab (Sun or Moon), and press the Track
button.

Then we have to input some parameters:
- Time interval (secs): Periodicity at which the software will update the Solys2 position.
- Height (m): Height of the observer. Used only in case that SPICE is being used. It won't make
a difference unless the height is very large, so if the observer is on Earht's surface, setting it
to 0 is a valid option.

### Cross

The Solys2 will perform a cross.

It's an option in both body tabs.

The input parameters are the following:
- Range (decimal degrees): Range of offsets that the Cross will be performed at.
- Step (decimal degrees): The cross will be performed going step by step inside the range of
values. First azimuth and then zenith.
- Countdown (secs): Number of seconds that the countdown will contain. The countdown will
let the user know when is the Solys2 at the exact position.
- Rest (secs): Rest time so that the user can have more time between positions.

### Mesh

The Solys2 will perform a Mesh.

It's like the cross but with all the positions of the matrix.

### Black

The Solys2 will go to a position where the body is not present. Only available for the Moon.

## Configuration

### Connection

Changes the connection parameters for the Solys2.

- IP: Solys2 IP.
- Port: Solys2 connection port.
- Password: Solys2 user password.

### SPICE

Configures the SPICE kernels directory, so the software can use SPICE.

#### Kernels

In order to use the SPICE libraries, a directory with all the kernels must be specified.

That directory must contain the following kernels:
- [https://naif.jpl.nasa.gov/pub/naif/JUNO/kernels/spk/de421.bsp](https://naif.jpl.nasa.gov/pub/naif/JUNO/kernels/spk/de421.bsp)
- [https://naif.jpl.nasa.gov/pub/naif/pds/wgc/kernels/pck/earth_070425_370426_predict.bpc](https://naif.jpl.nasa.gov/pub/naif/pds/wgc/kernels/pck/earth_070425_370426_predict.bpc)
- [https://naif.jpl.nasa.gov/pub/naif/generic_kernels/fk/planets/earth_assoc_itrf93.tf](https://naif.jpl.nasa.gov/pub/naif/generic_kernels/fk/planets/earth_assoc_itrf93.tf)
- [https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_latest_high_prec.bpc](https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_latest_high_prec.bpc)
- [https://naif.jpl.nasa.gov/pub/naif/generic_kernels/fk/satellites/moon_080317.tf](https://naif.jpl.nasa.gov/pub/naif/generic_kernels/fk/satellites/moon_080317.tf)
- [https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/moon_pa_de421_1900-2050.bpc](https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/moon_pa_de421_1900-2050.bpc)
- [https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/naif0011.tls](https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/naif0011.tls)
- [https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/pck00010.tpc](https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/pck00010.tpc)

### Log

Selects the logging directory. Otherwise it will use the original directory.

### Adjust

Adjust the Solys2 position.
