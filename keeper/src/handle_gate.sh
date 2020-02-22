#! /bin/bash

export LANG=C

PERSON=$1
GATE=$2

SH_HALL="shelly1-12C5F9"
SH_EATING="shelly1-12becb"

LOC="50N 7E"
TWILIGHT="angle 1"


echo $PERSON at $GATE on $(date)

DAYTIME=$(sunwait poll $TWILIGHT $LOC)


SHELLIES=""

case "$GATE@$DAYTIME" in

	main_gate@NIGHT)
		echo "$GATE at night."
		SHELLIES="$SH_HALL"
		;;
	
	*@NIGHT)
		echo "At night."
		;;
			
	*@DAY)
		echo "At daylight."
		;;
			
	*)
		;;
esac

for sh in $SHELLIES ; do
	echo $sh
	curl  http://ber:taco@${sh}.intern/relay/0 -d 'turn=on'
done

echo
echo Done.
