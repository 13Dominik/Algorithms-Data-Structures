import turtle


polska = [(80, 100, 'Z'), (180, 50, 'G'), (330, 80, 'N'), (420, 130, 'B'),
          (60, 200, 'F'), (140, 200, 'P'), (200, 140, 'C'), (260, 260, 'E'),
          (340, 200, 'W'), (430, 290, 'L'), (110, 300, 'D'), (180, 330, 'O'),
          (240, 350, 'S'), (320, 320, 'T'), (300, 400, 'K'), (400, 380, 'R')]

slownik = {rej: (x, y, rej) for x, y, rej in polska}

graf = [('Z', 'G'), ('Z', 'P'), ('Z', 'F'),
        ('G', 'Z'), ('G', 'P'), ('G', 'C'), ('G', 'N'),
        ('N', 'G'), ('N', 'C'), ('N', 'W'), ('N', 'B'),
        ('B', 'N'), ('B', 'W'), ('B', 'L'),
        ('F', 'Z'), ('F', 'P'), ('F', 'D'),
        ('P', 'F'), ('P', 'Z'), ('P', 'G'), ('P', 'C'), ('P', 'E'), ('P', 'O'), ('P', 'D'),
        ('C', 'P'), ('C', 'G'), ('C', 'N'), ('C', 'W'), ('C', 'E'),
        ('E', 'P'), ('E', 'C'), ('E', 'W'), ('E', 'T'), ('E', 'S'), ('E', 'O'),
        ('W', 'C'), ('W', 'N'), ('W', 'B'), ('W', 'L'), ('W', 'T'), ('W', 'E'),
        ('L', 'W'), ('L', 'B'), ('L', 'R'), ('L', 'T'),
        ('D', 'F'), ('D', 'P'), ('D', 'O'),
        ('O', 'D'), ('O', 'P'), ('O', 'E'), ('O', 'S'),
        ('S', 'O'), ('S', 'E'), ('S', 'T'), ('S', 'K'),
        ('T', 'S'), ('T', 'E'), ('T', 'W'), ('T', 'L'), ('T', 'R'), ('T', 'K'),
        ('K', 'S'), ('K', 'T'), ('K', 'R'),
        ('R', 'K'), ('R', 'T'), ('R', 'L')]


def coords(x, y):
    y = 470 - y
    dx = -250
    dy = -235
    return x + dx, y + dy


def draw_circle(x, y, letter):
    x, y = coords(x, y)
    turtle.penup()
    turtle.goto(x, y - 20)
    turtle.pendown()
    turtle.circle(20)
    turtle.write(letter, font=("Verdana", 18, "bold"))
    turtle.penup()


def draw_line(edge):
    x, y, _ = slownik[edge[0]]
    x, y = coords(x, y)
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    x, y, _ = slownik[edge[1]]
    x, y = coords(x, y)
    turtle.goto(x, y)
    turtle.penup()


def draw_map(edges, col=None):
    wn = turtle.Screen()
    wn.setup(width=500, height=470, startx=10, starty=10)
    wn.title("Polska")

    wn.addshape("polska.gif")

    myImage = turtle.Turtle()
    myImage.speed(0)
    myImage.shape("polska.gif")
    myImage.penup()
    myImage.goto(0, 0)
    turtle.speed(0)
    turtle.penup()

    if col is None:
        for x, y, r in polska:
            draw_circle(x, y, r)
    else:
        for k, c in col:
            x, y, _ = slownik[k]
            draw_circle(x, y, c)

    for i, e in enumerate(edges):
        draw_line(e)
    turtle.hideturtle()

    while True:
        wn.update()


if __name__ == "__main__":
    draw_map(graf)
