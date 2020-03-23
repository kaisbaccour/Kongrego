# Kongrego
Kongrego consolidates virtual machines from all kind of cloud providers or on premises to show them on one dashboard

It is a stack of a 
1- collector which is a python script that collects data from any machine to view (script)
2- inventory backend (Kongrego) that gathers that data sent by the machines and stores them in a mongodb (Flask)
3- KongreGUI that is the dashboard to view the data it retrieves from Kongrego (Flask)

Kongrego can support in the future other collectors like nodeexporter or collectd just to get some basic info about the machine

This repo is on its beginnings and needs a lot of new features and refactoring.
