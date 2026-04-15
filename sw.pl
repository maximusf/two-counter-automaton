#!/usr/bin/perl

while (<>) {
    s/[ \t\r]//g;
    print;
}
