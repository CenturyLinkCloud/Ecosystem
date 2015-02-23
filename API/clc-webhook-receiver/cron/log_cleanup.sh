#! /bin/sh
# Written by Tommy Hughes - 2/12/2015
### add to crontab of a user with permissions to remove the webhook logs
### 0 4 * * 0 /opt/scripts/log_cleanup.sh > /dev/null 2>&1
###

number_to_keep=12
logbase=/var/log/webhooks/logs

path=`dirname $0`
cd $path
script_dir=`pwd`

find $logbase/ -type f -iname "*.log" | sed -e 's/.\{8\}.log$//g' | sort | uniq > $script_dir/logfile_list
find $logbase/ -type f -iname "*.csv" | sed -e 's/.\{8\}.csv$//g' | sort | uniq > $script_dir/csvfile_list

Count=0
FileCount=`cat $script_dir/logfile_list | wc -l`

until [ "$Count" -ge "$FileCount" ]; do
  let Count+=1
  logfile=`cat -n $script_dir/logfile_list | grep -w $Count | awk '{print $2}'`

# Get list of newest files.
files=(`ls $logfile*.log | sort | tail -n $number_to_keep`)

# Loop over all files in this folder
for i in $logfile*.log; do 
 preserve=0
 # Check whether this file is in files array:
 for a in ${files[@]}; do 
  if [ $i == $a ]; then 
   preserve=1
  fi 
 done
 # If it wasn't, delete it
 if [ $preserve == 0 ]; then 
  rm $i
 fi
done

ls $logfile*.log | sort
echo
done

Count=0
FileCount=`cat $script_dir/csvfile_list | wc -l`

until [ "$Count" -ge "$FileCount" ]; do
  let Count+=1
  csvfile=`cat -n $script_dir/csvfile_list | grep -w $Count | awk '{print $2}'`

# Get list of newest files.
files=(`ls $csvfile*.csv | sort | tail -n $number_to_keep`)

# Loop over all files in this folder
for i in $csvfile*.csv; do 
 preserve=0
 # Check whether this file is in files array:
 for a in ${files[@]}; do 
  if [ $i == $a ]; then 
   preserve=1
  fi 
 done
 # If it wasn't, delete it
 if [ $preserve == 0 ]; then 
  rm $i
 fi
done

ls $csvfile*.csv | sort
echo
done

rm -f $script_dir/logfile_list $script_dir/csvfile_list
