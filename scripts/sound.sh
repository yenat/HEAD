#!/usr/bin/env bash
#
# dev.sh
#
# This script will launch ROS, WebUI, Blender and Behavior Tree.
#

set -e

export MAJOR_PROJECT=HEAD
export NAME=robot
BASEDIR=$(dirname $(readlink -f ${BASH_SOURCE[0]}))


export ROS_LOG_DIR="$HOME/.hr/log"
export ROS_PYTHON_LOG_CONFIG_FILE="$BASEDIR/python_logging.conf"
export ROSCONSOLE_FORMAT='[${logger}][${severity}] [${time}]: ${message}'

eval $($BASEDIR/hrtool -p|grep -E ^HR_WORKSPACE=)
echo HR_WORKSPACE=$HR_WORKSPACE

export HR_WORKSPACE=$HR_WORKSPACE

source $HR_WORKSPACE/$MAJOR_PROJECT/devel/setup.bash

export LAUNCH_DIR="$BASEDIR/../src/audiosysneeds/launch/"
export listener_dir="/home/yenat/hansonrobotics/HEAD/src/audiosysneeds/src"
export OCBHAVE="$HR_WORKSPACE/opencog/ros-behavior-scripting/"

#Kill existing session
if [[ $(tmux ls) == ${NAME}* ]]; then
    tmux kill-session -t $NAME
    echo "Killed session $NAME"
fi
cd $BASEDIR

tmux new-session -n 'roscore' -d -s $NAME 'roslaunch $LAUNCH_DIR/audio.launch basedir:=$LAUNCH_DIR name:=$NAME & rqt_console; $SHELL'
sleep 3
tmux new-window -n 'listener' '$listener_dir/./sample_sub_audioclass.py; $SHELL'

# blender
tmux new-window -n 'Blender' 'blender -y $HR_WORKSPACE/$MAJOR_PROJECT/src/blender_api/Sophia.blend -P \
    $HR_WORKSPACE/$MAJOR_PROJECT/src/blender_api/autostart.py; $SHELL'


# btree needs blender to be ready
sleep 8

# btree
export ROS_NAMESPACE=$NAME
if [[ -d $OCBHAVE ]]; then
    cd $OCBHAVE/src
    tmux new-window -n 'opencog' 'guile -l btree.scm; $SHELL'
    
fi
cd $BASEDIR
tmux new-window -n '$SHELL'
tmux attach;
