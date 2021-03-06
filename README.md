# Slacker
Python-based tool for pulling chat history from Slack channels using a stolen API token.

![alt_text](https://66.media.tumblr.com/13855c78853fc97012c76ed3ffa95c32/tumblr_ooltcu7Xe51remlq3o2_500.gif)

## How to use:
1. With the stolen API token, run the Channel_RIPper.py script to pull all of the channel IDs and names from a specific Slack group. This will output a dictionary file containing both the IDs and names of all channels.

2. Create a text file of the channels you would like to parse using the channel IDs.

3. Run the Chat_Raider.py script against the text file you created and indicate the number of messages you want to save. Output will be placed in a dated folder and contain files for each channel. 

The messages output will have time stamps and also text will be highlighted according to the regex indicated for the "regex_pattern" variable to make it easier to spot keywords when manually scrolling through messages (i.e., when you are not grepping).

### Example usage and output:
![alt text](https://github.com/Keramas/Slacker/blob/master/ExampleOutput.png?raw=true)

### Supplemental:
Set script to run with a daily cron in order to get the most recent messages automatically and diff the output files.
