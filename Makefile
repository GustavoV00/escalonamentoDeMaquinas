#!/usr/bin/python3

INPUTDIR=./inputs/*.txt


all:
	cp tarefas.py tarefas
	chmod 744 tarefas

run:
	clear; for i in $(INPUTDIR); do echo "./tarefas < $$i"; ./tarefas < $$i; done;
