import json
import os
import sys

from lib.cipher import get_cipher
from lib.config import client_config__handler

base_path = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(os.path.join(base_path, "./"))
import tornado

from service.client import Socks5Client, TunnelClient

cfgs = {}


def read_config():
    global cfgs
    with open(os.path.join(base_path, "config.json"), "r") as f:
        content = f.read()
        cfgs = json.loads(content)
    cfgs = client_config__handler(cfgs)


async def run():
    global cfgs
    cfg = cfgs.get('Socks5Client', None)
    if cfg:
        socks5_client = Socks5Client()
        socks5_client.set_remote_address(cfg['remote_host'], cfg['remote_port'])
        if cfg.get('key'):
            socks5_client.set_cipher(get_cipher('caesar', cfg['key']))
        socks5_client.listen(cfg['local_port'], cfg['local_host'] if cfg.get('local_host') else '')

    cfg = cfgs.get('TunnelClient', None)
    if cfg:
        tunnel_client = TunnelClient(cfg['key'])
        tunnel_client.set_remote_address(cfg['remote_host'], cfg['remote_port'])
        await tunnel_client.start()


def run2():
    global cfgs
    cfg = cfgs.get('Socks5Client', None)
    if cfg:
        socks5_client = Socks5Client()
        socks5_client.set_remote_address(cfg['remote_host'], cfg['remote_port'])
        if cfg.get('key'):
            socks5_client.set_cipher(get_cipher('caesar', cfg['key']))
        socks5_client.listen(cfg['local_port'], cfg['local_host'] if cfg.get('local_host') else '')

    tornado.ioloop.IOLoop.current().start()
if __name__ == '__main__':
    read_config()
    if cfgs.get('TunnelClient', None):
        tornado.ioloop.IOLoop.current().run_sync(run)
    else:
        run2()

