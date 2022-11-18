import curses


class TextWrapper:
    text = [[], ]
    y = 0
    x = 0

    def __init__(self, text: str):
        if text is None:
            return
        self.text = []
        temp = text.split("\n")
        for line in temp:
            self.text.append(list(line))

    def __len__(self):
        return len(self.text)

    def __iter__(self):
        return self.text.__iter__()

    def splitline(self):
        self.text.insert(self.y + 1, self.text[self.y][self.x:])
        self.text[self.y] = self.text[self.y][:self.x]
        self.y += 1
        self.x = 0

    def unite_lines(self, ):  # only to use when cursor is at x == 0
        if self.y != len(self.text) - 1:
            self.text[self.y] += self.text[self.y + 1]
            self.text.pop(self.y + 1)

    def insert_char(self, char, y=None, x=None, ):
        if x is None:
            x = self.x
        if y is None:
            y = self.y

        if char == "\n":
            self.splitline()
        else:
            self.text[y].insert(x, char)
            self.x += 1

    def delete_backspace(self):
        if self.x != 0:
            self.text[self.y].pop(self.x - 1)
            self.move_left()
        elif self.y != 0:  # when deleteing a line
            self.move_up()  # unite_lines is always the current line with the next line
            self.x = len(self.text[self.y])
            self.unite_lines()

    def delete_supr(self):
        if self.x != len(self.text[self.y]):
            self.text[self.y].pop(self.x)
        elif self.y != len(self.text) - 1:  # when deleteing a line
            self.x = len(self.text[self.y])
            self.unite_lines()

    def adjust_x(self):
        if self.x > len(self.text[self.y]):
            self.x = len(self.text[self.y])

    def move_left(self):
        if self.x != 0:
            self.x -= 1
        elif self.y != 0:
            self.move_up()
            self.x = len(self.text[self.y])

    def move_right(self):
        if not (self.x >= len(self.text[self.y])):
            self.x += 1
        elif self.y != len(self.text) - 1:
            self.move_down()
            self.x = 0

    def move_up(self):
        if self.y != 0:
            self.y -= 1
            self.adjust_x()

    def move_down(self):
        if not (self.y >= len(self.text) - 1):
            self.y += 1
            self.adjust_x()

    def flush(self):
        res = ""
        for line in range(len(self.text)):
            for char in range(len(self.text[line])):
                res += self.text[line][char]

            if line != len(self.text) - 1:
                res += "\n"
        return res


class TextRenderer:
    text = TextWrapper("")
    x_render_offst = 0
    y_render_offst = 0
    a = 0

    def __init__(self, stdscr: curses.window, text: TextWrapper):
        self.text = text
        self.stdscr = stdscr

    def render(self, yfst=0, xfst=0, key="", stdscr=None):
        if stdscr is None:
            stdscr = self.stdscr
        stdscr.clear()
        stdscr.refresh()
        stdscr.move(xfst, yfst)

        lines, columns = stdscr.getmaxyx()

        if self.text.x >= self.x_render_offst + columns - xfst - 1:
            self.x_render_offst = self.text.x - columns + xfst + 1
        elif self.text.x < self.x_render_offst:
            self.x_render_offst = self.text.x
        self.a = self.x_render_offst

        if self.text.y >= self.y_render_offst + lines - yfst - 1:
            self.y_render_offst = self.text.y - lines + yfst + 1
        elif self.text.y < self.y_render_offst:
            self.y_render_offst = self.text.y

        # rendering the text:
        for line in range(len(self.text.text)):
            if (line < self.y_render_offst) or (line >= self.y_render_offst + lines - yfst):
                continue
            stdscr.move(line - self.y_render_offst + yfst, 0 + xfst)

            for char in range(len(self.text.text[line])):
                if (char < self.x_render_offst) or (char >= self.x_render_offst + columns - xfst):
                    continue
                stdscr.addch(self.text.text[line][char])

        # position cursos to where user is editing
        stdscr.move(self.text.y - self.y_render_offst + yfst, self.text.x - self.x_render_offst + xfst)
        stdscr.refresh()


def editor(string: str, toptext="press crtl + x to exit"):

    def main(stdscr: curses.window):
        # initialization
        curses.curs_set(True)
        curses.noecho()
        text = TextWrapper(string)
        renderer = TextRenderer(stdscr, text)

        # main_loop
        key = ""
        while True:
            renderer.render(1, 1, key)
            coords = stdscr.getyx()
            stdscr.move(0, 0)
            stdscr.addstr(toptext)
            stdscr.move(coords[0], coords[1])

            key = stdscr.getkey()

            if key == "KEY_LEFT":
                text.move_left()
            elif key == "KEY_RIGHT":
                text.move_right()
            elif key == "KEY_UP":
                text.move_up()
            elif key == "KEY_DOWN":
                text.move_down()
            elif key == "KEY_BACKSPACE":
                text.delete_backspace()
            elif key == "KEY_DC":
                text.delete_supr()
            elif key == "\x18":
                stdscr.move(0, 0)
                stdscr.addstr(" do you want to save? y/n")
                while True:
                    key = stdscr.getkey()
                    if key == "y":
                        return text.flush()
                    elif key == "n":
                        return False

            elif len(key) == 1:
                text.insert_char(key)

    saved = curses.wrapper(main)
    if saved is False:
        return False
    else:
        return saved
