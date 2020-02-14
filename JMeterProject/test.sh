helpFunction()
{
   echo ""
   echo "Usage: $0 -n in"
   echo -e "\t-a Description of what is parameterA"
   echo -e "\t-b Description of what is parameterB"
   echo -e "\t-c Description of what is parameterC"
   exit 1 # Exit script after printing help
}


while getopts "n" opt
do
	case "$opt" in
	n ) paramN=$OPTARG ;;
	? ) helpFunction ;;
	esac
done
echo "$paramA $paramB"
