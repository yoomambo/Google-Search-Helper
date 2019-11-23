rm ../crawling_history/database/History_all_users.db
rm ../crawling_history/database/History_all_users_title_token.db
python ../crawling_history/database/user_history_merge.py
python ../crawling_history/database/title_token.py
