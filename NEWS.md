# NEWS

## 0.2.0

- Logfile improved. New file for each process, with UTC datetime in name.
- Model ConnectionStatus refactorized to SessionStatus
- Send Position page in configuration tab.
- Height is set in configuration.
- Using solys v0.2.1a1.
- Cross/Mesh informs the user of next step and number of remaining steps.
- Removed minimum size, now it's just initial size.
- Added missing imports
- Changed Set Position Azimuth maximum and minimum.
- Set position input now has the current value initially.
- Save log folder fixed.
- Fixed bug with position widget
- Adjust step set to 0.01.
- Cross/Mesh now says performed steps instead of remaining steps.
- Current adjustment label rounded to fourth decimal.
- Data from the ASD is saved in config tab.
- It should work with the ASD.
- Connection with ASD smoother, doesn't block GUI.
- Cross/Mesh informs about errors.
- ASD connection is closed after cross.
- Change Cross/Mesh measuring message when using ASD.
- Cross/Mesh ASD Pre-Checked when ASD ip is set.
- Using asdcontroller==0.0.3
- Default countdown value depends on if the checkbox is initially checked or not.
- Fixed bug when showing "MEASURING...", "MEASURE NOW" message.
- Fixed error in asd_acquire callback in Cross/Mesh
- Fixed the asd data printing format.
- ASD data printing format now followes Fieldspec format for spanish language.
- ASD data printing now prints more data.
- ASD data printing now with tab instead of space.
- Using asdcontroller==0.0.5
- Using asdcontroller==0.0.6
- Cross with ASD now tracks body temporarily.
- Change order of instantiating Cross Widget crosser attribute.
- Not sending logger to ConnectASDWorker Tracker, as it would close them when stopping the tracking.
- ConnectASDWorker Tracker has logger that logs only to the logfile.

## 0.2.1
- Using asdcontroller==0.0.10
- Using solys2==0.2.2
- Track option should capture ASD data if indicated.
- Corrected track gui bug.
- BodyTrackWidget now doesnt get blocked initially when connecting, and the optimization is done pointing to the body.
- Added graph when using ASD.
- Graph in a window, trying to improve the graph, more data, and only closes when tracking finishes.
- Graph bugs fixed.
- Drift not substracted in track.
- Track printing all vnir-header data to file.
- Using solys2==0.2.3
- Using spicedmoon==1.0.1
- Using asdcontroller==0.0.11
- drift substracted
- ASD Output format track changed.
- Fixed closing of graph window.
- to npl format before showing it into the graph.
- Fixed import bugs.
- Fixed QSS import bugs.
- Optimization made in position correctly.
- Using solys2==0.2.4
- Using SPICED...SAFE options from the solys2 package so even if it fails the software doesn't stop.
- Using solys2==0.2.5
- Using solys2==0.2.6
- Wait enough time so the tracker has sent at least the first position

## News
