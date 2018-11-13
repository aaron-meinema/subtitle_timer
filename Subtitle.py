class Subtitle:

    def __init__(self, arg_list):
        self.arg_list = arg_list
        self.sub_read = self._set_read_and_write('r')
        self.sub_write = open('lol.srt', 'w')

    def run_options(self):
        if self.arg_list[0][1] == "h":
            self.help_command()
        elif self.arg_list[0][1] == "r":
            print(self.read_sub())
        elif self.arg_list[0][1] == "w":
            self.write_sub()
        elif self.arg_list[0][1] == "a":
            self.add_sub()
        elif self.arg_list[0][1] == "s":
            self.sub_tract()

    def read_sub(self):
        return self.sub_read.read()

    def _set_read_and_write(self, rw):
        try:
            return open(self.arg_list[1], rw)
        except Exception:
            self.wrong_command()

    def write_sub(self):
        sub_write = self._set_read_and_write('w')
        sub_write.write(self.arg_list[2])
        sub_write.close()

    def add_sub(self):
        subtitle_line = 1
        with self.sub_read as sub:
            for line in sub:
                line_string = str(subtitle_line)
                if line[:len(line_string)] == line_string:
                    next_line = sub.readline()
                    self.add_ammount(next_line[:len(next_line) - 1],\
                                     line_string)
                    subtitle_line += 1
                elif subtitle_line == 1:
                    next_line = sub.readline()
                    self.add_ammount(next_line[:len(next_line) - 1],\
                                     line_string)
                    subtitle_line += 1
                else:
                    self.sub_write.write(line)

    def add_ammount(self, line, index):
        seconds = int(self.arg_list[2]) % 60
        start_and_end = line.split(' --> ')
        self.sub_write.write(index + '\n')
        for time in start_and_end:
            splitted = time.split(':')
            seconds_milisecons_str = str(int(splitted[2].split(',')[0])\
                                         + seconds) + "," + \
                                         splitted[2].split(',')[1]
            if time == start_and_end[0]:
                start = splitted[0] + ':' + splitted[1] +  ':' + \
                seconds_milisecons_str
            else:
                end = splitted[0] + ':' + splitted[1] +  ':' + \
                seconds_milisecons_str
        self.sub_write.write(start + ' --> ' + end + '\n')

    def end_program(self):
        self.sub_read.close()
        raise SystemExit(0)

    @staticmethod
    def help_command():
        print("commands are:")
        print("-h: shows all commands")
        print("-r: read the subtitle file")
        print("-a: add amount to subtitle in seconds")
        print("-s: subtract amount to subtitle in seconds")
        print("usage: -(option) path/to/subtitlefile amount_to_add/subtract")
        raise SystemExit(0)

    @staticmethod
    def wrong_command():
        print("you made a mistake in your arguments")
        print("this is the -h option:")
        Subtitle.help_command()

    def sub_tract(self):
        self.arg_list[2] = '-' + self.arg_list[2]
        self.add_sub()

    def error_checks(self):
        if int(self.arg_list[2]) < 0:
            print("don't use numbers lower than 0, if you want to subtract use -s")
            print("use -h option for help")
            raise SystemExit(0)
