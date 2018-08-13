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

TODAY=`date -d "$mockdate -0 days" '+%Y%m%d'`

WAIT_TIME=20
delta=`date -d $TODAY +%u`
sun_of_lastweek=`date -d "$TODAY -$delta days" '+%Y%m%d'`
Mon_of_thisweek=`date -d "$sun_of_lastweek +1 days " '+%Y%m%d'`
echo 'Mon of this week :' $Mon_of_thisweek
echo 'wait time' $WAIT_TIME

START_DATE='20171127'
START_DATE=`date  '+%Y%m%d' -d $START_DATE`
END_DATE=`date -d "$Mon_of_thisweek -1 weeks " '+%Y%m%d'`
FLAG_DATE=`date -d "$Mon_of_thisweek -1 weeks " "+%Y%m%d"`
echo 'FLAG_DATE' $FLAG_DATE
echo 'START_DATE' $START_DATE
echo 'END_DATE' $END_DATE
test1()
{
IS_SUCCESS=`cat {{log_path}} | grep -E 'die|error|fail'  | wc -l`

        if [ $START_DATE -ge $FLAG_DATE ]
        then
            echo 'paowangla'
            exit 0
        elif ( [ $IS_SUCCESS -gt 0 ] )
        then
            echo 'please check the code!!!'
            exit 1
        elif ( [ $IS_SUCCESS -eq 0 ] )
        then
            STOP_DATE_7=`date -d "$START_DATE +8 weeks" "+%Y%m%d"`
            echo 'STOP_DATE_7' $STOP_DATE_7
                if [ $END_DATE -lt $STOP_DATE_7 ]
                then 
                      echo 'in_START_DATE' $START_DATE
                      echo 'in_END_DATE' $END_DATE
                      sleep 1
                      echo 'in_start_time' `clock`
                      sh /root/bowen/staging_util2.sh -s $START_DATE -e $END_DATE -x {{sql_path}} -w 30  > {{log_path}} 2>&1
                      echo 'in_end_time' `clock`
                      IS_SUCCESS=`cat {{log_path}} | grep -E 'die|error|fail'  | wc -l`
                      COUNT=0
                      while [ $IS_SUCCESS -gt 0 ]
                      do
                          COUNT=$(( $COUNT + 1 ))
                          sleep 20
                          echo "current wait $COUNT times, "
                          echo 'error_start_time' `clock`
                          sh /root/bowen/staging_util2.sh -s $START_DATE -e $END_DATE -x {{sql_path}} -w 30  > {{log_path}} 2>&1
                          echo 'error_end_time' `clock`
                          IS_SUCCESS=`cat {{log_path}} | grep -E 'die|error|fail'  | wc -l`
                          if [ $COUNT -eq $WAIT_TIME ]
                          then
                              echo "wait for result too long... failed and exit !"
                              exit 2
                          fi
    
                      done
                fi

            START_DATE=`date -d "$START_DATE +1 weeks" "+%Y%m%d"`
            echo 'out_START_DATE' $START_DATE
            echo 'out_END_DATE' $END_DATE
            test1

        else
            echo 'bad request!!!'
        fi
}
test1

'''