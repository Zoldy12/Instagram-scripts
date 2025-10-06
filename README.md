# Instagram-scripts
Repository contains 2 python scripts and 1 text file. You need to install playwright library before running scripts.

Firstly, blogers.txt must have rows with format "{bloger_username} {int_number}", where bloger_username - instagram bloger username and int_number - amount of bloger's followers that you want to follow. For example, "mr_bill 50". The last row must be "end"!

Secondly, follow.py is using blogers.py to follow certain amounts of other blogers followers. When you run this file, you need to sign in your instagram account and then push Enter in terminal, after that scripts will work automaticly. For example, if blogers.txt contains 2 blogers jack and bill, number 40 for jack and number 120 for bill, after signing in you will push Enter and scripts will start subscribing users. In the end every follow will be saved in a new file: followed_users.txt and you will be able to check stats and working time in terminal, after all push Enter again to finish.

Finally, unfollow.py is using followed_users.py to unfollow everyone mentioned in this file. It's working like follow.py, so you need to log in in the beginning and in the end you can check stats in the terminal, but it is also deleting followed_users.py after finishing.

I advise not to subscribe more than 200 users at once, bc instagram can find it suspicious and mute your account for a couple of hours. Be careful! 💖

Zoldy12
