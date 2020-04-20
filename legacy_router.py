#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    # for example '-.-.-.-/24'is ip addfress format to set prefix length 
    info( '*** Add Router\n')
    r1 = net.addHost('r1', cls=Node, ip='10.0.0.1')
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')

    info('*** Add Switch\n')
    switch = net.addSwitch('s1')

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.3/8', defaultRoute='via 10.0.0.1')
    h2 = net.addHost('h2', cls=Host, ip='192.0.1.2/12', defaultRoute='via 192.0.1.1')

    info( '*** Add links\n')
    net.addLink(h1, r1, intfName2='r1-eth1', params2={'ip':'10.0.0.1/8'})
    net.addLink(h2, r1, intfName2='r1-eth2', params2={'ip':'192.0.1.1/12'})

    info( '*** Starting network\n')
    net.build()
    
    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches\n')
    
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

