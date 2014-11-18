#%windir%\SysWoW64\cmd.exe

cd ematch

for %%f in (*.scatt) do (
	echo %%f
	cscript scattexp.vbs %%f
)
cd ..

cd ua_online

for %%f in (*.scatt) do (
	echo %%f
	cscript scattexp.vbs %%f
)

cd ..