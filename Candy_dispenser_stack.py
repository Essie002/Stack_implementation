from tkinter import Button, Canvas, LEFT, RIGHT, Tk
from tkinter.messagebox import showerror, showinfo


class CandyDispenser:

    def __init__(self, window: Tk):
        self.window = window
        self.color_primary = "pink"
        self.color_secondary = "gray"

        self.candy_stack = []  # we declare the empty stack
        self.max_size = 14  # maximum amount of candy the list can hold

        # Spring
        self.spring_left = 73
        self.spring_right = 287
        self.spring_top = 120
        self.spring_bottom = 600
        self.spring_offset = 30  # Distance moved by spring
        self.spring_thickness = 15

        # New candy bar
        self.new_bar_bottom = self.spring_top + 30  # Candy height = 56px.
        self.new_bar_cx = (self.spring_left + self.spring_right) / 2  # Center X
        self.new_bar_cy = (self.spring_top + self.new_bar_bottom) / 2  # Center Y

        self.a_y = 120
        self.b_y = 220
        self.c_y = 330
        self.d_y = 430
        self.e_y = 530

        self.left_panel = Canvas(self.window, width=(window_width / 2), height=window_height)
        self.left_panel.pack(side=LEFT)

        self.right_panel = Canvas(self.window, width=(window_width / 2), height=window_height)
        self.right_panel.pack(side=RIGHT)

        # Draw spring
        self.a = self.left_panel.create_line(self.spring_left, self.a_y, self.spring_right, self.a_y, smooth=True)

        self.a_b1 = self.left_panel.create_line(self.spring_left, self.a_y, self.spring_right, self.b_y, smooth=True)

        self.a_b2 = self.left_panel.create_line(self.spring_left, self.b_y, self.spring_right, self.a_y, smooth=True)

        self.b = self.left_panel.create_line(self.spring_left, self.b_y, self.spring_right, self.b_y, smooth=True)

        self.b_c1 = self.left_panel.create_line(self.spring_left, self.c_y, self.spring_right, self.b_y, smooth=True)

        self.b_c2 = self.left_panel.create_line(self.spring_right, self.c_y, self.spring_left, self.b_y, smooth=True)

        self.c = self.left_panel.create_line(self.spring_left, self.c_y, self.spring_right, self.c_y, smooth=True)

        self.c_d1 = self.left_panel.create_line(self.spring_left, self.c_y, self.spring_right, self.d_y, smooth=True)

        self.c_d2 = self.left_panel.create_line(self.spring_right, self.c_y, self.spring_left, self.d_y, smooth=True)

        self.d = self.left_panel.create_line(self.spring_left, self.d_y, self.spring_right, self.d_y, smooth=True)

        self.d_e1 = self.left_panel.create_line(self.spring_left, self.d_y, self.spring_right, self.e_y, smooth=True)

        self.d_e2 = self.left_panel.create_line(self.spring_right, self.d_y, self.spring_left, self.e_y, smooth=True)

        self.left_panel.create_line(self.spring_left, self.e_y, self.spring_right, self.e_y, smooth=True)

        self.left_panel.create_line(70, 70, 70, 540, width=2)
        self.left_panel.create_line(290, 70, 290, 540, width=2)
        self.left_panel.create_line(290, 540, 70, 540, width=3)

        # Draw components for the right panel

        Button(self.right_panel, text="Push", bg=self.color_primary, font=("Montserrat", 16),
               command=self.push).place(x=52, y=100)

        Button(self.right_panel, text="Pop", bg=self.color_primary, font=("Montserrat", 16),
               command=self.pop).place(x=52, y=200)

        Button(self.right_panel, text="Top", bg=self.color_primary, font=("Montserrat", 16),
               command=self.peek).place(x=52, y=300)

        Button(self.right_panel, text="Len", bg=self.color_primary, font=("Montserrat", 16),
               command=self.report_size).place(x=52, y=400)

        Button(self.right_panel, text="Is Empty", bg=self.color_primary, font=("Montserrat", 16),
               command=self.report_empty_stat).place(x=52, y=490)

    def pop(self):
        if self.size() > 0:

            candy = self.candy_stack.pop()
            self.left_panel.delete(candy['bar'])
            self.left_panel.delete(candy['label'])

            self.update_dispenser('pop')
            showinfo("Popped", f'Popped "{candy["tag"]}"')

        else:
            showerror("Stack Underflow!", "The Candy Dispenser is empty.")

    def push(self):
        if self.size() < self.max_size:
            self.candy_stack.append(self.draw_candy())  # Add candy to stack.
            self.update_dispenser('push')
        else:
            showerror("Stack Overflow!", "The Candy Dispenser is full.")

    def draw_candy(self):
        bar = self.left_panel.create_oval(self.spring_left, self.spring_top, self.spring_right,
                                          self.new_bar_bottom, fill=self.color_secondary)
        tag = f'Candy {self.size() + 1}'
        label = self.left_panel.create_text(self.new_bar_cx, self.new_bar_cy, text=tag, fill='black')
        return {'bar': bar, 'label': label, 'tag': tag}

    def update_dispenser(self, mode):
        # Update position of all candies excluding the topmost in the stack.
        if mode == 'push':
            for i in range(self.size()):
                self.update_candy_pos(self.candy_stack[i], (self.size() - 1) - i)

            # Update spring's pitch for the 4 springs
            self.a_y += self.spring_offset
            self.b_y += self.spring_offset / 1.5
            self.c_y += self.spring_offset / 3
            self.d_y += self.spring_offset / 6

        elif mode == 'pop':
            stack_size = self.size()
            for i in range(stack_size):
                self.update_candy_pos(self.candy_stack[i], stack_size - (i + 1))

            # Update spring's pitch.
            self.a_y -= self.spring_offset
            self.b_y -= self.spring_offset / 1.5
            self.c_y -= self.spring_offset / 2
            self.d_y -= self.spring_offset / 3
        else:
            raise Exception

        # Update spring.
        self.left_panel.coords(self.a, self.spring_left, self.a_y, self.spring_right, self.a_y)
        self.left_panel.coords(self.a_b1, self.spring_left, self.a_y, self.spring_right, self.b_y)
        self.left_panel.coords(self.a_b2, self.spring_left, self.b_y, self.spring_right, self.a_y)
        self.left_panel.coords(self.b, self.spring_left, self.b_y, self.spring_right, self.b_y)
        self.left_panel.coords(self.b_c1, self.spring_left, self.c_y, self.spring_right, self.b_y)
        self.left_panel.coords(self.b_c2, self.spring_right, self.c_y, self.spring_left, self.b_y)
        self.left_panel.coords(self.c, self.spring_left, self.c_y, self.spring_right, self.c_y)
        self.left_panel.coords(self.c_d1, self.spring_left, self.c_y, self.spring_right, self.d_y)
        self.left_panel.coords(self.c_d2, self.spring_right, self.c_y, self.spring_left, self.d_y)
        self.left_panel.coords(self.d, self.spring_left, self.d_y, self.spring_right, self.d_y)
        self.left_panel.coords(self.d_e1, self.spring_left, self.d_y, self.spring_right, self.e_y)
        self.left_panel.coords(self.d_e2, self.spring_right, self.d_y, self.spring_left, self.e_y)

        self.left_panel.update()  # Redraw components

    def update_candy_pos(self, candy, y):
        updated_bar_top = self.spring_top + (self.spring_offset * y)
        updated_bar_bottom = self.new_bar_bottom + (self.spring_offset * y)

        self.left_panel.coords(
            candy['bar'], self.spring_left, updated_bar_top, self.spring_right, updated_bar_bottom
        )
        self.left_panel.coords(
            candy['label'], self.new_bar_cx, (updated_bar_top + updated_bar_bottom) / 2
        )

    def size(self):
        return len(self.candy_stack)

    def report_size(self):
        showinfo('Size', f'Candies in the dispenser: {self.size()}')

    def peek(self):
        if self.is_empty():
            showerror('Top Failed', 'The Candy dispenser is empty')
        else:
            showinfo('Top', f'The Candy at the top is: "{self.candy_stack[-1]["tag"]}"')

    def is_empty(self):
        if self.size() == 0:
            return True
        return False

    def report_empty_stat(self):
        msg = 'False!'
        if self.is_empty():
            msg = 'True :)'
        showinfo('Is Empty?', msg)


if __name__ == '__main__':
    window_height = 550
    window_width = 650

    root = Tk()
    root.title('Candy Dispenser')
    root.maxsize(window_width, window_height)
    root.minsize(window_width, window_height)
    CandyDispenser(root)
    root.mainloop()
