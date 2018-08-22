import os

from faustbot.model.config import Config


def read() -> Config:
    cwd = os.getcwd()
    path = os.path.join(cwd, '..', 'test-resources', 'example.config.json')
    config = Config(path)
    return config


def test():
    cfg = read()
    assert cfg.port == 6667
    assert cfg.nick in 'FaustBotDev'
    assert cfg.server in 'irc.freenode.org'
    assert len(cfg.channel) == 4
    channel = None
    for c in cfg.channel:
        if c.name in '#faust-bot':
            channel = c
            break
    assert channel is not None
    assert channel.group in 'dev'
    assert len(channel.mods) == 3
    assert 'Mod' in channel.mods
    assert 'Supermod' in channel.mods
    assert 'EvilMod' in channel.mods
    assert len(channel.blacklist) == 1
    assert 'kicker' in channel.blacklist
    assert channel.lang in 'de-de'
    assert channel.idle_time == 10


if __name__ == '__main__':
    test()
    print('Test successful!')
