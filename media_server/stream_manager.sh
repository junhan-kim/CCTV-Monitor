
# Remove streamers not used by clients

ACCESS_LOG_PATH=./logs/access.log

recent_access_log=$(tail -n 100 $ACCESS_LOG_PATH)

while IFS= read -r line; do
    time=$(grep -oP "" <<< $line)
    channel_names=$(grep -oP "[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}" <<< $line)
    echo "Text read from file: $channel_names"
done < $recent_access_log

# echo $recent_access_log
# channel_names=$(grep -oP "[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}" <<< $recent_access_log)

# echo $channel_names