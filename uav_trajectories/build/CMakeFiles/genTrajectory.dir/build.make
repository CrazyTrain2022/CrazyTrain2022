# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/crazycrowd/crazycrowd/visionen/uav_trajectories

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/crazycrowd/crazycrowd/visionen/uav_trajectories/build

# Include any dependencies generated for this target.
include CMakeFiles/genTrajectory.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/genTrajectory.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/genTrajectory.dir/flags.make

CMakeFiles/genTrajectory.dir/src/genTrajectory.cpp.o: CMakeFiles/genTrajectory.dir/flags.make
CMakeFiles/genTrajectory.dir/src/genTrajectory.cpp.o: ../src/genTrajectory.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/crazycrowd/crazycrowd/visionen/uav_trajectories/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/genTrajectory.dir/src/genTrajectory.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/genTrajectory.dir/src/genTrajectory.cpp.o -c /home/crazycrowd/crazycrowd/visionen/uav_trajectories/src/genTrajectory.cpp

CMakeFiles/genTrajectory.dir/src/genTrajectory.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/genTrajectory.dir/src/genTrajectory.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/crazycrowd/crazycrowd/visionen/uav_trajectories/src/genTrajectory.cpp > CMakeFiles/genTrajectory.dir/src/genTrajectory.cpp.i

CMakeFiles/genTrajectory.dir/src/genTrajectory.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/genTrajectory.dir/src/genTrajectory.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/crazycrowd/crazycrowd/visionen/uav_trajectories/src/genTrajectory.cpp -o CMakeFiles/genTrajectory.dir/src/genTrajectory.cpp.s

# Object files for target genTrajectory
genTrajectory_OBJECTS = \
"CMakeFiles/genTrajectory.dir/src/genTrajectory.cpp.o"

# External object files for target genTrajectory
genTrajectory_EXTERNAL_OBJECTS =

genTrajectory: CMakeFiles/genTrajectory.dir/src/genTrajectory.cpp.o
genTrajectory: CMakeFiles/genTrajectory.dir/build.make
genTrajectory: /usr/lib/x86_64-linux-gnu/libboost_program_options.so.1.71.0
genTrajectory: /usr/lib/x86_64-linux-gnu/libboost_filesystem.so.1.71.0
genTrajectory: libmav_trajectory_generation.a
genTrajectory: CMakeFiles/genTrajectory.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/crazycrowd/crazycrowd/visionen/uav_trajectories/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable genTrajectory"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/genTrajectory.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/genTrajectory.dir/build: genTrajectory

.PHONY : CMakeFiles/genTrajectory.dir/build

CMakeFiles/genTrajectory.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/genTrajectory.dir/cmake_clean.cmake
.PHONY : CMakeFiles/genTrajectory.dir/clean

CMakeFiles/genTrajectory.dir/depend:
	cd /home/crazycrowd/crazycrowd/visionen/uav_trajectories/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/crazycrowd/crazycrowd/visionen/uav_trajectories /home/crazycrowd/crazycrowd/visionen/uav_trajectories /home/crazycrowd/crazycrowd/visionen/uav_trajectories/build /home/crazycrowd/crazycrowd/visionen/uav_trajectories/build /home/crazycrowd/crazycrowd/visionen/uav_trajectories/build/CMakeFiles/genTrajectory.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/genTrajectory.dir/depend

