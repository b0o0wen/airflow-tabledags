SH_STR = '''while getopts ":t:" arg #选项后面的冒号表示该选项需要参数
do
    case $arg in
        t)
                        mockdate=$OPTARG #参数存在$OPTARG中
                        ;;
        ?)  #当有不认识的选项的时候arg为?
                       echo "-t means mockdate"
                       exit 1;;
    esac
done
echo " "
echo "==== mock today "$mockdate" ===="

TODAY=`date -d "$mockdate +0 days" "+%Y%m%d"`

START_DATE=`date -d "$TODAY -1 days" "+%Y%m%d"`
END_DATE=`date -d "$TODAY +0 days" "+%Y%m%d"`

echo 'startdate' $START_DATE
echo 'enddate' $END_DATE

declare -i trytime=1
while [ $trytime -le 20 ]
do
sh /root/bowen/staging_util.sh -s $START_DATE -e $END_DATE -x {{sql_path}} -w 30 -p xql > {{log_path}} 2>&1
returnvalue=`cat {{log_path}} | grep -E 'die|error|fail'  | wc -l`

if [ $returnvalue -eq 0 ]
then
echo 'success'
exit 0
else
        trytime=$trytime+1
        if [ $trytime -eq 21 ]
        then
        echo 'we have failed 20 times'
        echo 'you should check it Manually'
        exit 1
        else
        echo 'fail. The' $trytime 'th try coming soon.'
        fi
fi
done
'''