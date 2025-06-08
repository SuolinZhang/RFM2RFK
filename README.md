# RFM2RFK
Copy Renderman material network from Maya to Katana

## Currently supported Nodes:
PxrChecker, PxrDisney, PxrNormalMap, PxrSurface, PxrTexture

## Installation
### Linux
1. Place userSetup.py to `home/maya/version_number/prefs/scripts`
2. Update the M2K value in userSetup.py to match your local directory path
### Windows
1. Place userSetup.py to `C:/Users/Documents/maya/verision_number/prefs/scripts`
2. Update the M2K value in userSetup.py to match your local directory path. Note: use "/" or "\\" in string value

## Tests
### MayaBase
**Open maya script Editor and run:**

`from MayaBase.modules.utils import testing` 

`testing.testAllModules()`

### Rfm2Rfk
**Open maya script Editor and run:**

`from Rfm2Rfk import testing_Rfm2Rfk`

`testing_Rfm2Rfk.testAllModules()`

## Usage
1. Select shading network(except shadingEngine type node) you want to copy
2. Open Script Editor and run:

    `import Rfm2Rfk`

    `Rfm2Rfk.copy()`
3. Open Katana and create a NetworkMaterialCreate node
4. Enter NetworkMaterialCreat node then paste(ctrl+v)

## Note
1. As this tool was designed for my Pipeline assignment studying in NCCA Bournemouth University, the supported nodes are quite few, hope I can add more nodes in future. For now,DIY is encouraged! And I'm very happy to help if certain nodes are needed.
2. MayaBase is a module I wrote in the past, It contains a seperate readme file. Rfm2Rkf was written upon Mayabase.
3. The structure of the tool was referred to ababak's maya2katana, while the main body of code is different. Check out this link if interested: github.com/ababak/maya2katana.

## Contact
Feel free to reach me out if you have any questions.
Email: zsl980614@gmail.com
