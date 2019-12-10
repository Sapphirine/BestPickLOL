# The Best Pick and Ban Stratgy for LOL

## About

This hub is made for course project (Big Data Analysis course in Columbia University).

We are a team to build this. We are: 杨子涵 (Yang Zihan), 罗浩 (Luo Hao), 陈伟晗 (Chen Weihan).

Feel free to use and learn it. If possible, we strongly recommend you to add a refference link to this project, report bugs and make contribution!


## How to Use

You need to apply for one or more developer API key in [Riot official website](https://developer.riotgames.com/).

Then you can follow the following steps to start your progress:

### Get Data
- Pick a game id in the latest game version
- Open the file "python/getData/getData.py" and fill in your API key and the game id.
- If there's a "getData_record.txt" file in the same folder, you should delete it if you want start from your picked game id. Otherwise just leave it alone, because it records the last time's id it tested and will continue from there automatically.
- Run the python app "python/getData/getData.py". (You can use the bat file as me to make it more convenient)
- Wait untill you get enough data.

### Process Data
- move your csv data sheets to a folder and rename them in continuous numbers (like 1.csv, 2.csv, 3.csv, ...).
- Open the file "python/processData/filter.py" and fill in your csv files' path and the total number of them.
- Run it and you will get the filtered data for training.

### Model training
- Run Matlab and open the script "matlab/zzc_train.m".
- Modify the filtered csv file path (or move it to Matlab's work path).
- Run it and you will get the Mco.csv and Mop.csv files output which is our final model, and two weight in addition. You can use them to verify and make recommendations now.

### Verify Effectiveness
- Run Matlab run script "matlab/zzc_train.m" first to save Mco matrix into memory.
- Open the script "matlab/zzc_test.m" and modify the path of the filtered csv file that you want to test.
- Run it and you will get the prediction's correct rate.

### Make Recommendation
- Run php script "website/server/noserver.php" passing the parameters via GET/POST or parameters in command line.
- It will give you it's recommend based on Mco.csv, Mop.csv and two weights Wco and Wop. 

### Trick: Get Data Using More Instances

If you are a individual, it may be not realistic to apply for advanced API key, which means your request frequency is strictly limited. So you may apply for more API keys (let's say n keys), and
