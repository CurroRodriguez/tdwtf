@echo off

nosetests %1
if(%ERRORLEVEL%)==(0) (color 0A) else (color 0C)