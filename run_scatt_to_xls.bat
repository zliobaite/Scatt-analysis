#%windir%\SysWoW64\cmd.exe

for %%f in (ematch\*.scatt) do (
	echo %%f
	cscript scattexp.vbs %%f
)

for %%f in (ua_online\*.scatt) do (
	echo %%f
	cscript scattexp.vbs %%f
)