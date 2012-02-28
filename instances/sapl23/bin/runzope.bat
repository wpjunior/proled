@set ZOPE_HOME=/var/interlegis/SAPL-2.3/Zope-2.9
@set INSTANCE_HOME=/var/interlegis/SAPL-2.3/instances/sapl23
@set PYTHON=%ZOPE_HOME%\bin\python.exe
@set SOFTWARE_HOME=%ZOPE_HOME%\lib\python
@set CONFIG_FILE=%INSTANCE_HOME%\etc\zope.conf
@set PYTHONPATH=%SOFTWARE_HOME%
@set ZOPE_RUN=%SOFTWARE_HOME%\Zope2\Startup\run.py
"%PYTHON%" "%ZOPE_RUN%" -C "%CONFIG_FILE%" %1 %2 %3 %4 %5 %6 %7
