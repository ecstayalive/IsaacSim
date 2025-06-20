# Changelog
## [3.0.7] - 2025-05-19
### Changed
- Update copyright and license to apache v2.0

## [3.0.6] - 2025-05-16
### Changed
- Make extension target a specific kit version

## [3.0.5] - 2025-04-04
### Changed
- Version bump to fix extension publishing issues

## [3.0.4] - 2025-03-26
### Changed
- Cleanup and standardize extension.toml, update code formatting for all code

## [3.0.3] - 2025-03-25
### Changed
- Add import tests for deprecated extensions

## [3.0.2] - 2025-01-21
### Changed
- Update extension description and add extension specific test settings

## [3.0.1] - 2024-10-24
### Changed
- Updated dependencies and imports after renaming

## [3.0.0] - 2024-10-04
### Deprecated
- Extension deprecated since Isaac Sim 4.5.0. The built in optimization controller will be removed. The RL based controller will be replaced by "isaacsim.robot.policy"

## [2.0.1] - 2024-08-28
### Fixed
- Spot unit test

## [2.0.0] - 2024-08-01
### Added
- RL policy based robot simulation for anymal and spot quadruped

## [1.4.5] - 2024-04-30
### Changed
- Updated unitree folder structure and opt to use unitree models with sensors attached

## [1.4.4] - 2024-03-07
### Changed
- Removed the usage of the deprecated dynamic_control extension

## [1.4.3] - 2024-02-12
### Changed
- Removed IMU sensor from unitree.py (since the controller uses ground truth data)
- Reduced the frequency of osqp solver from every physics step to every 5 physics steps
- Contact sensor now uses the interface instead directly of the python wrapper

## [1.4.2] - 2024-02-02
### Changed
- Updated path to the nucleus extension

## [1.4.1] - 2023-12-11
### Fixed
- Add the missing import statement for the IMUSensor

## [1.4.0] - 2023-12-06
### Changed
- Added torque clamp to the quadruped control in response to physics change
- Behavior changed, investigating performance issue

## [1.3.2] - 2023-08-22
### Fixed
- Fixed robot articulation bug after stop or reset

## [1.3.1] - 2023-06-07
### Changed
- Eliminated dependency on "bezier" python package. Behavior is unchanged.

## [1.3.0] - 2023-02-01
### Removed
- Removed Quadruped class
- Removed dynamic control extension dependency
- Used omni.isaac.sensor classes for Contact and IMU sensors

## [1.2.2] - 2022-12-10
### Fixed
- Updated camera pipeline with writers

## [1.2.1] - 2022-11-03
### Fixed
- Incorrect viewport name issue
- Viewports not docking correctly

## [1.2.0] - 2022-08-30
### Changed
- Remove direct legacy viewport calls

## [1.1.2] - 2022-05-19
### Changed
- Updated unitree vision class to use OG ROS nodes
- Updated ROS1/ROS2 quadruped standalone samples to use OG ROS nodes

## [1.1.1] - 2022-05-15
### Fixed
- DC joint order change related fixes.

## [1.1.0] - 2022-05-05
### Added
- added the ANYmal robot

## [1.0.2] - 2022-04-21
### Changed
- decoupled sensor testing from A1 and Go1 unit test
- fixed contact sensor bug in example and standalone

## [1.0.1] - 2022-04-20
### Changed
- Replaced find_nucleus_server() with get_assets_root_path()

## [1.0.0] - 2022-04-13
### Added
- quadruped class, unitree class (support both a1, go1), unitree vision class (unitree class with stereo cameras), and unitree direct class (unitree class that subscribe to external controllers)
- quadruped controllers
- documentations and unit tests
- quadruped standalone with ros 1 and ros 2 vio examples
