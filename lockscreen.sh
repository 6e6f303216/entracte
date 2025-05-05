#!/bin/bash

start_break() {
    SLEEP_TIME=$1
    MINUTES=$((SLEEP_TIME / 60))
    paplay assets/sounds/break.ogg
    notify-send "Break" "Curtain! Time for a break of $MINUTES minutes!"
    sleep 5
    hyprctl dispatch togglespecialworkspace entracte
}

end_break() {
    hyprctl dispatch togglespecialworkspace entracte
    sleep 5
    notify-send "Work" "Applause! Time to return to the role!"
    paplay assets/sounds/work.ogg
}

if [ "$1" == "break" ]; then
    start_break "$2"
elif [ "$1" == "work" ]; then
    end_break
else
    echo "Usage: $0 {break|work} [SLEEP_TIME]"
fi
