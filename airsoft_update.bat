
call venv/Scripts/activate.bat


Так понимаю, что в файле должен быть список команд для исполенния там. Так как открывается новое окно

putty.exe -ssh user@host -pw password -m c:\path\command.txt


Второй способ
ssh user@host -pw password -m command_run

python manage.py dumpdata -o test_dump.json

pause
