import urwid
from anymesh import AnyMesh, AnyMeshDelegateProtocol, MeshMessage, MeshDeviceInfo


class AmDelegate(AnyMeshDelegateProtocol):
    def connectedTo(self, device_info):
        lb = frame.contents['body']
        lb[0].body.append(urwid.Text('connected to ' + device_info.name))
        loop.draw_screen()

    def disconnectedFrom(self, name):
        lb = frame.contents['body']
        lb[0].body.append(urwid.Text('disconnected from ' + name))
        loop.draw_screen()

    def receivedMessage(self, message):
        lb = frame.contents['body']
        lb[0].body.append(urwid.Text('Message from ' + message.sender + '\r\n Target: ' + message.data))
        loop.draw_screen()

def start_anymesh(name, listens_to):
    global delegate, any_mesh, status
    delegate = AmDelegate()
    if 'any_mesh' not in globals():
        any_mesh = AnyMesh(name, listens_to, delegate)

def handle_input(key):
    if key == 'esc':
        raise urwid.ExitMainLoop()


class SetupListBox(urwid.ListBox):
    def __init__(self):
        body = [urwid.Text('Setup your Mesh Instance'), urwid.Divider(), urwid.Edit("Enter device name: ")]
        super(SetupListBox, self).__init__(urwid.SimpleFocusListWalker(body))

    def keypress(self, size, key):
        key = super(SetupListBox, self).keypress(size, key)
        if key == 'enter':
            if self.focus_position > 2 and len(self.body[self.focus_position].edit_text) == 0:
                device_name = self.body[2].edit_text
                device_listens = []
                for index, item in enumerate(self.body):
                    if index > 2:
                        device_listens.append(item.edit_text)
                start_anymesh(device_name, device_listens)
                load_msg_frame()

            else:
                self.body.insert(self.focus_position + 1, urwid.Edit("Enter a keyword to listen to: "))
                self.focus_position += 1
        elif key == 'esc':
            raise urwid.ExitMainLoop()
class MessageListBox(urwid.ListBox):
    def __init__(self):
        body = [urwid.Text('Message Log'), urwid.Divider()]
        super(MessageListBox, self).__init__(urwid.SimpleListWalker(body))

class NewMsgListBox(urwid.ListBox):
    def __init__(self):
        body = [urwid.Edit("Target:"), urwid.Edit("Message:"), urwid.Button("Request", self.req_pressed), urwid.Button("Publish", self.pub_pressed)]
        super(NewMsgListBox, self).__init__(urwid.SimpleFocusListWalker(body))
    def req_pressed(self):
        pass
    def pub_pressed(self):
        pass


def load_msg_frame():
    global frame
    frame.body = MessageListBox()
    lb = NewMsgListBox()
    frame.footer = urwid.BoxAdapter(lb, 7)
    frame.focus_position = 'footer'
    lb.set_focus(0)



frame = urwid.Frame(SetupListBox())
text = urwid.Text('Connected devices')
columns = urwid.Columns([('weight', 2, urwid.BoxAdapter(frame, 50)), ('weight', 1, text)], 5)
fill = urwid.Filler(columns, 'top')

loop = urwid.MainLoop(fill, event_loop=urwid.TwistedEventLoop(), unhandled_input=handle_input)
loop.run()