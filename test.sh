while getopts "b:c" opt
do
	case "$opt" in
	c ) echo "$OPTARG" ;;
	b ) echo "$OPTARG" ;;
	esac
done

echo "$paramA"
echo "$paramB"
