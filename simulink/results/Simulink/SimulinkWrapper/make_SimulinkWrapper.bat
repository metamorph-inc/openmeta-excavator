call "%VS100COMNTOOLS%vsvars32.bat"
"%DevEnvDir%VCExpress.exe" SimulinkWrapper.sln /build Release /project SimulinkWrapper.vcxproj /projectconfig Release
