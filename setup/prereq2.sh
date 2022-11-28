sudo apt install -y python3-rosdep python3-rosinstall python3-rosinstall-generator python3-wstool build-essential
sudo rosdep init
rosdep update

sudo apt install -y ros-noetic-tf ros-noetic-tf-conversions ros-noetic-joy
sudo apt install -y libpcl-dev libusb-1.0-0-dev
sudo apt install -y swig libpython3-dev 

sudo apt install -y ffmpeg
python3 -m pip install ffmpeg-python
