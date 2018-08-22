from faustbot.model.irc_data import IRCData


def privmsg():
    msg = ':amy!amy@foo.example.com PRIVMSG rory :Don\'t blink!'
    data = IRCData(msg)
    pass


def join():
    msg = ':amy!amy@foo.example.com JOIN #tardis'
    data = IRCData(msg)
    assert data.nick == 'amy'
    assert data.user == 'amy'
    assert data.host == 'foo.example.com'
    assert data.command == 'JOIN'
    assert data.channel == '#tardis'
    assert data.message == '' or data.message is None


def channel_msg():
    msg = ':amy!amy@foo.example.com PRIVMSG #tardis :Doctor, they\'ve taken Rory!'
    data = IRCData(msg)
    assert data.nick == 'amy'
    assert data.user == 'amy'
    assert data.host == 'foo.example.com'
    assert data.command == 'PRIVMSG'
    assert data.channel == '#tardis'
    assert data.message == ':Doctor, they\'ve taken Rory!'


def leave():
    msg = 'doctor!doctor@baz.example.org PART #tardis :Off to save Rory'
    data = IRCData(msg)
    assert data.nick == 'doctor'
    assert data.user == 'doctor'
    assert data.host == 'baz.example.org'
    assert data.command == 'PART'
    assert data.channel == '#tardis'
    assert data.message == ':Off to save Rory'


def rpl_welcome():
    msg = ':bar.example.com 001 amy :Welcome to the IR Network amy!amy@foo.example.com'
    data = IRCData(msg)
    assert data.nick == 'bar.example.com'
    assert data.user == ''
    assert data.host == ''
    assert data.command == '001'
    assert data.channel == 'amy'
    assert data.message == ':Welcome to the IR Network amy!amy@foo.example.com'


def ping():
    msg = 'PING :irc.funet.fi'
    data = IRCData(msg)
    assert data.command == 'PING'
    assert data.nick == 'irc.funet.fi'


def pong():
    msg = 'PONG csd.bu.edu tolsun.oulu.fi'
    data = IRCData(msg)
    assert data.command == 'PONG'
    assert data.nick == 'csd.bu.edu'
    assert data.channel == 'tolsun.oulu.fi'


def test():
    privmsg()
    join()
    channel_msg()
    leave()
    rpl_welcome()
    ping()
    pong()


if __name__ == '__main__':
    test()
    print("Test successful!")
