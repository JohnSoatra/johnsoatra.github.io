# length = 251
# token = 50
# last = 0

# for i in range(0, length):
#     end = i + token
#     if end > length:
#         end = length
    
#     if i % token == 0:
#         last = end
#         fun(i, end)

# read length
length=$(python3 python/crawl/read_length.py)
window=2
token=3
window_counter=0
cmds=""

echo -e "lenght = $length"

# clear
echo -e "clear file"
python3 python/crawl/clear.py;

for ((i = 0; i < $length; i ++ ))
    do
        end=$(expr $i + $token);
        if [ $end -gt $length ]
            then end=$length;
        fi

        if [ $(expr $i % $token) -eq 0 ]
            then
                # run
                window_counter=$(expr $window_counter + 1)
                echo -e "\n------------- running on ($i - $end)";

                if [ $(expr $window_counter % $window) -eq 0 ] || [ $end -eq $length ]
                    then
                        cmds="$cmds python3 python/crawl/crawl.py --start=$i --end=$end";
                        cmds=$(echo $cmds | xargs)
                        
                        echo $cmds;
                        eval $cmds;
                        
                        cmds="";
                else
                    cmds="$cmds python3 python/crawl/crawl.py --start=$i --end=$end &";
                fi
        fi
    done
