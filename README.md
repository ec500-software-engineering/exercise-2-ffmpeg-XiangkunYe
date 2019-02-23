# FFmpeg exercise by Xiangkun Ye

## Introduction
This is the repository for Exercise2 in EC500, it implemented a library that can use multiprogress to convert
video into different resolution ratio and an unit test.

## Usage
In **main.py**, the **convert** class have several method, **ffprobe** will check if the conversion succeeded, **c480** and **c720**
will convert choosen video into 480p and 720p respectivly and the **multiconvert** will convert all videos in current
directory into both 480p and 720p, **track** will provide a tracking interface to show how many processes are running.
The **test.py** implement unit test by pytest. Just run them and you will see the result!

## Detail Infromation
### Maximum progress amount
Just like the screen shot below, due to the FFmpeg's default set, no matter how many progress are using it, it will take all the leisure compute resource of all
cores you have, so it would be hard to masure the maximum progress amount.

![CPU](https://github.com/ec500-software-engineering/exercise-2-ffmpeg-XiangkunYe/blob/master/FFmpeg_result.png)

### Managing number of workers
Since I use progress pool to manage multiprogress, the maximum concurrent running progress would equal to the core amount,
so no matter how many input you test, it will be robust.