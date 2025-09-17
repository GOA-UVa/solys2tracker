# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

[//]: # "## [unreleased] - yyyy-mm-dd"

## [unreleased] - yyyy-mm-dd

### Added
- Solys2 password is now stored in localdata, to avoid having to write it all the time if its not the default one.
- Slightly improve UI/UX with bigger buttons and bigger fonts in some buttons.

### Changed
- Using solys2==v0.2.7
- Using appdata

### Fixed
- BodyWidget was accessing its graph attribute even if no graph had been generated (not using ASD).
- Fixed Adjust and Position configuration actions, where sometimes UI crashed after sending the values to the solys.

## [0.2.2] - 2025-05-22

### Added
- Integration time of Detector 1 can be set to 544ms for crosses too now.
- Cross showing utility improved. Normalised correctly and now with more options.
- Solys Adjust tab can process values higher than 0.2, and it will split and process them internally.

## [0.2.1] - 2022-05-14

### Added
- Added graph when using ASD.
- Graph in a window, trying to improve the graph, more data, and only closes when tracking finishes.
- Graph bugs fixed.

### Fixed
- Track option should capture ASD data if indicated.
- Corrected track gui bug.
- BodyTrackWidget now doesnt get blocked initially when connecting, and the optimization is done pointing to the body.
- Fixed closing of graph window.
- Fixed import bugs.
- Fixed QSS import bugs.
- Wait enough time so the tracker has sent at least the first position

### Changed

- Drift not substracted in track.
- Track printing all vnir-header data to file.
- Using spicedmoon==1.0.1
- Using asdcontroller==0.0.11
- drift substracted
- ASD Output format track changed.
- to npl format before showing it into the graph.
- Optimization made in position correctly.
- Using SPICED...SAFE options from the solys2 package so even if it fails the software doesn't stop.
- Using solys2==0.2.6

## [0.2.0] - 2022-05-08

### Added

- Logfile improved. New file for each process, with UTC datetime in name.
- Cross/Mesh informs the user of next step and number of remaining steps.
- It should work with the ASD.
- Data from the ASD is saved in config tab.
- Cross/Mesh informs about errors.

### Fixed
- Added missing imports
- Save log folder fixed.
- Fixed bug with position widget
- Connection with ASD smoother, doesn't block GUI.
- Fixed bug when showing "MEASURING...", "MEASURE NOW" message.
- Fixed error in asd_acquire callback in Cross/Mesh
- Fixed the asd data printing format.

### Changed

- Model ConnectionStatus refactorized to SessionStatus
- Send Position page in configuration tab.
- Height is set in configuration.
- Using solys v0.2.1a1.
- Removed minimum size, now it's just initial size.
- Changed Set Position Azimuth maximum and minimum.
- Set position input now has the current value initially.
- Adjust step set to 0.01.
- Cross/Mesh now says performed steps instead of remaining steps.
- Current adjustment label rounded to fourth decimal.
- ASD connection is closed after cross.
- Change Cross/Mesh measuring message when using ASD.
- Cross/Mesh ASD Pre-Checked when ASD ip is set.
- Default countdown value depends on if the checkbox is initially checked or not.
- ASD data printing format now followes Fieldspec format for spanish language.
- ASD data printing now prints more data.
- ASD data printing now with tab instead of space.
- Using asdcontroller==0.0.6
- Cross with ASD now tracks body temporarily.
- Change order of instantiating Cross Widget crosser attribute.
- Not sending logger to ConnectASDWorker Tracker, as it would close them when stopping the tracking.
- ConnectASDWorker Tracker has logger that logs only to the logfile.


[unreleased]: https://github.com/javgat/solys2tracker/-/compare/v0.2.2...HEAD
[0.2.2]: https://github.com/javgat/solys2tracker/-/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/javgat/solys2tracker/-/compare/v0.2.0-beta.5...v0.2.1
[0.2.0]: https://gitlab.com/javgat/solys2tracker/-/releases/v0.2.0-beta.5