# trick-or-treat
A remaster of the [Discord Halloween Bot from 2020](https://support.discord.com/hc/en-us/articles/360057167253-Halloween-Bot-2020). 


# Setup:
- Add a `CHANNEL_ID`, `GUILD_ID`, and a `BOT_TOKEN` in an environment file. As it stands right now, just run `python3 main.py` to run the bot locally.


# TODO LIST
- ~~user function to claim a trick or treater~~ DONE
- ~~function to randomly send a trick or treater message~~ DONE
    - Have function trigger based on user activity
- Function to give random item to users that claim friends
- Database to keep track of items that a player has
    - At the end of the day, aggregate stats and showcase points and missed friends
    - Announce how many days until halloween are left
- Function to assign role to user with highest amount of items
- Function to set the channel it talks in
- user function to display leaderboard
- User function to display inventory
- Timeout function if no one "claims" a friend if, say, a minute passes.


# STRETCH GOALS
- Some sort of system to determine if the player should trick or treat the friend
- Double XP power hours
- New game plus items
- Send a link to the monster mash every once in a while (rare)
    - If people monster mash while this friend is around, items can drop for them.
- Clean up old events?
- User function to display missing items / missing friends


# VERY STRETCH GOALS
- Trading system?
- Skewing random item generation based on what items the user already has
- Actually join voice chat and play the monster mash during monster mash events

# Happy Spoopy Season 🎃

cmontminy + standard-robot