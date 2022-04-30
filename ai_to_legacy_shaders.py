# Lucas Santos 2022
# Make this tool turn it into a standard surface instead?

from maya import cmds
from maya.mel import eval

def MESH_SELECT():
    mesh_selection = cmds.ls(sl=1)
    return mesh_selection

def REPLACE_SHADERS(shaders):

    cmds.undoInfo(openChunk=1)

    
    replaceType = 'lambert'

    for s in shaders:
        legacyShader = cmds.createNode(replaceType)

        shaderConnex = cmds.listConnections(s,c=1)
        for sc in shaderConnex:
            if ".baseColor" in sc:
                mapInput = cmds.listConnections(f'{s}.baseColor',p=1)[0]

                eval(f'replaceNode {s} {legacyShader};')
                cmds.delete(s)
                replacedShader = cmds.rename(legacyShader,s)
                cmds.connectAttr(mapInput,f'{replacedShader}.color')


    cmds.undoInfo(closeChunk=1)

def ASSIGNED_SHADER(mesh_selection):

    shaders = []
    for m in mesh_selection:
        futureConnex = cmds.listHistory(str(m), f=1, pdo=1)

        if futureConnex is None:
            return None

        # Search for the connecting shading group
        for n in futureConnex:
            if cmds.attributeQuery("surfaceShader",node=n, exists=True):
                # Get shader from incoming connection of the shading group
                shader = cmds.listConnections("%s.surfaceShader" % (str(n)), source=True)

                if shader is None:
                    continue

                shader = str(shader[0])
                shaders.append(shader)
                

    return shaders 
    

confirm = cmds.confirmDialog(annotation=1,button=['OK','Cancel'],cancelButton='Cancel',defaultButton='OK',dismissString='NO',icon="question',message='This changes all selected mesh shaders' into Lamberts.",t='Do it?')
if confirm == 'OK':
    selection = MESH_SELECT()
    print(selection)
    materials = ASSIGNED_SHADER(selection)
    print(materials)
    REPLACE_SHADERS(materials)

    print('Done')