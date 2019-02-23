import os
from multiprocessing import Pool
import subprocess
import time
import json
from pathlib import Path


class convert:

    def ffprobe(self, fin, fout):
        """
        Get media metadata and check if the duration equal.
        """

        metain = subprocess.check_output(['ffprobe', '-v', 'warning',
                                        '-print_format', 'json',
                                        '-show_streams',
                                        '-show_format',
                                        fin])
        metaout = subprocess.check_output(['ffprobe', '-v', 'warning',
                                        '-print_format', 'json',
                                        '-show_streams',
                                        '-show_format',
                                        fout])
        metain = json.loads(metain)
        metaout = json.loads(metaout)

        induration = int(metain['format']['duration'].split('.')[0])
        outduration = int(metaout['format']['duration'].split('.')[0])

        if induration == outduration:
            print('Convert from {} into {} finished successfully!'.format(fin, fout))
        else:
            print('Convert from {} into {} failed!'.format(fin, fout))

        return induration, outduration

    def c480(self, input, output):
        '''
        It's used in the multiconvert method, but it can also be call directly to convert a specific video.
        '''

        print('Convert from {} into {} start!'.format(input, output))
        task = [
            'ffmpeg',
            '-i',
            input,
            '-r',
            '30',
            '-s',
            'hd480',
            '-b:v',
            '1024k',
            '-loglevel',
            'quiet',
            output]
        subprocess.call(task)
        self.ffprobe(input, output)

    def c720(self, input, output):
        '''
        It's used in the multiconvert method, but it can also be call directly to convert a specific video.
        '''

        print('Convert from {} into {} start!'.format(input, output))
        task = [
            'ffmpeg',
            '-i',
            input,
            '-r',
            '30',
            '-s',
            'hd720',
            '-b:v',
            '2048k',
            '-loglevel',
            'quiet',
            output]
        subprocess.call(task)
        self.ffprobe(input, output)

    def multiconvert(self):
        '''
        It will convert all mp4 or mov files in current directory into two formats.
        '''

        files = os.listdir()
        name = []
        # I didn't set the maximum ammount of concurrent running progress
        # so it would be the default which equal to the cores amount.
        p = Pool()
        for file in files:
            tmp = file.split('.')
            if tmp[-1] == 'mp4' or tmp[-1] == 'mov':
                out480 = tmp[0] + '_480p.' + tmp[-1]
                out720 = tmp[0] + '_720p.' + tmp[-1]
                name.append([file, out480, out720])
                p.apply_async(self.c480, args=(
                    file, tmp[0] + '_480p.' + tmp[-1]))
                p.apply_async(self.c720, args=(
                    file, tmp[0] + '_720p.' + tmp[-1]))
        self.track(p)
        p.close()
        p.join()
        return name

    def track(self, p):
        '''
        tracking interface to show how many processes are going on and success of each.
        '''

        while True:
            process_count = len(p._cache)
            if process_count != 0:
                print("{} processes running.".format(process_count))
            else:
                print("All processes are finished!")
                break
            time.sleep(3)


if __name__ == '__main__':
    ins = convert()
    ins.multiconvert()
    #ins.ffprobe("1.mp4", "1_480p.mp4")
